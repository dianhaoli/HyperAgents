# Design brief: ARC-AGI-2 coach experiment explorer

Every agent building the explorer follows this brief. The story and terms come from `WRITEUP.md`. Every number comes from `explorer/data/*.json` and is never typed in by hand.

**Sources.** The user's screenshot of a Transformer Circuits page (`scratchpad/ref/circuits_ref.webp`). Network access to distill.pub and transformer-circuits.pub was blocked in this session, so the conventions below come from the screenshot plus prior knowledge of the Distill template and the Circuits thread. Read the measurements as proportions, not pixel-exact specs.

**What the screenshot shows.**
- **Reading column.** The text block is about 0.48 of the page width. Body text is large (about 18–19 px at 1×) and set on very airy leading (about 1.8).
- **Figures.** Figures break out to about 1.5× the column width. Each sub-panel has a bold title, then 1–2 lines of plain explanation in body-size text, both placed *inside* the figure. Under that comes the drawing.
  - Line work is thin grey.
  - Label strips are filled warm stone.
  - Labels are mono.
- **Caption.** Small grey text in a sans face: "**Figure 1**: one sentence." It is left-aligned to the figure, not the column.
- **References.** Footnote superscripts and bracketed citations `[8]` are a muted blue. Links have a thin grey underline.
- **Colour.** One accent colour, used only to mean one thing ("Attention").

**Distill conventions to adopt.**
- A named grid: `l-body` (text), `l-page` (breakout), `l-screen` (full bleed). Margin asides go in the gutter.
- Hover a footnote to show its text in a popover.
- Interactive figures show a working default state. They invite interaction with a short inline hint ("hover a node", "drag the slider"), not with buttons that shout.
- Small multiples come before a single complex chart.
- One linked selection is shared across views: hover in one view highlights the same item in the others.

---

## (a) Principles

1. **Article first, app second.** The page is read top to bottom like an essay. Interactive figures deepen the text but never replace it. Each figure's at-rest state must tell its point with no interaction.
2. **The null result is the story.** Lead with "Neither improver beat two plain attempts". Show the CIs and the B0 band in every score view. Never sort, colour or animate in a way that suggests a winner.
3. **One accent, one meaning.** Blue means "selected / the thing the text is talking about". Correct and wrong are muted and used only for outcomes. Everything else is ink on beige.
4. **ARC colours belong to ARC.** The ten ARC palette colours appear *only inside puzzle grids*. UI chrome, semantic states and highlights must never look like an ARC colour fill. In grids, show highlights as outlines, rings or hatching, never as fills.
5. **Direct labelling over legends.** Label lines and points where they sit. Legends only when there is truly no room.
6. **Honest provenance.** Each figure states its source file and its caveats in the caption or a footnote. Examples:
   - "transcripts exist only for failed practice inputs"
   - "no hidden reasoning saved"
   - "6 extension runs have no held-out grids"
   - "seed 3 g20 final player = unedited A_0"
7. **Quiet motion.** Transitions are 150–250 ms. There is no autoplay, and reduced-motion is respected.
8. **Same vocabulary everywhere.** Use the same terms in every view: coach, player, source run, pay-off run, I_0, I_g, A_0, B0, generation, node, exam (held-out), practice set.

## (b) Tokens (provisional)

