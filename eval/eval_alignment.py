"""Evaluate exercise-to-speech alignment against gold/alignment_gold.json.

Methods compared (all predict one start time per question):
  screen_start : the time the question's screen first appears (no speech used)
  trigger_first: first segment in the search window that says "câu N" (regex only, no ordering constraint)
  greedy       : exercise_align.align_greedy (left-to-right, previous system)
  dp           : exercise_align.align_dp (monotonic dynamic programming)
  <m>+refine   : the same decoder followed by episode-start refinement (exercise_align.refine_starts)
  file:<path>  : any saved exercise_alignment.json (e.g. the output of an older version)

Metrics over questions whose gold start is not null: accuracy within ±10 s and ±30 s, median and mean absolute
error (s), and the number of order inversions in the prediction (q_k predicted later than q_k+1).
Usage: python eval/eval_alignment.py --lesson lessons/ece-toeic-starter-u4 [--json out.json] [--file old.json]"""
import argparse, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from exercise_align import candidates, decode, question_pattern, start_times  # noqa: E402


def predict(method, exercises, transcript):
    if method == "screen_start":
        return [ex["start"] for ex in exercises]
    if method == "trigger_first":
        out = []
        for ex in exercises:
            pat = question_pattern(ex["number"])
            hit = next((transcript[j]["start"] for j in candidates(ex, transcript) if pat.search(transcript[j]["text"])), None)
            out.append(hit if hit is not None else ex["start"])
        return out
    base, _, refine = method.partition("+")
    picks = decode(exercises, transcript, base, refine == "refine")
    return start_times(exercises, transcript, picks)


def score(pred, gold):
    pairs = [(p, g) for p, g in zip(pred, gold) if g is not None]
    err = [abs(p - g) for p, g in pairs]
    inv = sum(1 for a, b in zip(pred, pred[1:]) if a > b)
    return {
        "n": len(pairs),
        "acc_10s": round(sum(e <= 10 for e in err) / len(err), 3),
        "acc_30s": round(sum(e <= 30 for e in err) / len(err), 3),
        "median_abs_err_s": round(statistics.median(err), 1),
        "mean_abs_err_s": round(statistics.mean(err), 1),
        "order_inversions": inv,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default="lessons/ece-toeic-starter-u4")
    ap.add_argument("--file", action="append", default=[], help="extra saved alignment json(s) to score")
    ap.add_argument("--json", help="write results here")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    exercises = json.load(open(L("exercises.json")))
    transcript = json.load(open(L("transcript.json")))
    gold_doc = json.load(open(L("gold/alignment_gold.json")))
    if not gold_doc.get("verified"):
        print("note: gold/alignment_gold.json is a draft (verified=false) — check it against the video before citing")
    gold_by_id = {q["id"]: q["start"] for q in gold_doc["questions"]}
    gold = [gold_by_id.get(ex["id"]) for ex in exercises]

    results = {}
    for m in ["screen_start", "trigger_first", "greedy", "dp", "greedy+refine", "dp+refine"]:
        results[m] = score(predict(m, exercises, transcript), gold)
    for path in a.file:
        saved = {r["id"]: r["start"] for r in json.load(open(path))}
        results[f"file:{os.path.basename(path)}"] = score([saved.get(ex["id"], ex["start"]) for ex in exercises], gold)

    print(f"{'method':34s} {'n':>3s} {'acc±10s':>8s} {'acc±30s':>8s} {'median':>7s} {'mean':>7s} {'inversions':>10s}")
    for m, r in results.items():
        print(f"{m:34s} {r['n']:3d} {r['acc_10s']:8.1%} {r['acc_30s']:8.1%} {r['median_abs_err_s']:6.1f}s "
              f"{r['mean_abs_err_s']:6.1f}s {r['order_inversions']:10d}")
    if a.json:
        os.makedirs(os.path.dirname(a.json) or ".", exist_ok=True)
        json.dump({"lesson": os.path.basename(a.lesson.rstrip("/")), "gold_verified": gold_doc.get("verified", False),
                   "results": results}, open(a.json, "w"), indent=2)
