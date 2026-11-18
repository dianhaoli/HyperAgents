# Page text: Coaching the Coach

Edit the text under each `[[ID]]` line. Do not change or remove the `[[ID]]` lines.

Rules for the writer:
- `{{...}}` are numbers read from the data. Keep each one exactly as written; you may move it within its block.
- `[^N]` marks where footnote N attaches; footnote text is in its own `[[fn-N]]` block.
- Formatting: **bold**, *italic*, `code`, [text](link). `[n](#ref-x "cite")` is a citation: keep it.
- Raw HTML tags, if any, must stay balanced. Keep blocks to one paragraph (no blank lines inside a block).
- Part 2 strings live in code; some are joined to numbers, so keep their leading/trailing spaces and the
  sense of the fragment. Delete nothing; to drop a sentence, leave its block empty only if it is a whole sentence.

---

## Part 1: page prose (index.html)


### Top

[[top.h11]]  <!-- h1 -->
Can an AI coach teach itself to coach better?

[[top.p1]]  <!-- p -->
An AI **coach** rewrites the code of a puzzle-solving AI, the **player**, to make it better. We let the coach rewrite *itself* too, then tested whether the self-improved coach trains better players.

[[top.p2]]  <!-- p -->
It does not. On an exam of {{int:sets.heldout_tasks}} unseen puzzles, coached players scored about the same as an uncoached one. Letting the model simply think longer beat all coaching.

[[top.p3]]  <!-- p -->
Average exam score: share of the {{int:sets.heldout_tasks}} exam puzzles solved.

[[top.p4]]  <!-- p -->
Model: gpt-6-luna. Every player gets at most 2 model calls and 2 answers per puzzle. Total cost {{usd:spend.total}}. November 2026.

