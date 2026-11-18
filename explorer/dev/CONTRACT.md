# Explorer contract: how figure modules plug into the page

The page is `explorer/index.html`, styled by `assets/style.css` and run by `js/core.js` (`window.EX`). Each figure is one module that owns its own files. Five agents build modules in parallel, so the rules below exist so no two agents ever touch the same file.

Read first: `explorer/DESIGN_BRIEF.md` (the "Final direction" section wins over anything earlier), `WRITEUP.md`, and `explorer/data/manifest.json` (field-by-field data notes).

## 1. File ownership

| owner | files you may create or edit |
|---|---|
| foundation (done) | `index.html`, `assets/style.css`, `js/core.js`, `js/fig-setup.js`, `CONTRACT.md` |
| module `NAME` | `js/fig-NAME.js` (replace the stub entirely), optionally `assets/fig-NAME.css` |

- **Do not edit `index.html`, `style.css`, `core.js` or another module's files.** If your figure needs different title, explanation, hint or caption text, or a core change, put the exact text or request in your report. The orchestrator will apply it.
- If you add `assets/fig-NAME.css`, say so in your report so it can be linked from `index.html`. Until then, inject your CSS from JS: one `<style id="fx-NAME-css">`, added once.
- Every selector you write must start with `.fx-NAME` (your root element's class), for example `.fx-tree .node`. Never style bare elements or global classes.
- Data changes go through `arcexp/build_explorer_data.py`, then a rerun. Keep `data/` under 9 MB, and report any change you make.

## 2. Page structure your module lives in

```html
<figure class="fig l-page|l-wide" id="fig-NAME">
  <div class="fig-panel">                       <!-- stone panel, 24px padding -->
    <div class="fig-head">
      <div class="fig-title">…</div>            <!-- written in index.html -->
      <p class="fig-text">…</p>
      <p class="fig-hint">…</p>
    </div>
    <div class="mount" data-fig="NAME"><div class="mount-status">Loading figure…</div></div>
  </div>
  <figcaption><b>Figure N</b>: … <span class="src">file.json</span></figcaption>
</figure>
```

The figure title, explanation, hint and caption already live in `index.html`. Your module renders **only inside the `.mount` node**. Clear it first (`node.innerHTML = ''`). Sub-panel titles inside your drawing use `.fig-sub-title` and `.fig-sub-text`.

| # | mount | figure id | width class | section id |
|---|---|---|---|---|
| 1 | `setup` | `fig-setup` | `l-page` (1040) | `question` |
| 2 | `puzzle` | `fig-puzzle` | `l-page` | `puzzle` |
| 3 | `replay` | `fig-replay` | `l-wide` (1240) | `replay` |
| 4 | `results` | `fig-results` | `l-page` | `results` |
| 5 | `tree` | `fig-tree` | `l-wide` | `tree` |
| 6 | `extension` | `fig-extension` | `l-page` | `extension` |
| 7 | `transcripts` | `fig-transcripts` | `l-wide` | `transcripts` |
| 8 | `audit` | `fig-audit` | `l-page` | `audit` |

Content width inside a panel is the width class minus 48 px (minus 32 px below 720 px). At a 400 px viewport the mount is about 336 px wide.

Script order at the end of `index.html`: d3 7.8.5 (cdnjs, global `d3`), `js/core.js`, then `fig-setup`, `fig-puzzle`, `fig-tree`, `fig-results`, `fig-extension`, `fig-replay`, `fig-transcripts`, `fig-audit`. Your file is a plain script. It has no imports or modules, and it is wrapped in an IIFE with `'use strict'`.

## 3. Module skeleton

```js
/* fig-NAME.js — one-line purpose. Data: … Emits: … Listens: … */
(function(){
  'use strict';
  var CSS = '.fx-NAME{…}\n.fx-NAME .x{…}';
  EX.mount('NAME', function(node, ctx){
    if(!document.getElementById('fx-NAME-css')){ var s = document.createElement('style'); s.id = 'fx-NAME-css'; s.textContent = CSS; document.head.appendChild(s); }
    return EX.loadAll(['summary', 'trees']).then(function(d){
      var root = EX.h('div', { 'class': 'fx-NAME' }, node);
      // … draw the at-rest state (complete, no interaction needed) …
      ctx.onResize(function(w){ /* re-layout when the mount width changes */ });
    });   // a returned promise: rejection shows a quiet inline error in the figure
  });
})();
```

- `ctx` holds `{ name, node, figure, panel, width(), onResize(fn), setStatus(text), EX }`. `onResize` is debounced to one animation frame and fires only when the width really changes.
- A thrown error, or a rejected promise, replaces the mount with a quiet inline message. The rest of the page is unaffected. Do not catch errors only to hide them.

## 4. `window.EX` API (from `js/core.js`; full doc comment at the top of that file)

**Data**
- `EX.load(name)` returns a cached `Promise` of `data/<name>.json`.
- `EX.loadAll([names])` loads several at once.
- `heldout.json` is 4.4 MB. Load it lazily, only when the user opens a view that needs it, and never at init unless your at-rest state needs it.

**Format** (`EX.fmt`; inputs are fractions unless noted; negatives use U+2212 "−")
- `pct(0.2926)` → `29.3%`; `pct(x, 0)`; `pctRaw(29.26)` takes a value already in %.
- `pts(0.0042)` → `+0.4`; `ptsU(x)` → `+0.4 points`.
- `ci(lo, hi)` → `[−1.9, +2.8]` in signed points; `ciPct(lo, hi)` → `[28.1%, 31.3%]`.
- `tokens(47645)` → `47.6k`; `tokens(8555520)` → `8.56M`; `int(12345)` → `12,345`.
- `usd(152.227)` → `$152.23`; `usd(x, 4)` for tiny costs.
- `num(x, d)`, `signed(x, d)`, `secs(s)`.

**Runs and terms**
- `EX.runGroup(run)` → `'B0'|'xhigh'|'I0'|'Ig'|'g20'|'g40'|'source'`
- `EX.runLabel(run, {short})`, e.g. `payoff_I0_3` → "I₀ run 3"; `ext_source_s1_g40` → "gen-40 coach from s1".
- `EX.GROUP_ORDER`, `EX.GROUP_LABEL`.
- `EX.derive(summary)` → `{selfEditGens, totalGens, xhighGain, nI0, nIg, metaTokI0, metaTokIg, taskTokI0, taskTokIg, B0min, B0max}`.

**ARC grids** (the palette is fixed and identical in both themes; `EX.ARC[0..9]`)
- `EX.arcGrid(container, grid, opts)` returns an `<svg class="arc">`, or a dashed `.arc-empty` box when the grid is null. Options:
  - `cell` (px) or `maxSize` (longest side, default 160), plus `minCell` (2) and `maxCell` (24);
  - `gap` (default 1: hairline cell gaps drawn in `--rule`);
  - `diffAgainst: truthGrid` outlines wrong cells in `--wrong`; a size mismatch gets a dashed outline around the whole grid;
  - `highlight: [[r, c], …]` (accent outlines);
  - `label` (HTML caption above the grid, `.arc-cap`) and `title` (aria-label);
  - `onCell(r, c, v, evt)` makes the cells clickable;
  - `emptyText`.
- The returned `svg.__arc` holds `{cell, w, h, wrong, cells, setCell(r, c, v)}`. Use `setCell` for painting.
- `EX.arcPair(container, input, output, {labels: [a, b], maxSize, …})` draws input → output at the same scale.
- `EX.gridsEqual(a, b)`.
- Highlights on grids are always outlines, never fills. Correct and wrong states are text, ticks or outlines, never cell fills.

**Tooltip**
- `EX.tooltip.show(html, evtOrEl)`, `.move(evt)`, `.hide()`.
- `EX.tooltip.attach(el, htmlOrFn)` wires hover, focus and tap (tap toggles).
- Never put content *only* in a tooltip. The at-rest figure and a readout line must carry it too.

**Colours**
- In SVG and HTML, prefer CSS variables directly (`fill: var(--ink)`), so themes switch with no JS.
- For canvas or computed colours, use `EX.colors.get('accent')`, `EX.colors.all()` or `EX.colors.ramp(t)`, and redraw on `EX.on('theme', fn)`.

**Events** (cross-figure linking)
- `EX.on(evt, fn)` returns an unsubscribe function; also `EX.off(evt, fn)` and `EX.emit(evt, payload)`.
- `EX.select(kind, payload)` updates `EX.state = {run, node, task}` and emits the event. Use it for user-initiated selections (click, Enter), not for hover.

| event | payload | meaning |
|---|---|---|
| `select-run` | `{run, source}` | a run id from `trees.json` or `compute.json` was pinned |
| `select-node` | `{run, node, source}` | a node of a run's tree was pinned (`node` is a string id, e.g. `"initial"` or `"5"`) |
| `select-task` | `{task, set, source}` | a task was pinned (`set`: `heldout` \| `source` \| `payoff`) |
| `theme` | `{theme, setting}` | the theme changed (`theme` is the effective `light` or `dark`) |
| `hash` | `{section, params}` | the location hash changed |
| `figure-ready` | `{name}` | a module finished init |

- `source` is always your mount name. Ignore events whose `source` is your own mount.
- A listener must never scroll the page, never steal focus, and never open a modal. It updates its own figure quietly, for example by marking the run, switching the default task, or showing a small "linked from Fig 4" note.

**Hash**
- `EX.hash.get()` → `{section, params}` for `#tree?run=source_s1&node=3`.
- `EX.hash.set(section, params, {replace: true})`; `EX.hash.param(k)`.
- Use your section id as `section`. Write the hash only on a user pin, with `replace` (the default). Read it once at init to restore state.

**DOM and UI helpers**
- `EX.h(tag, attrs, parent, text)` builds HTML; `EX.s(...)` builds SVG. `attrs` supports `class`, `style` (object), `html` and `onclick`-style functions.
- `EX.esc(str)` HTML-escapes text. Always escape data text before using `innerHTML`, since transcripts and diffs contain `<`.
- `EX.seg(container, [{value, label}], value, onChange, {label, mono})` → `{set, get, el}` builds a segmented control (`.seg`, `aria-pressed`).
- `EX.selectBox(container, options | [{group, options}], value, onChange, {label, mono})` → `<select class="select">`.
- `EX.scrollHint(scrollEl)` wraps a wide scroller with a right-edge `--panel` fade and a muted "scroll →" hint. It returns `{update, scrollTo(x)}`; start scrolled to the selected item.
- `EX.reduceMotion`; `EX.dur(ms)` returns 0 under reduced motion. Use it for every d3 transition.
- `EX.uid(prefix)` gives unique ids, for SVG markers and similar.

## 5. Shared CSS you should reuse (in `assets/style.css`)

- **Layout:** `.grid-2`, `.grid-side` (main + 300 px side panel, which stacks below 900 px), `.controls` (a wrapping row of controls), `.control-label`, `.surface` (a lighter inset), `.scroll-x`.
- **Controls:**
  - `.btn` with `.primary`, `.quiet` and `.small` variants;
  - `.seg` (segmented control);
  - `.select`;
  - `input.slider` inside `.slider-row` with an `<output>`;
  - `.check`;
  - `.tabs` with `[role=tab][aria-selected]`.
- **Charts:**
  - axes: `.axis`, `.gridline`, `.zero-line`;
  - B0 band: `.b0-band`, `.b0-line`;
  - intervals and points: `.ci-line`, `.mean-tick`, `.dot`, `.dot-ref` (the xhigh reference dot);
  - labels: `.lbl`, `.lbl-sub`, `.halo` (a `--panel` halo behind labels);
  - lines: `.edge`, `.acc-line`, `.acc-text`;
  - states: `.is-sel`, `.is-dim` (35%, only while a selection is pinned), `.hit` (an invisible larger target).
- **Side panels:** `.side-panel`, `table.kv` (key–value record: sans keys, mono values, `--rule` hairlines), `.side-sec`, `.tag`, `.tag.acc|.ok|.no`.
- **Code and text:**
  - `pre.code` with `.wrap`, `.tall` (max 420 px) and `.short` (max 220 px);
  - `pre.code.diff` with lines as `<span class="ln add|del|hunk|meta">`;
  - `.turn` with `.turn-role` (transcript turns);
  - `.notice` (a provenance banner), `.empty` (a missing-state message);
  - `details.collapse`.
- **Grids:** `.arc-row`, `.arc-fig`, `.arc-cap` (`.ok` / `.no`), `.arc-pair`, `.mark-ok`, `.mark-no`.
- **Tables:** `table.t` (head in `--panel-strong`), `tr.sel` (accent wash plus a left bar), `td.r`, `td.m`.

**Tokens:**
- surfaces: `--bg`, `--panel`, `--panel-strong`, `--code-bg`;
- ink: `--ink`, `--ink-2`, `--ink-muted`;
- rules: `--rule`, `--rule-strong`;
- accent: `--accent`, `--accent-hover`, `--accent-pressed`, `--accent-wash`;
- states: `--correct`, `--wrong`;
- score ramp: `--ramp-0..4`;
- type: `--font-sans`, `--font-mono`;
- motion: `--dur` (180 ms).

**Blue (`--accent`) is allowed in only four roles:**
1. selection (ring, dot, row wash);
2. the coach self-edit loop;
3. the I_g pick and the transplant arrow (and extension pick labels);
4. links and footnote marks.

Everything else is ink on stone. Correct and wrong are muted. Never use any UI colour that equals an ARC colour.

## 6. Rules every module follows

1. **Complete at rest.** The default state tells the figure's point with no interaction. Nothing waits for scroll or hover, and there is no `opacity:0` waiting to animate in. There is no autoplay.
2. **No hard-coded numbers.** Every number comes from `data/*.json`. Scores are shown as % to one decimal, and differences in points.
3. **Null result first.** Every score view shows the CIs and the B0 band, and never uses "winner" styling or ranks arms by colour.
4. **Phone (≤ 400 px).**
   - Give the figure a real layout: rows reflow and side panels stack below.
   - Only the tree and the filmstrip may scroll horizontally, inside `EX.scrollHint`.
   - There is no horizontal page scroll, ever.
   - Tap targets are at least 40 px. Hover always has a tap path.
5. **Keyboard.** Every interactive mark is reachable (`tabindex=0`, `role=button`, `aria-label`) and works with Enter and Space. Arrow keys work where the brief says so, and only while focus is inside your figure. The focus ring is visible (the global `:focus-visible` handles HTML; use `.hit` or stroke rings in SVG).
6. **Themes.** Use tokens only, and check light and dark. ARC cells keep their canonical colours in both themes.
7. **Motion.** 150–250 ms, through `EX.dur()`.
8. **Provenance.** Say what is missing and why, for example "No transcript: this input was solved, and only failures were saved." Never show a blank box.
9. **Escaping.** Treat transcript and diff text as untrusted data. Escape it, and never `eval` it or inject it as HTML.
10. **No network** beyond `fetch('data/…')`. No `alert`, `confirm`, `prompt` or `print`. `localStorage` only for per-viewer conveniences, inside try/catch.

## 7. Module specs

### `puzzle`: Fig 2, "Try one" (`js/fig-puzzle.js`, optional `assets/fig-puzzle.css`)
- **Data:** `tasks.json` and `transcripts.json` (`player[]` gives the wrong answers for practice tasks; `solved_replays[]`). Optionally `heldout.json`, lazily, only if you show exam answers.
- **Shows:** a practice task's train pairs, plus the test input and an editable output grid.
  - The output grid has a resize control (rows × cols, defaulting to the test input's size) and a 10-colour palette that is keyboard-operable. There are also "copy input" and "clear" actions.
  - "Check" gives two attempts. After a pass or after the second miss, reveal the truth (wrong cells outlined with `diffAgainst`) and the player's two answers on the same input, with a ✓/✗ for each.
- **Default task:** a practice task with a single test input, small grids (≤ 12×12) and a failed player transcript, so the player's answers exist. Offer 3–5 such tasks in a small selector.
- **At rest:** the train pairs and a blank test grid. The hint is already in the HTML.
- **Emits:** `select-task {task, set}` when the user picks a task.
- **Listens:** nothing required.
- **Phone:** pairs stack, and the palette wraps to 2 rows of 40 px swatches.

### `replay`: Fig 3, replays (`js/fig-replay.js`, optional css)
- **Data:**
  - `transcripts.json`: `evolution_series`, `player` (failed answers) and `solved_replays` (solved answers);
  - `trees.json`: practice scores for the sparkline, and `per_task` per node;
  - `tasks.json`;
  - `heldout.json`: lazy, loaded only when the exam tab opens.
- **Two tabs (`.tabs`):**
  - **"Across generations" (default).** A flicker filmstrip for one evolution-series task.
    - One cell per generation, with a solved/missed tick. Both attempts sit beside the truth, wrong cells are outlined in `--wrong`, and the grids are kept small.
    - Below sits a practice-score sparkline with the current generation's dot in `--accent`.
    - Controls: previous/next, a slider, and a series selector over the 6 series.
  - **"Across exam runs".** Pick an exam task (default: one that splits the runs). Show one row per run (small multiples): the 2 attempts plus truth, with diff outlines.
    - Sort by arm or by "solved by how many runs".
    - The six runs without grids show flag-only rows that say why.
- **Emits:** `select-task`, and `select-run` when a row is pinned.
- **Listens:**
  - `select-task` with `set: heldout`: switch the exam view to that task, if the exam tab is already loaded; otherwise remember it.
  - `select-run`: mark that row.
- **Hash:** `#replay?task=…&run=…`.
- **Phone:** the filmstrip scrolls inside `EX.scrollHint` and starts at the current generation. Exam rows stack.

### `results`: Fig 4, main result (`js/fig-results.js`, optional css)
- **Data:** `summary.json` (B0, I0_runs, Ig_runs, xhigh, G, Delta, Ig_gain_over_B0, extension.per_generation["0"|"12"] for the arm CIs, final_runs) and `compute.json` (tokens per test input, `score_per_10k_tokens`).
- **Left panel:** dot strips for B0 (3), I₀ (6) and I_g (5), each with a mean tick and a 95% CI whisker. Show the B0 band (the min–max of the reps, `.b0-band`), labelled "B0 · two plain attempts · 29.3%" from data. xhigh is a solid `--ink-muted` reference dot, set apart below a hairline and labelled as a reference.
- **Right panel:** G and Δ (and optionally I_g − B0) as interval bars crossing a zero line, with labels on a `--panel` halo.
- **Toggle (`EX.seg`):** "Exam score" / "Score per 10k tokens", which re-plots the left panel from `compute.json` (a log or linear x-axis is your choice; say which). Footnote 8 in the prose already covers B0 rep 2's 0.67 calls per input. Show its dot as recorded.
- **Hover a dot:** a readout line (`aria-live`) with the run label, final node and coach origin (from `trees.json` `coach_origin`, if you load it). Click pins it.
- **Emits:** `select-run {run}`.
- **Listens:** `select-run` (rings that dot, if present).
- **Phone:** rows reflow vertically, and the G/Δ panel stacks under the dot strips.

### `tree`: Fig 5, evolution tree explorer (`js/fig-tree.js`, optional css)
- **Data:** `trees.json` (source runs) and `summary.json` (self_edit).
- **Top:** six small-multiple trees, s1–s6, on a shared 0–40 generation axis; s5 and s6 visibly stop at 12. They double as the run picker (click or Enter), and the selected run is marked with an accent ring or wash.
- **Below:** the detail tree for the selected run.
  - x is the generation, compressed, with a 0–40 scrubber; y is lineage.
  - Fill is the practice score on the `--ramp-0..4` ramp. Unscored nodes are dashed.
  - A thin `--ink` ring marks `touched_coach`. Accent labels mark the I_g pick and `ext_pick_at` (g6, g20, g30, g40).
- **Side panel:** a `table.kv` record with generation, parent, practice score, files changed (role, +/−), coach calls, tokens, cost, and "picked as" (I_g / extension gN).
  - Below it: a 25-task solved grid from `practice.per_task`, then a diff excerpt in `pre.code.diff`, noting when it is truncated (`diff_truncated`, `diff_full_chars`).
- **At rest:** `source_s1`, all generations, with the I_g node preselected.
- **Emits:** `select-node {run, node}` and `select-run {run}`.
- **Listens:**
  - `select-run` for a source run: open it.
  - `select-run` for a pay-off or extension run: open its `coach_origin.source_run` and select `source_node`, with a small "coach of RUN" note.
  - `select-node`.
- **Hash:** `#tree?run=…&node=…`.
- **Keyboard:** arrow keys move between nodes.
- **Phone:** the small multiples sit in a 2×3 grid and the detail tree scrolls (`EX.scrollHint`). The side panel stacks below.

### `extension`: Fig 6, coach generation vs exam score (`js/fig-extension.js`, optional css)
- **Data:** `summary.json` (`extension.per_generation`, `points`, `gen40_minus_gen0`, `paired_changes`) and `trees.json` (`coach_origin.source_node` for each extension and I_g run, to find repeated coach nodes).
- **Plot:**
  - x is the generation (0, 12, 20, 40), placed categorically or proportionally; say which.
  - Each column has its dots, its mean and its 95% CI. Thin `--rule-strong` lines join the same source run across 12, 20 and 40.
  - Annotate that "gen 12 is a different set of runs".
  - Mark repeated coach nodes, e.g. `source_s1` node 1 at 12, 20 and 40: 26.0 / 27.8 / 36.0, with a shared ring or a bracket and a label.
  - Show the B0 band and gen40 − gen0 with its interval.
- **Note:** `ext_source_s4_g20`'s final player was the unedited A₀ (`final_runs[].final_node === 'initial'`). Mark it.
- **Emits:** `select-run`.
- **Listens:** `select-run`.
- **Phone:** the plot fits 336 px. Labels may move below the plot as a key.

### `transcripts`: Fig 7, transcript reader (`js/fig-transcripts.js`, optional css)
- **Data:** `transcripts.json` and `tasks.json` (prompt grids are elided in the text, so draw the puzzle from tasks).
- **Layout:**
  - A picker for player transcripts (60, grouped by `why` or run) and coach transcripts (12).
  - The always-visible `.notice`: "Only failed practice inputs were saved; hidden reasoning is never recorded."
  - The turns in `.turn` blocks: role label in mono, text in `pre.code.wrap`, long turns collapsed with expand. `Elided` segments are shown as muted markers.
  - For a player transcript: the puzzle and the wrong answers (`answers`) beside the truth, with `diffAgainst`.
  - For a coach transcript: a `table.kv` with run, node, generation, parent, practice score vs parent and files changed.
- **Keyboard:** ←/→ step turns, only while focus is inside the figure.
- **Emits:** `select-node {run, node}` (coach) and `select-task {task, set}` (player).
- **Listens:** `select-node`. If a coach transcript exists for that run and node, offer "open coach transcript"; never switch silently.

### `audit`: Fig 8, diff audit (`js/fig-audit.js`, optional css)
- **Data:** `trees.json`: `trees[source_run].diff_audit[]` (pick, file, idx, tag, agreement, reason) and the nodes' `diff` excerpts. `summary.json` provides `diff_audit_summary` (32 / 3 / 29).
- **Shows:** hunks grouped by pick (for example "source_s3 · I_g · node 3"). Each row has its tag (`.tag.no` style for ARC-specific is fine; it is not a "wrong", so you may prefer `.tag` with the text "ARC-specific"), judge agreement and reason, and expands to the diff excerpt.
  - Filter (`EX.seg`): all / ARC-specific only.
  - At rest: the 3 ARC-specific hunks are expanded.
  - Note that the `source_s3` hunks come from one coach picked twice (I_g and g6), and that the `source_s4` g30 coach was never tested.
- **Emits:** `select-node {run, node}` when a pick header is clicked.
- **Listens:** `select-node` (scrolls *within your list only* to that pick's group, if present; never scrolls the page).

## 8. Local testing

- **Serve** (UTF-8, with the artifact skeleton added around `index.html`):
  `python3 /tmp/claude-0/-home-user-HyperAgents/8c16617e-5c2f-5da1-8214-0a60f50ac981/scratchpad/serve.py <port>`
  - Plain `python3 -m http.server` also works, but it sends no charset, so non-ASCII text shows as mojibake there only.
- **Screenshots:** `scratchpad/shoot.js` is an example harness. In Playwright, set `deviceScaleFactor: 1` and use widths 1280 and 400, with `colorScheme` light and dark.
- **d3:** cdnjs is blocked in this sandbox. Route it to the identical npm build in `scratchpad/vendor/d3.min.js` in your Playwright context:
  `ctx.route(/cdnjs\.cloudflare\.com\/ajax\/libs\/d3\/7\.8\.5\/d3\.min\.js/, r => r.fulfill({path: '<scratchpad>/vendor/d3.min.js', contentType: 'application/javascript'}))`
  - Abort Google Fonts too (`/fonts\.(googleapis|gstatic)/`), or the page waits on them. The fallback face looks slightly different from IBM Plex.
- **Before you report done, check:**
  - no console errors;
  - `document.documentElement.scrollWidth === innerWidth` at 400 px;
  - light and dark both look right;
  - keyboard focus is visible;
  - the at-rest state is complete.
