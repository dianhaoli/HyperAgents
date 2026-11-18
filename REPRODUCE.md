# REPRODUCE

Everything runs on one Linux VM as root (it creates an unprivileged `arcagent` user and network-less namespace
sandboxes). OpenAI access must be available to the root process (the gateway is the only route to the model).

## One-time setup
```bash
bash arcexp/setup_env.sh          # deps, agent user, private ARC-AGI-2 data (commit f3283f7), sysctls
bash arcexp/start_gateway.sh      # the single budget gateway (model gpt-6-luna, effort high, caps, ledger)
```

## Full pipeline, in order
Each step is resumable; long ones run detached via `arcexp/run_bg.sh`.
```bash
bash arcexp/setup_env.sh                      # once per VM: deps, agent user, private ARC data, sysctls
bash arcexp/start_gateway.sh                  # budget gateway (idempotent)
python3 -m arcexp.isolation_check <phase>     # answer-isolation check; run before each phase
python3 -m arcexp.make_splits stage1          # held-out / screen / smoke ids
python3 -m arcexp.run_loop --config exp/runs/smoke/config.json            # step 1 smoke test
python3 -m arcexp.phases screen               # step 3: 100 training tasks x 3 single calls
python3 -m arcexp.make_splits stage2 --set_size 25                        # source / pay-off sets
for r in 0 1 2; do python3 -m arcexp.phases b0 --only $r; done            # step 3: B0 x3
python3 -m arcexp.phases xhigh                # step 3: one held-out pass at xhigh
python3 -m arcexp.orchestrate pilot           # step 5: 2 I_0 pay-off runs
python3 -m arcexp.phases final --run payoff_I0_1; python3 -m arcexp.phases final --run payoff_I0_2
python3 -m arcexp.orchestrate source          # step 6: 6 source runs x 12 generations
python3 -m arcexp.evolved select              # step 6: choose I_g per seed
python3 -m arcexp.evolved transplant          # transplant each I_g's meta code onto A_0
python3 -m arcexp.orchestrate trial           # step 7: one trial iteration per I_g
python3 -m arcexp.orchestrate payoff          # step 8: I_g pay-off runs + remaining I_0 runs (freeze mode)
python3 -m arcexp.phases final --run <run>    # step 9: per pay-off run
python3 -m arcexp.evolved stats               # self-edit statistics
python3 analysis.py                           # results
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

## Explorer and traced demo
```bash
python3 arcexp/build_explorer_data.py && python3 arcexp/build_coach_sessions.py   # rebuild explorer/data
python3 -m http.server -d explorer 8000                                             # view at localhost:8000
python3 -m arcexp.demo_trace --help                                                 # traced demo (DECISIONS 41)
python3 -m arcexp.page_text extract   # all page text -> explorer/PAGE_TEXT.md; edit, then: apply
```
