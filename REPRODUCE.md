# REPRODUCE

Everything runs on one Linux VM as root (it creates an unprivileged `arcagent` user and network-less namespace
sandboxes). OpenAI access must be available to the root process (the gateway is the only route to the model).

## One-time setup
```bash
bash arcexp/setup_env.sh          # deps, agent user, private ARC-AGI-2 data (commit f3283f7), sysctls
bash arcexp/start_gateway.sh      # the single budget gateway (model gpt-6-luna, effort high, caps, ledger)
```

## Run a test for any seed and generation (extension, DESIGN_v2.md)
Seed index `i` = source run `source_s{i+1}`; generation `g` = the coach as it stood at generation g.
```bash
python3 -m arcexp.evolved ext_pick source_s1 20 && python3 -m arcexp.orchestrate ext source_s1 20 && python3 -m arcexp.phases final --run ext_source_s1_g20
```
(`ext_pick` applies the DESIGN_v2 pick rule to the archive as it stood at generation g, transplants that coach onto
A_0 and checks it; `orchestrate ext` runs the frozen 8-iteration test run on the pay-off set in the background;
wait until `python3 -m arcexp.orchestrate status` shows it done, then `phases final` re-scores the top two players and
scores the better one on the 120 held-out tasks; the score is appended to `exp/results/final_runs.jsonl`.)

## Score a player on the exam (120 held-out tasks, 2 calls / 2 answers per test input)
```bash
python3 -m arcexp.score_player <agent_dir> <label>
```
`<agent_dir>` is any agent repo containing `task_agent.py` (e.g. `agent_template` for A_0, or an extracted
`exp/archive_export/<run>/code/gen_<g>`). Results go to `exp/results/exam_<label>.jsonl`; the score is printed.

## Data and configuration that fully determine the experiment
- `splits.json`: seeds, held-out ids (all 120 public evaluation tasks), screen, source set, pay-off set.
- `exp/runs/<run>/config.json`: per-run seed, set, generations, freeze paths, template.
- `exp/archive_export/<run>/`: every agent of every run (code, scores, parent, children, archive per generation).
- `exp/ledger/calls.jsonl`: every model call (role, effort sent and echoed, model string returned, tokens, cost).
- `exp/results/*.jsonl`: every rollout (phase, arm, seed, iteration, task, test input, attempt, answer, correctness).
- Model: `gpt-6-luna` via the Responses API (the API returned exactly this string on every call; first call 2026-11-17).
