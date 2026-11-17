# Decisions log

Choices made while running the pre-registered experiment unattended. Newest at the bottom.
The user allowed deviations from the prompt's design where clearly better; each deviation is marked **DEVIATION**.

## Infrastructure
1. **Branch.** Work is committed to `arc2-improver` (the branch the user asked for) and mirrored to the
   session branch `claude/determined-johnson-g5g9yj`.
2. **OpenAI auth.** `curl https://api.openai.com/v1/models` with no auth header works (proxy-injected). No key is
   read or stored. `gpt-6-luna` is listed.
3. **API and effort.** The Chat Completions API rejects `reasoning_effort: "max"` for gpt-6-luna (supports up to
   `xhigh`). The Responses API accepts `reasoning.effort: "max"` and echoes it back, so the gateway uses the
   Responses API for every call. The effort the API echoes is logged with each call in `exp/ledger/calls.jsonl`.
4. **Meta-agent effort = high (user request).** The prompt specified max. Mid-run the user asked for high
   instead of xhigh/max, so the meta agent runs at `high`. The task agent runs at `high`; the one check pass runs at `xhigh`.
5. **No Docker.** The Docker daemon is not running, and the repo's image is a CUDA image with GPU and simulator
   dependencies. This VM is the sandbox instead: every agent process runs through `arcexp/sandbox.py`.
   That means fresh mount, network and pid namespaces, uid `arcagent` with all capabilities dropped and
   `no_new_privs`, a clean environment, the agent repo bound at `/hyperagents`, and a private `/tmp`.
   *Removing the proxy variables alone does not remove network access here*: a direct HTTPS request without
   them succeeded (HTTP 200 from pypi.org). That is why the sandbox uses an empty network namespace,
   not just env stripping. The only route out is the gateway's unix socket.
6. **Budget wrapper = a separate process.** `arcexp/gateway.py` runs as root outside every agent-editable tree and
   holds the only route to OpenAI. It fixes the model and effort per role, the 2-call cap per test input
   (one token per test input), the 600k-token cap per meta iteration (one token per iteration), the
   $150 global refusal, and the ledger by role. Agents' `agent/llm.py` and `task_agent.py` are thin clients.
   When a meta iteration's 600k tokens run out, the gateway returns a normal reply saying the budget is
   exhausted, so the iteration ends gracefully and its diff is still collected. It does not return an
   error, which would crash `run_meta_agent.py`, lose the diff and mark the parent invalid.
   Infra failures (upstream errors) do not consume a call slot.
7. **Answer isolation.** Ground truth lives only in `/opt/arc_private` (mode 700, root). The experiment repo
   `/home/user` (700) holds private logs. Agents see only what is bound into their sandbox. Scoring is
   host-side. Agent-visible eval output has per-task scores, wrong answers only, and chat logs only for
   unsolved test inputs, with any grid equal to a true output of that task redacted.
   `arcexp/isolation_check.py` probes as the agent user, scans every agent-readable file on the filesystem,
   and scans every agent-visible tree on the host for test outputs (3 serializations) and held-out grids.
   A planted leak is detected (tested).
