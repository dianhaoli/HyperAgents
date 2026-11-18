# SIMPLIFY_PLAN: Coaching the Coach, second pass

The user said the page is "a little much". It is for first-time readers, and the core idea is simple. This plan replaces the 8-figure article with a **5-figure main story** and a separate, tabbed **Explore the data** section. Where this plan conflicts with DESIGN_BRIEF.md or CONTRACT.md, this plan wins. CONTRACT.md's module rules still apply: one IIFE per file, selectors prefixed `.fx-NAME`, numbers read from `data/*.json`, complete at rest, no autoplay, no horizontal page scroll.

**Core idea, in one breath:** an AI coach rewrites a puzzle-solving AI's code to make it better. We also let the coach rewrite *itself* for many generations. Then we tested whether the self-improved coach is a better coach. It is not. Players trained by any coach scored about the same (~29%) as an untouched player. Simply letting the model think longer (41%) beat all coaching.

---

## 0. Global rules for every builder

1. **Plain words in the main story.** Use these names, and only these:

   | data | main-story name | Explore / tooltip name (allowed) |
   |---|---|---|
   | B0 (A₀, two plain attempts) | **No coach** | B0, "plain player A₀" |
   | I₀ pay-off runs | **Original coach** | I₀ |
   | I_g pay-off runs (gen-12 picks) | **Self-improved coach** | I_g, "gen-12 pick" |
   | g20 / g40 extension runs | **Generation-20 / generation-40 coach** | ext g20/g40 |
   | xhigh A₀ | **Think longer (no coach)** | xhigh |
   | source practice set / pay-off practice set | **practice puzzles** | source set / pay-off set |
   | held-out eval | **the exam (120 unseen puzzles)** | held-out, 167 test inputs |
   | task agent / meta agent | **player / coach** | |
   | generation | **generation** | gen |

   Run ids (`source_s3`, `payoff_I0_2`), "pass@2", "G", "Δ", "Welch" and node ids appear only inside Explore, in tooltips, or in footnotes.
