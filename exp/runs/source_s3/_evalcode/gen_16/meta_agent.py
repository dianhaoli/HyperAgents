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


def _report_score(report):
    """Return a scalar score from commonly used domain report formats."""
    if not isinstance(report, dict):
        return None
    for key in ("overall_accuracy", "score", "accuracy"):
        value = report.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
    return None


def _evaluation_summary(eval_path, max_candidates=3):
    """Summarize comparable, completed generations without trusting archive order."""
    if not os.path.isdir(eval_path):
        return "No prior evaluation directory was available to inspect."

    completed = {}
    incomplete = []
    try:
        generation_dirs = sorted(os.listdir(eval_path))
    except OSError:
        return "The prior evaluation directory could not be listed."

    for dirname in generation_dirs:
        if not dirname.startswith("gen_"):
            continue
        gen_dir = os.path.join(eval_path, dirname)
        if not os.path.isdir(gen_dir):
            continue
        metadata = _load_json(os.path.join(gen_dir, "metadata.json")) or {}
        is_initial = dirname == "gen_initial"
        try:
            eval_names = sorted(os.listdir(gen_dir))
        except OSError:
            continue
        for eval_name in eval_names:
            # Only use the primary report, not validation/test or ensemble reports.
            if not eval_name.endswith("_eval"):
                continue
            report = _load_json(os.path.join(gen_dir, eval_name, "report.json"))
            score = _report_score(report)
            if score is None:
                continue
            domain = eval_name[:-len("_eval")]
            sample_count = None
            for key in ("total_test_inputs", "total", "num_tasks"):
                value = report.get(key) if isinstance(report, dict) else None
                if isinstance(value, int) and not isinstance(value, bool):
                    sample_count = value
                    break
            scope = (domain, sample_count)
            record = {
                "generation": "initial" if is_initial else dirname[4:],
                "score": score,
                "parent": metadata.get("parent_genid"),
                "report": report,
                "complete": is_initial or metadata.get("run_full_eval") is True,
                "valid": is_initial or metadata.get("valid_parent") is not False,
            }
            if record["complete"] and record["valid"]:
                completed.setdefault(scope, []).append(record)
            else:
                incomplete.append((domain, record))

    lines = ["Prior evaluation evidence (scores are comparable only within the same domain and sample count):"]
    if not completed:
        lines.append("- No completed, valid generation reports were found; inspect available metadata and reports before making performance claims.")
    for (domain, sample_count), records in sorted(completed.items()):
        records.sort(key=lambda item: (item["score"], str(item["generation"])), reverse=True)
        count_text = "unknown sample count" if sample_count is None else f"{sample_count} test inputs/tasks"
        top_records = records[:max_candidates]
        # Keep the starting agent visible even when it is not among the top candidates.
        baseline = next((record for record in records if record["generation"] == "initial"), None)
        if baseline is not None and baseline not in top_records:
            top_records.append(baseline)
        entries = [
            f"gen_{record['generation']}={record['score']:.4f} (parent {record['parent']})"
            for record in top_records
        ]
        lines.append(f"- {domain}, {count_text}: best completed candidates and baseline: " + "; ".join(entries) + ".")

        report = records[0]["report"]
        failures = report.get("question_ids_failed", []) if isinstance(report, dict) else []
        if not failures and isinstance(report, dict):
            task_scores = report.get("per_task_score")
            if isinstance(task_scores, dict):
                failures = [
                    task_id for task_id, value in task_scores.items()
                    if isinstance(value, (int, float)) and value < 1
                ]
        if failures:
            lines.append(
                "  Best candidate's reported failing task IDs: "
                + ", ".join(map(str, failures[:12])) + "."
            )

    if incomplete:
        descriptions = []
        for domain, record in incomplete[:8]:
            status = "partial evaluation" if not record["complete"] else "invalid parent"
            descriptions.append(
                f"{domain} gen_{record['generation']} ({status}, score {record['score']:.4f})"
            )
        lines.append("- Excluded from best-candidate comparisons: " + "; ".join(descriptions) + ".")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Recursively improve the agent using repository code and evaluation evidence."""
        evidence = _evaluation_summary(eval_path)
        instruction = f"Modify any part of the codebase at `{repo_path}`."
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply with a tool call or DONE when finished."
            "\n\nUse this automatically compiled evaluation summary as a starting point, then verify the relevant reports, metadata, and patches yourself:\n"
            f"{evidence}\n\n"
            "Choose changes based on evidence, not generation number or recency. Compare scores only when domain and evaluation sample counts match; distinguish completed evaluations from skipped, partial, or invalid runs. Inspect the best candidate's patch and its failures, preserve improvements that are supported by results, and propose a focused change aimed at a demonstrated weakness. Do not assume a prompt change helped unless a comparable evaluation supports it."
        )
        if iterations_left is not None:
            instruction += f"\nThere are {iterations_left} future generation iterations remaining."

        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
