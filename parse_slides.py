"""Step 2: slides.pdf -> slides.json  (list of {slide, text}).
Usage: python parse_slides.py --lesson lessons/<id>     (reads <lesson>/slides.pdf, writes <lesson>/slides.json)
       python parse_slides.py some/slides.pdf           (paths relative to the current folder)"""
import argparse, json, os
import pymupdf

ap = argparse.ArgumentParser()
ap.add_argument("pdf", nargs="?", default="slides.pdf")
ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
ap.add_argument("--out", default="slides.json")
a = ap.parse_args()
out = os.path.join(a.lesson, a.out)

doc = pymupdf.open(os.path.join(a.lesson, a.pdf))
data = [{"slide": i + 1, "text": p.get_text().strip()} for i, p in enumerate(doc)]
json.dump(data, open(out, "w"), indent=2)
print(len(data), "slides,", sum(len(d["text"]) < 20 for d in data), "near-empty ->", out)
