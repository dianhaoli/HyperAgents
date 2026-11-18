# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import os

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, TypeError):
        return None


def _evaluation_summary(eval_path):
    """Summarize completed results, comparing generations only on matching cohorts."""
    try:
        generation_dirs = sorted(os.listdir(eval_path))
    except OSError:
        return "No readable prior evaluation directory was available."

    cohorts = {}
    excluded = []
    for dirname in generation_dirs:
        if not dirname.startswith("gen_"):
            continue
        gen_dir = os.path.join(eval_path, dirname)
        if not os.path.isdir(gen_dir):
            continue
        metadata = _load_json(os.path.join(gen_dir, "metadata.json")) or {}
        initial = dirname == "gen_initial"
        try:
            eval_dirs = sorted(os.listdir(gen_dir))
        except OSError:
            continue
        for eval_name in eval_dirs:
            if not eval_name.endswith("_eval"):
                continue
            report = _load_json(os.path.join(gen_dir, eval_name, "report.json"))
            if not isinstance(report, dict):
                continue
            score = next((report.get(k) for k in ("overall_accuracy", "score", "accuracy")
                          if isinstance(report.get(k), (int, float)) and not isinstance(report.get(k), bool)), None)
            if score is None:
                continue

            task_scores = report.get("per_task_score")
            if isinstance(task_scores, dict) and task_scores:
                task_ids = tuple(sorted(map(str, task_scores)))
                cohort_key = (eval_name, "task_ids", task_ids)
                cohort_label = f"{len(task_ids)} tasks with matching IDs"
            else:
                task_ids = None
                count = next((report.get(k) for k in ("total_test_inputs", "total", "num_tasks")
                              if isinstance(report.get(k), int) and not isinstance(report.get(k), bool)), None)
                cohort_key = (eval_name, "count", count)
                cohort_label = f"{count} reported tasks (IDs unavailable; matching counts do not guarantee identical samples)"

            complete = initial or metadata.get("run_full_eval") is True
            valid = initial or metadata.get("valid_parent") is not False
            record = {
                "generation": "initial" if initial else dirname[4:],
                "parent": metadata.get("parent_genid"),
                "score": float(score),
                "report": report,
            }
            if complete and valid:
                cohorts.setdefault((cohort_key, cohort_label), []).append(record)
            else:
                status = "partial or unevaluated" if not complete else "invalid parent"
                excluded.append(f"{eval_name} gen_{record['generation']} ({status})")

    if not cohorts:
        return "No completed, valid generation reports with scalar scores were found."

    lines = ["Completed evaluation evidence (compare only within the same domain and cohort):"]
    for (cohort_key, cohort_label), records in sorted(cohorts.items(), key=lambda item: str(item[0][0])):
        by_generation = {str(record["generation"]): record for record in records}
        records.sort(key=lambda record: record["score"], reverse=True)
        lines.append(f"- {cohort_key[0]}, {cohort_label}:")
        for record in records:
            parent = record["parent"]
            parent_record = by_generation.get(str(parent)) if parent is not None else None
            comparison = ""
            if parent_record is not None:
                delta = record["score"] - parent_record["score"]
                comparison = f"; parent gen_{parent}={parent_record['score']:.4f}, delta={delta:+.4f}"
            lines.append(
                f"  gen_{record['generation']}={record['score']:.4f} (parent {parent}){comparison}"
            )
        best = records[0]
        report = best["report"]
        failures = report.get("question_ids_failed", [])
        if not failures and isinstance(report.get("per_task_score"), dict):
            failures = [key for key, value in report["per_task_score"].items()
                        if isinstance(value, (int, float)) and value < 1]
        if failures:
            lines.append(
                "  Best candidate failing task IDs: "
                + ", ".join(map(str, failures[:12])) + "."
            )
    if excluded:
        lines.append("Excluded reports: " + "; ".join(excluded[:12]) + ".")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """
        A meta agent that recursively self-improves.

        Args:
            repo_path (str): The path to the repository.
            eval_path (str): The path to previously generated agents and their evaluation results.
            iterations_left (int, optional): The number of remaining iterations in which the meta agent will be invoked in future. Defaults to None.
        """
        evidence = _evaluation_summary(eval_path)
        instruction = f"Modify any part of the codebase at `{repo_path}`."
        # [experiment adaptation, see DECISIONS.md] gpt-6-luna otherwise asks for clarification and never edits.
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; use a tool call to edit, and finish only after the change is complete.\n\n"
            "Start with this automatically compiled evaluation summary, then verify relevant reports, metadata, patches, and failure logs yourself:\n"
            f"{evidence}\n\n"
            "Compare each candidate with its parent and the initial agent only when their evaluation cohorts are comparable; the newest generation is not necessarily the best, "
            "and an unevaluated generation is not evidence of improvement. Preserve behavior from the strongest completed result "
            "unless there is a specific, evidence-based reason to change it. Treat failed cases as clues for hypotheses, not as "
            "justification for unsupported task-specific hints. Prefer a small general change that addresses an identifiable failure "
            "mode while preserving solved cases, and keep agent interfaces and enforced budgets intact. Do not claim improvement "
            "unless evaluation confirms it."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