| token | light | warm dark | use |
|---|---|---|---|
| `--bg` | `#F6F1E7` | `#1E1B17` | page ground (beige) |
| `--panel` | `#ECE5D6` | `#2A2621` | figure panels |
| `--panel-strong` | `#E0D7C3` | `#36312A` | label strips, table head |
| `--ink` | `#24211C` | `#ECE6DA` | body text |
| `--ink-muted` | `#6B6458` | `#A79F90` | captions, axis labels |
| `--rule` | `#CFC6B4` | `#4A443A` | hairlines, gridlines, borders |
| `--accent` | `#2F5F98` | `#7FA8D8` | selection, links, footnote marks |
| `--accent-hover` | `#24507F` | `#9BBDE4` | hover |
| `--accent-pressed` | `#1B3E63` | `#B7D0EC` | active/pressed |
| `--accent-wash` | `#2F5F981A` | `#7FA8D826` | selected-row background |
| `--correct` | `#4E7D5B` | `#8DBB98` | solved / match (sage) |
| `--wrong` | `#A65446` | `#D4907F` | failed / mismatch (brick) |
| `--focus` | `#2F5F98` 2px ring + 2px `--bg` offset | `#9BBDE4` | keyboard focus |

- **Accent hue.** Keep the accent a desaturated slate blue, clearly distinct from ARC blue `#0074D9` and ARC cyan `#7FDBFF`.
- **Correct and wrong.** Sage and brick are muted enough to read as different from ARC green `#2ECC40` and ARC red `#FF4136`. Still, use them as text, ticks, outlines or hatching, and never as grid-cell fills.
- **Dark mode.** Use `prefers-color-scheme`, guarded so that `[data-theme]` overrides it.
- **Grid borders in dark mode.** ARC grids keep their canonical colours in both themes. Only the cell gap changes, using `--rule`.

## (c) Typography

- **Body.** Candidates, in preference order:
  1. **Source Sans 3**: humanist and open, close in spirit to the Circuits page's Helvetica/Roboto feel but warmer.
  2. **IBM Plex Sans**: more technical.
  3. **Public Sans**.

  Avoid Inter and Space Grotesk. They read as product UI, not essay.
- **Mono** (grids, ids, code, numbers in tables): **IBM Plex Mono**, or **JetBrains Mono** for diffs and transcripts. Use tabular figures everywhere numbers align.
- **Scale** (desktop / phone):

| role | size / line height | other |
|---|---|---|
| Title | 44/1.15 · 32 | weight 600 |
| Dek | 22/1.45 · 19 | `--ink-muted` |
| H2 | 28/1.25 · 24 | 600 |
| H3 | 20/1.3 | 600 |
| Body | 19/1.75 · 17/1.7 | |
| Figure title | 16/1.3 | 600 |
| Figure explanation | 15/1.5 | |
| Caption | 13/1.45 | `--ink-muted`; "**Figure N**:" bold ink |
| Axis/labels | 12 mono | |
| Footnote superscript | 0.7em | `--accent` |

## (d) Layout grid

- **Text column** (`l-body`): 700 px max, centred.
- **Breakout** (`l-page`): 1040 px max (about 1.5× the column). This is the default for figures.
- **Wide** (`l-wide`): 1240 px, for the tree explorer and the replays.
- **Full bleed** (`l-screen`): only for Fig 3 if needed.
- **Sidenotes.** At ≥1280 px, footnotes and asides sit in the right gutter, 220 px wide, top-aligned to their reference. Below 1280 px they become hover/tap popovers, with numbered notes repeated at the end.
- **Spacing.** 8 px base unit. Paragraph gap 1.1em. Figures get 56 px above and 48 px below.
- **Phone (<720 px).** 16 px gutters and no horizontal page scroll.
  - Figures collapse to the column width.
  - Side-by-side panels stack.
  - Wide figures (tree, replays) scroll inside their own panel with a visible hint.
  - Hover becomes tap. Tap targets are at least 44 px.

## (e) Figure grammar

- **Panel.** `--panel` background, 6 px radius, no shadow, 24 px padding.
- **Inside the panel, top-left:** a bold **title** (states the point, e.g. "Evolved coaches built slightly worse players — within noise"), then 1–2 lines of explanation, then a one-line interaction hint in muted italic ("Hover a run to see its final player").
- **Caption below the panel:** "**Figure N**: …" in caption style, with a source file reference in mono.
- **Axes.** Hairline `--rule` axes with sparse gridlines. Tick labels are mono 12 px muted.
- **Units.** Scores are shown as % with one decimal. Differences are in "points".
- **Reference marks.**
  - Baseline B0: a horizontal band (mean ± range of its 3 reps) in `--panel-strong`, labelled "B0 · two plain attempts · 29.3%".
  - CIs: thin whiskers with caps. Individual runs: small dots.
