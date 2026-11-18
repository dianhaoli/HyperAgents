# Copyright (c) Meta Platforms, Inc. and affiliates.

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent
import json
import os


def _evaluation_summary(eval_path, limit=12):
    """Summarize completed generation reports so edits are based on evidence."""
    if not os.path.isdir(eval_path):
        return "No readable prior-evaluation directory was found."

    records = []
    for generation in sorted(os.listdir(eval_path)):
        generation_dir = os.path.join(eval_path, generation)
        if not generation.startswith("gen_") or not os.path.isdir(generation_dir):
            continue
        metadata = {}
        try:
            with open(os.path.join(generation_dir, "metadata.json"), encoding="utf-8") as f:
                metadata = json.load(f)
        except (OSError, ValueError):
            pass
        # A staged/incomplete evaluation is not comparable to a completed run.
        if metadata.get("run_full_eval") is False:
            continue
        for root, _, files in os.walk(generation_dir):
            if "report.json" not in files:
                continue
            report_path = os.path.join(root, "report.json")
            try:
                with open(report_path, encoding="utf-8") as f:
                    report = json.load(f)
            except (OSError, ValueError):
                continue
            metrics = {
                key: value for key, value in report.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
                and ("accuracy" in key.lower() or "score" in key.lower())
            }
            if not metrics:
                continue
            failed = report.get("question_ids_failed", report.get("task_ids_failed", []))
            records.append({
                "generation": generation,
                "parent": metadata.get("parent_genid", "unknown"),
                "report": os.path.relpath(root, generation_dir),
                "metrics": metrics,
                "failed": failed if isinstance(failed, list) else [],
            })

    if not records:
        return "No completed evaluation reports with accuracy/score metrics were found."

    lines = ["Completed prior evaluation reports (scores are not guaranteed comparable across report types):"]
    for record in records[-limit:]:
        scores = ", ".join(f"{key}={value:.4g}" for key, value in record["metrics"].items())
        failed = record["failed"]
        failed_text = f"; failed IDs: {', '.join(map(str, failed[:12]))}" if failed else ""
        lines.append(
            f"- {record['generation']} (parent {record['parent']}), {record['report']}: "
            f"{scores}{failed_text}"
        )

    # Show the observed leader only among reports with the same report path and metric.
    groups = {}
    for record in records:
        for metric, value in record["metrics"].items():
            groups.setdefault((record["report"], metric), []).append((value, record))
    leaders = []
    for (report, metric), candidates in groups.items():
        value, record = max(candidates, key=lambda item: item[0])
        leaders.append((report, metric, value, record["generation"]))
    for report, metric, value, generation in sorted(leaders):
        lines.append(f"- Best observed for {report} / {metric}: {generation} at {value:.4g}.")
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
        instruction += (
            "\n\nUse the evaluation snapshot below as evidence, not as a substitute for inspection. "
            "Review the strongest completed, comparable generation's source patch and its failed-task "
            "examples/logs, and compare against the baseline or parent. Missing or incomplete evaluations "
            "are unknown, not zero. Make one focused, generalizable source change motivated by that evidence; "
            "do not hard-code answers to evaluation tasks. Preserve the task interface and model-call budget, "
            "avoid edits to `domains/` and generated files/caches, and run a relevant syntax or behavior check.\n\n"
            + _evaluation_summary(eval_path)
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
