# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
import re

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def summarize_evaluation_history(eval_path, max_reports=12):
    """Summarize prior generation reports for the meta-agent prompt.

    Reports are grouped by generation and evaluation type (for example, arc_eval).
    Malformed files and reports without accuracy scores are ignored so an incomplete
    history cannot prevent an improvement run.
    """
    if not eval_path or not os.path.isdir(eval_path):
        return "No evaluation reports were found (evaluation directory is unavailable)."

    reports = []
    task_observations = {}
    task_failures = {}
    task_statuses = {}
    prediction_diagnostics = []
    for root, dirs, files in os.walk(eval_path):
        dirs.sort()
        if "report.json" not in files:
            continue
        relative_parts = os.path.relpath(root, eval_path).split(os.sep)
        generation = None
        generation_index = None
        for index, part in enumerate(relative_parts):
            match = re.fullmatch(r"gen_(initial|\d+)(?:\..*)?", part)
            if match:
                label = match.group(1)
                generation = -1 if label == "initial" else int(label)
                generation_index = index
                break
        if generation is None:
            continue
        try:
            with open(os.path.join(root, "report.json"), encoding="utf-8") as stream:
                data = json.load(stream)
        except (OSError, ValueError, TypeError):
            continue
        if not isinstance(data, dict):
            continue
        score = data.get("overall_accuracy", data.get("accuracy"))
        try:
            score = float(score)
        except (TypeError, ValueError, OverflowError):
            continue
        if not math.isfinite(score):
            continue
        kind_parts = relative_parts[generation_index + 1:]
        kind = "/".join(kind_parts) if kind_parts else "report"
        task_scores = data.get("per_task_score", {})
        failed = []
        outcomes = {}
        if isinstance(task_scores, dict):
            for task, value in task_scores.items():
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    continue
                try:
                    finite_value = math.isfinite(value)
                except OverflowError:
                    finite_value = False
                if not finite_value:
                    continue
                task = str(task)
                outcomes[task] = value >= 1
                key = (kind, task)
                task_observations.setdefault(key, set()).add(generation)
                if value < 1:
                    failed.append(task)
                    task_failures.setdefault(key, set()).add(generation)
        task_statuses[(kind, generation)] = outcomes

        # Predictions can distinguish wrong answers from execution failures. Keep
        # only compact metadata; answer grids can be large and are inspected directly.
        if failed:
            try:
                with open(os.path.join(root, "predictions.json"), encoding="utf-8") as stream:
                    predictions = json.load(stream)
            except (OSError, ValueError, TypeError):
                predictions = []
            if isinstance(predictions, dict):
                normalized = []
                for task_id, prediction in predictions.items():
                    if isinstance(prediction, dict):
                        prediction = dict(prediction)
                        prediction.setdefault("task_id", task_id)
                        normalized.append(prediction)
                predictions = normalized
            if isinstance(predictions, list):
                failed_ids = set(failed)
                for prediction in predictions:
                    if not isinstance(prediction, dict):
                        continue
                    task_id = str(prediction.get("task_id", ""))
                    if task_id not in failed_ids:
                        continue
                    solved = prediction.get("solved")
                    status = ("test input solved" if solved is True else
                              "test input not solved" if solved is False else
                              "test input status unavailable")
                    detail = f"gen_{label} [{kind}] {task_id}: {status}"
                    test_input = prediction.get("test_input")
                    if isinstance(test_input, (int, str)) and not isinstance(test_input, bool):
                        detail += f" (test input {test_input})"
                    count = prediction.get("n_answers_returned")
                    if isinstance(count, int) and not isinstance(count, bool):
                        detail += f", {count} candidate(s)"
                    wrong = prediction.get("wrong_answers")
                    if isinstance(wrong, list) and wrong:
                        detail += f", {len(wrong)} wrong answer set(s)"
                    error = prediction.get("agent_error")
                    if error:
                        error_text = " ".join(str(error).split())[:120]
                        detail += f", agent_error={error_text}"
                    prediction_diagnostics.append((generation, detail))
        reports.append((generation, label, kind, score, data.get("total"), sorted(failed)))

    if not reports:
        return "No usable evaluation reports were found in the supplied history."

    reports.sort(key=lambda row: (row[0], row[2]))
    if max_reports is None:
        report_limit = len(reports)
    else:
        try:
            report_limit = max(1, int(max_reports))
        except (TypeError, ValueError, OverflowError):
            report_limit = 12

    # Keep recent records for the trend, but never hide the strongest checkpoint
    # for an evaluation type just because it fell outside the recent window.
    selected_reports = reports[-report_limit:]
    selected_keys = {(row[0], row[2]) for row in selected_reports}
    best_by_kind = {}
    for row in reports:
        previous = best_by_kind.get(row[2])
        if previous is None or (row[3], row[0]) > (previous[3], previous[0]):
            best_by_kind[row[2]] = row
    for row in best_by_kind.values():
        if (row[0], row[2]) not in selected_keys:
            selected_reports.append(row)
    selected_reports.sort(key=lambda row: (row[0], row[2]))

    lines = ["Prior evaluation results (accuracy; lower-scoring generations are useful regression evidence):"]
    for _, generation_label, kind, score, total, failed in selected_reports:
        count = f", {total} tasks" if isinstance(total, int) and not isinstance(total, bool) else ""
        failures = f"; partial/failed task IDs: {', '.join(failed[:12])}" if failed else "; no partial/failed tasks reported"
        lines.append(f"- gen_{generation_label} [{kind}]: {score:.3f}{count}{failures}")

    by_kind = {}
    for report in reports:
        by_kind.setdefault(report[2], []).append(report)
    for kind, entries in sorted(by_kind.items()):
        if len(entries) < 2:
            continue
        best = max(entries, key=lambda row: row[3])
        latest = entries[-1]
        if latest[3] < best[3]:
            lines.append(
                f"- Regression signal for {kind}: latest gen_{latest[1]} is {latest[3]:.3f}, "
                f"below gen_{best[1]} best {best[3]:.3f}; inspect its changes before proposing another."
            )

    for kind in sorted({report[2] for report in reports}):
        evaluated_generations = sorted({report[0] for report in reports if report[2] == kind})
        if len(evaluated_generations) < 2:
            continue
        previous_generation, latest_generation = evaluated_generations[-2:]
        previous = task_statuses.get((kind, previous_generation), {})
        latest = task_statuses.get((kind, latest_generation), {})
        common_tasks = previous.keys() & latest.keys()
        newly_partial = sorted(task for task in common_tasks if previous[task] and not latest[task])
        recovered = sorted(task for task in common_tasks if not previous[task] and latest[task])
        if newly_partial or recovered:
            changes = []
            if newly_partial:
                changes.append("newly partial/failed: " + ", ".join(newly_partial[:12]))
            if recovered:
                changes.append("recovered: " + ", ".join(recovered[:12]))
            lines.append(
                f"- Task-level changes from gen_{previous_generation} to gen_{latest_generation} "
                f"[{kind}]: " + "; ".join(changes)
            )

    recurring = []
    for (kind, task), failed_generations in task_failures.items():
        if len(failed_generations) >= 2:
            observed_generations = len(task_observations[(kind, task)])
            recurring.append((kind, task, len(failed_generations), observed_generations))
    if recurring:
        recurring.sort(key=lambda item: (item[0], -item[2], item[1]))
        details = ", ".join(
            f"{task} ({failure_count}/{observed_count} generations)"
            for _, task, failure_count, observed_count in recurring[:12]
        )
        lines.append(f"- Recurring partial/failed tasks across runs: {details}")

    lines.append(
        "Inspect cited generations' agent_output/model_patch.diff and arc_eval/predictions.json; "
        "for recurring task IDs, inspect their per-task prediction and available agent chat history. "
        "Use the reports and evidence to identify repeatable improvements, investigate recurring "
        "failures, and preserve changes that improve overall performance without causing avoidable regressions."
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
        evaluation_summary = summarize_evaluation_history(eval_path)
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Inspect relevant prior patches and predictions as well as the reports; do not assume that a single score change proves a technique is generally better. "
            "Use this compact report summary to guide that inspection:\n\n"
            f"{evaluation_summary}\n\n"
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
