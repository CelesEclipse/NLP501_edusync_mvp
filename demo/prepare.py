"""Usage: python prepare.py [slides.pdf] [--alignment alignment_bge_base.json] [--transcript ../transcript.json]
                         [--links ../links.json]
Turns a per-window alignment (one slide per window) into alignment.json (one row per slide visit),
copies the transcript (for search) and slide links (reading list) next to index.html when given,
and optionally renders the PDF pages to slides/slide_NN.png for the demo."""
import argparse, json, os, shutil
import pymupdf

ap = argparse.ArgumentParser()
ap.add_argument("pdf", nargs="?")
ap.add_argument("--alignment", default="alignment_bge_base.json")
ap.add_argument("--transcript")
ap.add_argument("--links")
a = ap.parse_args()

segs = []
for w in json.load(open(a.alignment)):
    if segs and segs[-1]["slide"] == w["slide"]:
        segs[-1]["end"] = w["end"]
    else:
        segs.append({"slide": w["slide"], "start": w["start"], "end": w["end"]})
json.dump(segs, open("alignment.json", "w"), indent=1)
print(len(segs), "slide visits,", len({s["slide"] for s in segs}), "slides aligned")

for src, dst in ((a.transcript, "transcript.json"), (a.links, "links.json")):
    if src and os.path.abspath(src) != os.path.abspath(dst):
        shutil.copy(src, dst)
        print("copied", src, "->", dst)

if a.pdf:
    os.makedirs("slides", exist_ok=True)
    for i, page in enumerate(pymupdf.open(a.pdf)):
        page.get_pixmap(dpi=100).save(f"slides/slide_{i+1:02d}.png")
