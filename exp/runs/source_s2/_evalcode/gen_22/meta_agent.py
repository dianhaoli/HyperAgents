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
            "Before editing, inspect the available evaluation reports and compare results across generations. Identify the strongest relevant result and its associated agent changes, then use per-task scores and available predictions to find concrete failures or regressions. "
            "Make a focused, generalizable change to the generation system that addresses evidence from those failures while preserving behavior responsible for successful tasks; do not assume one report or task is representative when more results are available. "
            "Inspect the affected code and run appropriate checks or tests after editing. Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
