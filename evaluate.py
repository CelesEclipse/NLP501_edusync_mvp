"""Step 6: score alignment files against hand-labeled slide start times.
Usage: python evaluate.py labels.json alignment_a.json alignment_b.json ...
A slide's predicted start = start of the first window assigned to it; unassigned slides count as missed."""
import json, sys
import numpy as np


def to_sec(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


labels = {int(k): to_sec(v) for k, v in json.load(open(sys.argv[1])).items()}
print(f"{'file':32s} {'found':>6s} {'mean':>7s} {'median':>7s} {'<=30s':>6s} {'<=60s':>6s}  missed")
for path in sys.argv[2:]:
    first = {}
    for w in json.load(open(path)):
        first.setdefault(w["slide"], w["start"])
    errs = {s: first[s] - t for s, t in labels.items() if s in first}
    a = np.abs(list(errs.values()))
    missed = [s for s in labels if s not in first]
    print(f"{path:32s} {len(a):>3d}/{len(labels)} {a.mean():6.1f}s {np.median(a):6.1f}s "
          f"{(a <= 30).sum():>3d}/{len(labels)} {(a <= 60).sum():>3d}/{len(labels)}  {missed}")
