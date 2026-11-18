# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
import re

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def summarize_evaluation_history(eval_path, max_reports=12):
    """Summarize prior scores and task-level regressions for the improvement prompt."""
    if not eval_path or not os.path.isdir(eval_path):
        return "No evaluation reports were found (evaluation directory is unavailable)."

    reports = []
    task_statuses = {}
    task_failures = {}
    task_observations = {}
    generation_pattern = re.compile(r"gen_(initial|\d+)(?:\..*)?")

    for root, dirs, files in os.walk(eval_path):
        dirs.sort()
        if "report.json" not in files:
            continue
        relative_parts = os.path.relpath(root, eval_path).split(os.sep)
        generation = label = generation_part_index = None
        for index, part in enumerate(relative_parts):
            match = generation_pattern.fullmatch(part)
            if match:
                label = match.group(1)
                generation = -1 if label == "initial" else int(label)
                generation_part_index = index
                break
        if generation is None:
            continue

        try:
            with open(os.path.join(root, "report.json"), encoding="utf-8") as stream:
                data = json.load(stream)
            if not isinstance(data, dict):
                continue
            raw_score = data.get("overall_accuracy", data.get("accuracy"))
            if isinstance(raw_score, bool):
                continue
            score = float(raw_score)
            if not math.isfinite(score):
                continue
        except (OSError, ValueError, TypeError, OverflowError):
            continue

        kind_parts = relative_parts[generation_part_index + 1:]
        kind = "/".join(kind_parts) if kind_parts else "report"
        outcomes = {}
        task_scores = data.get("per_task_score", {})
        if isinstance(task_scores, dict):
            for task_id, value in task_scores.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                try:
                    if not math.isfinite(value):
                        continue
                except (TypeError, ValueError, OverflowError):
                    continue
                task_id = str(task_id)
                passed = value >= 1
                outcomes[task_id] = passed
                key = (kind, task_id)
                task_observations.setdefault(key, set()).add(generation)
                if not passed:
                    task_failures.setdefault(key, set()).add(generation)

        task_statuses[(kind, generation)] = outcomes
        failures = sorted(task for task, passed in outcomes.items() if not passed)
        total = data.get("total")
        reports.append((generation, label, kind, score, total, failures))

    if not reports:
        return "No usable evaluation reports were found in the supplied history."

    reports.sort(key=lambda row: (row[0], row[2], row[1]))
    if max_reports is None:
        report_limit = len(reports)
    else:
        try:
            report_limit = max(1, int(max_reports))
        except (TypeError, ValueError, OverflowError):
            report_limit = 12

    # Show the recent trend and retain the strongest checkpoint for each eval type.
    selected = reports[-report_limit:]
    selected_keys = {(row[0], row[2], row[1]) for row in selected}
    best_by_kind = {}
    for row in reports:
        previous = best_by_kind.get(row[2])
        if previous is None or (row[3], row[0]) > (previous[3], previous[0]):
            best_by_kind[row[2]] = row
    for row in best_by_kind.values():
        key = (row[0], row[2], row[1])
        if key not in selected_keys:
            selected.append(row)
    selected.sort(key=lambda row: (row[0], row[2], row[1]))

    lines = ["Prior evaluation results (accuracy; lower-scoring generations are useful regression evidence):"]
    for _, label, kind, score, total, failures in selected:
        count = f", {total} tasks" if isinstance(total, int) and not isinstance(total, bool) else ""
        failure_text = "; partial/failed task IDs: " + ", ".join(failures[:12]) if failures else "; no partial/failed tasks reported"
        lines.append(f"- gen_{label} [{kind}]: {score:.3f}{count}{failure_text}")

    by_kind = {}
    for report in reports:
        by_kind.setdefault(report[2], []).append(report)
    for kind, entries in sorted(by_kind.items()):
        best = max(entries, key=lambda row: (row[3], row[0]))
        latest = entries[-1]
        if latest[3] < best[3]:
            lines.append(f"- Regression signal for {kind}: latest gen_{latest[1]} is {latest[3]:.3f}; best was gen_{best[1]} at {best[3]:.3f}.")

        generations = sorted({entry[0] for entry in entries})
        if len(generations) >= 2:
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
                lines.append(f"- Task-level changes from gen_{previous_generation} to gen_{latest_generation} [{kind}]: " + "; ".join(changes))

    recurring = [
        (kind, task, len(failed), len(task_observations[(kind, task)]))
        for (kind, task), failed in task_failures.items() if len(failed) >= 2
    ]
    if recurring:
        recurring.sort(key=lambda item: (item[0], -item[2], item[1]))
        details = ", ".join(f"{task} ({failed}/{observed} generations)" for _, task, failed, observed in recurring[:12])
        lines.append(f"- Recurring partial/failed tasks across runs: {details}")

    lines.append(
        "Inspect cited generations' agent_output/model_patch.diff and arc_eval/predictions.json. "
        "For recurring task IDs, inspect their predictions and available agent chat histories. "
        "Preserve reliable gains and validate changes against both regressions and recovered tasks."
    )
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Inspect the project and its evaluation history, then improve its mechanisms."""
        instruction = f"Modify any part of the codebase at `{repo_path}`."
        # [experiment adaptation, see DECISIONS.md] gpt-6-luna otherwise asks for clarification and never edits.
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Use the evaluation summary below to guide investigation, but inspect actual source, patches, "
            "and predictions before concluding that a change helped. Avoid undoing reliable improvements.\n\n"
            f"{summarize_evaluation_history(eval_path)}\n\n"
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )
        return chat_with_agent(
            instruction, model=self.model, msg_history=[], logging=self.log, tools_available="all"
        )
