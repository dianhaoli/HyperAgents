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
            "Use the tools to inspect the code and make your changes; a response without a tool call ends the session, so only reply without one when you are done."
        )
        instruction += (
            "\n\nTreat evaluation results as evidence, not as a reason to make an arbitrary edit. "
            "Inspect the available generation reports and metadata, compare each candidate's score with its parent and the initial agent, "
            "and examine wrong-answer details or chat logs for the failures before proposing a change. "
            "For candidates that improve or regress, inspect their model_patch.diff alongside the parent patch and the "
            "task-level pass/fail changes. Use the logs to check whether a changed behavior plausibly explains those "
            "differences; do not infer causation from score movement alone. "
            "Do not assume the newest generation is best: in the supplied source_s3 results, gen_1 scored 0.96, "
            "while gen_2 scored 0.84 and the initial agent scored 0.72. Preserve the strongest general behavior unless you can "
            "identify a specific, plausible cause of failure and a change that addresses it without undermining solved cases. "
            "Avoid unsupported task-specific hints (for example, hardcoded colors, shapes, or grid dimensions); prefer general "
            "improvements supported by multiple examples or repeated failure evidence. Keep the task-agent interface and enforced "
            "model-call/answer budgets intact. Make a focused change, and do not claim an improvement unless evaluation demonstrates it."
        )

        new_msg_history = chat_with_agent(instruction, model=self.model, msg_history=[], logging=self.log, tools_available='all')
