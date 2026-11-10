"""Evaluate the rule-based learner-error detector (feedback.py) on eval/gold/gec_heldout.json.

The held-out sentences were written independently of the rules (synthetic learner chat, verified=false until the
team checks them). Metrics:
  - sentence level: an error sentence is "detected" if the detector makes >= 1 edit; precision/recall/F1 over the
    error-vs-correct decision for in-scope categories (sentences whose only errors are OTHER count as negatives
    for the in-scope detector, but are reported separately).
  - category level: for each target category, recall = share of gold occurrences whose category the detector
    reports on that sentence; precision = share of predicted category labels that are in the gold tags.
  - exact correction: share of in-scope error sentences whose corrected text equals the gold correction
    (case- and space-insensitive), for sentences with only in-scope tags.
Usage: python eval/eval_gec.py [--json eval/results/gec_heldout.json] [--errors]"""
import argparse, json, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from feedback import GECRuleEngine, ERRANT_TYPE  # noqa: E402

TARGETS = list(ERRANT_TYPE)


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def run(items, engine):
    tp = fp = fn = tn = 0
    cat_tp, cat_fp, cat_fn = Counter(), Counter(), Counter()
    exact_ok = exact_n = 0
    other_flagged = other_n = 0
    errors = []
    for it in items:
        gold = set(it["tags"])
        in_scope = gold & set(TARGETS)
        edits, corrected = engine.check_sentence(it["text"])
        pred = {e["category"] for e in edits}
        if gold == {"OTHER"}:
            other_n += 1
            other_flagged += bool(pred)
        if in_scope:
            tp += bool(pred)
            fn += not pred
        else:
            fp += bool(pred)
            tn += not pred
        for c in TARGETS:
            if c in pred and c in gold:
                cat_tp[c] += 1
            elif c in pred:
                cat_fp[c] += 1
            elif c in gold:
                cat_fn[c] += 1
        if in_scope and gold <= set(TARGETS):
            exact_n += 1
            exact_ok += norm(corrected) == norm(it["corrected"])
        if pred != in_scope:
            errors.append({"id": it["id"], "text": it["text"], "gold": sorted(gold), "pred": sorted(pred),
                           "corrected": corrected})
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    per_cat = {}
    for c in TARGETS:
        p = cat_tp[c] / max(cat_tp[c] + cat_fp[c], 1)
        r = cat_tp[c] / max(cat_tp[c] + cat_fn[c], 1)
        per_cat[c] = {"errant_type": ERRANT_TYPE[c], "gold": cat_tp[c] + cat_fn[c], "precision": round(p, 3),
                      "recall": round(r, 3)}
    return {
        "n_items": len(items),
        "sentence": {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": round(prec, 3), "recall": round(rec, 3),
                     "f1": round(2 * prec * rec / max(prec + rec, 1e-9), 3)},
        "per_category": per_cat,
        "exact_correction": {"n": exact_n, "accuracy": round(exact_ok / max(exact_n, 1), 3)},
        "other_only_sentences_flagged": f"{other_flagged}/{other_n}",
    }, errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", default="eval/gold/gec_heldout.json")
    ap.add_argument("--json")
    ap.add_argument("--errors", action="store_true", help="print every misclassified sentence")
    a = ap.parse_args()
    doc = json.load(open(a.gold))
    if not doc.get("verified"):
        print("note: held-out set is a draft (verified=false)")
    res, errs = run(doc["items"], GECRuleEngine())
    s = res["sentence"]
    print(f"items={res['n_items']}  sentence-level P={s['precision']:.1%} R={s['recall']:.1%} F1={s['f1']:.1%} "
          f"(tp={s['tp']} fp={s['fp']} fn={s['fn']} tn={s['tn']})")
    print(f"exact correction on single-scope error sentences: {res['exact_correction']['accuracy']:.1%} "
          f"(n={res['exact_correction']['n']}); OTHER-only sentences flagged: {res['other_only_sentences_flagged']}")
    for c, r in res["per_category"].items():
        print(f"  {c:11s} {r['errant_type']:13s} gold={r['gold']:2d}  P={r['precision']:.1%}  R={r['recall']:.1%}")
    if a.errors:
        for e in errs:
            print(f"  {e['id']} gold={e['gold']} pred={e['pred']} | {e['text']} -> {e['corrected']}")
    if a.json:
        os.makedirs(os.path.dirname(a.json), exist_ok=True)
        json.dump({"gold_verified": doc.get("verified", False), **res}, open(a.json, "w"), indent=2)
