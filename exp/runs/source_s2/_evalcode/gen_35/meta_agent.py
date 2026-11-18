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
    task_statuses = {}
    task_observations = {}
    task_failures = {}
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
        if isinstance(score, bool):
            continue
        try:
            score = float(score)
        except (TypeError, ValueError, OverflowError):
            continue
        if not math.isfinite(score):
            continue
        kind_parts = relative_parts[generation_index + 1:]
        kind = "/".join(kind_parts) if kind_parts else "report"
        task_scores = data.get("per_task_score", {})
        outcomes = {}
        if isinstance(task_scores, dict):
            for task, value in task_scores.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                try:
                    if not math.isfinite(value):
                        continue
                except (TypeError, ValueError, OverflowError):
                    continue
                task = str(task)
                passed = value >= 1
                outcomes[task] = passed
                key = (kind, task)
                task_observations.setdefault(key, set()).add(generation)
                if not passed:
                    task_failures.setdefault(key, set()).add(generation)
        task_statuses[(kind, generation)] = outcomes
        failed = sorted(task for task, passed in outcomes.items() if not passed)
        total = data.get("total")
        if isinstance(total, bool) or not isinstance(total, int):
            total = None
        reports.append((generation, label, kind, score, total, failed))

    if not reports:
        return "No usable evaluation reports were found in the supplied history."

    reports.sort(key=lambda row: (row[0], row[2]))
    # Keep recent results, but don't let the report limit hide the best historical
    # checkpoint for an evaluation type. The best run is a useful comparison point
    # when diagnosing a regression in newer generations.
    try:
        report_limit = max(1, int(max_reports))
    except (TypeError, ValueError, OverflowError):
        report_limit = 12
    recent_reports = reports[-report_limit:]
    selected_keys = {(row[0], row[2]) for row in recent_reports}
    best_by_kind = {}
    for row in reports:
        previous = best_by_kind.get(row[2])
        if previous is None or (row[3], row[0]) > (previous[3], previous[0]):
            best_by_kind[row[2]] = row
    for row in best_by_kind.values():
        if (row[0], row[2]) not in selected_keys:
            recent_reports.append(row)
    recent_reports.sort(key=lambda row: (row[0], row[2]))

    lines = ["Prior evaluation results (accuracy; lower-scoring generations are useful regression evidence):"]
    for _, generation_label, kind, score, total, failed in recent_reports:
        count = f", {total} tasks" if isinstance(total, int) else ""
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

    for kind, entries in sorted(by_kind.items()):
        generations = sorted({entry[0] for entry in entries})
        if len(generations) < 2:
            continue
        previous_generation, latest_generation = generations[-2:]
        previous = task_statuses.get((kind, previous_generation), {})
        latest = task_statuses.get((kind, latest_generation), {})
        common_tasks = previous.keys() & latest.keys()
        regressed = sorted(task for task in common_tasks if previous[task] and not latest[task])
        recovered = sorted(task for task in common_tasks if not previous[task] and latest[task])
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
    for (kind, task), failed_generations in task_failures.items():
        if len(failed_generations) >= 2:
            observed = len(task_observations[(kind, task)])
            recurring.append((kind, task, len(failed_generations), observed))
    recurring.sort(key=lambda item: (item[0], -item[2], item[1]))
    if recurring:
        details = ", ".join(
            f"{task} ({failure_count}/{observed_count} generations)"
            for _, task, failure_count, observed_count in recurring[:12]
        )
        lines.append(f"- Recurring partial/failed tasks across runs: {details}")

    lines.append(
        "Inspect cited generations' agent_output/model_patch.diff and predictions for task-level "
        "regressions and recurring failures. Use this evidence to identify repeatable improvements "
        "and preserve changes that improve "
        "overall performance without causing avoidable regressions."
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
