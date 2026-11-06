"""Step 3b: lecture.mp4 + slides.pdf -> visual.npz  (frame x slide image similarity).
Samples one frame every --step seconds and compares it with every rendered slide page.
Usage: python visual.py --lesson lessons/<id> [--step 2]     (reads <lesson>/video.mp4 and slides.pdf)
       python visual.py lecture.mp4 slides.pdf [--out visual.npz]  (paths relative to the current folder)"""
import argparse, os
import cv2
import numpy as np
import pymupdf

SIZE = (96, 54)  # 16:9 thumbnail; small enough to ignore video compression and slide resolution


def feature(gray):
    """Blurred thumbnail, zero mean, unit norm: dot product of two features = normalized cross-correlation."""
    x = cv2.GaussianBlur(cv2.resize(gray, SIZE, interpolation=cv2.INTER_AREA), (3, 3), 0).astype(np.float32).ravel()
    x -= x.mean()
    return x / (np.linalg.norm(x) + 1e-9)


def slide_features(pdf):
    feats = []
    for page in pymupdf.open(pdf):
        pix = page.get_pixmap(dpi=40, colorspace=pymupdf.csGRAY)
        feats.append(feature(np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width)))
    return np.stack(feats)


def frame_features(video, step):
    """Decode sequentially (much faster than seeking) and keep one frame every `step` seconds."""
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    times, feats, i, nxt = [], [], 0, 0.0
    while cap.grab():
        t = i / fps
        if t >= nxt:
            _, frame = cap.retrieve()
            times.append(t)
            feats.append(feature(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)))
            nxt += step
        i += 1
    return np.array(times), np.stack(feats)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?", default="video.mp4")
    ap.add_argument("pdf", nargs="?", default="slides.pdf")
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    ap.add_argument("--step", type=float, default=2.0)
    ap.add_argument("--out", default="visual.npz")
    a = ap.parse_args()
    out = os.path.join(a.lesson, a.out)

    S = slide_features(os.path.join(a.lesson, a.pdf))
    t, F = frame_features(os.path.join(a.lesson, a.video), a.step)
    sim = F @ S.T
    np.savez_compressed(out, t=t, sim=sim, step=a.step)
    best = sim.max(1)
    print(f"{len(t)} frames x {len(S)} slides -> {out}; "
          f"best-match similarity median {np.median(best):.2f}, frames below 0.5: {(best < 0.5).sum()}")
