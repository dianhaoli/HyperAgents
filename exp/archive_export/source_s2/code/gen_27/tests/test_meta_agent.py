import json
import os
import tempfile
import unittest

from meta_agent import summarize_evaluation_history


class EvaluationHistorySummaryTests(unittest.TestCase):
    def test_summarizes_scores_failures_and_regressions(self):
        with tempfile.TemporaryDirectory() as root:
            reports = {
                "gen_initial/arc_eval/report.json": {
                    "overall_accuracy": 0.5,
                    "total": 2,
                    "per_task_score": {"task-a": 1.0, "task-b": 0.0},
                },
                "gen_1/arc_eval/report.json": {
                    "overall_accuracy": 0.75,
                    "total": 2,
                    "per_task_score": {"task-a": 1.0, "task-b": 0.5},
                },
                "gen_2/arc_eval/report.json": {
                    "overall_accuracy": 0.25,
                    "total": 2,
                    "per_task_score": {"task-a": 0.0, "task-b": 0.5},
                },
            }
            for relative, data in reports.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(data, stream)

            summary = summarize_evaluation_history(root)
            self.assertIn("gen_initial [arc_eval]: 0.500", summary)
            self.assertIn("partial/failed task IDs: task-b", summary)
            self.assertIn("Regression signal for arc_eval", summary)
            self.assertIn("gen_1 best 0.750", summary)


    def test_report_limit_keeps_best_historical_checkpoint(self):
        with tempfile.TemporaryDirectory() as root:
            reports = {
                "gen_1/arc_eval/report.json": {
                    "overall_accuracy": 1.0,
                    "total": 1,
                    "per_task_score": {"task": 1.0},
                },
                "gen_2/arc_eval/report.json": {
                    "overall_accuracy": 0.4,
                    "total": 1,
                    "per_task_score": {"task": 0.0},
                },
                "gen_3/arc_eval/report.json": {
                    "overall_accuracy": 0.6,
                    "total": 1,
                    "per_task_score": {"task": 0.0},
                },
            }
            for relative, data in reports.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(data, stream)

            summary = summarize_evaluation_history(root, max_reports=1)
            self.assertIn("gen_1 [arc_eval]: 1.000", summary)
            self.assertIn("gen_3 [arc_eval]: 0.600", summary)
            self.assertNotIn("gen_2 [arc_eval]", summary)

    def test_unavailable_or_invalid_history_is_safe(self):
        self.assertIn("unavailable", summarize_evaluation_history("/path/that/does/not/exist"))
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "gen_1", "arc_eval", "report.json")
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding="utf-8") as stream:
                stream.write("not json")
            self.assertIn("No usable", summarize_evaluation_history(root))


class TaskTransitionSummaryTests(unittest.TestCase):
    def test_reports_task_regressions_and_recoveries_between_latest_runs(self):
        with tempfile.TemporaryDirectory() as root:
            reports = {
                "gen_1/arc_eval/report.json": {
                    "overall_accuracy": 1.0,
                    "per_task_score": {"regressed": 1.0, "recovered": 0.0},
                },
                "gen_2/arc_eval/report.json": {
                    "overall_accuracy": 1.0,
                    "per_task_score": {"regressed": 0.0, "recovered": 1.0},
                },
            }
            for relative, data in reports.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(data, stream)

            summary = summarize_evaluation_history(root)
            self.assertIn("Task-level changes from gen_1 to gen_2", summary)
            self.assertIn("newly partial/failed: regressed", summary)
            self.assertIn("recovered: recovered", summary)


class ExtremeReportValuesTests(unittest.TestCase):
    def test_ignores_non_finite_and_unrepresentably_large_values(self):
        with tempfile.TemporaryDirectory() as root:
            reports = {
                "gen_1/arc_eval/report.json": {
                    "overall_accuracy": 0.5,
                    "total": 1,
                    "per_task_score": {"huge": 10 ** 1000, "ok": 0.0},
                },
                "gen_2/arc_eval/report.json": {
                    "overall_accuracy": float("inf"),
                    "total": 1,
                    "per_task_score": {"ok": 1.0},
                },
            }
            for relative, data in reports.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(data, stream)

            summary = summarize_evaluation_history(root)
            self.assertIn("gen_1 [arc_eval]: 0.500", summary)
            self.assertNotIn("huge", summary)
            self.assertNotIn("gen_2 [arc_eval]", summary)


if __name__ == "__main__":
    unittest.main()
