"""Step 6: score alignment files against hand-labeled slide start times.
Usage: python evaluate.py labels.json alignment_a.json alignment_b.json ...
A slide's predicted start = start of the first window assigned to it; unassigned slides count as missed.
'mean' and 'median' cover found slides only. 'all' also scores missed slides, using the start of the next
found slide as their prediction (that is where a viewer clicking the slide would land), so methods that
skip hard slides are not rewarded for it."""
import json, sys
import numpy as np


def to_sec(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


labels = {int(k): to_sec(v) for k, v in json.load(open(sys.argv[1])).items()}
n = len(labels)
print(f"{'file':32s} {'found':>6s} {'mean':>7s} {'median':>7s} {'all':>7s} {'<=5s':>6s} {'<=30s':>6s} {'<=60s':>6s}  missed")
for path in sys.argv[2:]:
    first = {}
    for w in json.load(open(path)):
        first.setdefault(w["slide"], w["start"])
    missed = [s for s in labels if s not in first]
    found = np.abs([first[s] - t for s, t in labels.items() if s in first])
    end = max(first.values())
    pred = {s: first.get(s, min([v for k, v in first.items() if k > s], default=end)) for s in labels}
    a = np.abs([pred[s] - t for s, t in labels.items()])
    mean, med = (found.mean(), np.median(found)) if len(found) else (np.nan, np.nan)
    print(f"{path:32s} {len(found):>3d}/{n} {mean:6.1f}s {med:6.1f}s {a.mean():6.1f}s "
          f"{(found <= 5).sum():>3d}/{n} {(found <= 30).sum():>3d}/{n} {(found <= 60).sum():>3d}/{n}  {missed}")
