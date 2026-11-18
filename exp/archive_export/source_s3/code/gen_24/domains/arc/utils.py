# ARC-AGI-2 domain (modelled on the IMO grading domain).
QUESTION_ID = "task_id"
GROUND_TRUTH_KEY = None  # test outputs are never available inside the agent's environment
MODEL = "gpt-6-luna"


def format_input_dict(task, test_idx):
    """Input to the task agent: the task's example pairs plus ONE test input."""
    return {
        "domain": "arc",
        "train": task["train"],
        "test_input": task["test"][test_idx]["input"],
    }
