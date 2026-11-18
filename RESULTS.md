# RESULTS

## Headline

**Neither improver beat two plain attempts on ARC-AGI-2**

## Main estimates (held-out ARC-AGI-2 public evaluation, 120 tasks, 167 test inputs)

- B0 (A_0, two plain attempts): 29.3% (reps: 30.1%, 27.9%, 29.7%)
- **G** (I_0-built agents minus B0): +0.4 points, 95% Welch CI [-1.9, +2.8] (df 5.3)
- **Delta** (evolved-improver agents minus I_0-built agents): -1.8 points, 95% Welch CI [-4.2, +0.6] (df 7.8)
- Evolved arm gain over B0: -1.4 points, 95% Welch CI [-4.0, +1.3] (df 5.9)
- Qualifying evolved improvers: 5 of 6 source seeds

## Per-run held-out scores

| run | arm | seed | final node | held-out | accepted candidates in run |
|---|---|---|---|---|---|
| payoff_I0_1 | I0 | r1 | 4 | 26.9% | 6 |
| payoff_I0_2 | I0 | r2 | 4 | 29.4% | 7 |
| payoff_I0_3 | I0 | r3 | 3 | 30.4% | 5 |
| payoff_I0_4 | I0 | r4 | 5 | 30.4% | 7 |
| payoff_I0_5 | I0 | r5 | 3 | 31.4% | 3 |
| payoff_I0_6 | I0 | r6 | 3 | 29.4% | 6 |
| payoff_Ig_source_s1 | Ig | 1 | 1 | 26.0% | 4 |
| payoff_Ig_source_s2 | Ig | 2 | 3 | 27.4% | 5 |
| payoff_Ig_source_s3 | Ig | 3 | 1 | 31.0% | 2 |
| payoff_Ig_source_s5 | Ig | 5 | 3 | 27.2% | 6 |
| payoff_Ig_source_s6 | Ig | 6 | 2 | 27.9% | 5 |
| ext_source_s1_g20 | g20 | 0 | 6 | 27.8% | 6 |
| ext_source_s2_g20 | g20 | 1 | 5 | 31.5% | 3 |
| ext_source_s3_g20 | g20 | 2 | 2 | 31.8% | 2 |
| ext_source_s4_g20 | g20 | 3 | initial | 27.9% | 2 |
| ext_source_s1_g40 | g40 | 0 | 8 | 36.0% | 4 |
| ext_source_s2_g40 | g40 | 1 | 1 | 31.5% | 6 |
| ext_source_s3_g40 | g40 | 2 | 3 | 24.9% | 5 |
| ext_source_s4_g40 | g40 | 3 | 7 | 28.9% | 5 |

Run-to-run SD: B0 1.2%, I_0 arm 1.5%, evolved arm 1.9%.

## Secondary results

- One held-out pass of A_0 at xhigh effort: 0.4111 (same 30-min per-test-input wall-clock limit; many xhigh inputs hit it).
- Self-edit rate in source runs: 21 of 72 generations changed meta-agent code; 15 of those became parents.
  - source_s1: 1/12 self-edits, 1 became parents
  - source_s2: 4/12 self-edits, 3 became parents
  - source_s3: 5/12 self-edits, 3 became parents
  - source_s4: 1/12 self-edits, 0 became parents
  - source_s5: 7/12 self-edits, 5 became parents
  - source_s6: 3/12 self-edits, 3 became parents
- Selected evolved improvers (I_g):
  - source_s1: gen 1, 1 children (1 scored), mean child improvement +12.0 pts, meta files changed vs I_0: meta_agent.py; meta edits in ancestry at generations [1]
  - source_s2: gen 5, 2 children (2 scored), mean child improvement -4.0 pts, meta files changed vs I_0: meta_agent.py; meta edits in ancestry at generations [5]
  - source_s3: gen 3, 1 children (1 scored), mean child improvement +0.0 pts, meta files changed vs I_0: meta_agent.py; meta edits in ancestry at generations [3]
  - source_s4: no qualifying agent (no meta-code change with a scored child) - no pay-off run
  - source_s5: gen 6, 1 children (1 scored), mean child improvement +8.0 pts, meta files changed vs I_0: meta_agent.py; meta edits in ancestry at generations [6]
  - source_s6: gen 4, 3 children (1 scored), mean child improvement -4.0 pts, meta files changed vs I_0: utils/git_utils.py; meta edits in ancestry at generations [4]
