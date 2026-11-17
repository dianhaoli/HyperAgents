#!/bin/bash
# one-line progress
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json, os, glob
from arcexp.common import gw_status
out = []
for r in sorted(glob.glob('exp/runs/*/config.json')):
    n = r.split('/')[2]
    if n.startswith(('smoke', 'trial')): continue
    c = json.load(open(r))
    a = f'exp/runs/{n}/generate_{n}/archive.jsonl'
    k = len(open(a).read().splitlines()) - 1 if os.path.exists(a) else 0
    tag = n.replace('payoff_', 'p').replace('source_', '').replace('ext_source_', 'x')
    out.append(f"{tag}:{k}{'*' if c.get('done') else ''}")
fin = {}
for l in open('exp/results/final_runs.jsonl'):
    d = json.loads(l); fin[d['run']] = d['heldout']
s = gw_status()
print(' '.join(out))
print('exams:', ' '.join(f"{k.replace('payoff_','')}={100*v:.1f}" for k, v in fin.items()), f"| spent ${s['spent']:.2f}")
PY