- **Direct labels.** Arm names sit next to their dot cluster. Series labels sit at the line end.
- **Linking.** One global `selection` state: run id, node id, or task id. Hover is transient; click pins.
  - The selected item turns `--accent` (stroke or ring, plus a wash on rows).
  - Everything not selected stays in place at full contrast. Dim to 35% only when a selection is pinned.
  - The selection syncs across Figs 3–8 and to the URL hash, so views are shareable.
- **Empty and missing states.** Say what is missing and why (e.g. "No transcript: this input was solved — only failures were saved").

## (f) Narrative outline

**Title:** *Does a self-improving coach get better at coaching?*

**Dek:** "We let an LLM agent rewrite itself while it coached another agent at ARC-AGI-2 puzzles. Then we checked whether the rewritten coach was any better."

**Meta line:** `An experiment report · ARC-AGI-2 · Nov 2026`

**TL;DR box** (`--panel`, four bullets drawn from `summary.json`):
- the headline;
- G and Delta with intervals;
- generation 40 − generation 0;
- xhigh 41.1% vs B0 29.3%, plus the $152.23 total.

**1. The question.** Coach vs player and the "a coach that rewrites itself" idea. State what counts as a win.
- **Fig 1 · Two loops** (static diagram, breakout).
  - *Purpose:* show that the coach edits the player's code, and in source runs also its own code (a self-loop arrow in blue).
  - *Panels:*
    - Left: source runs, 6 seeds, 12 gens (s1–s4 to 40), on the 25-task source set, producing an archive tree.
    - Right: pay-off runs. A frozen coach (lock icon) improves A_0 for 8 rounds on the pay-off set. The final player takes the exam (120 tasks / 167 inputs).
    - A fixed "gateway" strip runs underneath: model, effort high, ≤2 calls, 2 answers.
  - *At rest:* the full diagram. Hovering a box highlights its matching term in the text.

**2. What an ARC puzzle is.**
- **Fig 2 · Try one** (interactive, breakout).
  - *Purpose:* make pass@2 and exact-match strictness tangible.
  - *Content:* a practice task's train pairs, plus an editable output grid with a palette.
  - *Interaction:* "Check" gives two attempts, then reveals the truth and the player's answers for this task.
  - *At rest:* the train pairs and a blank test grid, with the hint "Paint the output. You get two tries, like the player."

**3. How coaches evolved.**
- **Fig 3 · Evolution tree explorer** (wide).
  - *Purpose:* show archive trees per source run, with self-edits and picks.
  - *Encoding:*
    - Nodes placed by generation (x) and lineage.
    - Fill shows practice score (single-hue ink ramp, not accent).
    - A coach-edited node gets a ring marker.
    - I_g and extension picks are labelled.
  - *Controls:* a run selector with s1 default, and a generation scrubber up to 40.
  - *Click a node:* opens its diff, meta tokens/cost and per-task scores.
  - *Teaches:* self-edits were rare (21 of 72 gens) and picks often repeat the same node.
  - *At rest:* s1, all generations, I_g node pre-selected.

**4. Main result.**
- **Fig 4 · Exam score by arm** (breakout).
  - *Content:* dot strips for B0 (3), I_0 (6) and I_g (5), plus xhigh as a separate reference marker set apart.
  - *Marks:* each arm shows its mean ± 95% CI. The B0 band runs across the plot.
  - *Side panel:* G and Delta as interval bars crossing zero.
  - *Hover a dot:* shows run id, final node and source coach, and links to Figs 3 and 6.
  - *At rest:* static and fully labelled.