- Tokens, arm I0: 27048 task-agent tokens per task evaluation (825 evaluations); 349804 meta tokens per iteration (48 iterations)
- Tokens, arm Ig: 23510 task-agent tokens per task evaluation (550 evaluations); 187914 meta tokens per iteration (40 iterations)

## Spend by role (USD, ledger)

- meta: $4.19
- probe: $0.00
- task: $148.03
- **total: $152.23** (hard stop: $150 under DESIGN.md, raised to $200 by the user; projection posted before the extension tests: ~$135-165)

## Crashes, aborts and reruns

- payoff_I0_1__harness_nonce_bug (see DECISIONS.md)
- payoff_I0_2__harness_nonce_bug (see DECISIONS.md)
- payoff_I0_2__sanitizer_dropped_gitignore_patch_gen7 (see DECISIONS.md)
- infra abort (resumed) in ext_source_s1_g40 at gen 8: upstream errors during meta step (rc=0, patch=False)
- infra abort (resumed) in payoff_I0_4 at gen 6: gateway restarted or global budget refusal during meta step
- infra abort (resumed) in payoff_I0_6 at gen 6: gateway restarted or global budget refusal during meta step
- infra abort (resumed) in payoff_Ig_source_s6 at gen 8: gateway restarted or global budget refusal during meta step
- infra abort (resumed) in source_s2 at gen 18: upstream errors during meta step (rc=0, patch=False)
- infra abort (resumed) in source_s3 at gen 15: upstream errors during meta step (rc=0, patch=False)
- infra abort (resumed) in source_s3 at gen 15: upstream errors during meta step (rc=0, patch=False)
- infra abort (resumed) in source_s4 at gen 19: gateway restarted or global budget refusal during meta step

## Timeouts per arm (rollouts that hit the per-test-input wall-clock limit)

| arm / phase | rollouts | timeouts |
|---|---|---|
| b0 / A0 | 501 | 0 |
| ext_payoff / g20 | 350 | 0 |
| ext_payoff / g40 | 520 | 0 |
| heldout / I0 | 1002 | 0 |
| heldout / Ig | 862 | 0 |
| heldout / g20 | 668 | 0 |
| heldout / g40 | 668 | 0 |
| initial / A0 | 221 | 0 |
| payoff / I0 | 1079 | 0 |
| payoff / Ig | 572 | 0 |
| rescore / I0 | 312 | 0 |
| rescore / Ig | 260 | 0 |
| rescore / g20 | 208 | 0 |
| rescore / g40 | 208 | 0 |
| screen / A0 | 309 | 0 |
| smoke / I0 | 13 | 0 |
| source / I0src | 3252 | 1 |
| trial / Ig | 78 | 0 |
| xhigh / A0 | 167 | 0 |

49 rollouts that hit an earlier (30-min) limit were invalidated and re-run under the 3 h limit.

## Model and reasoning effort actually used

- Model string returned by the API: `gpt-6-luna` (25820 calls); calls from 2026-11-17 to 2026-11-18.
- Effort echoed by the API, by role: meta=high: 3194, probe=high: 2, task=high: 22234, task=xhigh: 390.

# EXTENSION (DESIGN_v2.md, not pre-registered in f577cc7)

Does the coach get better at coaching over generations? Exam score of the player each coach builds, by coach generation.

![extension plot](exp/results/extension_plot.png)

| generation | runs | mean | 95% t-interval | scores |
|---|---|---|---|---|
| 0 | 6 | 29.7% | [28.1%, 31.3%] | 26.9%, 29.4%, 31.4%, 30.4%, 30.4%, 29.4% |
| 12 | 5 | 27.9% | [25.6%, 30.2%] | 27.4%, 31.0%, 27.2%, 26.0%, 27.9% |
| 20 | 4 | 29.8% | [26.2%, 33.3%] | 27.9%, 31.5%, 31.8%, 27.8% |
| 40 | 4 | 30.3% | [22.9%, 37.7%] | 28.9%, 24.9%, 31.5%, 36.0% |

