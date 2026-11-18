# STATUS: COMPLETE

Pre-registration: DESIGN.md / splits.json / analysis.py at `f577cc7`. Extension: DESIGN_v2.md at `991a237`.
All runs, exams and analyses are finished; nothing is running. Results: RESULTS.md.

## Part A (committed plan): done
- Headline: **"Neither improver beat two plain attempts on ARC-AGI-2"**.
- B0 30.1 / 27.9 / 29.7% (mean 29.3%); xhigh pass 41.1%; pilot exams 26.9% and 29.4% (gate passed).
- G = +0.4 pts, 95% Welch CI [-1.9, +2.8]; Delta = -1.8 pts [-4.2, +0.6]; 5 of 6 evolved coaches qualified.

## Part B (extension): done
- Coach at generations 0/12/20/40: means 29.7 / 27.9 / 29.8 / 30.3%. Gen 40 minus gen 0 = +0.6 pts [-6.5, +7.8]:
  flat within the interval. Several picks are the same coach node (DECISIONS 37).
- Diff audit: 32 hunks, 3 ARC-specific, 29 general (all unanimous).

## Spend
$152.23 total (task $148.03, meta $4.19) of the $200 cap.

## Reproduce
See REPRODUCE.md. After a VM restart: `bash arcexp/resume.sh` (no-op now: everything is finished).
