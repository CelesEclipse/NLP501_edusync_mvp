"""Usage: python demo/prepare.py --lesson lessons/<id>
Loads one lesson into the demo folder: alignment.json (one row per slide visit, from the lesson's per-unit
alignment), slides.json / transcript.json / links.json (copied when the lesson has them), slides/slide_NN.png
rendered from the lesson's slides.pdf, and lecture.mp4 as a link to the lesson's video.mp4."""
import argparse, json, os, shutil
import pymupdf

DEMO = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--lesson", required=True)
ap.add_argument("--alignment", default="alignment.json", help="per-unit alignment inside the lesson")
a = ap.parse_args()
L = lambda f: os.path.join(a.lesson, f)
D = lambda f: os.path.join(DEMO, f)

segs = []
for w in json.load(open(L(a.alignment))):
    if segs and segs[-1]["slide"] == w["slide"]:
        segs[-1]["end"] = w["end"]
    else:
        segs.append({"slide": w["slide"], "start": w["start"], "end": w["end"]})
json.dump(segs, open(D("alignment.json"), "w"), indent=1)
print(len(segs), "slide visits,", len({s["slide"] for s in segs}), "slides aligned")

for f in ("slides.json", "transcript.json", "links.json"):
    if os.path.exists(L(f)):
        shutil.copy(L(f), D(f))
    elif os.path.exists(D(f)):
        os.remove(D(f))  # left over from another lesson
print("copied:", [f for f in ("slides.json", "transcript.json", "links.json") if os.path.exists(D(f))])

if os.path.exists(L("slides.pdf")):
    shutil.rmtree(D("slides"), ignore_errors=True)
    os.makedirs(D("slides"))
    for i, page in enumerate(pymupdf.open(L("slides.pdf"))):
        page.get_pixmap(dpi=100).save(D(f"slides/slide_{i+1:02d}.png"))

video = L("video.mp4")
if os.path.lexists(D("lecture.mp4")) and not os.path.islink(D("lecture.mp4")):
    print("demo/lecture.mp4 is a real file; leaving it as it is")
elif os.path.exists(video):
    if os.path.islink(D("lecture.mp4")):
        os.remove(D("lecture.mp4"))
    os.symlink(os.path.relpath(os.path.abspath(video), DEMO), D("lecture.mp4"))
    print("lecture.mp4 ->", video)
else:
    print("no", video, "(download it as the README says); the demo will show slides without video")
