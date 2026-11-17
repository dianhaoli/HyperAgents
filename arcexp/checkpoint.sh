#!/bin/bash
# Bundle every run's agent repo (nested git repos are not committed), then commit + push the experiment state.
cd "$(dirname "$0")/.."
for r in exp/runs/*/generate_*/gen_initial/hyperagents; do
  [ -d "$r/.git" ] || continue
  d=$(dirname $(dirname $(dirname "$r")))
  git -C "$r" bundle create "$PWD/$d/agent_repo.bundle" --all >/dev/null 2>&1
done
git add -A >/dev/null 2>&1
git commit -qm "${1:-checkpoint}" >/dev/null 2>&1
for b in arc2-improver claude/determined-johnson-g5g9yj; do
  for i in 1 2 3 4; do git push -q origin HEAD:$b 2>/dev/null && break; sleep $((2**i)); done
done
git log --oneline | head -1
