import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from task_agent import TaskAgent


class TaskAgentSecondPassTests(unittest.TestCase):
    def test_second_call_reviews_first_candidate_and_keeps_both_answers(self):
        inputs = {
            "domain": "arc",
            "train": [{"input": [[0]], "output": [[1]]}],
            "test_input": [[0]],
        }
        responses = [
            "<answer>[[1]]</answer>",
            "<answer>[[2]]</answer>",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            agent = TaskAgent(chat_history_file=str(Path(tmp) / "history.md"))
            with patch("task_agent.call_model", side_effect=responses) as call:
                answers, _ = agent.forward(inputs)

        self.assertEqual(answers, [[[1]], [[2]]])
        self.assertEqual(call.call_count, 2)
        second_prompt = call.call_args_list[1].args[0]
        self.assertIn('First-attempt candidate (JSON grid):\n[[1]]', second_prompt)
        self.assertIn("Do not simply copy it", second_prompt)
        self.assertIn("Input (1x1):", second_prompt)

    def test_second_call_can_solve_when_first_answer_is_invalid(self):
        inputs = {
            "domain": "arc",
            "train": [{"input": [[0]], "output": [[1]]}],
            "test_input": [[0]],
        }
        with tempfile.TemporaryDirectory() as tmp:
            agent = TaskAgent(chat_history_file=str(Path(tmp) / "history.md"))
            with patch("task_agent.call_model", side_effect=["no grid", "<answer>[[1]]</answer>"]) as call:
                answers, _ = agent.forward(inputs)

        self.assertEqual(answers, [[[1]]])
        self.assertEqual(call.call_count, 2)
        self.assertIn("first attempt did not produce a valid grid", call.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
