"""Evaluate question-to-concept linking against gold/concept_gold.json (34 questions -> gp_1..gp_4 or none).

Every method produces a similarity matrix S (questions x concepts). A question is linked to argmax_j S[i, j] when
max_j S[i, j] >= theta, otherwise to "none". theta is chosen by leave-one-out: for each question, the threshold
that maximises accuracy on the other 33 questions is applied to it, so no question is scored with a threshold
tuned on itself.

Text views
  question      = stem + options (OCR)
  speech        = teacher's speech from the aligned start of the question to the next question (max 90 s)
  concept       = title + formula + English examples + Vietnamese explanation (grammar_points.json)

Methods
  tfidf, bm25            : lexical baselines, question vs concept
  minilm+cues            : the previous system (all-MiniLM-L6-v2 with the hand-written KEYWORD_CUES appended)
  minilm, mminilm, me5   : dense bi-encoders without cues: all-MiniLM-L6-v2 (English),
                           paraphrase-multilingual-MiniLM-L12-v2, multilingual-e5-small
  <model>+speech         : mean of cos(question, concept) and cos(speech, concept)
Metrics: accuracy over all 34 (with none), link precision/recall, and acc@1 on the questions whose gold is a concept
(argmax only, no threshold). Gold "also_ok" alternatives count as correct.
Usage: python eval/eval_concepts.py [--json eval/results/concepts_u4.json]"""
import argparse, json, math, os, re, sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from exercise_align import align_exercises  # noqa: E402

MODELS = {
    "minilm": ("sentence-transformers/all-MiniLM-L6-v2", "", ""),
    "mminilm": ("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "", ""),
    "me5": ("intfloat/multilingual-e5-small", "query: ", "passage: "),
}
LEGACY_CUES = {  # copied from the previous concept_link.py to reproduce it as a baseline
    "gp_1": ["participle", "adjective", "bored", "boring", "moving", "moved", "annoying", "annoyed", "pleased", "pleasing", "-ing", "-ed", "fall asleep", "noise"],
    "gp_2": ["causative", "have", "has", "had", "get", "shoes", "shine", "shined", "repair", "cut", "hair"],
    "gp_3": ["passive", "require", "demand", "suggest", "written", "papers", "ink", "modal", "be written", "should be"],
    "gp_4": ["modifier", "adjective", "noun", "central", "luxury", "hotel", "retail", "wholesale", "sales"],
}


def tokens(text):
    return [w for w in re.findall(r"\w+", text.lower()) if len(w) > 1]


def question_text(ex):
    return f"{ex.get('stem', '')} Options: " + " ".join(f"{k}. {v}" for k, v in ex.get("options", {}).items())


def concept_text(gp, cues=False):
    ex = " ".join(x.get("en", "") for x in gp.get("examples", []) if isinstance(x, dict))
    extra = (" Keywords: " + " ".join(LEGACY_CUES.get(gp["id"], []))) if cues else ""
    return f"{gp.get('title', '')}. Formula: {gp.get('formula', '')}. Examples: {ex}. {gp.get('explanation_vi', '')}{extra}"


def speech_windows(exercises, transcript, max_s=90.0):
    starts = [r["start"] for r in align_exercises(exercises, transcript)]
    out = []
    for k, t0 in enumerate(starts):
        t1 = min(starts[k + 1] if k + 1 < len(starts) and starts[k + 1] > t0 else t0 + max_s, t0 + max_s)
        out.append(" ".join(s["text"] for s in transcript if t0 <= s["start"] < t1))
    return out


def tfidf_matrix(qs, cs):
    from sklearn.feature_extraction.text import TfidfVectorizer
    vec = TfidfVectorizer(token_pattern=r"(?u)\b\w\w+\b").fit(qs + cs)
    Q, C = vec.transform(qs), vec.transform(cs)
    return (Q @ C.T).toarray()


def bm25_matrix(qs, cs, k1=1.5, b=0.75):
    docs = [tokens(c) for c in cs]
    N, avgdl = len(docs), sum(map(len, docs)) / len(docs)
    df = Counter(w for d in docs for w in set(d))
    S = np.zeros((len(qs), N))
    for i, q in enumerate(qs):
        for j, d in enumerate(docs):
            tf = Counter(d)
            for w in set(tokens(q)):
                if w in tf:
                    idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                    S[i, j] += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avgdl))
    return S


_cache = {}


def dense(model_key, qs, cs):
    from sentence_transformers import SentenceTransformer
    name, qp, cp = MODELS[model_key]
    if name not in _cache:
        _cache[name] = SentenceTransformer(name)
    m = _cache[name]
    Q = m.encode([qp + q for q in qs], normalize_embeddings=True)
    C = m.encode([cp + c for c in cs], normalize_embeddings=True)
    return Q @ C.T


def is_ok(pred, gold):
    return pred == gold["label"] or pred in gold.get("also_ok", [])


