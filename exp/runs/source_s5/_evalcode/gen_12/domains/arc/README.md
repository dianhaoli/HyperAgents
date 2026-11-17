# ARC-AGI-2 domain

Each task has a few demonstration pairs (`train`: list of `{"input": grid, "output": grid}`) and one
or more test inputs. A grid is a rectangular list of rows of integers 0-9 (at most 30x30).

## Task agent interface
`task_agent.py` must define `TaskAgent(model=..., chat_history_file=...)` with
`forward(inputs) -> (prediction, msg_history)`, called once per test input with
`inputs = {"domain": "arc", "train": [...], "test_input": grid}`.
`prediction` is a list of up to 2 candidate output grids (a single grid is also accepted).

## Scoring
Exact match of the full output grid. Two answers count per test input: a test input is solved if
either of the first two returned grids equals the true output. A task's score is the share of its
test inputs solved; a set's score (`overall_accuracy`) is the mean over tasks. Scoring happens
outside the agent's environment; true test outputs are never available to agents.

## Budget and environment (enforced outside the agent's code)
* At most 2 model calls per test input (further calls are refused) and 2 answers per test input.
  Model and reasoning effort are fixed by the gateway; call it as in `task_agent.py` / `agent/llm.py`.
* No network. Each test input runs in a fresh process whose working directory `/tmp/task` holds only
  that task's example pairs and the test input (`task.json`).
* Model-written code can be executed with `from arc_sandbox import run_python` (no network, fresh
  temp dir with `task.json`, 30 seconds wall clock per test input in total).
* Visible tasks of the current set (example pairs + test inputs, no test outputs) are in
  `domains/arc/data/tasks.json`. Evaluation results of earlier generations (per-task scores, wrong
  answers, chat logs of unsolved test inputs) are in the generation folders of the evals folder.
