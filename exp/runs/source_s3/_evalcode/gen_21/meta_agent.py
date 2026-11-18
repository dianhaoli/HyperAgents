# Copyright (c) Meta Platforms, Inc. and affiliates.

import hashlib
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
    """Summarize completed results, comparing only matching evaluation cohorts."""
    if not os.path.isdir(eval_path):
        return "No prior evaluation directory was available to inspect."

    cohorts = {}
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
            if not eval_name.endswith("_eval"):
                continue
            report = _load_json(os.path.join(gen_dir, eval_name, "report.json"))
            score = _report_score(report)
            if score is None:
                continue

            domain = eval_name[:-len("_eval")]
            sample_count = next((report.get(key) for key in
                                 ("total_test_inputs", "total", "num_tasks")
                                 if isinstance(report.get(key), int)
                                 and not isinstance(report.get(key), bool)), None)
            task_scores = report.get("per_task_score")
            if isinstance(task_scores, dict) and task_scores:
                task_ids = tuple(sorted(map(str, task_scores)))
                cohort = (domain, sample_count, "task_ids", task_ids)
                cohort_fingerprint = hashlib.sha1(
                    "\n".join(task_ids).encode("utf-8")
                ).hexdigest()[:8]
                count_label = (f"{sample_count} test inputs" if sample_count is not None
                               else "test-input count unavailable")
                cohort_label = (f"{len(task_ids)} task IDs [{cohort_fingerprint}], "
                                f"{count_label}")
            else:
                cohort = (domain, sample_count, "count")
                count_label = (f"{sample_count} reported samples" if sample_count is not None
                               else "sample count unavailable")
                cohort_label = (f"{count_label}; task IDs unavailable, so matching counts "
                                "do not guarantee identical samples")

            record = {
                "generation": "initial" if is_initial else dirname[4:],
                "parent": metadata.get("parent_genid"),
                "score": score,
                "report": report,
            }
            complete = is_initial or metadata.get("run_full_eval") is True
            valid = is_initial or metadata.get("valid_parent") is not False
            if complete and valid:
                cohorts.setdefault((cohort, cohort_label), []).append(record)
            else:
                status = "partial evaluation" if not complete else "invalid parent"
                incomplete.append(f"{eval_name} gen_{record['generation']} ({status})")

    if not cohorts:
        return "No completed, valid generation reports with scalar scores were found."

    lines = ["Completed evaluation evidence (compare only within the same domain and cohort):"]
    for (cohort, cohort_label), records in sorted(
            cohorts.items(), key=lambda item: str(item[0][0])):
        by_generation = {str(record["generation"]): record for record in records}
        records.sort(key=lambda record: record["score"], reverse=True)
        lines.append(f"- {cohort[0]}, {cohort_label}:")
        for record in records[:max_candidates]:
            parent = record["parent"]
            parent_record = (by_generation.get(str(parent))
                             if parent is not None and str(parent) != str(record["generation"])
                             else None)
            comparison = ""
            if parent_record is not None:
                delta = record["score"] - parent_record["score"]
                comparison = f"; matching-cohort parent gen_{parent}={parent_record['score']:.4f}, delta={delta:+.4f}"
            lines.append(
                f"  gen_{record['generation']}={record['score']:.4f} "
                f"(parent {parent}){comparison}"
            )

        baseline = next((record for record in records
                         if record["generation"] == "initial"), None)
        if baseline is not None and baseline not in records[:max_candidates]:
            lines.append(f"  gen_initial={baseline['score']:.4f} (baseline)")

        best = records[0]["report"]
        failures = best.get("question_ids_failed", [])
        if not failures:
            task_scores = best.get("per_task_score")
            if isinstance(task_scores, dict):
                failures = [task_id for task_id, value in task_scores.items()
                            if isinstance(value, (int, float)) and value < 1]
        if failures:
            lines.append("  Best candidate's reported failing task IDs: "
                         + ", ".join(map(str, failures[:12])) + ".")

    if incomplete:
        lines.append("- Excluded from completed comparisons: " + "; ".join(incomplete[:8]) + ".")
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
