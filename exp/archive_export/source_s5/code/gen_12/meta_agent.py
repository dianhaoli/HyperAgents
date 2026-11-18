# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import re
from pathlib import Path

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def summarize_evaluations(eval_path, max_reports=24, max_task_ids=8):
    """Summarize prior report metrics without exposing predictions or test outputs."""
    root = Path(eval_path)
    if not root.is_dir():
        return f"No evaluation directory found at {eval_path}."

    reports = {}
    for generation_dir in root.glob("gen_*"):
        match = re.fullmatch(r"gen_(initial|[0-9]+)", generation_dir.name)
        if not match or not generation_dir.is_dir():
            continue
        genid = match.group(1)
        try:
            metadata = json.loads((generation_dir / "metadata.json").read_text())
        except (OSError, ValueError):
            metadata = {}
        parent = metadata.get("parent_genid")
        parent = str(parent) if parent is not None else None

        for report_path in generation_dir.rglob("report.json"):
            try:
                data = json.loads(report_path.read_text())
            except (OSError, ValueError):
                continue
            score = next(
                (data.get(key) for key in (
                    "overall_accuracy", "accuracy_score", "points_percentage",
                    "average_progress", "average_fitness",
                ) if isinstance(data.get(key), (int, float))
                and not isinstance(data.get(key), bool)
                and math.isfinite(data[key])),
                None,
            )
            if score is None:
                continue

            raw_scores = data.get("per_task_score", {})
            if not isinstance(raw_scores, dict):
                raw_scores = {}
            task_scores = {str(key): value for key, value in raw_scores.items()}
            failed = data.get("question_ids_failed", [])
            failed = {str(task_id) for task_id in failed} if isinstance(failed, list) else set()
            failed.update(
                task_id for task_id, task_score in task_scores.items()
                if isinstance(task_score, (int, float)) and not isinstance(task_score, bool)
                and task_score < 1
            )
            passed = data.get("question_ids_passed", [])
            passed = {str(task_id) for task_id in passed} if isinstance(passed, list) else set()
            passed.update(
                task_id for task_id, task_score in task_scores.items()
                if isinstance(task_score, (int, float)) and not isinstance(task_score, bool)
                and task_score >= 1
            )
            relpath = report_path.relative_to(generation_dir).as_posix()
            reports[(genid, relpath)] = {
                "score": float(score),
                "total": data.get("total"),
                "task_scores": task_scores,
                "failed": failed,
                "passed": passed,
                "parent": parent,
            }

    if not reports:
        return f"No readable evaluation reports found under {eval_path}."

    def order(genid):
        return -1 if genid == "initial" else int(genid)

    entries = sorted(reports.items(), key=lambda item: (order(item[0][0]), item[0][1]))
    shown = entries[-max_reports:] if max_reports > 0 else []
    lines = ["Prior evaluation reports (metrics and task IDs only; predictions are not included):"]
    for (genid, relpath), report in shown:
        line = f"gen_{genid}/{relpath}: score={report['score']:.3f}"
        if isinstance(report["total"], int) and not isinstance(report["total"], bool):
            line += f", reported total={report['total']}"
        parent_id = report["parent"]
        parent = reports.get((parent_id, relpath)) if parent_id else None
        if parent is not None:
            line += f"; vs parent gen_{parent_id} {report['score'] - parent['score']:+.3f}"
            newly_passed = sorted(report["passed"] - parent["passed"])
            newly_failed = sorted(report["failed"] - parent["failed"])
            if newly_passed:
                line += "; newly passed: " + ", ".join(newly_passed[:max_task_ids])
            if newly_failed:
                line += "; newly failed: " + ", ".join(newly_failed[:max_task_ids])
        failed_ids = sorted(report["failed"])
        if failed_ids:
            line += f"; failed IDs ({len(failed_ids)}): " + ", ".join(failed_ids[:max_task_ids])
            if len(failed_ids) > max_task_ids:
                line += f", and {len(failed_ids) - max_task_ids} more"
        lines.append("- " + line)
    if len(entries) > len(shown):
        lines.append(f"- {len(entries) - len(shown)} older report(s) omitted.")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Recursively improve the system using prior implementation and evaluation evidence."""
        evaluation_summary = summarize_evaluations(eval_path)
        instruction = (
            f"Improve the agent-generation system in `{repo_path}`. Read its README.md and inspect "
            f"the implementation and previous generation patches/logs under `{eval_path}`.\n\n"
            f"{evaluation_summary}\n\n"
            "Compare like-for-like reports and parent generations; inspect a change before attributing "
            "score differences to it, since evaluations may be small or noisy. Identify one concrete "
            "weakness and make a focused, reversible improvement. Do not modify prior evaluation "
            "artifacts, predictions, or task data. Run relevant lightweight checks after editing and "
            "say what was verified. Work autonomously: do not ask questions; use the tools to inspect "
            "and edit the repository, and only finish after making a change."
        )
        if iterations_left is not None:
            instruction += (
                f"\nThere are {iterations_left} future improvement iterations; favor a change whose "
                "effect can be assessed in a later evaluation."
            )
        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
