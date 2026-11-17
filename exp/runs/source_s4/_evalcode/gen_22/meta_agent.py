# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _evaluation_snapshot(eval_path, limit=12):
    """Summarize comparable completed evaluations for the meta-agent prompt."""
    if not os.path.isdir(eval_path):
        return f"No readable evaluation directory found at {eval_path!r}."

    records = []
    for generation in os.listdir(eval_path):
        if not generation.startswith("gen_"):
            continue
        generation_dir = os.path.join(eval_path, generation)
        if not os.path.isdir(generation_dir):
            continue
        try:
            with open(os.path.join(generation_dir, "metadata.json"), encoding="utf-8") as f:
                metadata = json.load(f)
        except (OSError, ValueError):
            metadata = {}

        # Incomplete or explicitly skipped runs must not be mistaken for failures.
        if metadata.get("run_eval") is False or metadata.get("run_full_eval") is False:
            continue

        for root, dirs, files in os.walk(generation_dir):
            dirs[:] = [d for d in dirs if d not in {"hyperagents", "__pycache__"}]
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
                and math.isfinite(value)
                and ("accuracy" in key.lower() or "score" in key.lower())
            }
            if not metrics:
                continue

            failed = report.get("question_ids_failed", report.get("task_ids_failed", []))
            if not isinstance(failed, list):
                failed = []
            diagnostics = {}
            predictions_path = os.path.join(root, "predictions.json")
            try:
                with open(predictions_path, encoding="utf-8") as f:
                    predictions = json.load(f)
                if isinstance(predictions, list):
                    failed_set = {str(item) for item in failed}
                    for prediction in predictions:
                        if not isinstance(prediction, dict) or str(prediction.get("task_id")) not in failed_set:
                            continue
                        task_id = str(prediction.get("task_id"))
                        details = []
                        if prediction.get("agent_error"):
                            details.append("agent error")
                        if prediction.get("n_answers_returned", 0) == 0:
                            details.append("no parsed answer")
                        if details:
                            diagnostics[task_id] = ", ".join(details)
            except (OSError, ValueError, TypeError):
                pass

            records.append({
                "generation": generation,
                "parent": metadata.get("parent_genid", "unknown"),
                "report": os.path.relpath(root, generation_dir),
                "directory": generation_dir,
                "metrics": metrics,
                "failed": failed,
                "diagnostics": diagnostics,
            })

    if not records:
        return "No completed evaluation reports with numeric accuracy/score metrics were found."

    # Show recent completed runs as well as the best observed result for each report/metric.
    chosen = set(sorted(range(len(records)), key=lambda i: records[i]["generation"], reverse=True)[:6])
    best = {}
    for i, record in enumerate(records):
        for metric, value in record["metrics"].items():
            key = (record["report"], metric)
            if key not in best or value > records[best[key]]["metrics"][metric]:
                best[key] = i
    chosen.update(best.values())
    ordered = sorted(chosen, key=lambda i: records[i]["generation"])[-limit:]

    lines = ["Completed evaluation snapshot (scores are comparable only within the same report/split):"]
    for i in ordered:
        record = records[i]
        scores = ", ".join(f"{key}={value:.4g}" for key, value in record["metrics"].items())
        failed = ", ".join(map(str, record["failed"][:10])) or "none reported"
        lines.append(
            f"- {record['generation']} (parent {record['parent']}), {record['report']}: "
            f"{scores}; failed IDs: {failed}. Inspect {record['directory']}/agent_output/model_patch.diff "
            "and its arc_eval/agent_evals logs for evidence."
        )
        if record["diagnostics"]:
            lines.append("  Failure diagnostics: " + "; ".join(
                f"{task_id}: {detail}" for task_id, detail in list(record["diagnostics"].items())[:5]
            ))

    for (report, metric), i in sorted(best.items()):
        record = records[i]
        lines.append(f"- Best observed {report}/{metric}: {record['generation']} ({record['metrics'][metric]:.4g}).")
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
            f"\n\nThe repository's README.md describes the goal. Prior generations and evaluation results are at `{eval_path}`. "
            "Work autonomously; do not ask questions. Use the evaluation snapshot below to identify promising "
            "changes, then inspect the corresponding generation's source patch and failed-case logs before editing. "
            "Treat missing or incomplete evaluations as unknown, not as zero; compare scores only for the same "
            "evaluation split. Make one focused, generalizable source change motivated by evidence, not a "
            "task-specific hard-coded answer. Preserve the task interface and enforced model-call budget. "
            "Avoid editing `domains/` or generated caches/artifacts, and run a syntax or relevant behavior check. "
            "Use tools to inspect, edit, and validate; only finish when the change is complete.\n\n"
            + _evaluation_snapshot(eval_path)
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
