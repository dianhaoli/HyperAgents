# STATUS

## Done
- Infrastructure: gateway (`arcexp/gateway.py`), sandbox (`arcexp/sandbox.py`), ARC domain (`domains/arc`), A_0/I_0
  template (`agent_template/`), loop adapter (`arcexp/run_loop.py`), isolation check, phases, transplant/selection
  (`arcexp/evolved.py`), `analysis.py`.
- Step 1 smoke test: 10 tasks end to end + 1 meta iteration (I_0 made a working edit; child accepted).
  Prices: $0.0028/task call (training tasks), $0.007 per meta iteration.
- Step 2 design: **Full** (see DESIGN.md).

## Pre-registration commit (step 4)
DESIGN.md, splits.json and analysis.py were committed at `f577cc77d8fac1125623c6a85e9ad3ad86ca2964` (before any pay-off result).

## In progress
- Step 3 checks (hardened code): B0 reps 0-2 and the xhigh pass on held-out (jobs b0_rep0..2, xhigh).
  Screen done (splits.json stage 2 done: 25 source + 25 pay-off tasks).
- Step 5 sanity pilot: payoff_I0_1, payoff_I0_2 (8 iterations each, freeze mode).

## Next
- Once a pilot run completes one generation cleanly: `python -m arcexp.orchestrate source` (6 source runs, 12 gens).
- Pilot gate after both pilot runs finish: `python -m arcexp.phases final --run payoff_I0_1` (and _2).
- Then `python -m arcexp.evolved select`, `transplant`, `python -m arcexp.orchestrate trial`, then `payoff`, then
  `final` for every pay-off run, then `python analysis.py`.

## Resume (after a VM rebuild or worker restart)
```bash
cd /home/user/HyperAgents && bash arcexp/setup_env.sh && bash arcexp/start_gateway.sh
rm -rf exp/stage/*            # only when no job is running
for r in 0 1 2; do bash arcexp/run_bg.sh b0_rep$r python3 -m arcexp.phases b0 --only $r; done
bash arcexp/run_bg.sh xhigh python3 -m arcexp.phases xhigh
python3 -m arcexp.orchestrate pilot     # relaunches unfinished pilot runs (resumable)
python3 -m arcexp.orchestrate source    # once started: relaunches unfinished source runs
python3 -m arcexp.orchestrate status
```
Every job is resumable: finished (phase, arm, seed, iteration, task, test input) keys with matching code hash are skipped.
After a VM rebuild, restore each run's agent repo from `exp/runs/<run>/agent_repo.bundle` into
`exp/runs/<run>/generate_<run>/gen_initial/hyperagents` (`git clone <bundle> <dir>`), and `outputs/initial_arc_*`
from `exp/initial/`.