2. **Figure anatomy** for main-story figures:
   - **Title** = a plain takeaway sentence (`.fig-title`).
   - **One helper line** (`.fig-text`, at most about 25 words).
   - The drawing.
   - A grey `Figure N:` caption with the source file in `.src`.
   - **No `.fig-hint` lines** (delete the class's use everywhere). No paragraphs inside figures. No callout boxes.
3. **At most 2 font sizes per figure**:
   - `--fs-fig-text` (15px), used for labels, buttons and readouts;
   - `--fs-axis` (13px), used for ticks and secondary labels.
   - Main-story chart direct labels are ≥14px. No 11, 11.5 or 12.5px literals.
4. **Direct-label instead of legends.** No pills or badges. No mono metadata lines in the main story. Mono is only for numbers in tables inside Explore.
5. **Controls:**
   - sentence case, no letter-spacing, no uppercase control labels;
   - hit targets ≥ 40px tall on phone;
   - at most ONE interaction per main-story figure;
   - secondary controls in Explore sit behind a `More options` disclosure (`EX.more`, §6).
6. **Colour.**
   - Beige/stone ground and panels. Blue `--accent` is used only for selection, links/footnote marks, and the "self-improved coach" path in Fig 1. Everything else is ink.
   - `--correct` and `--wrong` are muted, and are used only for ✓/× and wrong-cell outlines, never cell fills.
   - The ARC palette appears only inside puzzle grids.
7. **Notation in Explore.** Use `EX.sym('Ig')`, `EX.sym('I0')` and `EX.sym('A0')` (real subscript; §6). Never a literal "I_g".
8. **No layout shift.** Every mount that loads data lazily reserves its final height (CSS `min-height` on `.mount`, desktop and ≤720px values) and renders a skeleton immediately. Hidden tabs are exempt until shown.
9. **Keyboard.** Lists and matrices use a roving tabindex: one tab stop per list or matrix, arrow keys inside. Main-story dot charts follow the same rule: one tab stop, ←/→ through the dots.
10. **Numbers.** Every number is read from data, through `data-v` bindings in prose or computed in JS. The few process facts with no data source (11 of 31 steps, 6 VM restarts, 49 inputs, 39.9%, 1,513) are cited as "DECISIONS n" in a footnote.

---

## 1. New page structure (index.html, builder A)

```
top bar      quiet: "Coaching the Coach" (sans, 14px, ink-muted) · text theme toggle "Auto · Light · Dark"
header       h1 + 3-line summary + one quiet facts line
§1 The setup                         Figure 1  (mount setup)       l-page
§2 What the puzzles look like        Figure 2  (mount puzzle)      l-mid
§3 The result                        Figure 3  (mount results)     l-page
§4 Did more generations help?        Figure 4  (mount generations) l-page
§5 Watch them answer                 Figure 5  (mount watch)       l-page
§6 What to take away                 3 bullets incl. the 3 caveats (no figure)
── visible divider ──
§7 Explore the data                  tab bar + 5 tab panels         l-wide (max 1160)
References and notes                 (refs list, short)
```

Remove the numbered TOC. Replace it with one quiet line under the summary: `Jump to: The result · Watch them answer · Explore the data`. Remove the 4-column byline and the "In short" bullets; the header replaces them.

### Header: exact text

- **h1:** `Can an AI coach teach itself to coach better?`
- **Summary** (`p.dek`, three short lines; numbers are `data-v` bound):
  > An AI **coach** rewrites the code of a puzzle-solving AI, the **player**, to make it better. We also let the coach rewrite *itself*, generation after generation, then tested whether the self-improved coach trains better players.
  > It does not. On an exam of 120 unseen ARC-AGI-2 puzzles, coached players scored about the same as a player nobody coached: <span data-v="pct:I0_mean">29.7%</span> (original coach) and <span data-v="pct:Ig_mean">27.9%</span> (self-improved coach), against <span data-v="pct:B0.mean">29.3%</span> (no coach).
  > Simply letting the model think longer, with no coaching at all, scored <span data-v="pct:xhigh.score">41.1%</span>.
- **Facts line** (13px, ink-muted, one line, wraps on phone):
  `Model gpt-6-luna · each player gets ≤2 model calls and 2 answers per puzzle · total cost <span data-v="usd:spend.total">$152.23</span> · Nov 2026`

### §1 The setup
Lead paragraph (2–3 sentences):
- The player is a short program that gets at most two model calls and two answers per puzzle.
- The coach reads how the player did on 25 practice puzzles and edits its code.
- In the first phase the coach may also edit its own code. We ran this six times for 12 generations, and four of those runs on to 40.

After the figure (2–3 sentences):
- To test a coach, we froze it and gave it a fresh, untouched player and 8 rounds on a second set of 25 practice puzzles.
- The finished player then sat the exam once.
- An exam score is the share of the 120 puzzles answered correctly in at most 2 tries (footnote: task-averaged pass@2, 167 test inputs).

Footnotes:
- (a) coach/player = the repo's meta agent / task agent.
- (b) How the "self-improved coach" was picked: "the coach whose edited players changed most favourably on practice; in some runs the only candidate" (fixes data-review 9).
- (c) The model, reasoning effort, call cap and budget sit behind a gateway that no agent could edit (keep the existing gateway sentence, shortened).

Keep footnote 4 only in Explore → Numbers, reworded per data-review 2:
> "Once (generation-20 coach from run s4), the untouched starting player had the higher mean of loop score and re-score of the two finalists (0.70 vs 0.66), so that exam score is the untouched player's own."

### §2 What the puzzles look like
One paragraph:
- Each puzzle shows a few input→output examples.
- You find the rule and paint the output for a new input.
- You get two tries, like the player.

### §3 The result
One paragraph with the plain differences:
- Original coach vs no coach: <span data-v="pts:G.est">+0.4</span> points (95% range <span data-v="ci:G">[−1.9, +2.8]</span>).
- Self-improved coach vs no coach: <span data-v="pts:Ig_gain_over_B0.est">−1.4</span> points (<span data-v="ci:Ig_gain_over_B0">[−4.0, +1.3]</span>).
- "Both ranges include zero: no detectable effect."

Footnote:
- Self-improved vs original: Δ = <span data-v="pts:Delta.est">−1.8</span>, <span data-v="ci:Delta">[−4.2, +0.6]</span>.
- Welch t-intervals [ref].
- The headline "Neither improver beat two plain attempts on ARC-AGI-2" was pre-registered.

Second short paragraph:
- Coaching didn't buy its score with more compute. Every player had the same two-call budget.
- Thinking longer is a setting no coach was allowed to change.

### §4 Did more generations help?
Paragraph:
- The self-improved coaches came from generation 12. In a follow-up that was not pre-registered, we also tested coaches from generations 20 and 40.
- Average exam scores were <span data-v="pct:extension.per_generation.0.mean">29.7%</span>, 27.9%, 29.8% and 30.3% for generations 0/12/20/40, all bound.
- Generation 40 minus generation 0 = <span data-v="pts:extension.gen40_minus_gen0.est">+0.6</span> points, <span data-v="ci:extension.gen40_minus_gen0">[−6.5, +7.8]</span>.
- The noise is large: the same unchanged coach, run three times, scored 26.0%, 27.8% and 36.0%. Read these from data; see the Fig 4 spec.

### §5 Watch them answer
One sentence:
- Each column is a different kind of player answering the same puzzle.
- Wrong answers are often close: a few cells or one colour off.

### §6 What to take away (exact bullets)
1. `No coach, original or self-improved, produced a player that beat two plain attempts on this exam.`
2. `Letting the model think longer was worth about 12 points; no amount of coaching came close.` Bind the 12 from `EX.derive().xhighGain`, or compute xhigh − B0 mean = 11.9. Write "about 12 points" only if it binds to a value that rounds to 12.
3. `Read with care:` the bullet then lists three caveats:
   - (i) re-running one identical coach moved its score by 10 points, so small differences are noise;
   - (ii) later-generation coaches were often the same code as earlier picks;
   - (iii) we saved transcripts only for failed practice answers, and they never include the model's hidden reasoning.

### §7 Explore the data (tabs shell, builder A)

Layout:
- `<section id="explore" class="l-wide explore">` starts with an h2 `Explore the data` and one line: `Everything behind the five figures: every run, every answer, every code change.`
- Then a `role="tablist"` with 5 tabs, then 5 `role="tabpanel"` elements. Only one panel is visible at a time.
- Default tab: **Evolution trees**. Each panel has a one-line intro (`.fig-text`), its mount, and a grey caption. Panels have no "Figure N" numbers: use `Explorer:` captions.

| tab label | tab id / panel id | mount(s) | owner | panel intro line (exact) |
|---|---|---|---|---|
| Evolution trees | `tab-tree` / `panel-tree` | `tree` | D | `Each node is one saved version of coach + player code, placed by generation. Pick a node to see what changed.` |
| Every exam answer | `tab-replay` / `panel-replay` | `replay` | D | `All 120 exam puzzles, with each run's two answers next to the truth.` |
| Transcripts | `tab-transcripts` / `panel-transcripts` | `transcripts` | D | `What the player and the coach actually wrote. Player transcripts were saved only for failed practice answers.` |
| Code changes | `tab-audit` / `panel-audit` | `audit` | D | `Every change the self-improved coaches made to their own code, and whether it was specific to ARC.` |
| Numbers & method | `tab-numbers` / `panel-numbers` | `results-detail` (B), `generations-detail` (C), then static HTML: Cost, Caveats in full, Appendix tables (A) | A shell; B, C mounts | `The full statistics, compute, cost and every design choice.` |

Captions (exact; A writes these into index.html):
- **tree:** `Explorer: archive trees. Source runs (coach and player co-evolve, scored on the source practice set) and pay-off / extension runs (frozen coach, pay-off practice set). Practice score = share of 25 practice puzzles solved. <span class="src">trees.json, summary.json</span>`
- **replay:** `Explorer: exam answers. Answer grids are kept for 17 of 23 exam runs; the six extension runs from s2–s4 keep right/wrong only. <span class="src">heldout.json, tasks.json</span>`
- **transcripts:** `Explorer: transcripts. Long prompts are shortened; the puzzle grids are drawn from tasks.json beside them. Hidden model reasoning was never recorded. <span class="src">transcripts.json, tasks.json, trees.json</span>` (fixes data-review 3)
- **audit:** `Explorer: diff audit of every picked coach against the original coach; each hunk judged general vs ARC-specific by three judges. <span class="src">trees.json, summary.json</span>`
- **numbers:** each mount and table gets its own caption, supplied by its builder in their report. A pastes it in.

Static content moved into the Numbers tab (A):
- Cost: re-set as `table.t` with a hairline header, `--fs-small`.
- Caveats in full: the old §9 text, with the fixes below.
- Appendix: the old §A tables.
- "Files in the repository".
- Change the old §11 claim to: `Every result number is read from explorer/data/*.json; process facts are from DECISIONS.md.` (data-review 8)
- Footnote about B0 rep 2 (data-review 4): `compute.json logs unusually few tokens for B0 rep 2 (0.67 calls, 15k tokens per input); the gateway ledger for the same run shows normal usage (7.73M tokens, 371 calls, $3.16), so this is a logging gap, not real efficiency.` Bind the ledger numbers to `compute.json` B0_rep2 `heldout_eval_ledger_*` where bindValues supports it; otherwise B shows them in its readout.

Hash routing:
- `#tree…`, `#replay…`, `#transcripts…` and `#audit…` open the matching tab and then scroll to the explore section.
- `#numbers`, `#cost` and `#appendix` open the Numbers tab and scroll to the anchor inside it.
- `#results` maps to §3, `#extension` to §4, `#puzzle` to §2.
- Old deep links must keep working (`#tree?run=…&node=…` etc.).

---

## 2. Main-story figures

### Figure 1: the loop (mount `setup`, figure `#fig-setup`, builder A, js/fig-setup.js)
- **Title:** `A coach edits the player's code. Then we let the coach edit its own.`
- **Helper line:** `Left: the coach improves itself for many generations. Right: we freeze it and test it on a fresh player.`
- **Drawing:** about 5 boxes, sans 15px labels, hairline arrows, and short arrow labels on the same line as the arrow.
  1. **Coach**, with a blue self-loop arrow labelled `rewrites itself`.
  2. **Player**, reached by a `edits code` arrow from Coach.
  3. **25 practice puzzles**: Player → `plays` → Practice → `scores` → back to Coach. Under the left group, a quiet label: `repeat for 12–40 generations`.
  4. **Self-improved coach**: a blue arrow from the left group, labelled `freeze`. Also a small grey box/tag `or the original coach`.
  5. **Exam: 120 unseen puzzles**: frozen coach → `trains a fresh player, 8 rounds` → Exam. Text under the Exam box: `score = puzzles solved in ≤2 tries`.
- **Interaction:** none. At rest it is complete.
- **Remove:**
  - the mini archive tree inside the loop and its filled "gen 0…12" bar;
  - the gateway strip (its content moves to a footnote and the facts line);
  - all mono arrow labels;
  - every run count ("6 runs with I_g", "pick I_g: …"), "I_g transplanted", and all I₀/I_g symbols;
  - the tooltip system on boxes (keep `[data-term]` prose highlighting only if it stays trivial; optional).
- **Dark mode:** boxes filled with `var(--panel-strong)` and a `--rule-strong` border (design 17).
- **Narrow (<640px mount):** stack vertically: Coach ⇄ Player ⇄ Practice, then ↓ freeze, then Fresh player → Exam. No horizontal scroll.
- **Reuse:** the existing SVG helpers and arrow marker code in fig-setup.js. Delete the archive-tree drawing, the gateway band and both tooltip tables.

### Figure 2: try a puzzle (mount `puzzle`, `#fig-puzzle`, builder B, js/fig-puzzle.js + assets/fig-puzzle.css)
- **Width:** `l-mid` (about 860px; new class from A).
- **Title:** `Find the rule from the examples, then paint the answer.`
- **Helper line:** `Pick a colour, click cells to paint, then press Check. You get two tries, like the player.`
- **At rest:**
  - the example pairs (input → output, same scale, in a row that wraps);
  - then the test input and **your answer grid side by side at the same cell size** (design 10);
  - a single row of 10 palette swatches (no index digits; colour names in `title` / aria-label), at least 32px each;
  - buttons: **Check** (primary) and a quiet **Another puzzle**.
  - The answer grid starts as a copy of the test-input size, filled black (same default as now).
- **The one interaction:** paint + Check. After Check:
  - the result reads `Correct!` or `Not quite: N cells differ (try 1 of 2)`;
  - after the 2nd failed try or a success, show the truth beside your answer, with wrong cells outlined;
  - one plain line from heldout.json: `How the AI did on this puzzle: no coach 2 of 3 runs · original coach 4 of 6 · self-improved coach 1 of 5 · think longer: solved` (computed per arm from `runs[r].results[task][0].c`, first test input);
  - plus a link `See every run's answer →`, which calls `EX.explore.open('replay')` and `EX.select('task', {task, set:'heldout', source:'puzzle'})`.
- **Behind "More tools"** (`EX.more`, collapsed): fill tool, resize rows/cols (clamped 1–30), copy input, clear, reveal answer, difficulty filter (easy/medium/hard by exam solve rate).
- **Remove:**
  - the run-picker select and the per-run attempt grids (now in Explore → Every exam answer);
  - the "Showing the 36 of 120…" sentence. If kept anywhere, it goes in the caption as `One of 36 exam puzzles small enough to paint (all grids ≤ 20×20).` (QA 10)
  - the "practice task" wording (QA 4).
- **Default task:** keep the existing medium-band default logic. Hash `#puzzle?task=` is still read at init; write it on "Another puzzle".
- **Caption:** `Figure 2: an exam puzzle from ARC-AGI-2 [ref]. Run results are from the 23 exam runs. <span class="src">tasks.json, heldout.json</span>`. Do not cite transcripts.json.
- **Loading:** heldout.json lazily, on first Check, or prefetched when the figure nears the viewport (existing logic).

### Figure 3: the result (mount `results`, `#fig-results`, builder B, js/fig-results.js + new assets/fig-results.css)
- **Title:** `Coached players scored the same as an uncoached one. Thinking longer scored much higher.`
- **Helper line:** `Each dot is one finished player's exam score. Bars show the average.`
- **Drawing:** a horizontal dot strip.
  - **x:** exam score, 20%–45%, ticks every 5%, at 13px.
  - **Three rows**, with direct labels on the left at 15px:
    - `No coach`: 3 dots;
    - `Original coach`: 6 dots;
    - `Self-improved coach`: 5 dots.
  - Each row has a mean tick with its value printed beside it (`29.3%`, `29.7%`, `27.9%`) and a thin 95% interval line.
  - The no-coach range is a vertical shaded band (`.b0-band`) running through all rows.
  - **Reference:** a dashed vertical line at xhigh, labelled at the top `Think longer, no coach: 41.1%`.
  - Blue is not used for any arm. Arms are ink, so this is not winner styling.
- **Interaction:** hover, focus or tap a dot shows a tooltip, `Original coach, run 3: 30.4%`. In the tooltip only, the run id goes on a muted second line. No toggle. The readout is the tooltip, and the numbers are already direct-labelled at rest.
- **Remove:**
  - the 3-view `EX.seg`;
  - the compute scatter and per-10k views;
  - the G/Δ Welch mini-plots;
  - the gen-20/gen-40 rows (they go to Fig 4);
  - the pinned readout box;
  - the hash `#results?run=`;
  - the trees.json lookup;
  - the `select-run` listener and emit.
- **Narrow:** labels go above each row instead of to the left, and the chart is full width.
- **Caption:** `Figure 3: exam scores (share of 120 puzzles solved in ≤2 tries) of every finished player. Bars: mean and 95% interval; shaded band: range of the three no-coach runs. <span class="src">summary.json</span>`

#### Second mount `results-detail` (same file, builder B; lives in Explore → Numbers)
Keep the old full figure here, fixed:
- the three views, with labels shortened to `Score · vs compute · per 10k tokens` (design 16);
- G, Δ and Ig−B0 as Welch intervals against 0;
- the gen-20/40 rows.

Fixes:
- In the per-10k and tokens views, use **ledger tokens per input** (`compute.json` `heldout_eval_ledger_tokens / n_test_inputs`) for every run that has it, and say so in the view note. B0 rep 2 is no longer a fake outlier (data-review 4).
- Title: `No arm differs detectably from two plain attempts` (data-review 7).
- Use `EX.sym` for I₀/I_g.
- One tab stop for the dots.
- Keep the hash `#numbers?run=` pin optional; it may emit `select-run`.

### Figure 4: did later generations help? (mount `generations`, `#fig-generations`, builder C, js/fig-extension.js + assets/fig-extension.css)
- **Title:** `Coaches from later generations were no better, and re-running one coach moves its score by 10 points.`
- **Helper line:** `Average exam score of players trained by coaches taken from each generation. The shaded area is the 95% range.`
- **Drawing:**
  - **x:** generation the coach was taken from: 0, 12, 20, 40, with proportional spacing.
    - Under 0: `original coach`.
    - Under 12: `self-improved coach (main test)`.
    - Under 20 and 40: a muted `follow-up` tag.
  - **y:** exam score, 20%–40%.
  - **Mean line** through the 4 means (ink, 2px). Each mean is direct-labelled (`29.7%`, `27.9%`, `29.8%`, `30.3%`) at 14px, above the point.
  - **Shaded 95% band** (`lo`/`hi` per generation, from `summary.extension.per_generation`), drawn as a light ink-wash area or as vertical interval bars.
  - **Individual runs** as small faint dots (`summary.extension.points`).
  - The no-coach band, horizontal, labelled at its left edge outside the data: `no coach 29.3%`.
  - A dashed reference at 41.1% `think longer`. This is optional if it compresses the y-range too much. If dropped, put it in the helper line instead.
  - ext_source_s4_g20 is a hollow dot. Tooltip: `This run's final player was the untouched starting player`.
- **The one interaction:** a toggle button, `Show one coach run three times`.
  - When on, it highlights in accent the three dots of the identical coach `source_s1` node 1: `payoff_Ig_source_s1` (gen 12), `ext_source_s1_g20` and `ext_source_s1_g40`. Identify them through `trees.json` `coach_origin`, or `summary.extension.picks_changed_code["source_s1:g20"] === 1` etc.
  - It connects the three with a thin accent line and labels them with their scores, read from data (26.0%, 27.8%, 36.0%).
  - It also shows the one-line note: `Same coach code each time: the spread is noise.`
  - Off by default. Hover on dots shows a tooltip with a plain label + score.
- **Remove:**
  - the per-seed lines;
  - the tokens x-axis;
  - callouts ①②③;
  - the `= gNN` sub-labels;
  - the seed table;
  - the gen40−gen0 inset;
  - Clear selection;
  - hash and `select-run` emit/listen.
- **Caption:** `Figure 4: the generation-20 and generation-40 coaches are a follow-up that was not pre-registered [ref]. Generation 40 minus generation 0: +0.6 points, 95% interval [−6.5, +7.8]. <span class="src">summary.json, trees.json</span>`. The numbers are bound in JS.
- **Narrow:** x labels on two lines; mean labels stay above their points; no collisions at 336px (QA 7).

#### Second mount `generations-detail` (same file, builder C; in Explore → Numbers)
The old figure, with the review fixes:
- seed lines in `var(--ink-2)` (design 25);
- direct labels to the right of the last column with leader lines;
- no `= gNN` sub-labels;
- "B0 29.3%" at the band's left edge;
- callout ③ either marked on the chart or un-numbered (QA 6);
- the inset with −5 / +5 end ticks and "← gen 0 better / gen 40 better →" (design 5);
- tokens axis ticks `0, 0.5M, 1.0M, 1.5M` (QA 7);
- the axis title right under the ticks;
- fix "In gen-20 coach from s4" (data-review 12);
- keep the seed table, sentence-case header.

### Figure 5: watch them answer (NEW mount `watch`, `#fig-watch`, builder C, new js/fig-watch.js + assets/fig-watch.css)
- **Title:** `Same puzzle, four kinds of player: wrong answers are often close.`
- **Helper line:** `The correct answer on the left; each player's two tries on the right. Press Next for another puzzle.`
- **At rest:**
  - a header line: `Puzzle 1 of 12` with the task's train pairs shown small in one row (max 3 pairs; `EX.arcPair`, maxSize about 90);
  - then one row of 5 columns at one shared cell size:

    | Correct answer | No coach | Original coach | Self-improved coach | Think longer |
    |---|---|---|---|---|

  - Each player column shows its 2 tries stacked (`EX.arcGrid` with `diffAgainst: truth`). Under each try is ✓ or ×. Wrong cells are outlined; colour is never used as a fill.
  - Under each column header is one muted line: `solved by 2 of 3 runs`, from per-arm counts over all runs in that arm that have the flag (`c`).
  - **Representative run per arm** (all have grids): `B0_rep0`, `payoff_I0_1`, `payoff_Ig_source_s1`, `xhigh`.
- **The one interaction:** a big **Next puzzle →** button (primary, ≥44px), plus a quiet `← Back`. Keyboard: ←/→ when the figure has focus.
- **Behind "More"** (`EX.more`): a `Show another run` select per arm (only runs with `has_preds`), and a link `Open in Every exam answer →` (`EX.explore.open('replay')` + `EX.select('task', …)`).
- **Curated puzzle list** (computed at runtime, deterministic):
  - exam tasks whose truth and test input are ≤ 16×16 (first test input only);
  - first test input not solved by all 4 representative runs AND not failed by all 4;
  - sort by a fixed key: tasks where think-longer solved and others did not come first, then mixed;
  - take the first 12;
  - if `3dc255db` qualifies, start there.
  - If fewer than 12 qualify, relax to ≤ 20×20.
  - Document the rule in the caption.
- **Data:**
  - `tasks.json` (truth: `tasks[id].test[i].output`; check dataspec.md for exact field names);
  - `heldout.json` `runs[run].results[task][i] = {c:[bool,bool], p:[grid,grid], …}`.
  - heldout.json is 4.5 MB. Load it when the figure nears the viewport (IntersectionObserver, rootMargin 800px), and render a skeleton with reserved height immediately.
- **Caption:** `Figure 5: answers to the exam's first test input for one representative run per kind of player; "solved by k of n" counts all runs of that kind. Puzzles chosen automatically: small grids where the players disagree. <span class="src">heldout.json, tasks.json</span>`
- **Narrow (<600px):** the Truth column on top, full width; then the 4 players in a 2×2 grid; tries side by side within each cell. No horizontal scroll.
- **Emits:** nothing, except via the "More" link.

---

## 3. Explore-the-data modules (builder D)

General rules:
- Each module opens in a simple default state.
- Secondary controls go behind `EX.more('More options')`.
- Each panel has one intro line and no in-figure hint lines.
- Modules are mounted lazily when their tab is first shown (§6 core).
- Cross-links between Explore modules use `EX.explore.open(tab)` + `EX.select(...)`. A listener never switches tabs on its own; only an explicit user click does.

### Tree (mount `tree`, js/fig-tree.js, assets/fig-tree.css)
- **Default:** run `source_s1`, no node selected. A run select (grouped, plain labels) heads the panel:
  - "Source runs: s1–s6"
  - "Tests of the original coach"
  - "Tests of self-improved coaches"
  - "Follow-up (gen 20/40)"
  Inside the group, options read e.g. `Self-improved coach from s3`.
- **Main tree:**
  - x = generation, y = lineage;
  - fill = practice score ramp;
  - a thin ink ring marks a node that changed coach code;
  - picks are labelled in accent text (`self-improved pick`, `gen 20 pick`).
  - Fixes: the gen-12 label sits at the top of the dashed rule; the axis title is `Generation`, right-aligned under the axis with no arrow (design 6).
- **Subtitle wording** must be theme-neutral: `Stronger fill = higher practice score` (QA 2). The same applies to the solved squares.
- **Detail panel** (side on desktop, below on phone), exactly 5 facts:
  1. Generation
  2. Practice score (with change vs parent, e.g. `0.62 (+0.08)`)
  3. What changed: `player` / `coach` / `both` / `nothing`
  4. Picked as (plain text, left-aligned)
  5. Exam score (only for final players)
  Then two quiet buttons: `Show code change` (expands the diff full-width below the tree, wrapped lines, no inner horizontal scroll) and `Read coach transcript` (only when one exists; it calls `EX.explore.open('transcripts')` and emits `open-transcript`).
- **Behind "More options":**
  - `Show all six source trees` small multiples (fix: `[hidden]` must hide it; A adds the global rule, and D also adds `.fx-tree .fxt-sm[hidden]{display:none}`);
  - the best-so-far / coach-tokens chart (axis title `Generation`, sentence case);
  - the 25-task solved grid;
  - files by role.
- **Remove:** the chip/badge cloud (design 15); the slider (keep arrow keys); the selected-thumbnail grey fill (accent border + wash only, design 25).
- **Data fix** (data-review 1): `utils/**` counts as coach code. Ring a node when its change vs parent touches coach files. source_s6 must show 3 self-edit nodes, including node 4 (the self-improved pick). D edits `arcexp/build_explorer_data.py` `classify_path` and reruns (§5).

### Every exam answer (mount `replay`, js/fig-replay.js, assets/fig-replay.css)
- **Default:** task `3dc255db`.
- **Left:** a searchable task list, about 10 rows visible, with the scroll snapped to a row boundary (design 21) and a roving tabindex.
- **Main:** the train pairs, then the test input, Truth, and a "stage" showing the chosen run's two tries large beside the truth. The run is chosen by a run select with plain grouped labels plus Prev/Next.
- **Behind "More options":**
  - None/Some/Every filters and the sorts (one count definition, used in both header and legend: `runs that solved every test input`; fixes QA 10);
  - `Show all 23 runs` matrix, with uniform under-thumbnail ✓/× and dashed placeholders for runs with flags only (design 21).
- **Remove:** Play/Pause autoplay; the outline toggle; status words under run names; the stale "sparkline / generations / two views" text (QA 3).
- **Listens:** `select-task` (set heldout) switches the task quietly.

### Transcripts (mount `transcripts`, js/fig-transcripts.js, assets/fig-transcripts.css)
- **Default:** the Player tab, first item, with **all turns shown** (no typewriter at rest).
- **Tabs:** `Player (90)` and `Coach (12)`, using the `.tabs` underline style.
- **List:** roving tabindex. Remove the red × on every row and add one header note: `Saved player transcripts are all failed attempts; solved ones show the answer only.`
- **Main:** the turns, with the puzzle and the final answers diffed against the truth beside them.
- **Behind "More options":**
  - run/kind filters;
  - the `Evolution series` view;
  - `Replay step by step` (Prev/Next only, no speed control).
- **Remove:** the "What was recorded." callout box (design 11; its sentence goes in the panel intro); the 1×/2×/4× speed control; the One transcript / Evolution segmented control.
- **Coach list note:** add `in source runs` to "the largest practice-score jumps, the largest drop" (data-review 10).
- **Listens:** `open-transcript` switches to that coach item. The tab switch is done by the emitter via `EX.explore.open`.

### Code changes (mount `audit`, js/fig-audit.js, assets/fig-audit.css)
- **At rest:**
  - one sentence (computed): `32 audited changes across 11 distinct coach versions (19 distinct changes); 3 judged ARC-specific.`
  - one stacked bar, general vs ARC-specific;
  - the hunk list grouped by coach node. Each row collapses to one line; the 3 ARC-specific rows start open. There is no max-height inner scroll (design 14).
- **Colours:** use the ink ramp, not blue, for the self-edit grid and bars (design 2). Replace the ARC-specific black pill with a small black square glyph and a text label (design 13). Tables use a hairline header in sentence case.
- **"Never tested" wording** (data-review 5): only `source_s4` node 6 (g6) and node 15 (g30) code was never examined. Other g6/g30 rows that share a coach node with a tested pick say `same code as the tested gen-N pick (score)`. Change the "grouped by pick" text to "grouped by coach version".
- **"Select in Fig 5 →"** becomes `Show in tree`, which calls `EX.explore.open('tree', {scroll:true})` + `EX.select('node', …)` (QA 5).
- **Behind "More options":** tag/order/run filters, the per-seed self-edit grid, and Open all / Close all.
- Self-edit counts must agree with the tree after the `utils/**` fix: summary.self_edit is the source of truth. Verify that the rings equal those counts.

---

## 4. Cut list per existing module (what to reuse)

| file | owner | keep / reuse | cut |
|---|---|---|---|
| js/core.js | A | everything (load, fmt, arcGrid/arcPair, tooltip, events, hash, seg, selectBox, scrollHint, mount, bindValues) | nothing; add the §6 APIs; change `runLabel` to use `EX.sym` / plain names |
| js/fig-setup.js | A | SVG/arrow helpers, responsive wide/narrow switch | archive mini-tree, gateway strip, tooltips table, run counts, I_g/I₀ labels |
| js/fig-puzzle.js | B | task pool + band logic, paint editor (palette, drag paint, keyboard paint), check ×2 logic, truth diff, lazy heldout prefetch, hash | run picker + per-run attempt grids, inline 3-row toolbars (move to More), index digits, "Showing the 36 of 120" sentence, Fig 3 link (re-point to Explore) |
| js/fig-results.js | B | dot/CI/band drawing, scales, view code (moves wholesale into `results-detail`), Welch mini-plots (detail) | from the main mount: views, mini-plots, g20/g40 rows, readout, hash, trees lookup, events |
| js/fig-extension.js | C | scales, mean/CI drawing, point drawing, coach_origin repeat detection (for the three-runs toggle); whole old figure → `generations-detail` | from the main mount: seed lines, tokens axis, callouts, table, inset, events, hash |
| js/fig-watch.js (new) | C | `EX.arcGrid` with `diffAgainst`, `EX.arcPair`; copy the heldout-results accessor pattern from fig-replay.js (read only, do not import) | n/a |
| js/fig-tree.js | D | tree layout, ramp fill, run select, detail record, diff renderer, best-so-far chart, transcript lookup | chips, slider, side "files by role" + solved grid (move to More), small multiples default-on |
| js/fig-replay.js | D | list, search, stage, matrix (behind More), heldout accessors | autoplay, outline toggle, stale copy, status words |
| js/fig-transcripts.js | D | tabs, list, turn renderer, puzzle-beside, coach diff | typewriter at rest, speed control, view seg (move series to More), callout box, per-row × |
| js/fig-audit.js | D | grouping by coach node, hunk renderer, bar | blue encodings, pills, max-height scroller, footnote stack, "never tested" logic |

---

## 5. Data and builder changes (builder D only; others request through D)

- In `arcexp/build_explorer_data.py`, `classify_path` puts `utils/**` (at least `utils/git_utils.py`) under **coach**. `touched_coach` becomes true for source_s6 node 4. Rerun and check:
  - every source run's ringed-node count over gens 1–12 equals `summary.self_edit[run]` (1/4/5/1/7/3);
  - the total is 21/72.
- Scrub the absolute local path `/home/user/HyperAgents/...` and the commit hash from the coach Tool-output turn in transcripts.json. Replace them with a repo-relative path (data-review 13).
- Keep data under 9 MB. Report the new sizes.
- No other data changes are needed. B reads ledger tokens from compute.json. C reads extension points, coach_origin and heldout results that already exist.

---

## 6. core.js / index.html / style.css API that builder A must provide

Other builders code against these. If one is missing when they test, they implement a local fallback with the same name inside their IIFE (e.g. `var more = EX.more || function(...){...}`).

**Mount ids**

| main-story figures | Explore panels |
|---|---|
| `#fig-setup` (setup, A) | `#panel-tree` → `tree` |
| `#fig-puzzle` (puzzle, B) | `#panel-replay` → `replay` |
| `#fig-results` (results, B) | `#panel-transcripts` → `transcripts` |
| `#fig-generations` (generations, C) | `#panel-audit` → `audit` |
| `#fig-watch` (watch, C) | `#panel-numbers` → `results-detail` (B), `generations-detail` (C), then static HTML |

Section ids: `setup`, `puzzle`, `results`, `generations`, `watch`, `takeaways`, `explore`, `numbers`, `cost`, `appendix`, `references`.

**Script order:** d3 7.8.5 (cdnjs), core, fig-setup, fig-puzzle, fig-results, fig-extension, fig-watch, fig-tree, fig-replay, fig-transcripts, fig-audit.

**Stylesheets:** style.css, fig-puzzle.css, fig-results.css, fig-extension.css, fig-watch.css, fig-tree.css, fig-replay.css, fig-transcripts.css, fig-audit.css. A links all of them; a builder that does not create its file injects its CSS from JS instead.

**API additions**
- **Lazy mounting in tabs.** `EX.mount(name, fn)` defers `fn` while the mount is inside a hidden `[role=tabpanel]` and runs it on first show. `ctx.onShow(fn)` fires every time the panel is shown, after layout, so modules can re-measure. `ctx.width()` is correct at that point.
- `EX.explore.open(tab, {scroll: true|false})` opens a tab and optionally scrolls to `#explore`. Tab names: `tree | replay | transcripts | audit | numbers`. It emits `tab-shown {tab}`. `EX.explore.current()` returns the open tab name.
- **Event** `tab-shown {tab}`.
- **Plain labels**
  - `EX.ARM_LABEL = {B0:'No coach', I0:'Original coach', Ig:'Self-improved coach', g20:'Generation-20 coach', g40:'Generation-40 coach', xhigh:'Think longer (no coach)'}`.
  - `EX.runLabel(run, {plain:true})` gives e.g. `Original coach, run 3`, `Self-improved coach from s2`, `Generation-40 coach from s1`, `No coach, run 2`, `Think longer`.
  - Without `plain`, it gives the technical label using `EX.sym`.
- **Symbols.** `EX.sym(name, mode)` takes a name `'I0'|'Ig'|'A0'` and a mode `'html'` (the default, returning `<i>I</i><sub>g</sub>`) or `'svg'` (returning a fragment string with `<tspan baseline-shift="sub" font-size="75%">g</tspan>`). For plain text contexts (select options), use `'text'`, which returns `I₀`, `I_g`, `A₀`. Use `'text'` sparingly.
- **Disclosure.** `EX.more(container, label, buildFn, {open:false})` builds a `<details class="more"><summary>label</summary>…</details>`. It calls `buildFn(bodyEl)` lazily on first open and returns `{el, body, open(), close()}`. It is styled as a quiet text summary with a chevron, 15px, ink-muted, and a ≥40px hit area.
- **Roving focus.** `EX.roving(containerEl, itemSelector, {onActivate, orientation:'vertical'|'horizontal'|'grid'})` makes one tab stop; arrows move focus; Enter/Space activates. It returns `{focus(i), refresh()}`.
- **Deep-link seeding** (QA 12). After all figures register, core reads the hash once. If it has `run`/`node`/`task`, core calls `EX.select` with `source:'hash'`, so the Explore modules follow.
- Keep the `select-run`, `select-node`, `select-task`, `open-transcript`, `theme`, `hash` and `figure-ready` events. Main-story figures neither listen nor emit (except Fig 2 and Fig 5's explicit "open in Explore" links).

**style.css changes (A)**
- `[hidden]{display:none !important}` (QA 1).
- New width classes:
  - `l-mid` (max 860px);
  - `l-page` (1040);
  - `l-wide` capped at 1160px with ≥48px side margins at 1280 (design 9).
- Type tokens: `--fs-fig-title:18px; --fs-fig-text:15px; --fs-small:14px; --fs-caption:13px; --fs-axis:13px`.
- Remove the `.fig-hint` styling.
- `.control-label`, `.side-sec`, `table.t thead th`: sentence case, 13px, ink-muted, letter-spacing 0. `table.t thead` gets no fill and a hairline bottom rule (design 7, 13, 24).
- `figure.fig figcaption{padding:0 24px; max-width:90ch}` (16px under 720px; design 8).
- Explore tabs: `.explore-tabs` uses the existing `.tabs` underline style, 15px, ≥44px tall, and scrolls horizontally inside itself on phone with `EX.scrollHint`. Only the active panel is displayed. A clear top divider separates Explore from the story, with more whitespace (≥96px).
- Header: no byline grid. The theme toggle is quiet text "Auto · Light · Dark" (12–13px, the active one underlined; no "THEME" label; design 20).
- **Sidenotes on narrow screens** (design 18): under 1280px, core.js moves each `.sidenote` to after its closing `</p>`, so sentences are not split.
- Buttons: `.btn.primary` is ≥44px tall on phone; `.btn.big` for Fig 5's Next.

---

## 7. Builder assignments (disjoint file ownership)

| builder | owns (may create/edit) | delivers |
|---|---|---|
| **A** | `index.html`, `assets/style.css`, `js/core.js`, `js/fig-setup.js`, `CONTRACT.md` (update to this plan) | page structure §1 with exact copy; header; footnotes (≤5 in the main story); takeaways; Explore tab shell + Numbers static HTML (cost, caveats, appendix, files); captions for all panels; Fig 1 redraw; all §6 APIs and CSS; hash routing for old and new links |
| **B** | `js/fig-puzzle.js`, `assets/fig-puzzle.css`, `js/fig-results.js`, new `assets/fig-results.css` | Fig 2, Fig 3 (mount `results`), mount `results-detail`; caption text for `results-detail` in the report |
| **C** | `js/fig-extension.js`, `assets/fig-extension.css` (new), new `js/fig-watch.js`, new `assets/fig-watch.css` | Fig 4 (mount `generations`), mount `generations-detail`, Fig 5 (mount `watch`); caption for `generations-detail` in the report |
| **D** | `js/fig-tree.js`, `js/fig-replay.js`, `js/fig-transcripts.js`, `js/fig-audit.js` and their 4 css files; `arcexp/build_explorer_data.py` + regenerated `data/*.json` | the 4 Explore modules simplified as in §3; data fixes §5 |

Nobody else edits index.html. B, C and D put any requested prose or caption changes in their report as exact text; A or the orchestrator applies them. Every builder checks its work at 1280 and 400px, light and dark: no console errors, no horizontal page scroll, no label collisions, and nothing grows by more than about 50px after its first render.

---

## 8. Review findings that still apply (after simplification)

**Data**
- [D] **DR1.** Self-edit rings miss `utils/**`, so source_s6 node 4 (the self-improved pick) is unringed. Fix in the builder and the tree.
- [A] **DR2.** Footnote 4 "A₀ beat every edited player" is false. Use the wording in §1.
- [A, D] **DR3.** Transcript caption about prompt grids. Use the new caption.
- [B, A] **DR4.** B0 rep 2 token count is a logging gap. Use ledger tokens in `results-detail` and fix the footnote.
- [D] **DR5.** "Never tested" overstated. Only s4 node 6 and node 15 were never examined.
- [A, B, C, D] **DR6.** Stale figure text. All copy is being rewritten; verify that no stale "sparkline / practice task / second view / grouped by pick / six source runs" remains.
- [B] **DR7.** Title too strong. Becomes "No arm differs detectably…" (in detail). The main title says "scored the same", which is supported by the intervals. The helper and caption must show the intervals.
- [A] **DR8.** "Every number is read from data". Use the softened claim.
- [A] **DR9.** I_g pick wording. Use "changed most favourably; in some runs the only candidate".
- [D] **DR10.** Add "in source runs" to the coach-list note.
- [A] **DR11.** A₀ tooltip wording. Removed with the Fig 1 tooltips; any prose says "each run starts from the untouched player".
- [all] **DR12.** I_g notation. Use `EX.sym` in Explore and plain words in the main story. Fix "In gen-20 coach from s4" [C].
- [D, orchestrator] **DR13.** Scrub the absolute path and commit hash. Exclude `_shots/`, `_directions/`, `CONTRACT.md`, `DESIGN_BRIEF.md`, `SIMPLIFY_PLAN.md` and `.gitignore` from the published files.
- [B, C] **Framing note.** Where hunks are counted, also say "19 distinct changes" (D's audit sentence).

**Design**
- [B, C, D] **D1.** Layout shift. Reserve heights and render skeletons immediately (watch, replay, transcripts especially).
- [D] **D2.** Audit uses blue for data. Switch to the ink ramp.
- [all] **D3.** Notation. See DR12.
- [C] **D4, D5.** Extension labels and inset. Fix in `generations-detail`; the main Fig 4 must have no collisions.
- [D] **D6.** Tree labels and axis titles.
- [A] **D7.** Uppercase control labels. Change the CSS to sentence case.
- [A] **D8.** Caption alignment.
- [A] **D9.** Width classes.
- [B] **D10.** Same cell size for input and answer; drop palette digits.
- [D] **D11, D12.** Transcript callout and control overload.
- [A, D] **D13.** Table header weight; ARC-specific pill.
- [D] **D14.** Audit nested scroll.
- [D] **D15.** Tree chips; diff full width.
- [B, D] **D16.** Segmented controls wrapping at 400px.
- [A] **D17.** Fig 1 craft and dark boxes. Redraw.
- [A] **D18.** Phone sidenotes.
- [A] **D19, D20.** Byline and theme toggle. Simplified.
- [D] **D21.** Replay matrix and list clipping.
- [all] **D22.** Hint lines. Removed.
- [all] **D23.** Type scale. Use the tokens only.
- [A] **D24.** Cost table.
- [C, D] **D25.** Dark mode: seed lines `--ink-2`; tree selection without the grey fill.

**QA**
- [A, D] **Q1.** `[hidden]` overridden by `display:grid`. Add the global rule.
- [D] **Q2.** Dark-mode "darker = higher". Use theme-neutral wording.
- [A, D] **Q3.** Fig 3 stale copy.
- [B, A] **Q4.** Fig 2 says "practice task".
- [D] **Q5.** Audit "Select in Fig 5" doesn't navigate. Use `EX.explore.open('tree',{scroll:true})`.
- [C] **Q6.** Callout ③ unanchored (detail mount).
- [C] **Q7.** Extension at 400px. Both mounts must work at 336px.
- [all] **Q8.** Notation.
- [A core + B, C, D] **Q9.** Too many tab stops. Use `EX.roving`.
- [B, D] **Q10.** Count wording ("the 36 of 120"; solved-fully vs at-least-one).
- [A] **Q11.** Gateway strip separators. The strip is removed; check the facts line wraps cleanly.
- [A] **Q12.** Deep links don't seed `EX.state`. Core seeds them.
- [orchestrator] **Q13.** Publishing hygiene. See DR13.

---

## 9. Acceptance checklist (orchestrator)
1. A first-time reader gets the whole story from the h1, the 3-line summary and Figures 1–3 with no interaction.
2. The main story has exactly 5 figures, each with ≤1 interaction, and no jargon (grep the main-story DOM for `I_g|I₀|B0|pass@2|source_s|payoff_` outside tooltips and footnotes: zero hits).
3. Explore shows exactly one panel at a time. Each opens in a simple state with secondary controls collapsed.
4. Every number matches summary.json, heldout.json and compute.json:
   - 29.3 (30.1/27.9/29.7)
   - 29.7 / 27.9
   - G +0.4 [−1.9, +2.8]
   - Δ −1.8 [−4.2, +0.6]
   - Ig−B0 −1.4 [−4.0, +1.3]
   - 29.7/27.9/29.8/30.3
   - +0.6 [−6.5, +7.8]
   - 41.1
   - $152.23 ($148.03 players, $4.19 coaches)
   - 26.0/27.8/36.0
5. Checked at 1280 and 400px, light and dark: no console errors, no horizontal scroll, no label collisions, no layout jumps.
6. Data stays under 9 MB. Published files exclude the internal docs and screenshot folders.
