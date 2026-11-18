# Copyright (c) Meta Platforms, Inc. and affiliates.

import json
import math
import os
from collections import Counter, defaultdict

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent


def _evaluation_summary(eval_path, max_candidates=3):
    """Summarize comparable prior evaluations to ground the next improvement.

    Reports are grouped by domain and exact task-ID cohort whenever task-level
    scores are available. Incomplete, explicitly skipped, or invalid generations
    are not treated as scored candidates.
    """
    completed = defaultdict(list)
    incomplete = []
    if not os.path.isdir(eval_path):
        return f"No prior evaluation directory found at {eval_path!r}; inspect available evidence before making performance claims."

    for dirname in sorted(os.listdir(eval_path)):
        if dirname != "gen_initial" and not (dirname.startswith("gen_") and dirname[4:].isdigit()):
            continue
        gen_dir = os.path.join(eval_path, dirname)
        if not os.path.isdir(gen_dir):
            continue
        metadata = {}
        metadata_path = os.path.join(gen_dir, "metadata.json")
        try:
            with open(metadata_path) as f:
                metadata = json.load(f)
            if not isinstance(metadata, dict):
                metadata = {}
        except (OSError, ValueError):
            pass

        report_paths = []
        for child in sorted(os.listdir(gen_dir)):
            report_path = os.path.join(gen_dir, child, "report.json")
            if child.endswith("_eval") and os.path.isfile(report_path):
                report_paths.append(report_path)
        if not report_paths:
            if metadata.get("run_eval") is False:
                incomplete.append(f"{dirname}: evaluation skipped")
            elif metadata.get("valid_parent") is False:
                incomplete.append(f"{dirname}: invalid generation")
            continue

        for report_path in report_paths:
            domain = os.path.basename(os.path.dirname(report_path))[:-5]
            label = f"{dirname}/{domain}"
            if metadata.get("valid_parent") is False:
                incomplete.append(f"{label}: invalid generation (report excluded)")
                continue
            if metadata.get("run_eval") is False:
                incomplete.append(f"{label}: evaluation marked skipped (report excluded)")
                continue
            try:
                with open(report_path) as f:
                    report = json.load(f)
            except (OSError, ValueError):
                incomplete.append(f"{label}: unreadable report")
                continue
            if not isinstance(report, dict):
                incomplete.append(f"{label}: malformed report")
                continue

            scores = {}
            raw_scores = report.get("per_task_score")
            if isinstance(raw_scores, dict):
                for task_id, value in raw_scores.items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        value = float(value)
                        if math.isfinite(value) and 0 <= value <= 1:
                            scores[str(task_id)] = value
            score = report.get("overall_accuracy")
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                score = sum(scores.values()) / len(scores) if scores else None
            if score is None or not math.isfinite(float(score)) or not 0 <= float(score) <= 1:
                incomplete.append(f"{label}: missing or invalid accuracy")
                continue
            score = float(score)

            if scores:
                cohort = ("task_ids", tuple(sorted(scores)))
                cohort_label = f"{len(scores)} exact task IDs"
            else:
                sample_count = report.get("total_test_inputs", report.get("total"))
                if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 0:
                    sample_count = None
                cohort = ("count", sample_count)
                cohort_label = "unknown-size cohort" if sample_count is None else f"{sample_count} tasks (IDs unavailable)"
            completed[(domain, cohort)].append({
                "generation": "initial" if dirname == "gen_initial" else dirname[4:],
                "score": score,
                "parent": metadata.get("parent_genid"),
                "task_scores": scores,
                "cohort_label": cohort_label,
            })

    lines = [
        "Prior evaluation evidence (compare scores only within the same domain and exact task cohort when available; matching counts without IDs are weaker evidence):"
    ]
    if not completed:
        lines.append("- No completed, valid reports found. Inspect available reports and metadata before making performance claims.")
    for (domain, cohort), records in sorted(completed.items(), key=lambda item: (item[0][0], repr(item[0][1]))):
        records.sort(key=lambda r: (-r["score"], str(r["generation"])))
        lines.append(f"- {domain}, {records[0]['cohort_label']}: top candidates and baseline:")
        selected = records[:max_candidates]
        baseline = next((r for r in records if r["generation"] == "initial"), None)
        if baseline is not None and baseline not in selected:
            selected.append(baseline)
        for record in selected:
            parent = "" if record["parent"] is None else f", parent {record['parent']}"
            failures = [task for task, value in record["task_scores"].items() if value < 1.0]
            fail_text = f"; failing task IDs: {', '.join(sorted(failures)[:10])}" if failures else ""
            lines.append(f"  gen_{record['generation']}={record['score']:.4f}{parent}{fail_text}")

        # Repeated failures across runs identify useful places to investigate, not
        # proven causes; keep the denominator explicit and only combine exact cohorts.
        task_records = [record for record in records if record["task_scores"]]
        if task_records:
            failed = Counter()
            for record in task_records:
                failed.update(task for task, value in record["task_scores"].items() if value < 1.0)
            recurrent = [(task, count) for task, count in failed.most_common(6) if count > 1]
            if recurrent:
                lines.append("  Recurrent failures (failed runs / reports with task scores): " + ", ".join(
                    f"{task} {count}/{len(task_records)}" for task, count in recurrent
                ))
    if incomplete:
        examples = "; ".join(incomplete[:8])
        suffix = " ..." if len(incomplete) > 8 else ""
        lines.append(f"- Excluded/incomplete runs: {len(incomplete)} ({examples}{suffix}).")
    return "\n".join(lines)


class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """Recursively improve the agent using repository and evaluation evidence."""
        instruction = (
            f"Modify any part of the codebase at `{repo_path}`.\n\n"
            f"The repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification.\n\n"
            "Use the evaluation summary below as a starting point, then inspect the relevant reports, metadata, and patches yourself. "
            "Choose changes based on comparable evaluation evidence, not generation number or recency. Recurrent failing task IDs are hypotheses to investigate, not proof of a shared cause. "
            "Favor focused changes, preserve behavior supported by the strongest comparable result, and distinguish completed evaluations from skipped, partial, invalid, or incomparable runs. "
            "Do not claim a change improved performance without a comparable evaluation.\n\n"
            f"{_evaluation_summary(eval_path)}\n\n"
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )
        return chat_with_agent(
            instruction,
            model=self.model,
            msg_history=[],
            logging=self.log,
            tools_available="all",
        )
