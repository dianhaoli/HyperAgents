# STATUS

## Done
- Infrastructure: gateway (`arcexp/gateway.py`), sandbox (`arcexp/sandbox.py`), ARC domain (`domains/arc`), A_0/I_0
  template (`agent_template/`), loop adapter (`arcexp/run_loop.py`), isolation check, phases, transplant/selection
  (`arcexp/evolved.py`), `analysis.py`.
- Step 1 smoke test: 10 tasks end to end + 1 meta iteration (I_0 made a working edit; child accepted).
  Prices: $0.0028/task call (training tasks), $0.007 per meta iteration.
- Step 2 design: **Full** (see DESIGN.md).

## In progress
- Step 3 checks: screen (100 tasks x 3), B0 x3 on held-out, xhigh pass (all running as background jobs).

## Next
- `python -m arcexp.make_splits stage2 --set_size 25`, check the B0 gate, commit DESIGN.md + splits.json + analysis.py
  (step 4), then the sanity pilot (2 I_0 pay-off runs).

## Resume (after a VM rebuild or worker restart)
```bash
cd /home/user/HyperAgents && bash arcexp/setup_env.sh && bash arcexp/start_gateway.sh
bash arcexp/run_bg.sh screen python3 -m arcexp.phases screen
bash arcexp/run_bg.sh b0 python3 -m arcexp.phases b0 --reps 3
bash arcexp/run_bg.sh xhigh python3 -m arcexp.phases xhigh
```
Every job is resumable: finished (phase, arm, seed, iteration, task, test input) keys with matching code hash are skipped.
After a VM rebuild, restore each run's agent repo from `exp/runs/<run>/agent_repo.bundle` into
`exp/runs/<run>/generate_<run>/gen_initial/hyperagents` (`git clone <bundle> <dir>`), and `outputs/initial_arc_*`
from `exp/initial/`.