**Generation 40 minus original coach: +0.6 points, 95% Welch CI [-6.5, +7.8] -> flat within the interval.**
- Paired change 12->20 (seeds 0-3): seed 0: +1.8, seed 1: +4.2, seed 2: +0.8; mean +2.3
- Paired change 20->40 (seeds 0-3): seed 0: +8.2, seed 1: +0.0, seed 2: -6.9, seed 3: +1.0; mean +0.6

**Caveat (identical coaches).** Several extension picks are the same coach node at several generations (DECISIONS 37). Seed 0's picks at generations 12, 20 and 40 are all node 1, and seed 2's at 20 and 40 are node 9. For those seeds the 'change' between generations is run-to-run variation of one coach's 8-round run. Seed 0's identical coach scored 26.0%, 27.8%, 36.0% (a spread of about 10 points), so the trend cannot be separated from that variation.

**Pick rules compared at generation 12** (extension rule vs committed rule, same archive):

| seed | committed rule | extension rule | same coach? |
|---|---|---|---|
| 0 (source_s1) | 1 | 1 | yes |
| 1 (source_s2) | 5 | 5 | yes |
| 2 (source_s3) | 3 | 3 | yes |
| 3 (source_s4) | none | 6 | no |

Seed 3: the committed rule needs a changed coach with at least one scored child and finds none. The extension rule falls back to the changed coach with the most descendants: node 6, with 0 descendants (tied with node 12 and broken by the earlier generation).
- Picks with changed coach code: generation 12 (part A rule) 5 of 6 seeds; extension 16 of 16 ({'source_s1:g6': 1, 'source_s2:g6': 5, 'source_s3:g6': 3, 'source_s4:g6': 6, 'source_s4:g20': 12, 'source_s2:g20': 9, 'source_s3:g20': 9, 'source_s1:g20': 1, 'source_s4:g30': 15, 'source_s2:g30': 9, 'source_s4:g40': 13, 'source_s3:g30': 9, 'source_s1:g30': 1, 'source_s2:g40': 5, 'source_s3:g40': 9, 'source_s1:g40': 1}).

## Diff audit of every picked coach (each changed hunk vs I_0; 2 independent judges + tiebreak)

| pick | file | hunk | tag | agreement |
|---|---|---|---|---|
| A_gen12:source_s1 | meta_agent.py | 0 | general | unanimous |
| A_gen12:source_s2 | meta_agent.py | 0 | general | unanimous |
| A_gen12:source_s2 | meta_agent.py | 1 | general | unanimous |
| A_gen12:source_s3 | meta_agent.py | 0 | ARC-specific | unanimous |
| A_gen12:source_s5 | meta_agent.py | 0 | general | unanimous |
| A_gen12:source_s6 | utils/git_utils.py | 0 | general | unanimous |
| A_gen12:source_s6 | utils/git_utils.py | 1 | general | unanimous |
| ext:source_s1_g20 | meta_agent.py | 0 | general | unanimous |
| ext:source_s1_g30 | meta_agent.py | 0 | general | unanimous |
| ext:source_s1_g40 | meta_agent.py | 0 | general | unanimous |
| ext:source_s1_g6 | meta_agent.py | 0 | general | unanimous |
| ext:source_s2_g20 | meta_agent.py | 0 | general | unanimous |
| ext:source_s2_g20 | meta_agent.py | 1 | general | unanimous |
| ext:source_s2_g30 | meta_agent.py | 0 | general | unanimous |
| ext:source_s2_g30 | meta_agent.py | 1 | general | unanimous |
| ext:source_s2_g40 | meta_agent.py | 0 | general | unanimous |
| ext:source_s2_g40 | meta_agent.py | 1 | general | unanimous |
| ext:source_s2_g6 | meta_agent.py | 0 | general | unanimous |
| ext:source_s2_g6 | meta_agent.py | 1 | general | unanimous |
| ext:source_s3_g20 | meta_agent.py | 0 | general | unanimous |
| ext:source_s3_g30 | meta_agent.py | 0 | general | unanimous |
| ext:source_s3_g40 | meta_agent.py | 0 | general | unanimous |
| ext:source_s3_g6 | meta_agent.py | 0 | ARC-specific | unanimous |
| ext:source_s4_g20 | agent/tools/bash.py | 0 | general | unanimous |
| ext:source_s4_g20 | agent/tools/bash.py | 1 | general | unanimous |
| ext:source_s4_g20 | agent/tools/bash.py | 2 | general | unanimous |
| ext:source_s4_g30 | meta_agent.py | 0 | ARC-specific | unanimous |
| ext:source_s4_g30 | meta_agent.py | 1 | general | unanimous |
| ext:source_s4_g40 | meta_agent.py | 0 | general | unanimous |
| ext:source_s4_g40 | meta_agent.py | 1 | general | unanimous |
| ext:source_s4_g6 | meta_agent.py | 0 | general | unanimous |
| ext:source_s4_g6 | run_meta_agent.py | 1 | general | unanimous |