8. **Code sandbox (30 s).** Task agents run model-written code via `arc_sandbox.run_python` (read-only at
   `/opt/arc_runner`): no network, a fresh temp dir holding only `task.json` (that task's pairs + the test input),
   and 30 s wall clock per test input in total. The whole `forward()` for one test input runs in its own
   sandbox with cwd `/tmp/task` holding only that task's pairs and test input. It has a 30-minute limit,
   because two high-effort calls cannot fit in 30 s.
9. **Loop adapter.** `arcexp/run_loop.py` runs the repo's `generate_loop.py` unchanged by importing it and
   swapping only the infrastructure functions. Docker container ops become `LocalContainer`, which runs the same
   commands in the sandbox. `eval_produced_agent` becomes a host-side ARC evaluator: answers must not
   enter the agent's environment, so `domains/report.py` cannot score inside it. Plotting is a no-op.
   Parent selection (`score_child_prop`), archive, lineage patches, the `domains/` reset, compile checks and
   validity rules are the repo's own. Staged eval is skipped (`--skip_staged_eval`), matching the pre-registered
   call counts. `stagedeval_frac("arc") = 1`, so scores are never rescaled.
10. **Agent repo template.** The original copies the host repo (incl. `.git`). Here the agent repo is built from
    `agent_template/` (repo files + ARC A_0 + gateway client in `agent/llm.py`) with its own fresh git repo.
    Without that, `git add` walked up and committed into the host repo; the bad commits were reset.
11. **Crash/resume.** On resume the agent repo is hard-reset to the recorded root commit. The original
    resumed from whatever HEAD was, which is wrong after a mid-generation crash. Eval results are skipped
    only if the agent code hash matches, so a re-run iteration with new code is re-evaluated (key + code hash).
12. **Answer handling.** `forward()` returns up to 2 grids. The runner normalises and validates them. The host
    keeps the first 2 valid grids. A test input is solved if either equals the truth. JSONL rows are written
    per attempt (1, 2).

## A_0 / I_0
13. **A_0** = `agent_template/task_agent.py`. `solve_once` is one direct response: pairs as digit rows, answer
    as a JSON list of rows in `<answer>` tags, with a tolerant parser (JSON, digit rows, code block, last
    `[[...]]`). `forward` = two independent `solve_once` attempts, the "two plain attempts" standard budget.
    It is self-contained (no imports from `agent/`), so a meta-code transplant cannot change A_0.
14. **DEVIATION: I_0 instruction.** With the verbatim instruction ("Modify any part of the codebase at
    `/hyperagents/`."), gpt-6-luna asked a clarifying question in 6/6 samples and never edited anything. That is
    the stop condition "meta agent cannot produce one working code edit", and it would make the experiment
    degenerate. One sentence is appended: the README describes the goal; earlier agents and results are at
    `{eval_path}` (an argument `forward` already receives); work autonomously; a reply with no tool call ends
    the session. No ARC-specific hints. Both arms start from this same I_0.
15. **DEVIATION: tool-call parsing.** gpt-6-luna emits tool JSON without `<json>` tags in about 25% of replies,
    and sometimes ends a turn after only announcing a plan. Two adaptations in `agent/llm_withtools.py`:
    a bare `{"tool_name","tool_input"}` object is accepted when no `<json>` block exists, and a reply with no
    tool call is nudged at most twice in a row ("make the next tool call, or reply DONE").
    Same starting point for both arms; evolved agents may change it.

## Hardening after an independent adversarial review (before any meta agent ran in earnest)
16. An adversarial review (4 reviewers, 2 skeptics per finding; 21 verified findings) found ways a hostile
    meta agent could get from its shell to root. The paths were: host git in agent-owned repos (hooks/fsmonitor),
    and root following agent-planted symlinks during copies and reads. It also found budget and scoring holes.
    Fixes, all before the pilot:
    - Every generation works in a **fresh clone** of the run's root-owned pristine repo (`_ctmp/<name>/ws`), deleted
      afterwards. Root never runs git in an agent-writable repo. Global `safe.directory=*` was removed and
      `fs.protected_*` sysctls were enabled.
    - Root reads and copies agent-written files only via `arcexp/safeio.py`: regular single-link files, opened
      with O_NOFOLLOW, never through a symlinked path component, no FIFOs or devices. Agent processes are dead
      (their pid namespace is gone) before any host read.
    - The **exact evaluated code** of every node is snapshotted (regular files) right before evaluation.
      Re-scoring, held-out scoring and transplants use the snapshot, not a patch replay.
    - Gateway: tokens are **revoked** as soon as their sandbox exits, and calls are serialized per token. The
      worst-case cost and tokens are reserved before each call, so the 600k-token cap and the $150 stop
      cannot be overshot. A restart revokes all older tokens. Errors that were certainly not billed refund the
      slot. Timeouts and bad 200 responses are charged at worst case and not retried.
    - Infra-failure classification uses only gateway facts (server/network errors, global-budget refusal,
      restart revocation), never agent-written text or exit codes. Up to 4 retry rounds with backoff.
      Incomplete evaluations abort the run (resumable), so a node is never recorded with a deflated score,
      and final scoring refuses to record incomplete held-out scores.
    - Gateway/infra outages during a run raise `InfraAbort` (a BaseException). The run stops, resumable,
      instead of the loop marking parents invalid and burning the remaining generations.
    - The freeze filter matches whole path components. `filter_patch_by_files` matched substrings and
      would have dropped, e.g., `agent_helpers.py`.
    - The sandbox mounts private tmpfs over every world-writable dir (/dev/shm, /var/tmp, /run/lock, ...).
    - Agent-visible chat logs, errors and wrong answers are **withheld whole** if any true output of the
      task appears in them as a digit sequence in any serialization. They used to be redacted in place,
      which could act as an oracle.
    - The isolation check also scans .git contents, shared writable dirs, workspaces, snapshots extracted for
      evaluation, final agents and node dirs, all with FIFO-safe reads.
17. The repo's `analysis/` folder is a namespace package that the required top-level `analysis.py` would
    shadow, so `analysis/__init__.py` was added.
18. Splits: 38 screened tasks were solved once or twice (24 twice, 14 once), 54 always and 8 never. Each set has
    19 intermediate tasks + 3 always-solved + 3 never-solved (identical composition), drawn with seed 20261118.
19. **Second adversarial review** (31 agents; 14 verified findings) of the hardened code. All fixed before the pilot:
    - `unshare -i -u --kill-child`: private IPC/UTS namespaces, and the whole pid namespace dies with the sandbox.
    - Root copies into agent-reachable dirs only via a fresh root-made staging dir plus rename.
    - A strict, hunk-aware **patch sanitizer**. It rejects the whole patch on any forged/odd header, `.git` path,
      absolute or `..` path, or a `---`/`+++` that names another file, and drops frozen-path blocks. A host
      hash check verifies frozen meta files before every meta step.
    - Agent-triggerable 4xx upstream errors consume the call slot and are not infra. A sandbox-start nonce
      separates "never started" (infra) from agent failure. Infra retries are capped at 5 per key.
    - Withholding is all-or-nothing per test input.
    - Meta-step upstream outages, a failed revoke, or a restart raise InfraAbort.
    - A stale gen dir from an aborted attempt is moved aside before the generation re-runs.
    - Admin calls check HTTP status and retry. The gateway listen backlog is 256 (the old default of 5 gave
      EAGAIN under load; those rows were classified infra and re-run).
20. **Check-phase rows from before the hardening** were reconciled (`arcexp/reconcile.py`). A row with
    fewer answers than expected is kept only if the ledger shows all its model calls completed or it timed out.
    No row needed invalidating. The old-code jobs were stopped mid-way and resumed on the new code;
    unfinished keys simply ran later.
21. **xhigh pass:** the same 30-minute per-test-input wall-clock limit applies. At xhigh, many test inputs
    hit it (14 of the first 80), so the xhigh score partly measures speed. It is reported as such.
22. **DEVIATION (timing only): overlapping phases.** Held-out calls take about 3 minutes each, so the
    strictly sequential procedure would take more than a day. (a) The sanity pilot starts once B0 rep 0 is
    complete and well inside the gate (the gate is still checked on the 3-rep mean when available; if it
    fails, everything stops). (b) The 6 source runs start once the pilot runs have completed one generation
    cleanly on the hardened infrastructure, instead of after the pilot gate. Source runs do not depend
    on the pilot. If the pilot gate fails, they are stopped and their spend is reported as wasted. No result
    is used to choose anything in another phase.
