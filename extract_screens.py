"""Screen content of a lesson video -> screens/screen_NNN.png + screens.json (with OCR text).
For lessons without a slides PDF (screen recordings, Zoom/Meet screen shares). A frame is sampled every
--step seconds; a new screen starts when a *stable* frame differs from the current screen's first frame in
more than --change of its pixels (a new page or slide). Small changes (highlighting, the cursor) stay in the
same screen, and the saved image is the screen's last stable frame, so what the teacher marked while
explaining is kept. Screens shown for less than --min-seconds (scrolling, transitions) are dropped.
Text is read with the macOS Vision OCR (Vietnamese + English). Short OCR lines found on more than a third of
the screens (a logo read as "e e", "ee", "e"; a header) are removed, and a screen whose text nearly equals an earlier one's is marked
same_as that screen (pixels are not enough: text pages with one layout look alike when shrunk).
Usage: python extract_screens.py --lesson lessons/<id> [--step 1] [--change 0.2] [--no-ocr]"""
import argparse, collections, difflib, json, os, re
import cv2
import numpy as np

SIZE = (160, 90)


def thumb(frame):
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(cv2.resize(g, SIZE, interpolation=cv2.INTER_AREA), (3, 3), 0).astype(np.int16)


def changed(a, b, tol=20):
    """Fraction of thumbnail pixels whose brightness differs by more than tol."""
    return float((np.abs(a - b) > tol).mean())


def find_screens(video, step, change, still, min_seconds):
    cap = cv2.VideoCapture(video)
    fps, n = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)
    found, cur, prev, i, nxt = [], None, None, 0, 0.0
    while cap.grab():
        t, i = i / fps, i + 1
        if t < nxt:
            continue
        nxt += step
        _, frame = cap.retrieve()
        th = thumb(frame)
        stable = prev is not None and changed(th, prev) < still
        prev = th
        if not stable:
            continue
        if cur is None or changed(th, cur["anchor"]) > change:
            if cur:
                found.append(cur)
            cur = {"start": t, "anchor": th}
        cur.update(last_seen=t + step, frame=frame, thumb=th)
    if cur:
        found.append(cur)
    found = [s for s in found if s["last_seen"] - s["start"] >= min_seconds]
    for s, nxt_s in zip(found, found[1:] + [None]):  # a screen lasts until the next one appears
        s["end"] = nxt_s["start"] if nxt_s else n / fps
    return found


def ocr(path):
    from ocrmac.ocrmac import OCR
    res = OCR(path, recognition_level="accurate", language_preference=["vi-VT", "en-US"]).recognize()
    # boxes are (x, y, w, h), normalized, origin at the bottom left: sort top to bottom, then left to right
    res = sorted(res, key=lambda r: (-round(r[2][1] + r[2][3], 2), r[2][0]))
    return [{"text": t, "conf": round(float(c), 3), "box": [round(float(v), 4) for v in b]} for t, c, b in res]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?", default="video.mp4")
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    ap.add_argument("--step", type=float, default=1.0, help="seconds between sampled frames")
    ap.add_argument("--change", type=float, default=0.2, help="pixel share that must change for a new screen")
    ap.add_argument("--still", type=float, default=0.02, help="max pixel share changing between two samples of a still screen")
    ap.add_argument("--min-seconds", type=float, default=3)
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--out", default="screens.json")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    found = find_screens(L(a.video), a.step, a.change, a.still, a.min_seconds)
    os.makedirs(L("screens"), exist_ok=True)
    out = []
    for k, s in enumerate(found):
        image = f"screens/screen_{k + 1:03d}.png"
        cv2.imwrite(L(image), s["frame"])
        out.append({"id": k + 1, "start": round(s["start"], 1), "end": round(s["end"], 1), "image": image,
                    "same_as": None, "lines": [] if a.no_ocr else ocr(L(image))})

    norm = lambda t: re.sub(r"\W+", "", t.lower())
    seen = collections.Counter(n for s in out for n in {norm(x["text"]) for x in s["lines"]})
    boiler = {n for n, c in seen.items() if len(out) >= 4 and c > len(out) / 3 and len(n) <= 20}
    for s in out:
        s["lines"] = [x for x in s["lines"] if norm(x["text"]) not in boiler]
        s["text"] = "\n".join(x["text"] for x in s["lines"])
    for k, s in enumerate(out):
        for j in range(k):
            if s["text"] or out[j]["text"]:
                same = difflib.SequenceMatcher(None, s["text"], out[j]["text"]).ratio() > 0.9
            else:
                same = changed(found[k]["thumb"], found[j]["thumb"]) < 0.05
            if same:
                s["same_as"] = j + 1
                break
    out = [{k: s[k] for k in ("id", "start", "end", "image", "same_as", "text", "lines")} for s in out]
    json.dump(out, open(L(a.out), "w"), ensure_ascii=False, indent=1)
    dur = [s["end"] - s["start"] for s in out]
    print(f"{len(out)} screens ({sum(s['same_as'] is not None for s in out)} repeats), median {np.median(dur):.0f} s, "
          f"{sum(len(s['lines']) for s in out)} OCR lines -> {L(a.out)}; removed as boilerplate: {sorted(boiler)}")
