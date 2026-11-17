# DESIGN (pre-registered)

Committed before any pay-off result exists. The commit hash is recorded in STATUS.md.
Deviations from the original prompt are listed in DECISIONS.md.

## Question
Given equal pay-off compute, does a meta agent that evolved itself improve a fresh task agent more than
the original meta agent does?
- A_0: starting task agent (`agent_template/task_agent.py`). I_0: original meta agent (`agent_template/`, with the
  adaptations in DECISIONS.md 14-15). I_g: an evolved meta agent.
- B0: A_0's held-out score with the standard budget (2 model calls and 2 answers per test input).
- G: mean held-out score of agents built by I_0, minus B0.
- Delta: mean held-out score of agents built by evolved meta agents, minus the mean for I_0.

## Models and budget
gpt-6-luna in both roles via the Responses API. Task agent: effort high. Meta agent: effort **high**
(user request; the prompt said max). Fixed in `arcexp/gateway.py`, which no agent can edit.
Caps: 2 task-agent calls and 2 answers per test input; 600k tokens per meta iteration in every run;
every call refused once total spend reaches $150. Prices: $0.10/M input, $0.01/M cached input,
$0.50/M output (reasoning bills as output).

## Chosen design: **Full**
Rule: projected cost = task calls x call price + meta iterations x iteration price, with prices measured in the
smoke test ($0.0028 per task call, $0.007 per meta iteration): Full = 13,820 x 0.0028 + 174 x 0.007 = $40 <= $135, so
**Full**: 6 source seeds, g = 12 generations, 6 runs with I_0, k = 8 iterations, 25 tasks per set, B0 scored 3 times.
Conservative re-projection with prices measured during the checks: held-out calls cost $0.0075, and ARC-AGI-2 has
167 held-out test inputs (334 calls per pass, not 240). That gives about 5,350 held-out calls ($40), about 8,500
training-set calls at <= $0.005 ($43), and 174 meta iterations at a worst case of about $0.30 each ($52): <= $135.
The gateway's $150 hard stop applies regardless.

## Data splits (splits.json, seed 20261117)
- Held-out: all 120 public evaluation tasks of ARC-AGI-2 (commit f3283f7); 167 test inputs. No meta agent sees them.
- Screen: 100 training tasks, 3 single A_0 calls each. A task counts as solved by a call iff that call solves
  all its test inputs. Source and pay-off sets (25 each, disjoint) are drawn from tasks solved once or twice.
  If too few qualify, both sets are filled with equal numbers of always-solved and never-solved tasks,
  split evenly between the two sets.

## Procedure
1. Smoke test: 10 tasks end to end plus one meta-agent iteration (done; prices above).
2. Design: Full (above).
3. Checks: B0 on held-out 3 times; one A_0 pass at xhigh; the training-task screen.
   Gate: continue only if 15% <= B0 <= 50%.
4. Commit DESIGN.md, splits.json, analysis.py; record the hash in STATUS.md.
5. Sanity pilot: 2 pay-off runs with I_0 (they count as the first two I_0 runs), scored on held-out.
   Gate: stop only if no candidate was ever accepted or both final agents score below B0.
6. Source runs: the repo's loop (`generate_loop.py`, parent selection score_child_prop, staged eval skipped)
   for 12 generations on the source set, one run per seed (6 seeds), all from the same original agent.
   - I_g for a seed: among agents whose meta code (the files the improvement step loads, excluding task-agent
     and domain code; compared as parsed ASTs, ignoring comments and whitespace) differs from I_0 and that
     produced at least one child with a score, take the one whose scored children improved most over it on
     average (ties: earlier generation). Record its generation, child count, and the meta edits in its ancestry.
   - A seed with no such agent gets no pay-off run (recorded).
7. Transplant check: each I_g runs one trial iteration from A_0. A failure on a missing file leads to a fixed,
   logged transplant boundary.
8. Pay-off runs, freeze mode on: one run of k = 8 iterations per qualifying seed with its I_g, plus the remaining
   4 I_0 runs, all from A_0 on the pay-off set.
9. Final scoring: in each run, re-score the two candidates with the best pay-off-set scores (any evaluated valid
   node, including the initial A_0) on that set. Take the higher mean of (loop score, re-score), then score that
   agent once on the 120 held-out tasks.
A crashed run is rerun with a new seed and listed.

## Analysis (analysis.py)
- G and Delta with 95% Welch t-intervals on per-run held-out scores (unit: seed for the evolved arm, run for the
  I_0 arm). G compares I_0 runs against the 3 B0 repetitions.
- Each arm's mean gain over B0 with its interval; self-edit rate (source generations whose diff touches
  meta-agent code, and how many of those became parents); tokens per task and per iteration by arm;
  run-to-run standard deviation.
- Headline, first row that applies:
  1. Fewer than half the seeds gave a qualifying I_g: "Hyperagents rarely put a rewritten improver to use: N of S runs".
  2. Neither arm's gain over B0 has an interval above 0: "Neither improver beat two plain attempts on ARC-AGI-2".
  3. Delta interval entirely above 0: "An evolved improver improves better".
  4. Delta interval entirely below 0: "Evolving made the improver worse".
  5. Otherwise: "The original improver gained G; evolving it changed that by between L and U points".
- Results are stated plainly. A difference inside its interval is not described as an effect. No runs are
  added after seeing results.
