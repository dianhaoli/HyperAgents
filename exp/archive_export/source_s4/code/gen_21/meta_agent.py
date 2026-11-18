# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import os
import re

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _generation_order(name):
    if name == "gen_initial":
        return (0, 0)
    match = re.fullmatch(r"gen_(\d+)", name)
    return (1, int(match.group(1))) if match else (-1, -1)


def _evaluation_summary(eval_path, limit=5):
    """Build a compact, comparable summary of completed prior evaluation reports."""
    if not os.path.isdir(eval_path):
        return f"No readable evaluation directory found at {eval_path!r}."

    records = []
    try:
        generations = sorted(os.listdir(eval_path), key=_generation_order)
    except OSError as exc:
        return f"Could not list evaluation directory {eval_path!r}: {exc}"

    for generation in generations:
        if _generation_order(generation)[0] < 0:
            continue
        generation_dir = os.path.join(eval_path, generation)
        if not os.path.isdir(generation_dir):
            continue
        try:
            with open(os.path.join(generation_dir, "metadata.json"), encoding="utf-8") as stream:
                metadata = json.load(stream)
        except (OSError, ValueError):
            metadata = {}

        # Missing metadata is common for older runs; an explicitly skipped or
        # staged-only evaluation, however, should never be treated as a result.
        if metadata.get("run_eval") is False or metadata.get("run_full_eval") is False:
            continue

        for root, dirs, files in os.walk(generation_dir):
            dirs[:] = [name for name in dirs if name not in {"__pycache__", ".git", "agent_evals"}]
            if "report.json" not in files:
                continue
            try:
                with open(os.path.join(root, "report.json"), encoding="utf-8") as stream:
                    report = json.load(stream)
            except (OSError, ValueError):
                continue
            if not isinstance(report, dict):
                continue

            metric = next((key for key in ("overall_accuracy", "accuracy", "score")
                           if isinstance(report.get(key), (int, float))
                           and not isinstance(report.get(key), bool)), None)
            if metric is None:
                continue
            failed = report.get("question_ids_failed", report.get("task_ids_failed", []))
            if not isinstance(failed, list):
                failed = []
            records.append({
                "generation": generation,
                "parent": metadata.get("parent_genid", "unknown"),
                "report": os.path.relpath(root, generation_dir),
                "metric": metric,
                "score": float(report[metric]),
                "failed": [str(item) for item in failed],
            })

    if not records:
        return "No completed evaluation reports with accuracy/score metrics were found."

    groups = {}
    for record in records:
        groups.setdefault((record["report"], record["metric"]), []).append(record)

    lines = [
        "Prior evaluation evidence (compare only reports with the same path and metric; "
        "missing reports are unknown, not failures):"
    ]
    for (report_path, metric), group in sorted(groups.items()):
        group.sort(key=lambda item: _generation_order(item["generation"]))
        leader = max(group, key=lambda item: item["score"])
        latest = group[-1]
        top = sorted(group, key=lambda item: (-item["score"], _generation_order(item["generation"])))[:limit]
        top_text = ", ".join(f"{item['generation']}={item['score']:.3f}" for item in top)
        lines.append(
            f"- {report_path} / {metric}: {len(group)} completed runs; "
            f"best {leader['generation']}={leader['score']:.3f} (parent {leader['parent']}); "
            f"latest {latest['generation']}={latest['score']:.3f}; top: {top_text}."
        )
        failures = {}
        for item in group:
            for task_id in set(item["failed"]):
                failures[task_id] = failures.get(task_id, 0) + 1
        recurring = sorted(failures.items(), key=lambda item: (-item[1], item[0]))[:8]
        if recurring:
            lines.append("  Frequently failed task IDs (count of reports): " + ", ".join(
                f"{task_id} ({count})" for task_id, count in recurring
            ) + ".")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Improve the agent-generation system using source and evaluation evidence."""
        instruction = f"Improve the agent-generation system in the codebase at `{repo_path}`."
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and "
            f"their evaluation results are at `{eval_path}`.\n\n"
            f"{_evaluation_summary(eval_path)}\n\n"
            "Inspect the relevant source code and use these results to identify a concrete, "
            "general weakness in agent generation or improvement. Review representative failure "
            "logs when available. Prioritize changes that plausibly improve performance across "
            "tasks; do not hardcode task IDs, answers, or evaluation outputs. Preserve interfaces, "
            "avoid editing `domains/` (the runner reverts those changes), and do not include "
            "generated caches or artifacts. Make a focused source change and run relevant checks "
            "when practical. Work autonomously: nobody will answer questions, so do not ask for "
            "clarification. Use the tools to inspect, edit, and validate; only finish when the "
            "work is done."
        )
        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
