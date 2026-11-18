# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
import re

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def summarize_evaluation_history(eval_path, max_reports=12):
    """Summarize recent and best evaluations, regressions, and failure evidence."""
    if not eval_path or not os.path.isdir(eval_path):
        return "No evaluation reports were found (evaluation directory is unavailable)."

    reports = []
    task_statuses = {}
    task_observations = {}
    task_failures = {}
    prediction_diagnostics = []
    for root, dirs, files in os.walk(eval_path):
        dirs.sort()
        if "report.json" not in files:
            continue
        relative_parts = os.path.relpath(root, eval_path).split(os.sep)
        generation = generation_label = generation_index = None
        for index, part in enumerate(relative_parts):
            match = re.fullmatch(r"gen_(initial|\d+)(?:\..*)?", part)
            if match:
                generation_label = match.group(1)
                generation = -1 if generation_label == "initial" else int(generation_label)
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
        raw_score = data.get("overall_accuracy", data.get("accuracy"))
        if isinstance(raw_score, bool):
            continue
        try:
            score = float(raw_score)
        except (TypeError, ValueError, OverflowError):
            continue
        if not math.isfinite(score):
            continue

        kind_parts = relative_parts[generation_index + 1:]
        kind = "/".join(kind_parts) if kind_parts else "report"
        outcomes = {}
        task_scores = data.get("per_task_score", {})
        if isinstance(task_scores, dict):
            for task, value in task_scores.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                try:
                    finite_value = math.isfinite(value)
                except (TypeError, ValueError, OverflowError):
                    continue
                if not finite_value:
                    continue
                task = str(task)
                passed = value >= 1
                outcomes[task] = passed
                key = (kind, task)
                task_observations.setdefault(key, set()).add(generation)
                if not passed:
                    task_failures.setdefault(key, set()).add(generation)
        failed = sorted(task for task, passed in outcomes.items() if not passed)
        task_statuses[(kind, generation)] = outcomes
        total = data.get("total")
        if isinstance(total, bool) or not isinstance(total, int):
            total = None
        reports.append((generation, generation_label, kind, score, total, failed))

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
                for prediction in predictions:
                    if not isinstance(prediction, dict):
                        continue
                    task_id = str(prediction.get("task_id", ""))
                    if task_id not in failed:
                        continue
                    count = prediction.get("n_answers_returned")
                    count_text = (f"{count} candidate(s)" if isinstance(count, int) and not isinstance(count, bool)
                                  else "answer count unavailable")
                    detail = f"gen_{generation_label} [{kind}] {task_id}: "
                    detail += "solved" if prediction.get("solved") is True else "not solved"
                    detail += f", {count_text}"
                    wrong = prediction.get("wrong_answers")
                    if isinstance(wrong, list) and wrong:
                        detail += f", {len(wrong)} wrong answer set(s)"
                    if prediction.get("agent_error"):
                        error_text = " ".join(str(prediction["agent_error"]).split())[:120]
                        detail += f", agent_error={error_text}"
                    prediction_diagnostics.append((generation, detail))

    if not reports:
        return "No usable evaluation reports were found in the supplied history."

    reports.sort(key=lambda row: (row[0], row[2]))
    try:
        limit = len(reports) if max_reports is None else max(1, int(max_reports))
    except (TypeError, ValueError, OverflowError):
        limit = 12
    selected = reports[-limit:]
    selected_keys = {(row[0], row[2]) for row in selected}
    by_kind = {}
    for report in reports:
        by_kind.setdefault(report[2], []).append(report)
    for entries in by_kind.values():
        best = max(entries, key=lambda row: (row[3], row[0]))
        if (best[0], best[2]) not in selected_keys:
            selected.append(best)
    selected.sort(key=lambda row: (row[0], row[2]))

    lines = ["Prior evaluation results (accuracy; compare patches and predictions across generations, not just scores):"]
    for _, label, kind, score, total, failed in selected:
        count = f", {total} tasks" if total is not None else ""
        failures = f"; partial/failed task IDs: {', '.join(failed[:12])}" if failed else "; no partial/failed tasks reported"
        lines.append(f"- gen_{label} [{kind}]: {score:.3f}{count}{failures}")

    for kind, entries in sorted(by_kind.items()):
        best = max(entries, key=lambda row: (row[3], row[0]))
        latest = entries[-1]
        if len(entries) > 1 and latest[3] < best[3]:
            lines.append(
                f"- Regression signal for {kind}: latest gen_{latest[1]} is {latest[3]:.3f}, "
                f"below gen_{best[1]} best {best[3]:.3f}; inspect its changes before proposing another."
            )
        generations = sorted({entry[0] for entry in entries})
        if len(generations) > 1:
            previous_generation, latest_generation = generations[-2:]
            previous = task_statuses.get((kind, previous_generation), {})
            current = task_statuses.get((kind, latest_generation), {})
            common = previous.keys() & current.keys()
            regressed = sorted(task for task in common if previous[task] and not current[task])
            recovered = sorted(task for task in common if not previous[task] and current[task])
            if regressed or recovered:
                changes = []
                if regressed:
                    changes.append("newly partial/failed: " + ", ".join(regressed[:12]))
                if recovered:
                    changes.append("recovered: " + ", ".join(recovered[:12]))
                lines.append(
                    f"- Task-level changes from gen_{previous_generation} to gen_{latest_generation} "
                    f"[{kind}]: " + "; ".join(changes)
                )

    recurring = []
    for (kind, task), generations in task_failures.items():
        if len(generations) >= 2:
            recurring.append((kind, task, len(generations), len(task_observations[(kind, task)])))
    if recurring:
        recurring.sort(key=lambda row: (row[0], -row[2], row[1]))
        entries = ", ".join(
            f"{task} ({failures}/{observed} generations)"
            for _, task, failures, observed in recurring[:12]
        )
        lines.append(f"- Recurring partial/failed tasks (evidence across runs, not a single miss): {entries}")

    if prediction_diagnostics:
        lines.append("Prediction diagnostics for failed tasks (answer grids omitted):")
        for _, detail in sorted(prediction_diagnostics)[-16:]:
            lines.append(f"- {detail}")
    lines.append(
        "- Inspect cited generations' agent_output/model_patch.diff and arc_eval/predictions.json; "
        "for recurring or changed task IDs, inspect available arc_eval/agent_evals/chat_history_<task>_0.md."
    )
    lines.append(
        "Use the evidence to identify repeatable improvements, investigate recurring failures, and "
        "preserve changes that improve overall performance without causing avoidable regressions."
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
