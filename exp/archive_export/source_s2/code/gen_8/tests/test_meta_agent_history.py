import json
import os
import tempfile
import unittest

from meta_agent import summarize_evaluation_history


class EvaluationHistorySummaryTests(unittest.TestCase):
    def test_reports_regression_recurring_failures_and_evidence_paths(self):
        with tempfile.TemporaryDirectory() as root:
            reports = {
                "gen_initial/arc_eval/report.json": {
                    "overall_accuracy": 0.5, "total": 2,
                    "per_task_score": {"repeat": 0.0, "one-off": 1.0},
                },
                "gen_1/arc_eval/report.json": {
                    "overall_accuracy": 0.8, "total": 2,
                    "per_task_score": {"repeat": 1.0, "one-off": 0.0},
                },
                "gen_2/arc_eval/report.json": {
                    "overall_accuracy": 0.2, "total": 2,
                    "per_task_score": {"repeat": 0.5, "one-off": 1.0},
                },
            }
            for relative, report in reports.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(report, stream)

            summary = summarize_evaluation_history(root)
            self.assertIn("Regression signal for arc_eval", summary)
            self.assertIn("gen_1 best 0.800", summary)
            self.assertIn("repeat (2/3 generations)", summary)
            self.assertIn("agent_output/model_patch.diff", summary)
            self.assertIn("arc_eval/predictions.json", summary)
            self.assertIn("chat_history_<task>_0.md", summary)

    def test_ignores_nonfinite_scores_and_handles_limits(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "gen_1", "arc_eval", "report.json")
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding="utf-8") as stream:
                json.dump({"overall_accuracy": float("nan")}, stream)
            self.assertIn("No usable", summarize_evaluation_history(root))
            self.assertIn("unavailable", summarize_evaluation_history("/path/that/does/not/exist"))


if __name__ == "__main__":
    unittest.main()
