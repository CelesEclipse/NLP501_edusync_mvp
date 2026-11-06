"""Steps 3-5: transcript.json + slides.json [+ visual.npz] -> alignment file.
Usage: python align.py --method bge-base --out alignment_bge_base.json                 (text only, ~30 s windows)
       python align.py --method bge-base --visual visual.npz --out alignment_fused.json  (text + video frames, 2 s grid)
       python align.py --method none --visual visual.npz --out alignment_visual.json     (video frames only)
Methods: none | tfidf | bge-small | bge-base.  Decoders: dp (order-constrained) | argmax."""
import argparse, json
import numpy as np


def make_windows(tr, size=30):
    windows, cur, start = [], [], tr[0]["start"]
    for s in tr:
        cur.append(s["text"])
        if s["end"] - start >= size:
            windows.append({"start": start, "end": s["end"], "text": " ".join(cur)})
            cur, start = [], s["end"]
    if cur:
        windows.append({"start": start, "end": tr[-1]["end"], "text": " ".join(cur)})
    return windows


def similarity(method, wtexts, stexts):
    if method == "tfidf":
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer(stop_words="english", sublinear_tf=True, ngram_range=(1, 2)).fit(wtexts + stexts)
        return (vec.transform(wtexts) @ vec.transform(stexts).T).toarray()
    from sentence_transformers import SentenceTransformer
    names = {"bge-small": "BAAI/bge-small-en-v1.5", "bge-base": "BAAI/bge-base-en-v1.5"}
    model = SentenceTransformer(names[method])
    W = model.encode(wtexts, normalize_embeddings=True)
    S = model.encode(stexts, normalize_embeddings=True)
    return W @ S.T


def normalize(sim, k=3):
    """z-score per slide (removes 'popular slide' bias), then smooth over k windows."""
    z = (sim - sim.mean(0)) / (sim.std(0) + 1e-9)
    return np.array([z[max(0, i - k // 2): i + k // 2 + 1].mean(0) for i in range(len(z))])


def visual_scores(sim, min_sim=0.5):
    """z-score per slide over frames that show a slide; frames that match nothing
    (camera on the speaker) get 0 for every slide so the text and the order constraint decide there."""
    shown = sim.max(1) >= min_sim
    v = sim[shown]
    z = np.zeros_like(sim)
    z[shown] = (v - v.mean(0)) / (v.std(0) + 1e-9)
    return z


def dp_align(scores, pen=0.15):
    """Best monotone path: the slide index can only stay or move forward; skipping costs pen per slide."""
    n, m = scores.shape
    D = np.full((n, m), -1e9)
    P = np.zeros((n, m), int)
    D[0] = scores[0]
    for i in range(1, n):
        for j in range(m):
            cand = D[i - 1, : j + 1] - pen * (j - np.arange(j + 1))
            P[i, j] = cand.argmax()
            D[i, j] = cand.max() + scores[i, j]
    path = [int(D[-1].argmax())]
    for i in range(n - 1, 0, -1):
        path.append(int(P[i, path[-1]]))
    return path[::-1]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", default="transcript.json")
    ap.add_argument("--slides", default="slides.json")
    ap.add_argument("--method", default="bge-base", choices=["none", "tfidf", "bge-small", "bge-base"])
    ap.add_argument("--decode", default="dp", choices=["dp", "argmax"])
    ap.add_argument("--no-normalize", action="store_true")
    ap.add_argument("--window", type=float, default=30)
    ap.add_argument("--penalty", type=float, default=0.15)
    ap.add_argument("--visual", help="visual.npz from visual.py; switches to its frame grid and adds image scores")
    ap.add_argument("--w-visual", type=float, default=1.0)
    ap.add_argument("--w-text", type=float, default=0.5)
    ap.add_argument("--min-visual", type=float, default=0.5, help="frames whose best slide match is below this are ignored")
    ap.add_argument("--drop-visual", type=float, default=0.0,
                    help="experiment: hide this fraction of 60 s blocks of frames (simulates a camera that leaves the slides)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--plot", help="optional PNG path for the heatmap with the path drawn on it")
    ap.add_argument("--out", default="alignment.json")
    a = ap.parse_args()

    sl = json.load(open(a.slides))
    if a.method != "none":
        windows = make_windows(json.load(open(a.transcript)), a.window)
        sim = similarity(a.method, [w["text"] for w in windows], [d["text"] or " " for d in sl])
        scores = sim if a.no_normalize else normalize(sim)

    if a.visual:
        vis = np.load(a.visual)
        t = vis["t"]
        units = [{"start": float(s), "end": float(e)} for s, e in zip(t, np.append(t[1:], t[-1] + vis["step"]))]
        vsim = vis["sim"].copy()
        if a.drop_visual:
            block = (t // 60).astype(int)
            hidden = np.random.default_rng(a.seed).random(block.max() + 1) < a.drop_visual
            vsim[hidden[block]] = 0
        fused = a.w_visual * visual_scores(vsim, a.min_visual)
        if a.method != "none":
            # each frame takes the (already normalized) text score of the transcript window it falls in
            idx = np.clip(np.searchsorted([w["start"] for w in windows], t, "right") - 1, 0, len(windows) - 1)
            fused += a.w_text * scores[idx]
        scores = fused
    elif a.method == "none":
        ap.error("--method none needs --visual")
    else:
        units = windows

    path = dp_align(scores, a.penalty) if a.decode == "dp" else scores.argmax(1).tolist()

    json.dump([{"window": i, "start": w["start"], "end": w["end"], "slide": path[i] + 1}
               for i, w in enumerate(units)], open(a.out, "w"), indent=2)
    print(len(units), "units ->", a.out)

    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 6))
        plt.imshow(scores, aspect="auto", cmap="viridis")
        plt.plot(path, range(len(path)), "r-", lw=1.5)
        plt.xlabel("slide"); plt.ylabel("time step (30 s window, or 2 s frame with --visual)"); plt.colorbar()
        plt.savefig(a.plot, dpi=150, bbox_inches="tight")