3 of 32 hunks ARC-specific, 29 general. Reasons in exp/results/diff_audit.json.

## Deviations from f577cc7 and DESIGN_v2.md

Every deviation and harness fix is numbered in DECISIONS.md (items marked DEVIATION; harness bugs and reruns at 23, 24, 26, 28, 33, 35).

## analysis.py output

```
HEADLINE: Neither improver beat two plain attempts on ARC-AGI-2
B0 = 29.3% (reps: 30.1%, 27.9%, 29.7%)
G                +0.4 pts  95% CI [-1.9, +2.8]  df=5.3
Delta            -1.8 pts  95% CI [-4.2, +0.6]  df=7.8
I0_gain_over_B0  +0.4 pts  95% CI [-1.9, +2.8]  df=5.3
Ig_gain_over_B0  -1.4 pts  95% CI [-4.0, +1.3]  df=5.9

| run | arm | seed | final node | held-out |
|---|---|---|---|---|
| payoff_I0_1 | I0 | r1 | 4 | 26.9% |
| payoff_I0_2 | I0 | r2 | 4 | 29.4% |
| payoff_I0_3 | I0 | r3 | 3 | 30.4% |
| payoff_I0_4 | I0 | r4 | 5 | 30.4% |
| payoff_I0_5 | I0 | r5 | 3 | 31.4% |
| payoff_I0_6 | I0 | r6 | 3 | 29.4% |
| payoff_Ig_source_s1 | Ig | 1 | 1 | 26.0% |
| payoff_Ig_source_s2 | Ig | 2 | 3 | 27.4% |
| payoff_Ig_source_s3 | Ig | 3 | 1 | 31.0% |
| payoff_Ig_source_s5 | Ig | 5 | 3 | 27.2% |
| payoff_Ig_source_s6 | Ig | 6 | 2 | 27.9% |
| ext_source_s1_g20 | g20 | 0 | 6 | 27.8% |
| ext_source_s2_g20 | g20 | 1 | 5 | 31.5% |
| ext_source_s3_g20 | g20 | 2 | 2 | 31.8% |
| ext_source_s4_g20 | g20 | 3 | initial | 27.9% |
| ext_source_s1_g40 | g40 | 0 | 8 | 36.0% |
| ext_source_s2_g40 | g40 | 1 | 1 | 31.5% |
| ext_source_s3_g40 | g40 | 2 | 3 | 24.9% |
| ext_source_s4_g40 | g40 | 3 | 7 | 28.9% |

run-to-run SD: {'B0': '1.2%', 'I0': '1.5%', 'Ig': '1.9%'}
self-edit: {'source_s1': {'gens': 12, 'self_edit_gens': 1, 'self_edit_parents': 1}, 'source_s2': {'gens': 12, 'self_edit_gens': 4, 'self_edit_parents': 3}, 'source_s3': {'gens': 12, 'self_edit_gens': 5, 'self_edit_parents': 3}, 'source_s4': {'gens': 12, 'self_edit_gens': 1, 'self_edit_parents': 0}, 'source_s5': {'gens': 12, 'self_edit_gens': 7, 'self_edit_parents': 5}, 'source_s6': {'gens': 12, 'self_edit_gens': 3, 'self_edit_parents': 3}} rate 0.2916666666666667
tokens by arm: {'I0': {'task_tokens_per_task_eval': 27048.02303030303, 'meta_tokens_per_iteration': 349804.3333333333, 'n_task_evals': 825, 'n_meta_iterations': 48}, 'Ig': {'task_tokens_per_task_eval': 23510.296363636364, 'meta_tokens_per_iteration': 187913.875, 'n_task_evals': 550, 'n_meta_iterations': 40}}
spend by role: {'probe': 0.0, 'task': 148.033, 'meta': 4.194} total 152.227
```
