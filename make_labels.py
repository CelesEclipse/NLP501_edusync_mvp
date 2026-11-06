"""Silver labels: first time each slide is on screen, from a visual alignment -> labels_silver.json.
Only for evaluating text-only methods on every slide; check agreement with the hand labels first
(python evaluate.py labels.json results/visual.json). Slides seen for less than --min-seconds are skipped.
Usage: python make_labels.py results/visual.json --out labels_silver.json"""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("alignment")
ap.add_argument("--min-seconds", type=float, default=6)
ap.add_argument("--out", default="labels_silver.json")
a = ap.parse_args()

first, seen = {}, {}
for w in json.load(open(a.alignment)):
    first.setdefault(w["slide"], w["start"])
    seen[w["slide"]] = seen.get(w["slide"], 0) + w["end"] - w["start"]
labels = {str(k): f"{round(t) // 60}:{round(t) % 60:02d}" for k, t in sorted(first.items()) if seen[k] >= a.min_seconds}
json.dump(labels, open(a.out, "w"), indent=1)
print(len(labels), "slides ->", a.out)
