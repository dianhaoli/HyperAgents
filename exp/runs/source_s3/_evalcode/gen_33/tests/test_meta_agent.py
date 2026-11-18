import json
import tempfile
import unittest
from pathlib import Path

from meta_agent import _evaluation_summary


class EvaluationSummaryTests(unittest.TestCase):
    def _generation(self, root, name, score, task_scores, metadata=None):
        gen = Path(root) / name
        report_dir = gen / "arc_eval"
        report_dir.mkdir(parents=True)
        (report_dir / "report.json").write_text(json.dumps({
            "overall_accuracy": score,
            "total": len(task_scores),
            "per_task_score": task_scores,
        }))
        if metadata is not None:
            (gen / "metadata.json").write_text(json.dumps(metadata))

    def test_ranks_candidates_and_surfaces_recurrent_misses(self):
        with tempfile.TemporaryDirectory() as root:
            cohort = {"task_a": 1.0, "task_b": 0.0}
            self._generation(root, "gen_initial", 0.5, cohort)
            self._generation(root, "gen_1", 1.0, {"task_a": 1.0, "task_b": 1.0})
            self._generation(root, "gen_2", 0.5, cohort)

            summary = _evaluation_summary(root)

        self.assertIn("gen_1=1.0000", summary)
        self.assertIn("gen_2=0.5000", summary)
        self.assertIn("gen_initial=0.5000", summary)
        self.assertIn("task_b 2/3", summary)

    def test_does_not_compare_different_task_cohorts_and_excludes_invalid(self):
        with tempfile.TemporaryDirectory() as root:
            self._generation(root, "gen_1", 1.0, {"task_a": 1.0})
            self._generation(root, "gen_2", 0.0, {"task_b": 0.0}, {"valid_parent": False})
            skipped = Path(root) / "gen_3"
            skipped.mkdir()
            (skipped / "metadata.json").write_text(json.dumps({"run_eval": False}))

            summary = _evaluation_summary(root)

        self.assertEqual(summary.count("arc, 1 exact task IDs"), 1)
        self.assertIn("gen_1=1.0000", summary)
        self.assertNotIn("gen_2=", summary)
        self.assertIn("gen_3: evaluation skipped", summary)

    def test_missing_directory_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            summary = _evaluation_summary(str(Path(root) / "missing"))
        self.assertIn("No prior evaluation directory", summary)


if __name__ == "__main__":
    unittest.main()
