# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
import re

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent

def summarize_evaluation_history(eval_path, max_reports=12):
    """Summarize prior generation scores and regression signals for the prompt."""
    if not eval_path or not os.path.isdir(eval_path):
        return "No evaluation reports were found (evaluation directory is unavailable)."

    reports = []
    for root, dirs, files in os.walk(eval_path):
        dirs.sort()
        if "report.json" not in files:
            continue
        parts = os.path.relpath(root, eval_path).split(os.sep)
        generation = generation_label = generation_index = None
        for index, part in enumerate(parts):
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
            if not isinstance(data, dict):
                continue
            score = float(data.get("overall_accuracy", data.get("accuracy")))
        except (OSError, ValueError, TypeError):
            continue
        if not math.isfinite(score):
            continue
        task_scores = data.get("per_task_score", {})
        failed = sorted(str(task) for task, value in task_scores.items()
                        if isinstance(value, (int, float)) and value < 1) if isinstance(task_scores, dict) else []
        kind_parts = parts[generation_index + 1:]
        kind = "/".join(kind_parts) if kind_parts else "report"
        reports.append((generation, generation_label, kind, score, data.get("total"), failed))

    if not reports:
        return "No usable evaluation reports were found in the supplied history."
    reports.sort(key=lambda row: (row[0], row[2]))
    lines = ["Prior evaluation results (accuracy; partial task scores are regression evidence):"]
    for _, label, kind, score, total, failed in reports[-max(1, max_reports):]:
        count = f", {total} tasks" if isinstance(total, int) else ""
        failures = "; partial/failed IDs: " + ", ".join(failed[:12]) if failed else "; no partial/failed tasks reported"
        lines.append(f"- gen_{label} [{kind}]: {score:.3f}{count}{failures}")

    by_kind = {}
    for report in reports:
        by_kind.setdefault(report[2], []).append(report)
    for kind, entries in sorted(by_kind.items()):
        best = max(entries, key=lambda row: row[3])
        latest = entries[-1]
        if len(entries) > 1 and latest[3] < best[3]:
            lines.append(f"- Regression signal for {kind}: latest gen_{latest[1]} is {latest[3]:.3f}; best was gen_{best[1]} at {best[3]:.3f}.")
    lines.append("Inspect prior patches and predictions before drawing conclusions; preserve reliable gains and check proposed changes against earlier failures.")
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
            "Inspect prior patches and predictions as well as reports; do not assume a single score change proves a technique is generally better. "
            "Use this summary to guide your investigation:\n\n"
            f"{evaluation_summary}\n\n"
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