**5. Over generations and against compute.**
- **Fig 5a · Extension.** Means at gen 0/12/20/40 with CIs, plus thin lines joining paired seeds.
  - Annotate that gen 12 is a different run set.
  - Mark repeated coach nodes: s1 node 1 at 12/20/40 scored 26.0/27.8/36.0.
  - Label the panel "Not pre-registered".
- **Fig 5b · Test-time compute.** Exam score vs tokens per test input (log x) for all 23 runs.
  - A toggle switches between raw and normalized (score per 10k tokens).
  - *Teaches:* effort (xhigh) moved the score, coaching did not.
  - Footnote the B0 rep 2 token/call oddity from `compute.json` (0.67 calls per input) rather than hiding it.

**6. Puzzle replays.**
- **Fig 6 · Replays** (wide).
  - *Content:* pick an exam or practice task, then see each run's 2 attempts beside the truth.
  - *Diff overlay:* hatched/outlined wrong cells.
  - *Small multiples:* one row per run.
  - *Sorting:* by arm, or by "solved by how many runs".
  - *At rest:* a task that splits the runs.
  - Six extension runs show flags only (no grids).

**7. Reading the transcripts.**
- **Fig 7 · Transcript reader.** Step through the player prompt/answer and the coach's tool calls for a selected node.
  - A banner explains that only failed inputs were saved and that hidden reasoning is never recorded.
  - Mono text with collapsible long blocks. Keyboard ←/→ steps.

**8. What coaches changed.**
- **Fig 8 · Diff audit.** 32 hunks, grouped by pick, tagged general (29) or ARC-specific (3), with the judges' reasons.
  - *Filter:* show ARC-specific only.
  - *At rest:* the three ARC-specific hunks expanded.

**9. Caveats.** From WRITEUP:
- the coach adaptation;
- no-edit rounds;
- harness bugs;
- broken edits;
- timeouts re-run;
- small n;
- the identical-coach spread;
- seed 3 g20 = A_0.

**10. Cost.** Players $148.03, coaches $4.19, total $152.23. A small horizontal bar by role and phase.

**Appendix.** Experiments in order (1–16), the design choices, and the facts list, from WRITEUP's appendix. Shown as a numbered list with collapsible details.

**Footnotes and references.** DECISIONS item numbers, file paths, and the reference URLs.

## (g) Avoid

- **Colour.**
  - Accent blue on anything that is not selected or a link.
  - Gradients or rainbow scales.
  - Red/green fills on ARC grids.
  - Any UI colour equal to an ARC palette colour.
- **Overclaiming.**
  - Ranking arms with "winner" styling.
  - Hiding CIs or the B0 band.
  - Calling generation 12→40 a trend.
- **Hard-coded numbers.** Every figure binds to the data files.
- **Dashboard look.** Cards with shadows, KPI tiles, dense toolbars, emoji, icons as decoration.
- **Interaction as a gate.** A figure that is empty until clicked, autoplaying animation, or hover-only content without a tap path.
- **Layout.** Lines longer than about 75 characters, centred body text, and justified text.
- **Terms.** Using the repo's "meta/task agent" in UI text without "coach/player" first.

## Final direction

**Winner: Direction A, "Circuits stone"** (`_directions/a/index.html`). Summed judge scores: A 8.5 + 8 = **16.5**, B 7 + 7 = 14, C 6.5 + 7.5 = 14. A won outright, so no tie-break was needed. Both judges named A the closest to the Circuits/Distill references. Its base is a flat stone panel on warm paper, hairline warm-grey rules, IBM Plex Sans at 19/1.75 in a 700 px column, and blue used only where it carries meaning. The grafts below fix A's weak points: the ground is not beige enough, Fig 1 is sparse, there is a single tree, and figures clip on phone.

### Final tokens

