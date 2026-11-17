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
        instruction = f"Modify any part of the codebase at `{repo_path}`."
        # [experiment adaptation, see DECISIONS.md] gpt-6-luna otherwise asks for clarification and never edits.
        instruction += (
            f"\n\nThe repository's README.md describes the goal. Previously generated agents and their evaluation results are at `{eval_path}`. "
            "Work autonomously: nobody will answer questions, so do not ask for clarification. "
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done.\n\n"
            "Before editing, inspect the available evaluation reports, generation metadata, candidate patches, and relevant failure logs. "
            "Compare candidates only when their evaluation settings and sample sizes are comparable; distinguish completed evaluations from skipped, partial, or missing results. "
            "Use concrete failure patterns to form a focused hypothesis, and avoid unsupported task-specific hints or claiming causation from bundled changes. "
            "Prefer changes that preserve behavior already supported by evaluation, keep the task-agent interface and enforced call/answer budgets intact, "
            "and run appropriate syntax or tests after editing. Do not claim a performance improvement unless a comparable evaluation demonstrates it."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
