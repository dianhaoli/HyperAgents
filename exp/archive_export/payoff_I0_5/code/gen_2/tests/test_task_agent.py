import tempfile
import unittest
from unittest.mock import patch

import task_agent


class TaskAgentTests(unittest.TestCase):
    def setUp(self):
        self.inputs = {
            "domain": "arc",
            "train": [{"input": [[1, 0]], "output": [[0, 1]]}],
            "test_input": [[2, 0]],
        }

    def test_prompt_represents_training_and_test_grids(self):
        prompt = task_agent.build_prompt(self.inputs)
        self.assertIn("Input (1x2):", prompt)
        self.assertIn("Output (1x2):", prompt)
        self.assertIn("Test", prompt)
        self.assertIn("test output may have different dimensions", prompt)

    def test_second_attempt_receives_first_candidate(self):
        prompts = []
        responses = iter([
            "<answer>[[0, 2]]</answer>",
            "<answer>[[2, 0]]</answer>",
        ])

        def fake_call(prompt):
            prompts.append(prompt)
            return next(responses)

        with tempfile.NamedTemporaryFile() as log:
            agent = task_agent.TaskAgent(chat_history_file=log.name)
            with patch.object(task_agent, "call_model", side_effect=fake_call):
                answers, history = agent.forward(self.inputs)

        self.assertEqual(answers, [[[0, 2]], [[2, 0]]])
        self.assertEqual(history, [])
        self.assertNotIn("Candidate from an earlier attempt", prompts[0])
        self.assertIn('[[0, 2]]', prompts[1])


if __name__ == "__main__":
    unittest.main()
