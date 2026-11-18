# Copyright (c) Meta Platforms, Inc. and affiliates.

from agent.base_agent import AgentSystem
from agent.llm_withtools import chat_with_agent

class MetaAgent(AgentSystem):
    def forward(self, repo_path, eval_path, iterations_left=None):
        """
        A meta agent that recursively self-improves.

        Args:
            repo_path (str): The path to the repository.
            eval_path (str): The path to previously generated agents and their evaluation results.
            iterations_left (int, optional): The number of remaining iterations in which the meta agent will be invoked in future. Defaults to None.
        """
        instruction = f"Improve the agent-generation system in `{repo_path}`."
        instruction += (
            f"\n\nRead `{repo_path}/README.md` and inspect previous generations and evaluation results under `{eval_path}` before deciding what to change. "
            "Compare the available evaluation reports across generations, including scores and task-level failures, and inspect the corresponding patches or logs when available. "
            "Distinguish measured results from hypotheses: small evaluations can be noisy, and a score change alone does not prove why performance changed. "
            "Use the evidence to identify one specific weakness and prefer a focused, reversible change. Avoid repeating a change associated with a regression unless you have a materially different, evidence-based approach. "
            "Do not modify prior evaluation artifacts. Run relevant tests or lightweight validation after editing, and report what was and was not verified. "
            "Work autonomously; nobody will answer questions, so do not ask for clarification. Use the tools to inspect and edit the repository, and only finish after making the change."
        )
        if iterations_left is not None:
            instruction += f"\nThere are {iterations_left} future self-improvement iterations available; favor changes that can be evaluated in a later iteration."

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
