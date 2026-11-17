#!/bin/bash
# Compact progress summary.
cd "$(dirname "$0")/.."
date -u +%H:%M
python3 -m arcexp.orchestrate status | grep -v smoke
grep -h "B0 rep\|xhigh pass" exp/logs/*.log 2>/dev/null | sort -u
python3 -m arcexp.phases status
grep -l "INFRA ABORT\|Traceback" exp/runs/*/run.log 2>/dev/null | sed 's/^/ABORT\/ERROR in: /'
alive() { [ -f exp/logs/$1.pid ] && kill -0 $(cat exp/logs/$1.pid) 2>/dev/null; }
for r in exp/runs/*/; do n=$(basename $r); [ -f $r/config.json ] || continue
  grep -q '"done": true' $r/config.json && continue; alive run_$n || echo "NOT RUNNING: $n"; done
for j in b0_rep0 b0_rep1 b0_rep2 xhigh; do alive $j && echo "job running: $j"; done
true
