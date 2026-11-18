# Does a self-improving coach get better at coaching? A test on ARC-AGI-2

**TL;DR.** On the pre-registered test, players built by the original coach scored no better on a held-out ARC-AGI-2 exam than a player that simply asks the model twice (29.3%), and players built by self-evolved coaches scored 1.8 points lower than the original coach's players (95% interval -4.2 to +0.6, so no clear difference). In a follow-up that was not pre-registered, coaches taken from later in evolution (up to generation 40) built players that scored about the same as the original coach's players (+0.6 points, 95% interval -6.5 to +7.8). Several of those "later" coaches were the same code as earlier ones, so this is weak evidence either way. The whole study cost $152.23 in model calls.

## The question

This repo has two LLM agents. The **coach** (the repo's *meta agent*) reads results and edits code. The **player** (the repo's *task agent*) solves ARC puzzles. The coach can edit the player, and it can also edit itself. The idea is that a coach that rewrites itself might become a better coach. We asked: if you take a coach that has evolved itself and give it the same budget as the original coach, does it build a better player? An extension then asked whether coaches from later generations do better than coaches from earlier ones.

## How we tested it

1. **Puzzles.** ARC-AGI-2: small coloured-grid puzzles where you must infer a rule from a few examples. The **exam** is all 120 public evaluation tasks (167 test inputs). No coach ever saw it.
2. **Practice sets.** Two disjoint sets of 25 training tasks: a *source* set (where coaches evolve) and a *pay-off* set (where coaches are tested). Each set has 19 tasks the starting player solves sometimes but not always, plus 3 it always solves and 3 it never solves (too few intermediate tasks qualified to fill both sets).
3. **Budget.** Every player gets at most 2 model calls and 2 answers per test input. A puzzle input counts as solved if either answer is exactly right. Model: `gpt-6-luna` at reasoning effort `high` (effort is an API setting for how long the model thinks before it answers; `xhigh` is the next level up). A separate budget process fixes the model and effort, so no coach can change them.
4. **Starting player A_0.** It just asks the model for the answer twice. Its exam score is **B0** (measured 3 times).
5. **Source runs.** Starting from the original coach (I_0), the repo's own evolution loop ran for 12 generations on the source set, 6 times (runs `source_s1` to `source_s6`). Each generation, the coach edits the code, including possibly its own code.
6. **Picking the evolved coach (I_g).** In each source run, among coaches whose code differs from I_0 and that produced at least one scored child, take the one whose children improved most. 5 of 6 runs had one.
7. **Pay-off runs.** Each coach gets A_0 and 8 rounds on the pay-off set, with its own code frozen. So it can only improve the player. Six runs used I_0; five used an I_g.
8. **Final exam.** In each run, the two players with the best pay-off-set scores are re-scored on that set. The one with the higher mean of its loop score and re-score takes the exam once. The unedited A_0 is eligible. In one run (`source_s4` at generation 20) it won, so that exam score is A_0's own.

## Results: the pre-registered experiment

Pre-registered headline: **"Neither improver beat two plain attempts on ARC-AGI-2."**

| run | coach | exam score |
|---|---|---|
| B0 rep 0 / 1 / 2 | none (A_0) | 30.1% / 27.9% / 29.7% (mean 29.3%) |
| A_0 at xhigh effort (one pass) | none | 41.1% |
| payoff_I0_1 | original | 26.9% |
| payoff_I0_2 | original | 29.4% |
| payoff_I0_3 | original | 30.4% |
| payoff_I0_4 | original | 30.4% |
| payoff_I0_5 | original | 31.4% |
| payoff_I0_6 | original | 29.4% |
| payoff_Ig_source_s1 | evolved (from source_s1; coach created at generation 1) | 26.0% |
| payoff_Ig_source_s2 | evolved (from source_s2; coach created at generation 5) | 27.4% |
| payoff_Ig_source_s3 | evolved (from source_s3; coach created at generation 3) | 31.0% |
| payoff_Ig_source_s5 | evolved (from source_s5; coach created at generation 6) | 27.2% |
| payoff_Ig_source_s6 | evolved (from source_s6; coach created at generation 4) | 27.9% |

`source_s4` had no qualifying evolved coach, so it had no pay-off run.