def evaluate(S, gp_ids, gold):
    n = len(gold)
    best = S.argmax(1)
    best_val = S.max(1)
    pred_link = [gp_ids[j] for j in best]
    # acc@1 on concept questions
    concept_idx = [i for i, g in enumerate(gold) if g["label"] != "none"]
    acc1 = sum(is_ok(pred_link[i], gold[i]) for i in concept_idx) / len(concept_idx)

    def predict(i, theta):
        return pred_link[i] if best_val[i] >= theta else "none"

    cands = sorted(set(np.round(best_val, 6))) + [float("inf")]
    preds = []
    for i in range(n):
        others = [k for k in range(n) if k != i]
        theta = max(cands, key=lambda t: (sum(is_ok(predict(k, t), gold[k]) for k in others), -t))
        preds.append(predict(i, theta))
    acc = sum(is_ok(p, g) for p, g in zip(preds, gold)) / n
    links = [(p, g) for p, g in zip(preds, gold) if p != "none"]
    prec = sum(is_ok(p, g) for p, g in links) / max(len(links), 1)
    rec = sum(1 for p, g in zip(preds, gold) if g["label"] != "none" and is_ok(p, g)) / len(concept_idx)
    return {"acc_with_none_loo": round(acc, 3), "link_precision": round(prec, 3), "link_recall": round(rec, 3),
            "links_made": len(links), "acc1_concept_questions": round(acc1, 3), "n_concept_questions": len(concept_idx)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default="lessons/ece-toeic-starter-u4")
    ap.add_argument("--json")
    ap.add_argument("--file", action="append", default=[], help="saved exercise_concept_links.json to score as deployed")
    ap.add_argument("--theory", action="append", default=[],
                    help="grammar_points.json whose timestamps are scored against the gold theory moments")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    exercises = json.load(open(L("exercises.json")))
    transcript = json.load(open(L("transcript.json")))
    gps = json.load(open(L("grammar_points.json")))
    gold_doc = json.load(open(L("gold/concept_gold.json")))
    if not gold_doc.get("verified"):
        print("note: gold/concept_gold.json is a draft (verified=false)")
    gold_by_id = {g["id"]: g for g in gold_doc["labels"]}
    gold = [gold_by_id[ex["id"]] for ex in exercises]
    gp_ids = [g["id"] for g in gps]

    qs = [question_text(e) for e in exercises]
    sp = speech_windows(exercises, transcript)
    cs = [concept_text(g) for g in gps]
    mats = {
        "majority(none)": None,
        "tfidf": tfidf_matrix(qs, cs),
        "bm25": bm25_matrix(qs, cs),
        "minilm+cues (v1)": dense("minilm", qs, [concept_text(g, cues=True) for g in gps]),
    }
    for key in MODELS:
        mats[key] = dense(key, qs, cs)
        mats[f"{key}+speech"] = (mats[key] + dense(key, sp, cs)) / 2

    results = {}
    print(f"{'method':22s} {'acc(34, LOO θ)':>15s} {'link P':>7s} {'link R':>7s} {'links':>5s} {'acc@1 (concept q)':>18s}")
    for name, S in mats.items():
        if S is None:
            acc = sum(g["label"] == "none" or "none" in g.get("also_ok", []) for g in gold) / len(gold)
            r = {"acc_with_none_loo": round(acc, 3), "link_precision": 0.0, "link_recall": 0.0, "links_made": 0,
                 "acc1_concept_questions": None}
            print(f"{name:22s} {acc:15.1%} {'-':>7s} {'-':>7s} {0:5d} {'-':>18s}")
        else:
            r = evaluate(S, gp_ids, gold)
            print(f"{name:22s} {r['acc_with_none_loo']:15.1%} {r['link_precision']:7.1%} {r['link_recall']:7.1%} "
                  f"{r['links_made']:5d} {r['acc1_concept_questions']:18.1%}")
        results[name] = r
    deployed = {}
    for path in a.file:  # score a saved output exactly as deployed (its own threshold)
        saved = {l["question_id"]: (l.get("grammar_point_id") or "none") for l in json.load(open(path))}
        preds = [saved.get(ex["id"], "none") for ex in exercises]
        n_c = sum(g["label"] != "none" for g in gold)
        links = [(p_, g) for p_, g in zip(preds, gold) if p_ != "none"]
        deployed[path] = {
            "accuracy": round(sum(is_ok(p_, g) for p_, g in zip(preds, gold)) / len(gold), 3),
            "link_precision": round(sum(is_ok(p_, g) for p_, g in links) / max(len(links), 1), 3),
            "link_recall": round(sum(1 for p_, g in zip(preds, gold) if g["label"] != "none" and is_ok(p_, g)) / n_c, 3),
            "links_made": len(links)}
        r = deployed[path]
        print(f"deployed {path}: acc={r['accuracy']:.1%} link P={r['link_precision']:.1%} R={r['link_recall']:.1%} links={r['links_made']}")
    theory = {}
    gold_theory = {t["id"]: t["start"] for t in json.load(open(L("gold/alignment_gold.json"))).get("theory", [])}
    for path in a.theory:
        errs = {g["id"]: round(abs(g["timestamp"] - gold_theory[g["id"]]), 1) for g in json.load(open(path)) if g["id"] in gold_theory}
        theory[path] = {"abs_err_s": errs, "mean_abs_err_s": round(sum(errs.values()) / max(len(errs), 1), 1)}
        print(f"theory timestamps {path}: {errs} mean={theory[path]['mean_abs_err_s']}s")
    if a.json:
        os.makedirs(os.path.dirname(a.json), exist_ok=True)
        json.dump({"gold_verified": gold_doc.get("verified", False), "n_questions": len(gold),
                   "label_counts": Counter(g["label"] for g in gold), "results": results,
                   "deployed": deployed, "theory_timestamps": theory}, open(a.json, "w"), indent=2)
