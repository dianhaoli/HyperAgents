import json
import os
import tempfile
import unittest
from meta_agent import summarize_evaluation_history


class EvaluationSummaryTests(unittest.TestCase):
    def test_scores_failures_and_regression(self):
        with tempfile.TemporaryDirectory() as root:
            data = {
                "gen_initial/arc_eval/report.json": {"overall_accuracy": 0.5, "total": 2,
                    "per_task_score": {"a": 1.0, "b": 0.0}},
                "gen_1/arc_eval/report.json": {"overall_accuracy": 0.75, "total": 2,
                    "per_task_score": {"a": 1.0, "b": 0.5}},
                "gen_2/arc_eval/report.json": {"overall_accuracy": 0.25, "total": 2,
                    "per_task_score": {"a": 0.0, "b": 0.5}},
            }
            for relative, report in data.items():
                path = os.path.join(root, relative)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(report, stream)
            summary = summarize_evaluation_history(root)
            self.assertIn("gen_initial [arc_eval]: 0.500", summary)
            self.assertIn("partial/failed IDs: b", summary)
            self.assertIn("Regression signal for arc_eval", summary)

    def test_unavailable_history(self):
        self.assertIn("unavailable", summarize_evaluation_history("/path/not/available"))


if __name__ == "__main__":
    unittest.main()
