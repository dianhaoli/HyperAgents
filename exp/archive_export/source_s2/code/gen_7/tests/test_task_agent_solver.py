import unittest
from task_agent import _infer_geometric_solution


class GeometricSolverTests(unittest.TestCase):
    def test_rotation_and_color_mapping(self):
        inputs = {
            "train": [{"input": [[1, 2, 1], [2, 2, 1]],
                       "output": [[3, 2], [3, 3], [2, 2]]}],
            "test_input": [[1, 1], [2, 1]],
        }
        self.assertEqual(_infer_geometric_solution(inputs), [[3, 2], [2, 2]])

    def test_ambiguous_or_unseen_colors_fall_back(self):
        self.assertIsNone(_infer_geometric_solution({
            "train": [{"input": [[1, 2]], "output": [[1, 2]]}],
            "test_input": [[3, 4], [5, 6]],
        }))
        self.assertIsNone(_infer_geometric_solution({
            "train": [{"input": [[1, 0]], "output": [[1, 0]]}],
            "test_input": [[2, 0]],
        }))

    def test_non_geometric_rule_falls_back(self):
        self.assertIsNone(_infer_geometric_solution({
            "train": [{"input": [[1, 0], [0, 0]], "output": [[1, 1], [0, 0]]}],
            "test_input": [[2, 0], [0, 0]],
        }))


if __name__ == "__main__":
    unittest.main()
