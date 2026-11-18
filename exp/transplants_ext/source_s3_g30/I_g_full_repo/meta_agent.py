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
            "Inspect completed evaluation reports, generation metadata, patches, and relevant failure logs before proposing a change. "
            "Compare each candidate with its parent and the initial agent; the newest generation is not necessarily the best, "
            "and an unevaluated generation is not evidence of improvement. Preserve behavior from the strongest completed result "
            "unless there is a specific, evidence-based reason to change it. Treat failed cases as clues for hypotheses, not as "
            "justification for unsupported task-specific hints. Prefer a small general change that addresses an identifiable failure "
            "mode while preserving solved cases, and keep agent interfaces and enforced budgets intact. Do not claim improvement "
            "unless evaluation confirms it."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
