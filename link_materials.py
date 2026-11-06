"""Step 7b: link every slide to learning materials -> links.json  ({slide: [material, ...]}).
Query for a slide = its text + what the lecturer said while it was on screen (from the alignment).
Documents = materials/catalog.json entries (title + abstract/description); a local materials/<id>.pdf adds
one passage per ~150 words of each page, so the link can point at the right page of the paper.
A material is 'cited' when the slide names it (paper title on the slide, or an alias in the slide title);
otherwise it is 'related' when its best passage is unusually close to this slide (bge-base cosine,
z-scored per passage over all slides).
Usage: python link_materials.py --lesson lessons/<id>   (reads slides/transcript/alignment.json, writes links.json)
--materials is the shared reading library (default: materials/ next to this script), not part of the lesson."""
import argparse, json, os, re
import numpy as np
import pymupdf
from sentence_transformers import SentenceTransformer

QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # bge retrieval instruction
MATERIALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials")


def norm(s):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s.lower()).split())


def slide_queries(slides, units, transcript):
    """Slide text plus the transcript segments whose midpoint falls inside a unit assigned to that slide."""
    spoken = {d["slide"]: [] for d in slides}
    starts = np.array([u["start"] for u in units])
    for seg in transcript:
        i = np.searchsorted(starts, (seg["start"] + seg["end"]) / 2, "right") - 1
        if i >= 0:
            spoken[units[i]["slide"]].append(seg["text"])
    return {d["slide"]: (d["text"] + "\n" + " ".join(spoken[d["slide"]])).strip() for d in slides}


def passages(catalog, folder, words=150):
    out = []
    for m in catalog:
        out.append({"id": m["id"], "page": None, "text": m["title"] + ". " + m["text"]})
        pdf = os.path.join(folder, m["id"] + ".pdf")
        if os.path.exists(pdf):
            for p, page in enumerate(pymupdf.open(pdf), 1):
                w = page.get_text().split()
                for k in range(0, len(w), words):
                    out.append({"id": m["id"], "page": p, "text": " ".join(w[k:k + words])})
    return out


def cited(m, slide_text):
    title_line = norm(slide_text.split("\n", 1)[0])
    if any(re.search(rf"\b{norm(a)}\b", title_line) for a in m["aliases"]):
        return True
    head = " ".join(norm(m["title"].split(":")[-1] if len(m["title"]) > 60 else m["title"]).split()[:5])
    return len(head.split()) >= 2 and head in norm(slide_text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; slides/transcript/alignment/out are relative to it")
    ap.add_argument("--slides", default="slides.json")
    ap.add_argument("--transcript", default="transcript.json")
    ap.add_argument("--alignment", default="alignment.json", help="per-unit alignment from align.py")
    ap.add_argument("--materials", default=MATERIALS)
    ap.add_argument("--k", type=int, default=3, help="max related (non-cited) materials per slide")
    ap.add_argument("--min-score", type=float, default=0.6, help="min cosine similarity for a related link")
    ap.add_argument("--min-z", type=float, default=1.0, help="min z-score (passage vs. all slides) for a related link")
    ap.add_argument("--out", default="links.json")
    a = ap.parse_args()
    for k in ("slides", "transcript", "alignment", "out"):
        setattr(a, k, os.path.join(a.lesson, getattr(a, k)))

    slides = json.load(open(a.slides))
    catalog = {m["id"]: m for m in json.load(open(os.path.join(a.materials, "catalog.json")))}
    queries = slide_queries(slides, json.load(open(a.alignment)), json.load(open(a.transcript)))
    pas = passages(catalog.values(), a.materials)

    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    Q = model.encode([QUERY_PREFIX + queries[d["slide"]] for d in slides], normalize_embeddings=True)
    P = model.encode([p["text"] for p in pas], normalize_embeddings=True, batch_size=32)
    sim = Q @ P.T
    # Same fix as the alignment's per-slide z-score: a long paper has many passages, so its best one is close
    # to every slide.  z-scoring each passage over slides keeps only passages that fit THIS slide unusually well.
    z = (sim - sim.mean(0)) / (sim.std(0) + 1e-9)

    links = {}
    for r, d in enumerate(slides):
        best = {}  # material id -> index of its best passage for this slide
        for j, p in enumerate(pas):
            if p["id"] not in best or z[r, j] > z[r, best[p["id"]]]:
                best[p["id"]] = j
        ranked = sorted(best.items(), key=lambda kv: -z[r, kv[1]])
        cites = [(mid, j) for mid, j in ranked if cited(catalog[mid], d["text"])]
        related = [(mid, j) for mid, j in ranked
                   if (mid, j) not in cites and z[r, j] >= a.min_z and sim[r, j] >= a.min_score][: a.k]
        links[d["slide"]] = []
        for why, group in (("cited", cites), ("related", related)):
            for mid, j in group:
                m, p = catalog[mid], pas[j]
                item = {k: m[k] for k in ("id", "title", "authors", "year", "kind", "url")}
                item.update(why=why, score=round(float(sim[r, j]), 3))
                if p["page"]:
                    item.update(page=p["page"], url=f"{m['pdf']}#page={p['page']}", snippet=p["text"][:240])
                links[d["slide"]].append(item)

    json.dump(links, open(a.out, "w"), indent=1)
    n_cited = sum(x["why"] == "cited" for v in links.values() for x in v)
    print(f"{len(pas)} passages from {len(catalog)} materials; {n_cited} cited + "
          f"{sum(len(v) for v in links.values()) - n_cited} related links -> {a.out}")