Intervals are 95% Welch intervals: a standard confidence interval for the difference of two group means that does not assume equal spread. If an interval contains 0, the data cannot tell the difference from no effect.

| estimate | value | 95% Welch interval |
|---|---|---|
| **G** = original-coach players minus B0 | +0.4 points | [-1.9, +2.8] |
| **Delta** = evolved-coach players minus original-coach players | -1.8 points | [-4.2, +0.6] |
| Evolved-coach players minus B0 | -1.4 points | [-4.0, +1.3] |

Run-to-run standard deviation: B0 1.2, original-coach runs 1.5, evolved-coach runs 1.9 points.

In plain terms: every interval includes zero, so we found no evidence that either coach helped, and no evidence that evolving the coach helped or hurt. For reference, a single pass of A_0 at xhigh effort scored 41.1%. The model can do much better with more thinking per call, but effort was locked at high for every player, so this gain was not available to any coach.

## Results: the extension (does the coach improve over generations?)

This part was planned after the main result (DESIGN_v2.md), not pre-registered. Source runs `source_s1` to `source_s4` were continued to 40 generations. "The coach at generation g" means the coach picked from a run's saved versions as they stood after g generations; it may have been created much earlier. For generations 20 and 40 the rule was: among changed coaches with at least 3 descendants, take the one whose children improved most; if none has 3, take the changed coach with the most descendants. Each picked coach was then tested exactly like a pay-off run. Coaches were also picked at generations 6 and 30, but those were only stored, not tested. Generation 0 is the six original-coach runs. Generation 12 is the five evolved-coach runs above, which include `source_s5` and `source_s6` (not continued) and lack `source_s4` (no qualifying coach). So generation 12 is not the same set of runs as 20 and 40.

![](exp/results/extension_plot.png)

| generation | runs | mean | 95% interval | scores |
|---|---|---|---|---|
| 0 | 6 | 29.7% | [28.1%, 31.3%] | 26.9, 29.4, 31.4, 30.4, 30.4, 29.4 |
| 12 | 5 | 27.9% | [25.6%, 30.2%] | 27.4, 31.0, 27.2, 26.0, 27.9 |
| 20 | 4 | 29.8% | [26.2%, 33.3%] | 27.9, 31.5, 31.8, 27.8 |
| 40 | 4 | 30.3% | [22.9%, 37.7%] | 28.9, 24.9, 31.5, 36.0 |

**Generation 40 minus generation 0: +0.6 points, 95% Welch interval [-6.5, +7.8]. The interval is wide and includes 0, so there is no detectable trend.**

Paired changes for the same source run: 12 to 20 was +1.8, +4.2, +0.8 (`source_s1` to `source_s3`; `source_s4` had no generation-12 coach), mean +2.3. 20 to 40 was +8.2, +0.0, -6.9, +1.0 (`source_s1` to `source_s4`), mean +0.6.