[[top.p5]]  <!-- p -->
Jump to: [The result](#results) · [Watch them answer](#watch) · [Inside one coaching round](#demo) · [Explore the data](#explore)


### 1. The setup

[[1-the-setup.h21]]  <!-- h2 -->
The setup

[[1-the-setup.p1]]  <!-- p -->
The player is a short program that solves a puzzle with at most two model calls.[^1] The coach looks at how the player did on {{int:sets.source_practice_tasks}} practice puzzles and edits the player's code. One such round is a **generation**. In step 1, the coach may also edit its own code, so it can get better at coaching.

[[1-the-setup.title1]]  <!-- title -->
A coach edits the player's code. Then we let the coach edit its own.

[[1-the-setup.p2]]  <!-- p -->
Step 1: the coach improves itself over many generations. Step 2: we freeze it and test it on a fresh player.

[[1-the-setup.figcaption1]]  <!-- figcaption -->
**Figure 1**: how the experiment works.

[[1-the-setup.p3]]  <!-- p -->
We ran step 1 {{int:n_source_seeds}} times for {{int:derived.sourceGens}} generations each. To test a coach, we froze it (either the original coach or the self-improved one from each run[^2]) and gave it a fresh, untouched player and {{int:derived.rounds}} rounds on another {{int:sets.payoff_practice_tasks}} practice puzzles. The finished player then sat the exam once: {{int:sets.heldout_tasks}} puzzles it had never seen.[^3]

[[1-the-setup.p4]]  <!-- p -->
For comparison, the uncoached player also sat the exam as it was, and once with the model set to **think longer** (reasoning effort one step higher), still with two calls and two answers per puzzle. No coach could change that setting.[^4]


### 2. Puzzles

[[2-puzzles.h21]]  <!-- h2 -->
What the puzzles look like

[[2-puzzles.p1]]  <!-- p -->
Each puzzle shows a few input→output examples. You find the rule and paint the output for a new input, cell for cell. Try one.

[[2-puzzles.title1]]  <!-- title -->
Find the rule from the examples, then paint the answer.

[[2-puzzles.p2]]  <!-- p -->
Pick a colour, click cells to paint, then press Check. You get two tries, like the player.

[[2-puzzles.figcaption1]]  <!-- figcaption -->
**Figure 2**: an exam puzzle from ARC-AGI-2 [[1]](#ref-arc "cite").


### 3. Result

[[3-result.h21]]  <!-- h2 -->
The result

[[3-result.p1]]  <!-- p -->
Players trained by the original coach scored {{pts:G.est}} points above the uncoached player, and players trained by a self-improved coach {{pts:Ig_gain_over_B0.est}} points. Both differences are smaller than the noise between runs.[^5] Thinking longer added about {{pp0:derived.xhighGain}} points.

[[3-result.title1]]  <!-- title -->
Coached players scored the same as an uncoached one. Thinking longer scored much higher.

[[3-result.p2]]  <!-- p -->
Each dot is one finished player's exam score; the bar marks the average. Hover or tap a dot.

[[3-result.figcaption1]]  <!-- figcaption -->
**Figure 3**: exam scores of every finished player. Think longer was run once.


### 4. Generations

[[4-generations.h21]]  <!-- h2 -->
Did more generations help?

[[4-generations.p1]]  <!-- p -->
Coaches rarely changed themselves. Their own code changed in only {{int:derived.selfEditGens}} of {{int:derived.totalGens}} generations. In a follow-up that was not pre-registered [[4]](#ref-design2 "cite"), {{int:extension.per_generation.40.n}} runs continued to generation {{int:derived.extMaxGen}}, and we tested coaches picked at generations 20 and 40 too. Later picks were often the very same code: in run 1, the coach picked at generations 12, 20 and 40 was one version, made at generation 1.

[[4-generations.p2]]  <!-- p -->
Its three tests scored {{pct:derived.sameCoach.g12}}, {{pct:derived.sameCoach.g20}} and {{pct:derived.sameCoach.g40}}. That spread is pure noise, and it is larger than any difference between generations.

[[4-generations.title1]]  <!-- title -->
Coaches from later generations were no better.

[[4-generations.p3]]  <!-- p -->
Each dot is one finished player; the line joins the averages. The button rings one coach that was tested three times.

[[4-generations.figcaption1]]  <!-- figcaption -->
**Figure 4**: exam score by the generation the coach was picked at. Generation 40 minus generation 0: {{pts:extension.gen40_minus_gen0.est}} points, 95% interval {{ci:extension.gen40_minus_gen0}}. Generations 20 and 40 are the follow-up [[4]](#ref-design2 "cite").


### 5. Watch

[[5-watch.h21]]  <!-- h2 -->
Watch them answer

[[5-watch.p1]]  <!-- p -->
Here are real exam answers, side by side. Some misses are a single cell off; others are far from the answer.

[[5-watch.title1]]  <!-- title -->
Same puzzle, four kinds of player: some misses are one cell off, others far off.

[[5-watch.p2]]  <!-- p -->
The correct answer first, then each player's two tries. Press Next for another puzzle.

[[5-watch.figcaption1]]  <!-- figcaption -->
**Figure 5**: one run of each kind, answering the puzzle's first test input; "solved by k of n" counts every run of that kind. Shown: puzzles where the four disagree, those only the think-longer player solved first.


### 6. Inside one round (demo)

[[6-inside-one-round-demo.h21]]  <!-- h2 -->
Inside one coaching round

[[6-inside-one-round-demo.p1]]  <!-- p -->
The study did not record what the model was thinking. So we re-ran one coaching round with the model's reasoning summaries saved, and you can follow what the player and the coach were thinking, step by step. This is a separate illustrative run, not part of the results. These are not the model's raw thoughts: the API returns a summary of the hidden reasoning, which can run to thousands of words and can be lossy or garbled, and only some calls returned one.[^6]

[[6-inside-one-round-demo.title1]]  <!-- title -->
The coach turned the player's second try into a self-check. In repeat runs, one puzzle was solved more often and the other never.

[[6-inside-one-round-demo.p2]]  <!-- p -->
Pick a puzzle, then step through: the player tries, the coach reads and edits, the player tries again.

[[6-inside-one-round-demo.figcaption1]]  <!-- figcaption -->
**Figure 6**: a traced re-run of one coaching round on the practice puzzles, made after the study. “Reasoning summary” is the summary of the model's hidden reasoning that the API returned; commands and outputs are as the coach saw them, with long outputs shortened. Not part of the results.


### 7. Takeaways

[[7-takeaways.h21]]  <!-- h2 -->
What to take away

[[7-takeaways.li1]]  <!-- li -->
No coach, original or self-improved, trained a player that beat the uncoached one on this exam.

[[7-takeaways.li2]]  <!-- li -->
Letting the model think longer was worth about {{pp0:derived.xhighGain}} points; no coaching came close.

[[7-takeaways.li3]]  <!-- li -->
Coaches seldom rewrote themselves, and testing one unchanged coach three times moved its score by {{pp0:derived.sameCoachSpread}} points, so small differences here are noise.

[[7-takeaways.li4]]  <!-- li -->
Up close, a coach's edit can be sensible and still help only some puzzles: in the traced round, the player with a self-check on its second try solved one puzzle more often and another one never. That is one round, so it illustrates how coaching works; it is not evidence about how well it works.

[[7-takeaways.p1]]  <!-- p -->
Below, you can browse every run, every exam answer and every change a coach made to itself ([Code changes](#audit)). The caveats, costs and full method are under [Numbers & method](#numbers).


### 7. Explore

[[7-explore.h21]]  <!-- h2 -->
Explore the data

[[7-explore.p1]]  <!-- p -->
Everything behind Figures 1 to 5. Pick a tab.

[[7-explore.p2]]  <!-- p -->
How practice score changed, version by version. Pick a dot to follow its coach and see what changed.

[[7-explore.figcaption1]]  <!-- figcaption -->
Practice score: share of the 25 practice puzzles solved. A tested coach was frozen and used to train a fresh player for 8 rounds; that player then sat the exam.

[[7-explore.p3]]  <!-- p -->
All 120 exam puzzles. Pick one to see each run's two answers next to the correct one.

[[7-explore.figcaption2]]  <!-- figcaption -->
Answer grids were kept for 17 of the 23 exam runs; for the other six (follow-up runs 2 to 4) only right or wrong was kept.

[[7-explore.p4]]  <!-- p -->
What the player and the coach actually wrote.

[[7-explore.figcaption3]]  <!-- figcaption -->
Player transcripts were saved only for failed practice answers. Long prompts are shortened. The model's hidden reasoning was never recorded.

[[7-explore.p5]]  <!-- p -->
Every change the tested coaches made to their own code, and whether it was general or specific to these puzzles.

[[7-explore.figcaption4]]  <!-- figcaption -->
Each picked coach compared with the original coach; each change was judged by two judges.

[[7-explore.p6]]  <!-- p -->
The statistics, the cost, the caveats and the method.

[[7-explore.figcaption5]]  <!-- figcaption -->
Exam score of every finished player, also against the tokens it used, and the pre-registered comparisons as 95% intervals against zero.

[[7-explore.h31]]  <!-- h3 -->
Cost

[[7-explore.p7]]  <!-- p -->
The study cost {{usd:spend.total}} in model calls: players {{usd:spend.by_role.task}}, coaches {{usd:spend.by_role.meta}}. A coach used about {{tokens:derived.metaTokI0}} tokens per round (original coach) or {{tokens:derived.metaTokIg}} (self-improved coaches).

[[7-explore.th1]]  <!-- th -->
Phase

[[7-explore.th2]]  <!-- th -->
Player

[[7-explore.th3]]  <!-- th -->
Coach

[[7-explore.td1]]  <!-- td -->
Exams, all coached players

[[7-explore.td2]]  <!-- td -->
$80.86

[[7-explore.td3]]  <!-- td -->
Step 1: self-improvement runs

[[7-explore.td4]]  <!-- td -->
$23.03

[[7-explore.td5]]  <!-- td -->
$2.25

[[7-explore.td6]]  <!-- td -->
Step 2: test runs (8 rounds each)

[[7-explore.td7]]  <!-- td -->
$12.02

[[7-explore.td8]]  <!-- td -->
$1.17

[[7-explore.td9]]  <!-- td -->
No coach, 3 exams

[[7-explore.td10]]  <!-- td -->
$8.76

[[7-explore.td11]]  <!-- td -->
Re-scoring finalists

[[7-explore.td12]]  <!-- td -->
$7.72

[[7-explore.td13]]  <!-- td -->
Follow-up test runs

[[7-explore.td14]]  <!-- td -->
$6.95

[[7-explore.td15]]  <!-- td -->
$0.69

[[7-explore.td16]]  <!-- td -->
Think longer, 1 exam

[[7-explore.td17]]  <!-- td -->
$5.75

[[7-explore.td18]]  <!-- td -->
Scoring the starting player

[[7-explore.td19]]  <!-- td -->
$1.32

[[7-explore.td20]]  <!-- td -->
Transplant checks

[[7-explore.td21]]  <!-- td -->
$0.81

[[7-explore.td22]]  <!-- td -->
$0.04

[[7-explore.td23]]  <!-- td -->
Screening puzzles

[[7-explore.td24]]  <!-- td -->
$0.71

[[7-explore.td25]]  <!-- td -->
Smoke test

[[7-explore.td26]]  <!-- td -->
$0.08

[[7-explore.td27]]  <!-- td -->
$0.03

[[7-explore.td28]]  <!-- td -->
Total

[[7-explore.td29]]  <!-- td -->
$148.03

[[7-explore.td30]]  <!-- td -->
$4.19

[[7-explore.caption1]]  <!-- caption -->
Spend by phase from the gateway ledger. Phases under one cent are left out of the rows but counted in the totals.

[[7-explore.h32]]  <!-- h3 -->
Caveats

[[7-explore.li1]]  <!-- li -->
**Noise.** There were only 3 to 6 runs per group. One unchanged coach scored {{pct:derived.sameCoach.g12}}, {{pct:derived.sameCoach.g20}} and {{pct:derived.sameCoach.g40}} in three tests, and several later picks were the same code as earlier ones.

[[7-explore.li2]]  <!-- li -->
**The original coach needed adapting.** With the repository's instruction as written, the model only asked clarifying questions. We added one sentence ("work autonomously") and loosened tool-call parsing. Both kinds of coach started from this adapted version.

[[7-explore.li3]]  <!-- li -->
**The original coach often made no edit.** It ended 11 of its first 31 rounds without one, mostly from tool-call format problems. This was left as it was, as pre-registered.

[[7-explore.li4]]  <!-- li -->
**Some coach edits broke the player.** One edit passed an argument the function did not accept, and that player scored 0. Such results count.

[[7-explore.li5]]  <!-- li -->
**Re-runs.** Harness bugs forced restarts of two original-coach test runs (one of them twice) and cost one self-improvement run a generation. An early 30-minute limit cut off 49 exam answers for the no-coach and think-longer players; all were re-run under a 2 to 3 hour limit (think longer: 39.9% before, {{pct:xhigh.score}} after). Six machine restarts lost no result.

[[7-explore.li6]]  <!-- li -->
**An untouched final player.** In one follow-up test (generation-20 coach, run 4), the untouched starting player beat the best edited finalist on practice ({{num2:derived.untouchedWin.untouched}} vs {{num2:derived.untouchedWin.edited}}), so that exam score is the untouched player's own.

[[7-explore.li7]]  <!-- li -->
**Transcripts are partial.** They were saved only for failed practice answers (1,513 of them) and contain no hidden reasoning.

[[7-explore.p8]]  <!-- p -->
Every deviation, bug and re-run is logged in `DECISIONS.md` [[5]](#ref-decisions "cite").

[[7-explore.h33]]  <!-- h3 -->
Method in full

[[7-explore.summary1]]  <!-- summary -->
Design, fixed before the results

[[7-explore.li8]]  <!-- li -->
**Question.** With equal compute, does a coach that evolved itself train a better player than the original coach?

[[7-explore.li9]]  <!-- li -->
**Pre-registration.** `DESIGN.md`, `splits.json` and `analysis.py` were committed at `f577cc7` before any test result existed; the follow-up plan, `DESIGN_v2.md`, at `991a237` before any follow-up test.

[[7-explore.li10]]  <!-- li -->
**Model.** gpt-6-luna through the OpenAI Responses API, for player and coach. Reasoning effort high for both; the think-longer exam used xhigh.

[[7-explore.li11]]  <!-- li -->
**Player budget.** At most 2 model calls and 2 answers per test input. A test input counts as solved if either answer matches exactly.

[[7-explore.li12]]  <!-- li -->
**Coach budget.** 600k tokens per coaching round.

[[7-explore.li13]]  <!-- li -->
**Spending cap.** $150, raised to $200 before the follow-up. Prices: input $0.10, cached input $0.01, output $0.50 per million tokens.

[[7-explore.li14]]  <!-- li -->
**Enforcement.** A gateway (`arcexp/gateway.py`) that no agent can edit is the only route to the model. It enforces the caps and keeps a ledger.

[[7-explore.li15]]  <!-- li -->
**Sandbox.** Every test input runs as an unprivileged user with no network, in a fresh directory, without access to the answers.

[[7-explore.li16]]  <!-- li -->
**Puzzle sets.** ARC-AGI-2 commit `f3283f7`, seed 20261117. The exam is all 120 public evaluation tasks (167 test inputs). The two practice sets have 25 training tasks each and do not overlap.

[[7-explore.li17]]  <!-- li -->
**Score.** Share of test inputs solved within each task, averaged over the 120 tasks (task-averaged pass@2).

[[7-explore.li18]]  <!-- li -->
**Final player of a run.** The two best players are re-scored on practice, the untouched starting player included; the better one sits the exam exactly once.

[[7-explore.li19]]  <!-- li -->
**Picking a self-improved coach.** Among coaches whose code differs from the original and that have at least one scored child, take the one whose children improved most on average; ties go to the earlier generation.

[[7-explore.li20]]  <!-- li -->
**Statistics.** 95% Welch t-intervals on per-run exam scores. The headline is the first matching row of a pre-written list.

[[7-explore.summary2]]  <!-- summary -->
What was run, in order

[[7-explore.li21]]  <!-- li -->
**No coach.** The starting player sat the exam 3 times: {{pct:B0.reps.0}}, {{pct:B0.reps.1}}, {{pct:B0.reps.2}} (average {{pct:B0.mean}}).

[[7-explore.li22]]  <!-- li -->
**Think longer.** The starting player at xhigh effort, one exam: {{pct:xhigh.score}}.

[[7-explore.li23]]  <!-- li -->
**Step 1.** 6 self-improvement runs of 12 generations. The coach's own code changed in {{int:derived.selfEditGens}} of {{int:derived.totalGens}} generations (runs 1 to 6: 1, 4, 5, 1, 7, 3). Run 4 produced no qualifying coach, so 5 self-improved coaches were tested.

[[7-explore.li24]]  <!-- li -->
**Step 2.** Original coach, 6 test runs: {{pct:I0_runs.payoff_I0_1}}, {{pct:I0_runs.payoff_I0_2}}, {{pct:I0_runs.payoff_I0_3}}, {{pct:I0_runs.payoff_I0_4}}, {{pct:I0_runs.payoff_I0_5}}, {{pct:I0_runs.payoff_I0_6}} (average {{pct:I0_mean}}). Self-improved coaches from runs 1, 2, 3, 5, 6: {{pct:Ig_runs.payoff_Ig_source_s1}}, {{pct:Ig_runs.payoff_Ig_source_s2}}, {{pct:Ig_runs.payoff_Ig_source_s3}}, {{pct:Ig_runs.payoff_Ig_source_s5}}, {{pct:Ig_runs.payoff_Ig_source_s6}} (average {{pct:Ig_mean}}).

[[7-explore.li25]]  <!-- li -->
**Pre-registered analysis.** Original minus no coach {{pts:G.est}} {{ci:G}}; self-improved minus original {{pts:Delta.est}} {{ci:Delta}}. Headline: "{{raw:headline}}."

[[7-explore.li26]]  <!-- li -->
**Follow-up.** Runs 1 to 4 continued to 40 generations; coaches picked at generations 20 and 40 were tested under the same rules. Averages at generations 0, 12, 20, 40: {{pct:extension.per_generation.0.mean}}, {{pct:extension.per_generation.12.mean}}, {{pct:extension.per_generation.20.mean}}, {{pct:extension.per_generation.40.mean}}.

[[7-explore.li27]]  <!-- li -->
**Code audit.** {{int:diff_audit_summary.hunks}} changed blocks in the picked coaches: {{int:diff_audit_summary.arc_specific}} specific to these puzzles, {{int:diff_audit_summary.general}} general.

[[7-explore.p9]]  <!-- p -->
Every number on this page is read from `explorer/data/*.json`, built from the experiment's records by `arcexp/build_explorer_data.py`. The full write-up is `WRITEUP.md`.


### References

[[references.h21]]  <!-- h2 -->
References

[[references.li1]]  <!-- li -->
ARC Prize Foundation. *ARC-AGI-2*, public evaluation set, commit `f3283f7`. [github.com/arcprize/ARC-AGI-2](https://github.com/arcprize/ARC-AGI-2)

[[references.li2]]  <!-- li -->
`DESIGN.md`, the pre-registered design, committed at `f577cc7` before any test result.

[[references.li3]]  <!-- li -->
B. L. Welch (1947). The generalization of "Student's" problem when several different population variances are involved. *Biometrika* 34(1–2), 28–35.

[[references.li4]]  <!-- li -->
`DESIGN_v2.md`, the follow-up plan, committed at `991a237` before any follow-up test.

[[references.li5]]  <!-- li -->
`DECISIONS.md`: every deviation, bug and re-run.


### Footnotes

[[fn-1]]
"Player" and "coach" are the repository's *task agent* and *meta agent*. Both use the same model.

[[fn-2]]
From each run we took the self-edited coach whose players improved most on practice. The rule was fixed before any exam result existed [[2]](#ref-design "cite").

[[fn-3]]
The 120 public ARC-AGI-2 evaluation tasks [[1]](#ref-arc "cite"), with {{int:sets.heldout_test_inputs}} test inputs. A puzzle with several test inputs gives partial credit.

[[fn-4]]
A gateway no agent could edit fixed the model, its reasoning effort (*high*; *xhigh* for the think-longer run), the call cap and the budget.

[[fn-5]]
95% intervals: original coach minus no coach {{ci:G}} points; self-improved minus no coach {{ci:Ig_gain_over_B0}}; self-improved minus original {{pts:Delta.est}} {{ci:Delta}}. All include zero. Welch t-intervals [[3]](#ref-welch "cite"); the headline was pre-registered [[2]](#ref-design "cite").

[[fn-6]]
Same model, reasoning effort, call cap and practice puzzles as in the study. One difference: the demo asked for “detailed” reasoning summaries, the study for “auto” (which returned none in a short test). We show the only round, of several tried, that changed the player without breaking it, and two puzzles picked to illustrate: one the edit fixed and one it did not. Runs are not deterministic, so each player was run on each puzzle several times.


---

## Part 2: text inside the figures (js/*.js)


### core.js

[[js:core.js:23:2]]
Self-improved coach

[[js:core.js:23:3]]
Think longer (no coach)

[[js:core.js:80:0]]
http://www.w3.org/2000/svg

[[js:core.js:116:0]]
(prefers-reduced-motion: reduce)

[[js:core.js:193:1]]
Think longer, no coach

[[js:core.js:194:1]]
Self-improved coach

[[js:core.js:195:2]]
Self-improvement run

[[js:core.js:209:2]]
Self-improved coach

[[js:core.js:210:2]]
Think longer, no coach

[[js:core.js:210:3]]
Self-improvement run

[[js:core.js:224:0]]
No coach, run 

[[js:core.js:225:1]]
Think longer, no coach

[[js:core.js:226:0]]
Original coach, run 

[[js:core.js:227:0]]
Self-improved coach from run 

[[js:core.js:228:1]]
 coach from run 

[[js:core.js:229:0]]
Self-improvement run 

[[js:core.js:266:0]]
(prefers-color-scheme: dark)

[[js:core.js:277:0]]
(prefers-color-scheme: dark)

[[js:core.js:516:1]]
This figure could not be drawn. 

[[js:core.js:517:1]]
The text around it still holds; reloading the page may help. 


### fig-setup.js

[[js:fig-setup.js:43:0]]
trains a fresh player, 

[[js:fig-setup.js:46:0]]
Diagram. Step 1, the coach improves itself: the coach edits the player's code, the player plays 

[[js:fig-setup.js:47:0]]
, the scores go back to the coach, and the coach also rewrites itself; repeated for 

[[js:fig-setup.js:48:0]]
 generations. Step 2, we test it: the self-improved coach, or the original coach, is frozen and 

[[js:fig-setup.js:49:0]]
; that player sits the 

[[js:fig-setup.js:49:3]]
. For comparison, an uncoached player sat the same exam, both normally and thinking longer.

[[js:fig-setup.js:92:1]]
Step 1 · The coach improves itself

[[js:fig-setup.js:93:1]]
Step 2 · We test it

[[js:fig-setup.js:111:0]]
Self-improved coach

[[js:fig-setup.js:127:1]]
Step 1 · The coach improves itself

[[js:fig-setup.js:144:1]]
Step 2 · We test it

[[js:fig-setup.js:145:0]]
Self-improved coach

[[js:fig-setup.js:148:1]]
trains a fresh player,


### fig-puzzle.js

[[js:fig-puzzle.js:128:4]]
Copy test input

[[js:fig-puzzle.js:130:4]]
Show the answer

[[js:fig-puzzle.js:134:3]]
Keyboard: arrows move, Space paints, 0–9 pick a colour, F fills.

[[js:fig-puzzle.js:192:0]]
Test input (1 of 

[[js:fig-puzzle.js:216:3]]
. Arrow keys move, Space paints, digits 0 to 9 pick a colour, F fills an area.

[[js:fig-puzzle.js:332:1]]
 On your second try.

[[js:fig-puzzle.js:333:0]]
Here is the answer.

[[js:fig-puzzle.js:334:1]]
. That was your last try. Wrong cells are outlined in white below.

[[js:fig-puzzle.js:354:0]]
Loading how the AI players did…

[[js:fig-puzzle.js:357:0]]
How the AI players did could not be loaded.

[[js:fig-puzzle.js:359:4]]
See every run’s answer →


### fig-results.js

[[js:fig-results.js:21:2]]
assets/fig-results.css

[[js:fig-results.js:34:2]]
Self-improved coach

[[js:fig-results.js:35:1]]
Think longer (no coach)

[[js:fig-results.js:45:0]]
No coach, run 

[[js:fig-results.js:47:0]]
Original coach, run 

[[js:fig-results.js:48:0]]
Self-improved coach from 

[[js:fig-results.js:142:2]]
Self-improved coach

[[js:fig-results.js:142:3]]
Think longer, no coach

[[js:fig-results.js:146:1]]
Exam score of every finished player. 

[[js:fig-results.js:180:0]]
Exam score (share of 120 puzzles solved)

[[js:fig-results.js:180:1]]
Exam score: share of the 120 exam puzzles solved in two tries

[[js:fig-results.js:266:2]]
Self-improved coach

[[js:fig-results.js:267:2]]
Think longer, no coach

[[js:fig-results.js:325:3]]
No kind of coach differs detectably from no coach

[[js:fig-results.js:332:5]]
Exam score of every final player, grouped by arm

[[js:fig-results.js:444:3]]
 tokens per test input

[[js:fig-results.js:448:1]]
 tokens per test input

[[js:fig-results.js:449:1]]
 score per 10k tokens

[[js:fig-results.js:453:0]]
Hover over, focus or tap a dot to read its run. Click or press Enter to pin it.

[[js:fig-results.js:456:2]]
 tokens per test input

[[js:fig-results.js:549:0]]
Exam score against ledger tokens per test input, one mark per final player

[[js:fig-results.js:550:1]]
Exam score per 10k ledger tokens, one dot per final player, grouped by arm

[[js:fig-results.js:551:0]]
Exam score of every final player, grouped by arm, with arm means and 95% intervals

[[js:fig-results.js:578:1]]
exam score (share of 120 puzzles solved)

[[js:fig-results.js:578:3]]
exam score per 10k tokens

[[js:fig-results.js:586:1]]
no-coach range · mean 

[[js:fig-results.js:586:2]]
no-coach range · mean 

[[js:fig-results.js:597:0]]
no-coach range · mean 

[[js:fig-results.js:656:0]]
Tokens are the gateway ledger’s player tokens for the exam run, divided by its 167 test inputs. 

[[js:fig-results.js:657:1]]
Bars: arm mean and a 95% interval, for display only; the pre-registered comparisons are the Welch intervals 

[[js:fig-results.js:658:3]]
. Shaded band: the range of the three no-coach runs. Tied scores are nudged apart vertically.

[[js:fig-results.js:659:1]]
Each run’s exam score divided by its tokens per test input, per 10k tokens. 

[[js:fig-results.js:660:0]]
Bars: arm mean and 95% interval (display only); ◂ ▸ mark an interval that runs off the scale.

[[js:fig-results.js:661:0]]
y: exam score. Bars: each arm’s 95% interval for score, drawn at its mean token use (display only). Every player had the same two-call budget, so the arms sit in one cluster.

[[js:fig-results.js:669:3]]
The pre-registered comparisons

[[js:fig-results.js:670:3]]
Differences in exam score, in points, with 95% Welch intervals. An interval that crosses 0 cannot be told apart from no effect.

[[js:fig-results.js:672:2]]
Original coach vs no coach

[[js:fig-results.js:673:2]]
Self-improved vs original coach

[[js:fig-results.js:674:0]]
Ig_gain_over_B0

[[js:fig-results.js:674:2]]
Self-improved coach vs no coach

[[js:fig-results.js:690:3]]
Crosses 0: no detectable difference.


### fig-extension.js

[[js:fig-extension.js:15:2]]
assets/fig-extension.css

[[js:fig-extension.js:91:7]]
Highlight one coach tested three times

[[js:fig-extension.js:107:0]]
Hide the highlight

[[js:fig-extension.js:107:1]]
Highlight one coach tested three times

[[js:fig-extension.js:109:0]]
Highlighted: the same coach code, scored 

[[js:fig-extension.js:109:2]]
. The spread is noise.

[[js:fig-extension.js:118:1]]
Average exam score by the generation the coach was taken from: 

[[js:fig-extension.js:146:1]]
 (band: its 3 runs)

[[js:fig-extension.js:151:1]]
 (band: its 3 runs)

[[js:fig-extension.js:157:1]]
Think longer, no coach 

[[js:fig-extension.js:180:2]]
. This run's final player was the untouched starting player

[[js:fig-extension.js:200:1]]
Ringed: one unchanged coach,

[[js:fig-extension.js:201:2]]
tested 3 times. The spread is noise.

[[js:fig-extension.js:202:0]]
Ringed: one unchanged coach, tested 3 times. The spread is noise.

[[js:fig-extension.js:221:2]]
self-improved coach (main test)

[[js:fig-extension.js:233:0]]
Generation the coach was picked at

[[js:fig-extension.js:233:1]]
Picked at generation


### fig-watch.js

[[js:fig-watch.js:19:2]]
assets/fig-watch.css

[[js:fig-watch.js:26:1]]
Self-improved coach

[[js:fig-watch.js:26:2]]
payoff_Ig_source_s1

[[js:fig-watch.js:39:0]]
800px 0px 800px 0px

[[js:fig-watch.js:87:1]]
Exam puzzle and answers. Left and right arrow keys change the puzzle.

[[js:fig-watch.js:175:0]]
Counts every exam run of this kind on this test input

[[js:fig-watch.js:188:1]]
× same as try 1

[[js:fig-watch.js:202:0]]
Back to puzzle 1

[[js:fig-watch.js:230:4]]
Open this puzzle in Exam answers →

[[js:fig-watch.js:278:0]]
No puzzle matched the selection rule.


### fig-demo.js

[[js:fig-demo.js:15:2]]
assets/fig-demo.css

[[js:fig-demo.js:20:1]]
The player tries

[[js:fig-demo.js:21:1]]
The coach looks at the misses

[[js:fig-demo.js:22:1]]
The coach thinks and edits

[[js:fig-demo.js:23:1]]
The player tries again

[[js:fig-demo.js:24:1]]
Did it hold up?

[[js:fig-demo.js:27:1]]
Solved more often after the edit

[[js:fig-demo.js:28:1]]
Still wrong after the edit

[[js:fig-demo.js:33:0]]
Looks around the code

[[js:fig-demo.js:33:1]]
Reads the run log and the code

[[js:fig-demo.js:33:2]]
Reads how practice runs are scored

[[js:fig-demo.js:34:0]]
Opens the practice report

[[js:fig-demo.js:34:1]]
Skims the failure logs

[[js:fig-demo.js:34:2]]
Rewrites the prompt and the second try

[[js:fig-demo.js:35:0]]
Rewords the review instruction

[[js:fig-demo.js:35:1]]
Checks that the code still compiles

[[js:fig-demo.js:35:2]]
Describes its change

[[js:fig-demo.js:36:0]]
Says it is done

[[js:fig-demo.js:42:0]]
The summaries weigh several ideas, among them a path between the two red (2) cells and filling the regions that the blue (1) lines wall off. The correct answer is one yellow (4) path that winds between the blue lines from one red cell to the other. Try 1 came close to it; try 2 filled larger areas.

[[js:fig-demo.js:43:0]]
This time the summaries lean on filling regions and outer strips walled off by the blue (1) lines. The answer paints yellow (4) down the right edge and in blocks on the left instead of one path between the red (2) cells, and the review returned the same grid.

[[js:fig-demo.js:48:0]]
Right now, there are two direct calls repeating the same prompt, so I want to change that.

[[js:fig-demo.js:49:0]]
Instead, I should ask the model to critique the first candidate and validate it against training pairs.

[[js:fig-demo.js:111:3]]
Loading the traced run…

[[js:fig-demo.js:165:3]]
Its reasoning summary

[[js:fig-demo.js:167:3]]
No reasoning summary came back for this call (the API returns one for only some calls).

[[js:fig-demo.js:181:3]]
Reasoning summary, full text

[[js:fig-demo.js:187:2]]
code wrap fxd-code 

[[js:fig-demo.js:206:0]]
× same as try 1, so the player sent only one answer

[[js:fig-demo.js:206:1]]
× same as try 1

[[js:fig-demo.js:224:3]]
Our reading of its summaries and answers (not the model's words)

[[js:fig-demo.js:232:4]]
Colour key: the number behind each colour

[[js:fig-demo.js:269:0]]
, and only one answer was sent

[[js:fig-demo.js:275:4]]
: a review of try 1

[[js:fig-demo.js:287:3]]
No model calls were recorded for this run.

[[js:fig-demo.js:292:0]]
The player sees the examples and the test input, then gets two tries. Wrong cells are outlined.

[[js:fig-demo.js:303:0]]
Before editing, the coach gets the practice report: which puzzles the player solved and a log of each miss. Here is what it actually looked at.

[[js:fig-demo.js:305:3]]
The practice report: 

[[js:fig-demo.js:306:4]]
Practice puzzles, solved or missed

[[js:fig-demo.js:313:3]]
The outlined square is this puzzle.

[[js:fig-demo.js:320:3]]
What it looked at

[[js:fig-demo.js:321:0]]
Each of the 

[[js:fig-demo.js:321:1]]
 missed puzzles, this one included, has a log of the player's prompts and answers. 

[[js:fig-demo.js:324:0]]
The coach named 

[[js:fig-demo.js:325:0]]
 in one command (turn 

[[js:fig-demo.js:325:1]]
), but from each it printed only the lines that start with "Input:" or "Output:" or contain "Error:"

[[js:fig-demo.js:326:3]]
, each cut to 

[[js:fig-demo.js:327:0]]
A prompt runs over many lines, so it saw only its first line, the same opening sentence for every puzzle, and the start of each answer. 

[[js:fig-demo.js:328:0]]
It saw no examples, no test input and no correct answer, so these lines could not show it what went wrong.

[[js:fig-demo.js:330:0]]
No command that opened these logs was found in the trace.

[[js:fig-demo.js:336:3]]
Everything it printed from this puzzle's log (line number, then the line)

[[js:fig-demo.js:337:1]]
What the coach saw of this puzzle's log

[[js:fig-demo.js:339:3]]
The same command also printed the puzzle README, the helper code and lines of the scoring code. Its reasoning summary for that turn is mostly about those.

[[js:fig-demo.js:340:0]]
Its reasoning summary in that turn

[[js:fig-demo.js:341:3]]
The command it ran

[[js:fig-demo.js:342:1]]
Command in turn 

[[js:fig-demo.js:343:0]]
Show everything the command printed

[[js:fig-demo.js:344:4]]
. The coach saw all of it.

[[js:fig-demo.js:345:2]]
Output of turn 

[[js:fig-demo.js:353:0]]
The coach edits the player's code. First what it changed, then how it got there.

[[js:fig-demo.js:356:3]]
What it changed

[[js:fig-demo.js:358:3]]
No summary of the edit was written.

[[js:fig-demo.js:359:3]]
Our plain-language summary of the code change.

[[js:fig-demo.js:363:3]]
Why, in its reasoning summary (turn 

[[js:fig-demo.js:368:3]]
On the 25 practice puzzles the original player scored 

[[js:fig-demo.js:369:0]]
. In the round's own check of the edited player it scored 

[[js:fig-demo.js:370:0]]
: one puzzle more, from one run each, which is within run-to-run noise. In that check it 

[[js:fig-demo.js:373:0]]
Show code change

[[js:fig-demo.js:382:3]]
How it got there, in 

[[js:fig-demo.js:383:3]]
In each turn the coach reasons, then may run one command on the player's code. Turn names are our labels for each command. Reasoning summaries are shown as the API returned them; they are lossy and sometimes garbled.

[[js:fig-demo.js:389:3]]
No reasoning summary came back for this turn.

[[js:fig-demo.js:395:0]]
Show the command and what it printed

[[js:fig-demo.js:395:1]]
Show the command

[[js:fig-demo.js:396:3]]
The command it ran

[[js:fig-demo.js:397:1]]
Command in turn 

[[js:fig-demo.js:399:3]]
What it printed

[[js:fig-demo.js:399:5]]
; the coach saw all of it)

[[js:fig-demo.js:400:1]]
Output of turn 

[[js:fig-demo.js:404:0]]
Show the reminder the harness sent back (the coach ran no command this turn)

[[js:fig-demo.js:405:1]]
Reminder after turn 

[[js:fig-demo.js:408:3]]
The round ends here.

[[js:fig-demo.js:417:0]]
 made no edit

[[js:fig-demo.js:418:0]]
 broke the player so that it scored 0

[[js:fig-demo.js:419:4]]
 coaching rounds for this demo. Of the other 

[[js:fig-demo.js:420:2]]
. This is the only one that changed the player without breaking it.

[[js:fig-demo.js:426:0]]
The edited player gets the same puzzle and the same two tries. This is a separate run made after the round

[[js:fig-demo.js:427:1]]
 on the practice puzzles)

[[js:fig-demo.js:428:0]]
; in the round's own practice check (

[[js:fig-demo.js:428:1]]
) the edited player 

[[js:fig-demo.js:433:0]]
[its first answer]

[[js:fig-demo.js:437:3]]
New since the edit: try 2 is a review. Its prompt ends with

[[js:fig-demo.js:445:0]]
Try 1 gave the same wrong grid as try 1 before the edit. It is a new call that happened to give the same answer.

[[js:fig-demo.js:448:0]]
Its closest answer is further off than before the edit: 

[[js:fig-demo.js:455:0]]
Runs are not deterministic: the same player can solve a puzzle once and miss it the next time. So we ran each player on this puzzle 

[[js:fig-demo.js:489:0]]
The original player solved this puzzle in 

[[js:fig-demo.js:489:2]]
 runs; the edited player in 

[[js:fig-demo.js:490:0]]
 Every one of the edited player's solves came the same way: try 1 was wrong and the review in try 2 fixed it.

[[js:fig-demo.js:497:0]]
 traced runs of the edited player, the review returned the same wrong grid as try 1, so it sent one answer instead of two.

[[js:fig-demo.js:498:0]]
 The original player's 

[[js:fig-demo.js:498:3]]
 came from its second try, an independent attempt that the edit replaced with the review.

[[js:fig-demo.js:500:0]]
 The original player's 

[[js:fig-demo.js:500:3]]
 came on try 1.

[[js:fig-demo.js:504:3]]
"Round's check" is the edited player's run in the coaching round's own practice check (72% overall); only its score is shown here.

[[js:fig-demo.js:506:5]]
 runs each, and two puzzles picked to illustrate, this shows how the edit works, not whether it helps on average.

[[js:fig-demo.js:508:3]]
This traced demo cost 

[[js:fig-demo.js:508:4]]
 in model calls. It is not part of the experiment's results.

[[js:fig-demo.js:523:0]]
See the puzzle that stayed wrong →

[[js:fig-demo.js:523:1]]
Back to the start

[[js:fig-demo.js:543:1]]
Notes on these traces


### fig-tree.js

[[js:fig-tree.js:103:0]]
 generations · the coach changed its own code in 

[[js:fig-tree.js:105:0]]
no coach qualified for testing at gen 

[[js:fig-tree.js:106:1]]
 of its coaches were tested

[[js:fig-tree.js:113:1]]
nothing (the starting code)

[[js:fig-tree.js:115:0]]
 (but it failed checks)

[[js:fig-tree.js:115:1]]
nothing saved (the edit failed checks)

[[js:fig-tree.js:120:0]]
rejected: failed checks (had scored 

[[js:fig-tree.js:120:2]]
failed checks, not scored

[[js:fig-tree.js:155:3]]
Six independent tries of the same self-improvement loop. Each started from the same coach and player, and each evolved differently. All six ran 12 generations; runs 1 to 4 were then extended to 40, as planned in the follow-up design (fixed before any follow-up result).

[[js:fig-tree.js:156:5]]
Self-improvement run

[[js:fig-tree.js:209:1]]
Practice score by generation in run 

[[js:fig-tree.js:209:3]]
 versions. Tab here, then arrow keys move between versions, up goes to the parent, Enter picks, Escape clears.

[[js:fig-tree.js:221:6]]
 was not extended past gen 

[[js:fig-tree.js:240:7]]
best in this run 

[[js:fig-tree.js:274:0]]
, the coach changed its own code

[[js:fig-tree.js:305:0]]
best in this run 

[[js:fig-tree.js:305:1]]
, with this coach

[[js:fig-tree.js:308:0]]
best with this coach 

[[js:fig-tree.js:355:1]]
Best practice score

[[js:fig-tree.js:358:3]]
Pick a dot to see how its coach did.

[[js:fig-tree.js:371:2]]
Its coach is the original coach.

[[js:fig-tree.js:371:3]]
Its coach is the original, unchanged coach.

[[js:fig-tree.js:372:0]]
Its coach is new: the coach changed itself here.

[[js:fig-tree.js:373:0]]
Its coach came from version 

[[js:fig-tree.js:375:0]]
 Nothing was built on it.

[[js:fig-tree.js:379:3]]
none passed the checks.

[[js:fig-tree.js:379:4]]
it failed the checks.

[[js:fig-tree.js:380:0]]
their best score reached 

[[js:fig-tree.js:381:0]]
their best score climbed from 

[[js:fig-tree.js:382:0]]
none beat its own 

[[js:fig-tree.js:387:6]]
Hide code change

[[js:fig-tree.js:387:7]]
Show code change

[[js:fig-tree.js:395:4]]
Read coach transcript

[[js:fig-tree.js:412:3]]
What happened when we froze this coach and gave a fresh player 8 rounds

[[js:fig-tree.js:413:3]]
Pick a dot above to see its coach here.

[[js:fig-tree.js:417:4]]
This version’s coach (from version 

[[js:fig-tree.js:418:0]]
 was never frozen and tested. Only the coaches picked by the rule were tested: the blue diamonds.

[[js:fig-tree.js:425:0]]
The original coach was tested 

[[js:fig-tree.js:425:1]]
 times. Its final players scored 

[[js:fig-tree.js:426:0]]
 on the exam (120 new puzzles). Every self-improved coach is compared with this.

[[js:fig-tree.js:430:0]]
Made at generation 

[[js:fig-tree.js:431:0]]
by the rule at gen 

[[js:fig-tree.js:432:0]]
by the fallback rule at gen 

[[js:fig-tree.js:432:1]]
 (no coach qualified, so it took the one with the most versions built on it)

[[js:fig-tree.js:434:0]]
. On the exam (120 new puzzles) its final player

[[js:fig-tree.js:435:0]]
; the original coach’s scored 

[[js:fig-tree.js:442:4]]
picked at gen 

[[js:fig-tree.js:459:3]]
Best practice score so far

[[js:fig-tree.js:502:1]]
Code change in 

[[js:fig-tree.js:504:4]]
Code change in 


### fig-replay.js

[[js:fig-replay.js:3:0]]
s examples, then the test input, the truth and one run

[[js:fig-replay.js:50:0]]
Loading the exam answers…

[[js:fig-replay.js:88:4]]
Search puzzle id

[[js:fig-replay.js:88:6]]
Search exam puzzles by id

[[js:fig-replay.js:102:3]]
. The bar and number: how many of the 

[[js:fig-replay.js:102:4]]
 runs solved it.

[[js:fig-replay.js:103:3]]
No puzzle matches.

[[js:fig-replay.js:135:1]]
Run whose answers are shown

[[js:fig-replay.js:148:2]]
Solved by no run

[[js:fig-replay.js:149:2]]
Solved by some runs

[[js:fig-replay.js:150:2]]
Solved by every run

[[js:fig-replay.js:151:0]]
Runs that solved it

[[js:fig-replay.js:154:1]]
Most solved first

[[js:fig-replay.js:155:1]]
Least solved first

[[js:fig-replay.js:157:3]]
“Solved” means the run solved every test input of the puzzle.

[[js:fig-replay.js:158:4]]
 runs, try 1 and try 2

[[js:fig-replay.js:272:3]]
Dashed squares: the 

[[js:fig-replay.js:272:4]]
 runs whose answer grids were not kept (right/wrong only).


### fig-transcripts.js

[[js:fig-transcripts.js:78:0]]
Self-improvement runs

[[js:fig-transcripts.js:78:2]]
Self-improved coach

[[js:fig-transcripts.js:78:5]]
Short test runs

[[js:fig-transcripts.js:83:0]]
Trial of the self-improved coach from run 

[[js:fig-transcripts.js:262:1]]
Two model calls (refine or verify)

[[js:fig-transcripts.js:264:1]]
Same puzzle across generations

[[js:fig-transcripts.js:266:1]]
Solved (answer only)

[[js:fig-transcripts.js:269:1]]
Back to one transcript

[[js:fig-transcripts.js:269:2]]
Evolution series view

[[js:fig-transcripts.js:273:5]]
Show all turns

[[js:fig-transcripts.js:273:6]]
Replay step by step

[[js:fig-transcripts.js:299:3]]
Saved player transcripts are all failed attempts; solved ones show the answer only.

[[js:fig-transcripts.js:301:3]]
No transcripts match these filters.

[[js:fig-transcripts.js:336:3]]
Pick an item from the list.

[[js:fig-transcripts.js:340:4]]
Solved, so no transcript was saved: only the answer survives (right).

[[js:fig-transcripts.js:345:0]]
This practice puzzle failed at several generations of this run.

[[js:fig-transcripts.js:346:0]]
This edited player makes a second model call to 

[[js:fig-transcripts.js:346:3]]
 its first answer.

[[js:fig-transcripts.js:347:0]]
The player crashed before it could answer.

[[js:fig-transcripts.js:348:0]]
A failed practice answer sampled from this run.

[[js:fig-transcripts.js:353:3]]
Final answers vs the correct answer

[[js:fig-transcripts.js:379:5]]
 saved generations of 

[[js:fig-transcripts.js:379:6]]
, left to right.

[[js:fig-transcripts.js:409:3]]
The coaching sessions could not be loaded.

[[js:fig-transcripts.js:431:6]]
, one per generation

[[js:fig-transcripts.js:432:1]]
 changed the code.

[[js:fig-transcripts.js:444:3]]
Scroll the list to see all 

[[js:fig-transcripts.js:445:3]]
“restarted”: an attempt the harness stopped while scoring it; the generation was then run again.

[[js:fig-transcripts.js:477:1]]
Started from the original code (generation 0)

[[js:fig-transcripts.js:477:2]]
Started from the code of generation 

[[js:fig-transcripts.js:478:0]]
Starting generation not recorded

[[js:fig-transcripts.js:482:3]]
The coach finished this session, but the harness was stopped while the result was being scored and ran generation 

[[js:fig-transcripts.js:482:4]]
 again, so this attempt has no score.

[[js:fig-transcripts.js:484:4]]
Loading this run’s sessions…

[[js:fig-transcripts.js:490:3]]
This session’s steps are missing.

[[js:fig-transcripts.js:495:3]]
This run’s sessions could not be loaded (

[[js:fig-transcripts.js:532:0]]
How to read the session

[[js:fig-transcripts.js:533:5]]
Step through the session

[[js:fig-transcripts.js:543:3]]
These are the coach’s visible messages and the commands it ran; the model’s hidden reasoning was not recorded. 

[[js:fig-transcripts.js:544:0]]
The harness runs one command per message; when a message has none, it sends a short reminder (small grey lines).

[[js:fig-transcripts.js:546:4]]
The session, step by step

[[js:fig-transcripts.js:606:1]]
What the coach was shown

[[js:fig-transcripts.js:608:0]]
The instructions, earlier scores and 

[[js:fig-transcripts.js:608:1]]
 failed practice puzzle

[[js:fig-transcripts.js:608:4]]
 (what the player saw and answered).

[[js:fig-transcripts.js:609:0]]
The instructions, with a summary of earlier scores.

[[js:fig-transcripts.js:609:1]]
The instructions only; the coach had to look up earlier results itself.

[[js:fig-transcripts.js:611:5]]
What the coach was shown

[[js:fig-transcripts.js:616:0]]
Shown in full.

[[js:fig-transcripts.js:618:0]]
long puzzle grids (answers included) are cut short

[[js:fig-transcripts.js:621:0]]
Shortened for display from 

[[js:fig-transcripts.js:631:3]]
Written after the command, in the same message (before it ran):

[[js:fig-transcripts.js:635:3]]
This message contains a tool call the harness could not read (or one past the first), so it did not run.

[[js:fig-transcripts.js:638:6]]
Show the whole message

[[js:fig-transcripts.js:641:2]]
Show the whole message

[[js:fig-transcripts.js:644:3]]
A long run of repeated text in this message was collapsed.

[[js:fig-transcripts.js:665:2]]
(command not recorded)

[[js:fig-transcripts.js:710:4]]
 characters in full.

[[js:fig-transcripts.js:712:3]]
The same message asked for 

[[js:fig-transcripts.js:712:7]]
; the harness runs only the first.

[[js:fig-transcripts.js:714:3]]
What came back

[[js:fig-transcripts.js:716:3]]
Shortened to the start and end: 

[[js:fig-transcripts.js:716:4]]
 characters in full.

[[js:fig-transcripts.js:730:0]]
A coach message with no readable text

[[js:fig-transcripts.js:730:1]]
 coach messages with no readable text

[[js:fig-transcripts.js:733:0]]
Reminder: no command in that message.

[[js:fig-transcripts.js:733:1]]
 reminders: no command in those messages.

[[js:fig-transcripts.js:734:0]]
The model gateway replied

[[js:fig-transcripts.js:734:1]]
The model gateway replied 

[[js:fig-transcripts.js:734:3]]
 in place of the coach: its token budget for this round (600k) was spent.

[[js:fig-transcripts.js:736:1]]
The coach said DONE.

[[js:fig-transcripts.js:746:3]]
Only compiled cache files changed.

[[js:fig-transcripts.js:746:4]]
The coach changed no code in this round.

[[js:fig-transcripts.js:750:3]]
The coach changed both the player’s code and its own (coach) code.

[[js:fig-transcripts.js:751:0]]
The coach changed only its own (coach) code; the player stayed the same.

[[js:fig-transcripts.js:751:1]]
The coach changed the player’s code.

[[js:fig-transcripts.js:751:2]]
The coach changed only other files; the player stayed the same.

[[js:fig-transcripts.js:762:1]]
Show code change

[[js:fig-transcripts.js:787:4]]
Show in tree

[[js:fig-transcripts.js:809:3]]
A puzzle counts as gained when its practice score went up, for example from one of its two tests to both.

[[js:fig-transcripts.js:810:0]]
 With the player unchanged, these differences come from scoring it again.

[[js:fig-transcripts.js:819:4]]
 (no picture saved for this one).

[[js:fig-transcripts.js:821:5]]
the first two of its 

[[js:fig-transcripts.js:830:4]]
Read the player’s failed attempt (

[[js:fig-transcripts.js:836:3]]
No player transcript was saved for this puzzle in this run.

[[js:fig-transcripts.js:843:1]]
No code changed in this attempt, and it was not scored.

[[js:fig-transcripts.js:843:2]]
No code changed, so the player stayed as it was.

[[js:fig-transcripts.js:844:1]]
The harness was stopped while scoring this attempt, so the edit has no score.

[[js:fig-transcripts.js:844:2]]
This edit was not scored.

[[js:fig-transcripts.js:845:1]]
The edited player broke: it scored 0% on practice puzzles

[[js:fig-transcripts.js:845:5]]
The edited player broke and could not be scored.

[[js:fig-transcripts.js:848:1]]
The practice score stayed at 

[[js:fig-transcripts.js:849:0]]
The practice score 

[[js:fig-transcripts.js:850:0]]
 The player itself was not changed, so 

[[js:fig-transcripts.js:850:3]]
 only reflects scoring the same player again (run-to-run noise).

[[js:fig-transcripts.js:851:0]]
 The harness marked this version invalid, so later rounds could not start from it.

[[js:fig-transcripts.js:858:5]]
Step through turns

[[js:fig-transcripts.js:888:0]]
Answer in this turn

[[js:fig-transcripts.js:898:3]]
Model answer (call 1)

[[js:fig-transcripts.js:898:5]]
Refine prompt (call 2)

[[js:fig-transcripts.js:898:7]]
Model answer (call 2)

[[js:fig-transcripts.js:899:1]]
Verify prompt (call 2)

[[js:fig-transcripts.js:899:3]]
Model answer (call 2)

[[js:fig-transcripts.js:901:1]]
Task given to the coach


### fig-audit.js

[[js:fig-audit.js:73:2]]
, the untouched player was kept

[[js:fig-audit.js:80:1]]
 (same code as the tested pick

[[js:fig-audit.js:80:5]]
: code never examined on the exam

[[js:fig-audit.js:91:3]]
The tested coaches made 

[[js:fig-audit.js:91:4]]
 distinct changes to their own code. 

[[js:fig-audit.js:92:0]]
 of them were judged specific to these puzzles (ARC-specific); the rest are general advice.

[[js:fig-audit.js:96:6]]
 ARC-specific distinct changes

[[js:fig-audit.js:103:3]]
Counted once per picked coach, as in the write-up: 

[[js:fig-audit.js:128:7]]
 in the tree

[[js:fig-audit.js:128:8]]
Show in tree

[[js:fig-audit.js:149:3]]
No change text was saved.

[[js:fig-audit.js:152:3]]
No change matches these options.

[[js:fig-audit.js:179:3]]
How often the coach edited its own code

[[js:fig-audit.js:180:4]]
 generations of each source run: 

[[js:fig-audit.js:181:0]]
 generations changed coach code; 

[[js:fig-audit.js:181:1]]
 of those were later built on.
