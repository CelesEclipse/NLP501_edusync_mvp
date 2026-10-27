"""Steps 3-5: transcript.json + slides.json -> alignment file (one slide per ~30 s window).
Usage: python align.py --method bge-base --out alignment_bge_base.json
Methods: tfidf | bge-small | bge-base.  Decoders: dp (order-constrained) | argmax."""
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
    ap.add_argument("--method", default="bge-base", choices=["tfidf", "bge-small", "bge-base"])
    ap.add_argument("--decode", default="dp", choices=["dp", "argmax"])
    ap.add_argument("--no-normalize", action="store_true")
    ap.add_argument("--window", type=float, default=30)
    ap.add_argument("--penalty", type=float, default=0.15)
    ap.add_argument("--plot", help="optional PNG path for the heatmap with the path drawn on it")
    ap.add_argument("--out", default="alignment.json")
    a = ap.parse_args()

    tr, sl = json.load(open(a.transcript)), json.load(open(a.slides))
    windows = make_windows(tr, a.window)
    sim = similarity(a.method, [w["text"] for w in windows], [d["text"] or " " for d in sl])
    scores = sim if a.no_normalize else normalize(sim)
    path = dp_align(scores, a.penalty) if a.decode == "dp" else scores.argmax(1).tolist()

    json.dump([{"window": i, "start": w["start"], "end": w["end"], "slide": path[i] + 1}
               for i, w in enumerate(windows)], open(a.out, "w"), indent=2)
    print(len(windows), "windows ->", a.out)

    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 6))
        plt.imshow(scores, aspect="auto", cmap="viridis")
        plt.plot(path, range(len(path)), "r-", lw=1.5)
        plt.xlabel("slide"); plt.ylabel("transcript window"); plt.colorbar()
        plt.savefig(a.plot, dpi=150, bbox_inches="tight")