**Caveat: often the "later" coach is the same coach.** The pick rule often chose the same coach node (a node is one saved version of the code in a run's archive) at several generations (DECISIONS 37). `source_s1` picked node 1 at generations 12, 20 and 40. `source_s3` picked node 9 at 20 and 40. `source_s2` picked node 5 at 12 and 40 (node 9 at 20), so its 12-to-40 comparison is one fixed coach re-run. For `source_s1` (all generations) and `source_s3` (20 to 40), the reported paired changes are just the noise of re-running one fixed coach. `source_s1`'s identical coach scored 26.0%, 27.8% and 36.0%, a spread of about 10 points. So no trend can be separated from that noise.

**Pick rule check.** At generation 12, the extension rule and the committed rule pick the same coach for `source_s1`, `source_s2` and `source_s3`. For `source_s4` the committed rule picks none, while the extension rule falls back to node 6, a coach with 0 descendants. So the two rules agree wherever both pick a coach. The only difference is that the extension rule will pick a barely tested coach when nothing better exists.

## What the evolved coaches actually changed

- **Self-edits were uncommon.** In the first 12 generations, 21 of 72 generations (29%) changed coach code, and 15 of those changed coaches were later chosen as the starting point for a further edit. By run (`source_s1` to `source_s6`): 1, 4, 5, 1, 7 and 3 of 12.
- **Diff audit.** All 21 picked coaches (5 from the main test, 16 from the extension at generations 6, 20, 30 and 40) were compared with I_0. Every changed piece ("hunk") was tagged by two independent judges as ARC-specific or general. All tags were unanimous. 3 of 32 hunks were ARC-specific:
  - The `source_s3` coach (node 3, picked both by the main rule and as the extension's generation-6 pick) wrote this run's own scores into its prompt ("gen_1 scored 0.96, while gen_2 scored 0.84...") and warned against "hardcoded colors, shapes, or grid dimensions". These are two of the three hunks, but they are the same coach code.
  - The `source_s4` coach picked at generation 30 pointed the coach at the `arc_eval` log folder and used this harness's prediction fields. This coach was stored but not tested.
- **Most edits were bookkeeping and advice.** Typical changes added a helper that reads past evaluation reports, lists failed tasks, and flags regressions. They also added prompt text like "be evidence-driven, compare with the parent, make one focused change, don't hard-code answers". A few were plumbing: one fixed the git diff helper to skip bytecode files; one made the bash tool keep a persistent shell.

## Caveats and what went wrong

- **The original coach needed adapting (DECISIONS 14, 15).** With the repo's verbatim instruction, the model only asked clarifying questions and never edited code. One sentence was added (work autonomously) and tool-call parsing was loosened. Both groups started from this adapted coach.
- **The original coach often made no edit (DECISIONS 27).** It ended 11 of its first 31 coaching steps without an edit, mostly from tool-call format problems. Left unchanged, as pre-registered.
- **Harness bugs (DECISIONS 23, 24).** One bug broke the first two original-coach pay-off runs (the "pilot") before any coach ran; both restarted with new seeds. Another discarded coach edits that created a `.gitignore` file: payoff_I0_2 was restarted a second time; source_s6 kept its run, losing one of 12 generations.
- **Some coach edits broke the player (DECISIONS 32),** e.g. passing an argument the function did not accept, scoring 0. These count as real outcomes.
- **Time limit (DECISIONS 26, 29).** A 30-minute limit per test input killed 49 B0 and xhigh inputs. All were re-run under a 2-3 h limit; no final score includes a timeout. The final xhigh score is 41.1% (39.9% before the re-runs).
- **Infrastructure (DECISIONS 28, 35, 39).** 6 VM restarts and some dropped network calls; all runs resumed, only in-flight work redone, no result lost. Streaming changed only the transport. Since DECISIONS 35, a call still refused by the provider's safety filter after two retries counts as the caller's failed call, not an infrastructure retry.
- **Timing (DECISIONS 22, 31).** Some steps started before earlier ones finished (e.g. pay-off runs began before the pilot exams were scored). No result from one step chose anything in another.
- **Small samples and noise.** 6, 5, 4 and 4 runs per group. One fixed coach varied by about 10 points across re-runs.

## Cost

| role | spend (USD) |
|---|---|
| player (task) | $148.03 |
| coach (meta) | $4.19 |
| probe | $0.00 |
| **total** | **$152.23** |

The original hard stop was $150 (DESIGN.md). The user raised it to $200 before the extension. Players are cheap per call but make many calls; coaches used about 350k tokens per round in the original-coach runs and about 188k in the evolved-coach runs.

## Where to find things

- `RESULTS.md`: all numbers, with the analysis output.
- `DESIGN.md` (pre-registered, commit f577cc7) and `DESIGN_v2.md` (extension plan).
- `DECISIONS.md`: every deviation, bug and rerun, numbered.
- `exp/results/analysis.json`, `exp/results/ext_analysis.json`: computed estimates.
- `exp/results/final_runs.jsonl`: exam score per run.
- `exp/results/diff_audit.json`: hunk-by-hunk audit with judges' reasons.
- `exp/results/pick_rule_comparison_g12.json`, `exp/results/ig_selection.json`, `exp/results/ext_picks.json`: which coach was picked and why.
- `exp/results/extension_plot.png`: the extension figure.

## Appendix: every experiment, fact and design choice in one list

### Design (fixed before results)
- **Question:** given equal compute for the pay-off, does a coach (meta agent) that evolved itself build a better player (task agent) than the original coach?
- **Pre-registration:** DESIGN.md, splits.json and analysis.py committed at `f577cc7` before any pay-off result existed. Extension plan DESIGN_v2.md committed at `991a237` before any extension test run.
- **Model:** gpt-6-luna through the OpenAI Responses API for both roles.
  - Player effort: high.
  - Coach effort: high (the user changed this from max).
  - One extra A_0 pass at xhigh.
- **Player budget:** at most 2 model calls and 2 answers per test input. A test input counts as solved if either answer matches the true grid exactly.
- **Coach budget:** 600k tokens per coaching round.
- **Spending cap:** $150 hard stop, raised by the user to $200 before the extension.
- **Prices:**
  - Input: $0.10 per million tokens.
  - Cached input: $0.01 per million tokens.
  - Output: $0.50 per million tokens. Reasoning tokens are billed as output.
- **Enforcement (`arcexp/gateway.py`):** the gateway is the only route to the API and no agent can edit it.
  - It enforces the caps.
  - It keeps a ledger by role.
  - It refuses every call once the spending cap is reached.
- **Sandbox:** every test input runs as an unprivileged user with no network, in a fresh temporary directory, and cannot see the answers.
  - An isolation check ran before every phase and passed every time, including the final one.
- **Time limit per test input:** 3 h for every arm, applied in the end and never reached. An early 30-minute limit was replaced and the inputs it cut off were re-run.
- **Splits (seed 20261117, ARC-AGI-2 commit f3283f7):**
  - **Held-out exam:** all 120 public evaluation tasks (167 test inputs). No coach ever saw them.
  - **Screen:** 100 training tasks, each given 3 single A_0 calls.
  - **Practice sets:** the source set (for evolving) and the pay-off set (for testing coaches), 25 tasks each and disjoint. They were drawn from screen tasks solved once or twice. All 38 such tasks were used, plus 6 always-solved and 6 never-solved filler tasks.
- **Scoring:** the exam score is averaged over the 120 tasks. A task with several test inputs gives partial credit.
- **Final player of a run:**
  - Re-score the two best players on the pay-off set, counting any valid node, including the unedited A_0.
  - Keep the one with the higher mean of loop score and re-score.
  - Give that player the exam exactly once.
- **Pick rule for the evolved coach (I_g):** consider agents whose coach code differs from I_0 (compared as parsed ASTs) and that had at least one scored child. Pick the one whose children improved most on average. Ties go to the earlier generation.
- **Pick rule in the extension:** the same, but a candidate also needs at least 3 descendants. Fallback: the changed coach with the most descendants.
- **Freeze mode:** in pay-off and test runs the coach's code is locked. Only the player changes.
- **Statistics:** 95% Welch t-intervals on per-run exam scores. The headline is the first matching row of a pre-written list.

### Experiments run, in order
1. **Smoke test.** 10 tasks end to end plus one coaching round. Used to measure prices: $0.0028 per player call and $0.007 per coaching round. These gave the "Full" design: 6 source seeds, 12 generations, 6 I_0 runs, 8 rounds per pay-off run.
2. **Screen.** 100 training tasks × 3 single calls, used to build the practice sets.
3. **B0: the plain player A_0, two attempts, on the exam, 3 times.** 30.1%, 27.9%, 29.7%; mean 29.3%, SD 1.2 points. The gate (15–50%) passed.
4. **xhigh check: A_0 at xhigh effort, one exam pass.** 41.1%. It was 39.9% before re-running inputs that had hit the old 30-minute limit.
5. **Pilot: the first two original-coach (I_0) pay-off runs, 8 rounds each, then the exam.** 26.9% and 29.4%. The gate passed.
   - A harness bug crashed the first attempt before any coach ran. Both runs restarted with new seeds (DECISIONS 23).
6. **Source runs: 6 seeds (s1–s6), coach and player both evolve for 12 generations on the source set.**
   - Coach code was changed in 21 of the 72 generations (29%).
   - Changed-coach generations per seed: s1 1, s2 4, s3 5, s4 1, s5 7, s6 3.
7. **I_g selection.** 5 of 6 seeds had a qualifying evolved coach:
   - s1: generation 1
   - s2: generation 5
   - s3: generation 3
   - s5: generation 6
   - s6: generation 4

   Seed s4 had none. Its only coach edit had no scored child.
8. **Transplant check.** Each I_g ran one trial round starting from A_0. All passed.
9. **Pay-off runs (frozen coach, 8 rounds from A_0 on the pay-off set, then one exam).**
   - The remaining four I_0 runs scored 30.4, 30.4, 31.4 and 29.4%. With the pilot, the six I_0 runs average 29.7%.
   - The five I_g runs scored 26.0% (s1), 27.4% (s2), 31.0% (s3), 27.2% (s5) and 27.9% (s6), averaging 27.9%.
   - payoff_I0_2 was restarted once more after a sanitizer bug dropped a coach edit (DECISIONS 24).
10. **Pre-registered analysis.**
    - G (I_0 minus B0) = +0.4 points [−1.9, +2.8].
    - Delta (I_g minus I_0) = −1.8 points [−4.2, +0.6].
    - I_g minus B0 = −1.4 points [−4.0, +1.3].
    - Headline (row 2): **"Neither improver beat two plain attempts on ARC-AGI-2."**
11. **Extension: evolution continued.** Seeds 0–3 (= source_s1–s4) were run on to 40 generations.
12. **Extension picks.** Coaches were picked at generations 6, 20, 30 and 40. Those at 6 and 30 were stored and transplant-checked but not tested.

    | seed | gen 20 pick | gen 40 pick |
    |---|---|---|
    | 0 (s1) | node 1 | node 1 |
    | 1 (s2) | node 9 | node 5 |
    | 2 (s3) | node 9 | node 9 |
    | 3 (s4) | node 12 | node 13 |

    Several picks are the same coach node as an earlier pick. For example, seed 0's node 1 is also its generation-12 I_g (DECISIONS 37).
13. **Extension test runs (8 runs, same rules as the pay-off runs).**

    | seed | gen 20 | gen 40 |
    |---|---|---|
    | 0 | 27.8% | 36.0% |
    | 1 | 31.5% | 31.5% |
    | 2 | 31.8% | 24.9% |
    | 3 | 27.9% | 28.9% |

    In seed 3's generation-20 run, the final player was the unedited A_0, because it beat every edited player on the practice set.
14. **Extension analysis.**
    - Means at generations 0 / 12 / 20 / 40: 29.7 / 27.9 / 29.8 / 30.3%.
    - Generation 40 minus generation 0 = +0.6 points [−6.5, +7.8]: flat within the interval.
    - Paired change from generation 12 to 20: mean +2.3 points. From 20 to 40: mean +0.6 points.
    - The same coach code (seed 0, node 1) scored 26.0%, 27.8% and 36.0% across three runs.
15. **Pick-rule comparison at generation 12.** The extension rule and the committed rule agree for seeds 0–2. For seed 3 the committed rule picks no coach and the extension rule picks node 6.
16. **Diff audit of every picked coach.** 32 changed hunks: 3 ARC-specific and 29 general. Two judges agreed on every hunk.

### Facts worth remembering
- **Spend:** $152.23 in total: players $148.03, coaches $4.19.
- **Coach tokens per round:** about 350k for I_0 and 188k for I_g.
- **Player tokens per practice-task evaluation:** about 27.0k under I_0 and 23.5k under I_g.
- **Noise:** run-to-run SD was 1.2 points for B0, 1.5 for I_0 and 1.9 for I_g. One fixed coach varied by about 10 points across re-runs.
- **The biggest lever was reasoning effort, not coaching:** xhigh gave +11.8 points over B0. No coach could change effort; it was fixed in the gateway.
- **The original coach needed two small adaptations to work at all (DECISIONS 14–15):**
  - An instruction to work autonomously.
  - Looser tool-call parsing.

  Even then, it ended 11 of its first 31 rounds without an edit.
- **Run conditions:**
  - 6 VM restarts.
  - All runs resumed from logs, and no result was lost.
  - Timeouts in final scores: 0 in every arm.
- **Where it is all recorded:** every deviation is in DECISIONS.md (items 1–40), and every coach's code is in `exp/archive_export/`.
