# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import re
from pathlib import Path

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _evaluation_summary(eval_path, limit=12):
    """Summarize recent machine-readable evaluations for the improvement agent.

    Include coverage signatures so scores from different task sets are not mistaken
    for directly comparable results. Missing or malformed reports are ignored.
    """
    root = Path(eval_path)
    if not root.is_dir():
        return "No evaluation report directory was available for automatic summarization."

    reports = []
    for report_path in root.rglob("report.json"):
        try:
            with report_path.open(encoding="utf-8") as f:
                report = json.load(f)
            if not isinstance(report, dict) or not any(
                key in report for key in ("overall_accuracy", "per_task_score")
            ):
                continue
            task_scores = report.get("per_task_score")
            if isinstance(task_scores, dict):
                task_ids = tuple(sorted(str(key) for key in task_scores))
            else:
                task_ids = tuple(sorted(
                    str(task_id)
                    for task_id in (
                        list(report.get("question_ids_passed", []))
                        + list(report.get("question_ids_failed", []))
                    )
                ))
            reports.append((report_path, report, task_ids))
        except (OSError, ValueError, TypeError):
            continue

    if not reports:
        return "No readable evaluation reports were found for automatic summarization."

    def generation_order(item):
        match = re.search(r"(?:^|/)gen_(initial|\d+)(?:/|$)", item[0].as_posix())
        if not match:
            return (2, item[0].as_posix())
        generation = match.group(1)
        return (0, 0) if generation == "initial" else (1, int(generation))

    reports.sort(key=generation_order)
    reports = reports[-limit:]

    cohorts = {}
    for _, _, task_ids in reports:
        if task_ids:
            cohorts.setdefault(task_ids, f"C{len(cohorts) + 1}")

    lines = [
        "Automatically collected evaluation evidence (verify relevant predictions and logs before drawing conclusions):"
    ]
    for report_path, report, task_ids in reports:
        try:
            label = report_path.relative_to(root).as_posix()
        except ValueError:
            label = report_path.as_posix()
        accuracy = report.get("overall_accuracy")
        accuracy_text = f"accuracy={accuracy:.3f}" if isinstance(accuracy, (int, float)) else "accuracy=unknown"
        total = report.get("total")
        if isinstance(total, int):
            accuracy_text += f", tasks={total}"
        test_inputs = report.get("total_test_inputs")
        if isinstance(test_inputs, int):
            accuracy_text += f", test_inputs={test_inputs}"
        if task_ids:
            accuracy_text += f", coverage={cohorts[task_ids]} ({len(task_ids)} task IDs)"
        failed = report.get("question_ids_failed")
        if not isinstance(failed, list) and isinstance(report.get("per_task_score"), dict):
            failed = [
                task_id for task_id, score in report["per_task_score"].items()
                if isinstance(score, (int, float)) and score < 1
            ]
        if isinstance(failed, list):
            shown = ",".join(str(task_id) for task_id in failed[:16])
            accuracy_text += f", failed={len(failed)} [{shown}{',…' if len(failed) > 16 else ''}]"
        lines.append(f"- {label}: {accuracy_text}")

    lines.append(
        "Reports with the same coverage label contain the same task IDs and are the safest score comparisons; "
        "different labels may cover different tasks. Inspect per-task predictions and chat histories before changing the agent."
    )
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
        instruction = f"Modify any part of the codebase at `{repo_path}`."
        # [experiment adaptation, see DECISIONS.md] gpt-6-luna otherwise asks for clarification and never edits.
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Before editing, inspect the evaluation reports and metadata for the latest generations and their parents. "
            "Use the automatically collected report summary below as a starting point, not as a substitute for inspecting useful failed-task predictions and chat logs. "
            "Compare scores only when their coverage labels match, and use per-task results to distinguish persistent failures from regressions. "
            "Make a focused change to the agent or generation mechanism that addresses a concrete failure pattern. "
            "Do not edit evaluation outputs or add caches/bytecode. Run lightweight checks for your change and do not claim an untested improvement.\n\n"
            f"{_evaluation_summary(eval_path)}\n\n"
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
