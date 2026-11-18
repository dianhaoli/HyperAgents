import json
import os
import tempfile
import unittest

from meta_agent import summarize_evaluation_history


class EvaluationHistorySummaryTests(unittest.TestCase):
    def write_report(self, root, relative, report):
        path = os.path.join(root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as stream:
            json.dump(report, stream)

    def test_summary_includes_best_recent_and_task_regressions(self):
        with tempfile.TemporaryDirectory() as root:
            self.write_report(root, "gen_1/arc_eval/report.json", {
                "overall_accuracy": 1.0, "total": 2,
                "per_task_score": {"stable": 1.0, "repeat": 0.0, "recover": 0.0},
            })
            self.write_report(root, "gen_2/arc_eval/report.json", {
                "overall_accuracy": 0.5, "total": 2,
                "per_task_score": {"stable": 0.0, "repeat": 0.0, "recover": 1.0},
            })
            summary = summarize_evaluation_history(root, max_reports=1)
            self.assertIn("gen_1 [arc_eval]: 1.000", summary)
            self.assertIn("gen_2 [arc_eval]: 0.500", summary)
            self.assertIn("newly partial/failed: stable", summary)
            self.assertIn("recovered: recover", summary)
            self.assertIn("repeat (2/2 generations)", summary)

    def test_malformed_and_nonfinite_reports_are_ignored(self):
        with tempfile.TemporaryDirectory() as root:
            self.write_report(root, "gen_1/arc_eval/report.json", {
                "overall_accuracy": 0.5, "per_task_score": {"ok": 1.0, "bad": 10 ** 1000},
            })
            self.write_report(root, "gen_2/arc_eval/report.json", {"overall_accuracy": float("inf")})
            path = os.path.join(root, "gen_3", "arc_eval", "report.json")
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding="utf-8") as stream:
                stream.write("not json")
            summary = summarize_evaluation_history(root, max_reports=None)
            self.assertIn("gen_1 [arc_eval]: 0.500", summary)
            self.assertNotIn("gen_2", summary)
            self.assertNotIn("bad", summary)

    def test_missing_history_is_safe(self):
        self.assertIn("unavailable", summarize_evaluation_history("/no/such/eval/path"))


if __name__ == "__main__":
    unittest.main()