This table supersedes §(b). The light ground and panels are warmed (graft 1). `--ink-muted`, `--correct` and `--wrong` are darkened a little in light mode so that 13 px captions and ticks still reach ≥4.5:1 on `--panel`. Every other value is A's as built.

| token | light | warm dark | use |
|---|---|---|---|
| `--bg` | `#F5EFE4` | `#1D1B18` | page ground (beige) |
| `--panel` | `#ECE4D6` | `#27241F` | figure panels (flat, 6 px radius, no shadow) |
| `--panel-strong` | `#DFD5C3` | `#35312A` | label bands, B0 band, gateway strip, table head |
| `--ink` | `#26241F` | `#ECE6DA` | body text |
| `--ink-2` | `#4A463E` | `#CFC7B8` | figure explanation text, secondary labels |
| `--ink-muted` | `#665E52` | `#A0988A` | captions, axis ticks, hints |
| `--rule` | `#CBC1AF` | `#46413A` | hairlines, gridlines, ARC cell gaps |
| `--rule-strong` | `#A39A8A` | `#6E675B` | axes, zero line, panel edges |
| `--accent` | `#2F5F98` | `#7FA8D8` | selection, I_g pick, self-edit loop, links, footnote/citation marks |
| `--accent-hover` | `#24507F` | `#9BBDE4` | hover |
| `--accent-pressed` | `#1B3E63` | `#B7D0EC` | active/pressed |
| `--accent-wash` | `#2F5F981A` | `#7FA8D826` | selected row / pinned background |
| `--correct` | `#476F52` | `#8DBB98` | solved / match (text, tick, outline only) |
| `--wrong` | `#9C4A3D` | `#D4907F` | missed / mismatch (text, tick, outline only) |
| `--ramp-0` | `#E2DACB` | `#3A352D` | node fill, lowest practice score |
| `--ramp-1` | `#BDB4A4` | `#5E574B` | |
| `--ramp-2` | `#8C8473` | `#8E8676` | |
| `--ramp-3` | `#5A5447` | `#C2B9A7` | |
| `--ramp-4` | `#2E2B25` | `#EEE7D9` | node fill, highest practice score |
| focus | 2 px `--bg` + 2 px `--accent` ring | same | keyboard focus |

Contrast checked in light mode on `--panel`: ink 12.3, ink-2 7.4, ink-muted 5.1, accent 5.2, correct 4.5, wrong 4.8. In dark mode on `--panel`: ink-muted 5.4, accent 6.3. `--ramp-0` is nudged from `#E6E0D4` to `#E2DACB` so that low-score nodes still read against the warmer panel.

Dark mode is applied through `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {…} }` and again through `:root[data-theme="dark"]`. There is a visible Theme toggle (light / dark / auto) in the page header, saved in `localStorage` wrapped in try/catch.

### Fonts

- **Body and headings:** IBM Plex Sans 400/500/600 plus italic 400. Fallbacks: `"Helvetica Neue", Helvetica, Arial, system-ui, sans-serif`.
- **Mono** (labels, axes, ids, tree, record table, diff, transcripts): IBM Plex Mono 400/500. Fallbacks: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
- Google Fonts URL (one request):
  `https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap`
  with `<link rel="preconnect" href="https://fonts.googleapis.com">` and `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`.
- Use `font-variant-numeric: tabular-nums` everywhere. The type scale is unchanged from §(c). No serif display face: B's Source Serif was rejected as off-reference.

### Grafts adopted

