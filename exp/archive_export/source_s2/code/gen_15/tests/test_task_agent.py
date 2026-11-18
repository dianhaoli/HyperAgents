import unittest

from task_agent import _infer_geometric_solution


class GeometricSolverTests(unittest.TestCase):
    def test_rotation_and_color_mapping(self):
        # The training transform is clockwise rotation followed by 1->2, 2->3.
        inputs = {
            "train": [{
                "input": [[1, 2, 1], [2, 2, 1]],
                "output": [[3, 2], [3, 3], [2, 2]],
            }],
            "test_input": [[1, 1], [2, 1]],
        }
        self.assertEqual(_infer_geometric_solution(inputs), [[3, 2], [2, 2]])

    def test_disagreeing_geometric_hypotheses_fall_back(self):
        inputs = {
            "train": [{"input": [[1, 2]], "output": [[1, 2]]}],
            "test_input": [[3, 4], [5, 6]],
        }
        self.assertIsNone(_infer_geometric_solution(inputs))

    def test_unseen_test_colors_fall_back(self):
        inputs = {
            "train": [{"input": [[1, 0]], "output": [[1, 0]]}],
            "test_input": [[2, 0]],
        }
        self.assertIsNone(_infer_geometric_solution(inputs))

    def test_non_geometric_rule_falls_back(self):
        inputs = {
            "train": [{"input": [[1, 0], [0, 0]], "output": [[1, 1], [0, 0]]}],
            "test_input": [[2, 0], [0, 0]],
        }
        self.assertIsNone(_infer_geometric_solution(inputs))


if __name__ == "__main__":
    unittest.main()
