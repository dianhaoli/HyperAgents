# STATUS

Pre-registration: DESIGN.md / splits.json / analysis.py at `f577cc7`. Extension: DESIGN_v2.md at `991a237`.
Hard cap $200 (gateway). One gateway (`arcexp/start_gateway.sh` is locked and idempotent).

## Done
- **PART A COMPLETE.** Headline: "Neither improver beat two plain attempts on ARC-AGI-2". G = +0.4 pts [-1.9, +2.8]; Delta = -1.8 pts [-4.2, +0.6]. 6 I0 + 5 Ig exams in exp/results/final_runs.jsonl; RESULTS.md.
- B0 complete: 30.1 / 27.9 / 29.7 (mean 29.3%). xhigh pass 41.1%. Pilot exams: payoff_I0_1 26.9%, payoff_I0_2 29.4% -> pilot gate PASSED.
- Part A trials passed (all 5 transplanted coaches ran). Part A pay-off runs launched (5 I_g + I0_3..6).
- Smoke test, screen, splits, B0 reps 0-1 (30.1%, 27.9%), source runs s1-s6 to 12 generations, pilot runs
  payoff_I0_1/2 (8 iterations each).
- Part A I_g selection at generation 12: 5 of 6 qualify (s1 g1, s2 g5, s3 g3, s5 g6, s6 g4; s4 none);
  transplants in `exp/transplants/`.

## Running (all resumable)
- `driver` job (arcexp/driver.py): launches final exams as runs finish, extension picks at gens 6/20/30/40, extension test runs at 20/40; commits after each action.
- Part A: B0 rep 2 and xhigh re-runs of formerly timed-out inputs; final exams of payoff_I0_1/2 (pilot gate);
  trial iterations `trial_Ig_source_s{1,2,3,5,6}`.
- Part B: source_s1..s4 continuing to 40 generations.

## Next
1. When the trials pass: `python3 -m arcexp.orchestrate payoff` (5 I_g runs + payoff_I0_3..6).
2. Pilot gate when both pilot exams exist (`exp/results/final_runs.jsonl`).
3. When a source run reaches gen 20 / 40: `python3 -m arcexp.evolved ext_pick source_sN 6,20` (or 30,40), then the
   extension test runs (`python3 -m arcexp.orchestrate ext <run> <gen>`).
4. Finals for every pay-off/extension run: `python3 -m arcexp.phases final --run <run>`.
5. `python3 analysis.py`, extension analysis, `python3 -m arcexp.make_results`.

## Resume after a VM restart (copy-paste)
```bash
cd /home/user/HyperAgents && bash arcexp/resume.sh
python3 -m arcexp.orchestrate resume      # relaunches every unfinished run and phase job recorded in exp/logs/*.pid
bash arcexp/monitor.sh
```
