# Coaching the Coach: interactive explorer

A static web page (no build step, no server code) that explains and lets people explore an experiment:
can an AI coach (meta agent) that rewrites itself train a better puzzle-solving player (task agent) on
ARC-AGI-2? It cannot: coached players scored about the same as an uncoached one (29.3%), and letting the
model think longer (41.1%) beat all coaching.

This folder is self-contained. Everything below is relative to it.

## Run it locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` from disk (file://) does not work: browsers block
`fetch()` of the data files.

## Files

| Path | What it is |
|---|---|
| `index.html` | The whole article: all prose, figure titles/captions, footnotes, the Explore tabs. Each figure is an empty `<div class="mount" data-fig="NAME">` filled by its script. |
| `assets/style.css` | Design tokens (colors, type, spacing) for light and dark, layout grid, shared components. Change the look here. |
| `assets/fig-*.css` | Styles owned by one figure. |
| `js/core.js` | Shared helpers on `window.EX` (API documented at the top of the file): data loading, ARC grid drawing, tooltips, tabs, theme, events, hash links, number binding. |
| `js/fig-*.js` | One file per figure; each registers with `EX.mount('NAME', fn)`. |
| `data/*.json` | All numbers and records shown. Never type numbers into the page; read them from here. |
| `data/coach/*.json` | Every recorded coaching session, one file per run (loaded on demand). |
| `CONTRACT.md` | Module contract: which file owns which mount, events, data used. |
| `DESIGN_BRIEF.md` | Design principles and the chosen visual direction (beige + one blue accent, Distill / Transformer Circuits style). |
| `SIMPLIFY_PLAN.md` | Why the page is structured the way it is (simple main story, details under Explore). |

## Figures (mount name -> file)

Main story: `setup` (fig-setup.js), `puzzle` (try a puzzle), `results`, `generations` (fig-extension.js),
`watch` (answers side by side), `demo` (traced coaching round).
Explore tabs: `tree` (score over generations per run), `replay` (every exam answer), `transcripts`
(player transcripts + coaching sessions), `audit` (coach code changes), `results-detail` (numbers & method).

## Data

`data/manifest.json` documents every field. Main files: `summary.json` (headline numbers), `trees.json`
(every saved version per run), `compute.json` (score vs tokens), `tasks.json` (puzzles with answers),
`heldout.json` (every exam answer), `transcripts.json`, `demo.json` (traced demo), `coach/`.

Prose numbers are bound to data with attributes like `<span data-v="pct:B0.mean">29.3%</span>`
(`EX.bindValues` replaces the text from `summary.json` at load; the text in the HTML is a fallback).

The data was generated from the experiment repository (github.com/dianhaoli/HyperAgents, branch
`arc2-improver`) by `arcexp/build_explorer_data.py`, `arcexp/build_coach_sessions.py` and
`arcexp/build_demo_bundle.py`. Edit those and re-run them rather than hand-editing JSON.

## Rules to keep when editing

- Keep it simple: one idea and one obvious interaction per main-story figure; plain words (player, coach,
  practice puzzles, exam); jargon only under Explore.
- Colors only through the CSS tokens in `assets/style.css`; check light and dark.
- Must work at 400px wide with no horizontal page scroll.
- Never state a number that is not in `data/`; differences inside their 95% interval are not called effects.
- If publishing as a claude.ai Artifact: `index.html` has no `<html>/<head>/<body>` (the host adds them);
  scripts only from local files or cdnjs pinned versions; no `alert/confirm/print`.

## Hosting elsewhere (GitHub Pages, Vercel, any static host)

Add a standard wrapper around the current `index.html` content: `<!doctype html><html lang="en"><head>`
with `<meta charset="utf-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`,
move the existing `<title>`, `<meta>` and `<link>` tags into the head, and wrap the rest in `<body>`.
