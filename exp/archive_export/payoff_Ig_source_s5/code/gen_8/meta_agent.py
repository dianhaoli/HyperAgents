# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import re
from pathlib import Path

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def summarize_evaluations(eval_path, max_reports=40, max_task_ids=8):
    """Summarize report metrics and parent comparisons without reading predictions."""
    root = Path(eval_path)
    if not root.is_dir():
        return f"No evaluation directory found at {eval_path}."

    generations = {}
    for generation_dir in root.glob("gen_*"):
        match = re.fullmatch(r"gen_(initial|[0-9]+)", generation_dir.name)
        if not match or not generation_dir.is_dir():
            continue

        genid = match.group(1)
        metadata = {}
        try:
            metadata = json.loads((generation_dir / "metadata.json").read_text())
        except (OSError, ValueError):
            pass

        reports = {}
        for report_path in generation_dir.rglob("report.json"):
            try:
                report = json.loads(report_path.read_text())
            except (OSError, ValueError):
                continue
            score = next(
                (report.get(key) for key in (
                    "overall_accuracy", "accuracy_score", "points_percentage",
                    "average_progress", "average_fitness",
                ) if isinstance(report.get(key), (int, float))
                and math.isfinite(report[key])),
                None,
            )
            if score is None:
                continue

            task_scores = report.get("per_task_score", {})
            if not isinstance(task_scores, dict):
                task_scores = {}
            failed = report.get("question_ids_failed", [])
            if not isinstance(failed, list):
                failed = []
            passed = report.get("question_ids_passed", [])
            if not isinstance(passed, list):
                passed = []
            reports[report_path.relative_to(generation_dir).as_posix()] = {
                "score": float(score),
                "total": report.get("total"),
                "task_scores": task_scores,
                "failed": {str(task_id) for task_id in failed},
                "passed": {str(task_id) for task_id in passed},
            }

        generations[genid] = {
            "parent": metadata.get("parent_genid"),
            "reports": reports,
        }

    order = lambda genid: (-1 if genid == "initial" else int(genid))
    entries = []
    for genid, generation in generations.items():
        for relpath, report in generation["reports"].items():
            entries.append((genid, relpath, report, generation["parent"]))
    entries.sort(key=lambda entry: (order(entry[0]), entry[1]))
    if not entries:
        return f"No readable evaluation reports found under {eval_path}."

    lines = [
        "Read-only evaluation summary (metrics/task IDs only; predictions are not included):"
    ]
    for genid, relpath, report, parent in entries[:max_reports]:
        line = f"gen_{genid}/{relpath}: score={report['score']:.3f}"
        if isinstance(report["total"], int):
            line += f", reported total={report['total']}"

        parent_id = str(parent) if parent is not None else None
        parent_report = generations.get(parent_id, {}).get("reports", {}).get(relpath)
        if parent_report is not None:
            delta = report["score"] - parent_report["score"]
            line += f"; vs parent gen_{parent_id} {delta:+.3f}"
            newly_passed = sorted(
                (report["passed"] - parent_report["passed"])
                | {
                    str(task_id) for task_id, score in report["task_scores"].items()
                    if isinstance(score, (int, float)) and score >= 1
                    and isinstance(parent_report["task_scores"].get(task_id), (int, float))
                    and parent_report["task_scores"][task_id] < 1
                }
            )
            newly_failed = sorted(
                (report["failed"] - parent_report["failed"])
                | {
                    str(task_id) for task_id, score in parent_report["task_scores"].items()
                    if isinstance(score, (int, float)) and score >= 1
                    and isinstance(report["task_scores"].get(task_id), (int, float))
                    and report["task_scores"][task_id] < 1
                }
            )
            if newly_passed:
                line += f"; newly passed IDs: {', '.join(newly_passed[:max_task_ids])}"
            if newly_failed:
                line += f"; newly failed IDs: {', '.join(newly_failed[:max_task_ids])}"
        if report["failed"]:
            line += f"; failed IDs: {', '.join(sorted(report['failed'])[:max_task_ids])}"
        lines.append(line)

    if len(entries) > max_reports:
        lines.append(f"({len(entries) - max_reports} additional reports omitted.)")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Recursively improve the agent-generation system using prior evaluations."""
        evaluation_summary = summarize_evaluations(eval_path)
        instruction = (
            f"Improve the agent-generation system in `{repo_path}`. Read its README.md and inspect "
            f"the relevant implementation and previous generation patches under `{eval_path}`.\n\n"
            f"{evaluation_summary}\n\n"
            "Use the evaluation summaries as evidence, not as proof of causation: compare each candidate "
            "with its recorded parent where available, consider the number of evaluated tasks, and inspect "
            "the candidate's patch before attributing score or task-level changes to it. Results may be "
            "noisy or incomplete. Prefer one focused change that addresses a concrete weakness and can be "
            "evaluated in a later iteration. Do not modify prior evaluation artifacts, predictions, or "
            "domain data. Run relevant lightweight tests or validation after editing and state what was "
            "verified. Work autonomously; nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect and edit the repository, and only finish after making the change."
        )
        if iterations_left is not None:
            instruction += (
                f"\nThere are {iterations_left} future self-improvement iterations available; favor "
                "changes whose effects can be checked in a later evaluation."
            )

        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
