"""Usage: python prepare.py [slides.pdf]
Turns alignment_bge_base.json (one slide per window) into alignment.json (one row per slide),
and optionally renders the PDF pages to slides/slide_NN.png for the demo."""
import json, os, sys
import pymupdf

windows = json.load(open("alignment_bge_base.json"))
segs = []
for w in windows:
    if segs and segs[-1]["slide"] == w["slide"]:
        segs[-1]["end"] = w["end"]
    else:
        segs.append({"slide": w["slide"], "start": w["start"], "end": w["end"]})
json.dump(segs, open("alignment.json", "w"), indent=1)
print(len(segs), "slides aligned")

if len(sys.argv) > 1:
    os.makedirs("slides", exist_ok=True)
    for i, page in enumerate(pymupdf.open(sys.argv[1])):
        page.get_pixmap(dpi=100).save(f"slides/slide_{i+1:02d}.png")
