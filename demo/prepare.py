"""Usage: python demo/prepare.py --lesson lessons/<id>
Loads one lesson into the demo folder:
  - For PDF lessons (e.g. cs224n-bert): slides/slide_NN.png rendered from slides.pdf, alignment.json,
    slides.json, links.json, transcript.json, speakers.json.
  - For screen-recording lessons (e.g. ece-toeic-starter-u4): screens/ symlinked from lesson/screens,
    alignment.json built from screens.json, exercises.json, exercise_alignment.json, transcript.json, speakers.json.
  - In both cases: demo/lecture.mp4 is symlinked to lesson/video.mp4."""
import argparse, json, os, shutil
import pymupdf

DEMO = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--lesson", required=True)
ap.add_argument("--alignment", default="alignment.json", help="per-unit alignment inside the lesson")
a = ap.parse_args()
L = lambda f: os.path.join(a.lesson, f)
D = lambda f: os.path.join(DEMO, f)

has_pdf = os.path.exists(L("slides.pdf"))
has_screens = os.path.exists(L("screens.json"))

# 1. Build demo/alignment.json
if os.path.exists(L(a.alignment)):
    segs = []
    for w in json.load(open(L(a.alignment))):
        if segs and segs[-1]["slide"] == w["slide"]:
            segs[-1]["end"] = w["end"]
        else:
            segs.append({"slide": w["slide"], "start": w["start"], "end": w["end"]})
    json.dump(segs, open(D("alignment.json"), "w"), indent=1)
    print(f"{len(segs)} slide visits, {len({s['slide'] for s in segs})} slides aligned")
elif has_screens:
    screens = json.load(open(L("screens.json")))
    segs = []
    for s in screens:
        segs.append({
            "slide": s["id"],
            "start": s["start"],
            "end": s["end"],
            "text": s.get("text", ""),
            "image": s.get("image", f"screens/screen_{s['id']:03d}.png")
        })
    json.dump(segs, open(D("alignment.json"), "w"), indent=1)
    print(f"{len(segs)} screens mapped to alignment.json")
else:
    print("warning: neither alignment.json nor screens.json found")

# 2. Files to copy or clean up
shared_files = [
    "transcript.json", "speakers.json", "lesson.json",
    "exercises.json", "exercise_alignment.json", "screens.json",
    "vocab.json"
]
for f in shared_files:
    if os.path.exists(L(f)):
        shutil.copy(L(f), D(f))
    elif os.path.exists(D(f)):
        os.remove(D(f))

# 3. PDF slides vs Screen images
if has_pdf:
    # Cleanup screens artifacts
    if os.path.islink(D("screens")):
        os.remove(D("screens"))
    elif os.path.isdir(D("screens")):
        shutil.rmtree(D("screens"), ignore_errors=True)

    shutil.rmtree(D("slides"), ignore_errors=True)
    os.makedirs(D("slides"))
    for i, page in enumerate(pymupdf.open(L("slides.pdf"))):
        page.get_pixmap(dpi=100).save(D(f"slides/slide_{i+1:02d}.png"))
    for f in ("slides.json", "links.json"):
        if os.path.exists(L(f)):
            shutil.copy(L(f), D(f))
        elif os.path.exists(D(f)):
            os.remove(D(f))
elif has_screens:
    # Cleanup slides artifacts
    shutil.rmtree(D("slides"), ignore_errors=True)
    for f in ("slides.json", "links.json"):
        if os.path.exists(D(f)):
            os.remove(D(f))

    # Link screens directory
    src_screens = os.path.abspath(L("screens"))
    if os.path.isdir(src_screens):
        if os.path.islink(D("screens")):
            os.remove(D("screens"))
        elif os.path.isdir(D("screens")):
            shutil.rmtree(D("screens"), ignore_errors=True)
        os.symlink(os.path.relpath(src_screens, DEMO), D("screens"))
        print("screens/ ->", src_screens)

    # Link vocab_audio directory
    src_vocab_audio = os.path.abspath(L("vocab_audio"))
    if os.path.isdir(src_vocab_audio):
        if os.path.islink(D("vocab_audio")):
            os.remove(D("vocab_audio"))
        elif os.path.isdir(D("vocab_audio")):
            shutil.rmtree(D("vocab_audio"), ignore_errors=True)
        os.symlink(os.path.relpath(src_vocab_audio, DEMO), D("vocab_audio"))
        print("vocab_audio/ ->", src_vocab_audio)

# 4. Link video
video = L("video.mp4")
if os.path.lexists(D("lecture.mp4")) and not os.path.islink(D("lecture.mp4")):
    print("demo/lecture.mp4 is a real file; leaving it as it is")
elif os.path.exists(video):
    if os.path.islink(D("lecture.mp4")):
        os.remove(D("lecture.mp4"))
    os.symlink(os.path.relpath(os.path.abspath(video), DEMO), D("lecture.mp4"))
    print("lecture.mp4 ->", video)
else:
    print("no", video, "; demo will operate without local video")

copied = [f for f in shared_files if os.path.exists(D(f))]
print(f"[prepare] Done loading {a.lesson}. Copied: {copied}")
