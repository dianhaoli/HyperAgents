# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
from collections import Counter, defaultdict

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _evaluation_summary(eval_path, max_candidates=3):
    """Summarize valid prior runs without comparing different evaluation cohorts."""
    if not os.path.isdir(eval_path):
        return (
            f"No prior evaluation directory found at {eval_path!r}. "
            "Inspect available evidence before making performance claims."
        )

    completed = defaultdict(list)
    incomplete = []
    for dirname in sorted(os.listdir(eval_path)):
        if dirname != "gen_initial" and not (
            dirname.startswith("gen_") and dirname[4:].isdigit()
        ):
            continue
        gen_dir = os.path.join(eval_path, dirname)
        if not os.path.isdir(gen_dir):
            continue

        metadata = {}
        try:
            with open(os.path.join(gen_dir, "metadata.json"), encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                metadata = loaded
        except (OSError, ValueError):
            pass

        reports = []
        for child in sorted(os.listdir(gen_dir)):
            report_path = os.path.join(gen_dir, child, "report.json")
            if child.endswith("_eval") and os.path.isfile(report_path):
                reports.append(report_path)
        if not reports:
            if metadata.get("run_eval") is False:
                incomplete.append(f"{dirname}: evaluation skipped")
            elif metadata.get("valid_parent") is False:
                incomplete.append(f"{dirname}: invalid generation")
            continue

        for report_path in reports:
            domain = os.path.basename(os.path.dirname(report_path))[:-5]
            label = f"{dirname}/{domain}"
            if metadata.get("valid_parent") is False:
                incomplete.append(f"{label}: invalid generation (report excluded)")
                continue
            if metadata.get("run_eval") is False:
                incomplete.append(f"{label}: evaluation marked skipped (report excluded)")
                continue
            try:
                with open(report_path, encoding="utf-8") as f:
                    report = json.load(f)
            except (OSError, ValueError):
                incomplete.append(f"{label}: unreadable report")
                continue
            if not isinstance(report, dict):
                incomplete.append(f"{label}: malformed report")
                continue

            task_scores = {}
            raw_scores = report.get("per_task_score")
            if isinstance(raw_scores, dict):
                for task_id, value in raw_scores.items():
                    if (isinstance(value, (int, float)) and not isinstance(value, bool)
                            and math.isfinite(value) and 0 <= value <= 1):
                        task_scores[str(task_id)] = float(value)

            score = report.get("overall_accuracy")
            if not (isinstance(score, (int, float)) and not isinstance(score, bool)
                    and math.isfinite(score) and 0 <= score <= 1):
                score = (
                    sum(task_scores.values()) / len(task_scores) if task_scores else None
                )
            if score is None:
                incomplete.append(f"{label}: missing or invalid accuracy")
                continue

            if task_scores:
                cohort = ("task_ids", tuple(sorted(task_scores)))
                cohort_label = f"{len(task_scores)} exact task IDs"
            else:
                sample_count = next(
                    (report.get(key) for key in ("total_test_inputs", "total", "num_tasks")
                     if isinstance(report.get(key), int)
                     and not isinstance(report.get(key), bool)
                     and report.get(key) >= 0),
                    None,
                )
                cohort = ("count", sample_count)
                cohort_label = (
                    f"{sample_count} tasks (IDs unavailable)"
                    if sample_count is not None else "unknown-size cohort"
                )

            completed[(domain, cohort)].append({
                "generation": "initial" if dirname == "gen_initial" else dirname[4:],
                "score": float(score),
                "parent": metadata.get("parent_genid"),
                "task_scores": task_scores,
                "cohort_label": cohort_label,
            })

    lines = [
        "Prior evaluation evidence. Compare results only within the same domain and exact task-ID cohort when available; equal sample counts without IDs are weaker evidence."
    ]
    if not completed:
        lines.append("- No completed, valid reports found; inspect available reports and metadata.")
    for (domain, _cohort), records in sorted(
        completed.items(), key=lambda item: (item[0][0], repr(item[0][1]))
    ):
        records.sort(key=lambda record: (-record["score"], str(record["generation"])))
        lines.append(f"- {domain}, {records[0]['cohort_label']}:")
        selected = records[:max_candidates]
        baseline = next((r for r in records if r["generation"] == "initial"), None)
        if baseline is not None and baseline not in selected:
            selected.append(baseline)
        for record in selected:
            parent = "" if record["parent"] is None else f", parent {record['parent']}"
            failed = sorted(
                task for task, value in record["task_scores"].items() if value < 1
            )
            failure_note = (
                f"; failing task IDs: {', '.join(failed[:10])}" if failed else ""
            )
            lines.append(
                f"  gen_{record['generation']}={record['score']:.4f}"
                f"{parent}{failure_note}"
            )

        # Repeated misses suggest where to investigate; they do not establish a cause.
        scored_records = [r for r in records if r["task_scores"]]
        failures = Counter(
            task
            for record in scored_records
            for task, value in record["task_scores"].items()
            if value < 1
        )
        recurrent = [(task, count) for task, count in failures.most_common(6) if count > 1]
        if recurrent:
            lines.append(
                "  Recurrent failures (failed reports / reports with task scores): "
                + ", ".join(
                    f"{task} {count}/{len(scored_records)}" for task, count in recurrent
                )
            )

    if incomplete:
        examples = "; ".join(incomplete[:8])
        suffix = " ..." if len(incomplete) > 8 else ""
        lines.append(f"- Excluded/incomplete runs: {len(incomplete)} ({examples}{suffix}).")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Improve the agent using repository and prior evaluation evidence."""
        instruction = (
            f"Modify any part of the codebase at `{repo_path}`.\n\n"
            f"The repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification.\n\n"
            "Use this summary as a starting point, then inspect relevant reports, metadata, patches, and failure details yourself. "
            "Choose changes based on comparable evaluation evidence, not generation number or recency. Recurrent failures are hypotheses to investigate, not proof of a shared cause. "
            "Favor focused, general changes, preserve behavior supported by the strongest comparable result, and distinguish completed evaluations from skipped, invalid, or incomparable runs. "
            "Keep the task-agent interface and enforced model-call/answer budgets intact. Do not claim performance improvement without comparable evaluation.\n\n"
            f"{_evaluation_summary(eval_path)}\n\n"
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )
        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