1. **Warmer beige ground (from B).** `--bg` goes to `#F5EFE4` and `--panel` to `#ECE4D6`, so the beige shows on the page and not only in the panels. A's flat panels and hairlines stay. The TL;DR box gets lighter: a `--panel` fill with a single `--rule` top and bottom hairline, not a `--panel-strong` block.
2. **Numbered sidenotes (from B).** At ≥1280 px they sit in the right gutter, 220 px wide, top-aligned to their mark, and are written as spans inside the paragraph. Below 1280 px they become inline ruled notes (a hairline above and below, `--ink-2`, 15 px). The footnote superscripts stay `--accent`.
3. **Fig 1 rebuilt on B's drawing, with C's annotation.**
   - Explicit loop: coach → player → "practice scores" → back to the coach. The self-edit loop is drawn in `--accent`.
   - A real archive tree (not the dot cluster), with a curved `--accent` arrow labelled "I_g transplanted" running to the frozen coach. This fills the empty right side of the Source panel.
   - A one-line note for the pick: "pick I_g: the changed coach whose children gained most".
   - A full-width `--panel-strong` gateway strip, "fixed for every player".
   - All counts stay bound to data.
4. **Flicker filmstrip as the replay component (from B).** It is not the hero. It comes after the ARC puzzle section (Fig 2), so readers learn what a puzzle is first. Contents:
   - generation cells with solved/missed ticks;
   - wrong cells outlined in `--wrong`;
   - both attempts shown beside the truth;
   - a practice-score sparkline with the current generation dot in `--accent`.
   The grids are kept small so the ARC oranges never dominate a viewport.
5. **Six source trees as small multiples (from C).** They share one 0–40 generation axis (s5/s6 visibly stop at 12) and are drawn in A's stone and hairline style above the detailed tree. They double as the run picker: clicking or pressing Enter loads that seed into the detail view. The detail tree compresses x-spacing, with a gen-axis scrubber for 0–40, to fix the sparse 62 px/generation edges.
6. **Node marks and record table (from C).**
   - A thin `--ink` ring marks nodes where the coach edited its own code. The `--accent` ring stays reserved for selection.
   - The side panel opens with a restrained key–value record table: generation, parent, practice score, files changed, coach calls, tokens, cost, picked as (I_g / extension gN).
   - The table uses mono values, sans keys and `--rule` row hairlines, with no graph-paper texture and no "FIG./§" chrome.
   - A's 25-task solved grid and coloured diff excerpt follow below the table.
   - The same layout is used for replay and transcript side panels.

### Brief changes

- **§(b) Tokens.** Replaced by the final table above. Added `--ink-2`, `--rule-strong` and `--ramp-0..4`.
- **§(c) Typography.** IBM Plex Sans is now the body face, not Source Sans 3. The scale is unchanged.
- **§(d) Sidenotes below 1280 px.** These are now inline ruled notes, not hover/tap popovers, so no content needs hover.
- **§(d) Phone.** Every figure needs a real phone layout, not just a scroller:
  - Fig 1 gets a stacked vertical version below 720 px: Source loop above, the gateway strip as a horizontal band, then Pay-off runs.
  - The result chart reflows rows vertically.
  - Wide figures that must still scroll inside their panel (tree, filmstrip) get a right-edge fade in `--panel` plus a muted "scroll →" hint, and start scrolled to the selected item.
- **§(e) Figure grammar.** The figure title and 1–2 lines of explanation sit inside the panel, above the drawing. The caption "**Figure N**:" sits below it with a mono source-file reference. Blue is allowed in only four roles:
  - selection (node ring, run dot, row wash);
  - the coach self-edit loop;
  - the I_g pick and transplant arrow;
  - links, footnote and citation marks.
- **§(e) Reference marks.** xhigh is drawn as a solid `--ink-muted` reference dot, set apart from the compared arms. The G and Δ intervals are drawn crossing zero, with labels on a `--panel` halo.
- **§(f) Narrative.** The order is: TL;DR, Fig 1 (two loops), Fig 2 (ARC puzzle), the replay filmstrip, the result chart, then the tree (small multiples, then the detail view). The null result is stated in the TL;DR, not in a hero figure.
- **§(g) Avoid.** Add: graph-paper or grid textures; cool blue-grey rules; serif display faces; mono numerals inline in body sentences (keep them in tables and figures); a saturated ARC grid as the first full-width image.
