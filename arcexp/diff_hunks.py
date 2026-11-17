"""Extract every changed hunk of every picked coach vs I_0 (coach files only).

  python3 -m arcexp.diff_hunks   -> exp/results/diff_hunks.json  {pick_id: {"files": [...], "hunks": [{file, text}]}}
Picks: part A I_g (exp/transplants/<run>/) and extension picks (exp/transplants_ext/<run>_g<g>/).
"""
import difflib
import glob
import json
import os

from arcexp.common import EXP, REPO

TEMPLATE = os.path.join(REPO, "agent_template")


def hunks_for(tdir):
    man = json.load(open(os.path.join(tdir, "manifest.json")))
    out = []
    for f in man["files_differing_from_I0"]:
        a = os.path.join(TEMPLATE, f)
        b = os.path.join(tdir, "template", f)
        al = open(a).read().splitlines() if os.path.exists(a) else []
        bl = open(b).read().splitlines() if os.path.exists(b) else []
        diff = list(difflib.unified_diff(al, bl, f"a/{f}", f"b/{f}", n=2, lineterm=""))
        cur = []
        for line in diff[2:]:
            if line.startswith("@@") and cur:
                out.append({"file": f, "text": "\n".join(cur)})
                cur = []
            cur.append(line)
        if cur:
            out.append({"file": f, "text": "\n".join(cur)})
    return man, out


def main():
    res = {}
    for d in sorted(glob.glob(os.path.join(EXP, "transplants", "*"))) + sorted(glob.glob(os.path.join(EXP, "transplants_ext", "*"))):
        if not os.path.exists(os.path.join(d, "manifest.json")):
            continue
        man, hs = hunks_for(d)
        pid = ("A_gen12:" if "/transplants/" in d else "ext:") + os.path.basename(d)
        res[pid] = {"source_run": man["source_run"], "node": man["gen"], "files": man["files_differing_from_I0"], "hunks": hs}
    json.dump(res, open(os.path.join(EXP, "results", "diff_hunks.json"), "w"), indent=1)
    print({k: len(v["hunks"]) for k, v in res.items()})


if __name__ == "__main__":
    main()
