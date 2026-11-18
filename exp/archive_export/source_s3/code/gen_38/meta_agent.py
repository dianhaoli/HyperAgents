# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import re
from collections import Counter
from pathlib import Path

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _evaluation_history(eval_path, limit=10):
    """Build a small, deterministic summary of prior scored generations."""
    root = Path(eval_path)
    if not root.is_dir():
        return ""

    reports = []
    for report_path in root.rglob("report.json"):
        try:
            with report_path.open(encoding="utf-8") as report_file:
                report = json.load(report_file)
        except (OSError, json.JSONDecodeError):
            continue
        accuracy = report.get("overall_accuracy") if isinstance(report, dict) else None
        if not isinstance(accuracy, (int, float)):
            continue
        match = re.search(r"gen_(\d+)", str(report_path))
        generation = int(match.group(1)) if match else -1
        failed = report.get("question_ids_failed", [])
        if not isinstance(failed, list):
            failed = []
        reports.append((generation, str(report_path), float(accuracy), failed))

    reports.sort(key=lambda row: (row[0], row[1]))
    if not reports:
        return ""

    recent = reports[-limit:]
    failures = Counter(
        question_id
        for _, _, _, question_ids in recent
        for question_id in question_ids
        if isinstance(question_id, (str, int))
    )
    recurring = [question_id for question_id, count in failures.most_common() if count > 1]
    best = max(reports, key=lambda row: row[2])
    lines = ["Prior evaluation summary (reports found under the supplied evaluation path):"]
    lines.append(f"Best observed: gen_{best[0]} accuracy={best[2]:.3f}.")
    lines.append("Most recent scored reports:")
    for generation, path, accuracy, failed in recent:
        label = f"gen_{generation}" if generation >= 0 else Path(path).parent.name
        lines.append(f"- {label}: accuracy={accuracy:.3f}; failed IDs={failed[:12]}.")
    if recurring:
        lines.append(f"IDs failing in multiple recent reports: {recurring[:20]}.")
    lines.append(
        "Use these results as evidence, not as a guarantee: inspect the associated patches and "
        "evaluation details, distinguish recurring weaknesses from one-off stochastic failures, "
        "and avoid degrading strong behavior while addressing a measured gap."
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
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )
        history = _evaluation_history(eval_path)
        if history:
            instruction += "\n\n" + history

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
