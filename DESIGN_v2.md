# DESIGN_v2: extension (committed before any extension test run)

This extends the pre-registered experiment (DESIGN.md, commit f577cc7). Part A (the committed plan) is unchanged
and reported first and separately. Budget hard cap raised from $150 to $200 by the user.

## Question
Does the coach (meta agent) get better at coaching over generations? Take the coach as it stood at generations
0, 12, 20 and 40. Give each one the same starting player (A_0) and the same budget. Does a later coach produce a
better player?

## Evolution
- Continue the source runs for seeds 0, 1, 2 and 3 (by seed index: seed index i = run `source_s{i+1}`, whatever
  their results) from their saved archives to 40 generations. Same rules as the existing source runs.

## Which coach represents generation g
Use the archive as it stood at generation g. Among agents with changed coach code (parsed-AST comparison with
I_0 of the files the improvement step loads, excluding task-agent and domain code) and at least 3 descendants,
take the one whose (scored) children improved most on average. If none has 3, take the changed coach with the
most descendants. If no coach has changed code, record that and skip. Ties: earlier generation.
(`python -m arcexp.evolved ext_pick <runs> <gens>`; the pick is the node's exact evaluated-code snapshot.)

## Tests to run now
For seeds 0 to 3, the coach at generation 20 and at generation 40: eight test runs.
- Transplant the coach onto the starting player (same transplant tool as A). Memory/state files start empty
  and may be written during the run (not frozen).
- One frozen test run with exactly the rules of the committed pay-off runs: same practice (pay-off) set, 8 rounds,
  same 2-call cap, coach code locked (freeze mode).
- Re-score the top two players, then one exam (120 held-out tasks) for the better one (same as committed step 9).
- If a picked coach's parsed code is identical to an earlier pick for that seed, still run a fresh test. Never
  copy a result.
- Generation 0 = the original-coach (I_0) pay-off runs from A. Generation 12 = the evolved-coach (I_g) pay-off runs
  from A (A's committed pick rule at generation 12).

## Picks to store but not test
For seeds 0 to 3, the coach at generations 6 and 30, picked by the same rule, transplanted and checked (sandboxed
import check of coach and task agent), saved ready to run (`exp/transplants_ext/<run>_g<g>/`).

## Analysis (reported separately, labelled as an extension)
- Plot exam score against generation (0, 12, 20, 40): one dot per run, a line per seed for seeds 0-3, B0 and the
  xhigh score as horizontal lines.
- Mean and 95% t-interval at each generation.
- Mean at generation 40 minus the mean of the original-coach runs, with a 95% Welch interval: "rising" if the
  interval is above 0, "falling" if below 0, otherwise "flat within the interval".
- For seeds 0-3, the paired changes from 12 to 20 and from 20 to 40.
- How many picks had changed coach code, and a diff audit tagging each changed hunk of every picked coach as
  ARC-specific or general.

## Common rules (both parts)
- Same time limit for every arm including B0: 3 h per test input (never binds in practice); timeouts reported per arm.
- Coach effort: `high`, as used by the source runs (every coach call so far was sent and echoed as `high`).
- Model: `gpt-6-luna` (the exact model string returned by the API on every call, 2026-11-17).

## Results that existed at this commit
- B0 summaries: 5 lines (reps 0,1 complete; rep 2 re-running its timed-out inputs)
- xhigh pass: rows 376 (re-running inputs that hit the old limit)
- run payoff_I0_1: phase payoff, archive entries 9, done=True
- run payoff_I0_2: phase payoff, archive entries 9, done=True
- run smoke: phase smoke, archive entries 2, done=True
- run source_s1: phase source, archive entries 13, done=False
- run source_s2: phase source, archive entries 13, done=False
- run source_s3: phase source, archive entries 13, done=False
- run source_s4: phase source, archive entries 13, done=False
- run source_s5: phase source, archive entries 13, done=True
- run source_s6: phase source, archive entries 13, done=True
- run trial_Ig_source_s1: phase trial, archive entries 1, done=False
- run trial_Ig_source_s2: phase trial, archive entries 2, done=True
- run trial_Ig_source_s3: phase trial, archive entries 1, done=False
- run trial_Ig_source_s5: phase trial, archive entries 1, done=False
- run trial_Ig_source_s6: phase trial, archive entries 1, done=False
- final_runs.jsonl (held-out scores of pay-off runs): 0 records (pilot exams in progress)
- ig_selection.json (A's I_g picks at generation 12), source_stats.json, transplants for A
- No extension pick (generations 6/20/30/40) and no extension test run exists.
