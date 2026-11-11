"""Evaluate question extraction and alignment on the multi-source test set (lessons with gold/questions_gold.json).

The gold here differs from U4/U5's alignment_gold.json, which annotates the system's own exercise list. Here the
gold is the list of questions the teacher actually works through, written without looking at the system output.
That lets the test also count questions the system never found. Three measurements:
  extraction : share of gold questions that exercises.py found. A match needs the same number and a similar
               stem/options text (see match_extracted); each extracted question is used once.
  end-to-end : start-time accuracy over ALL gold questions. A question the extractor missed counts as wrong.
               The error statistics (median/mean) cover only the matched questions.
  oracle     : the aligner alone. It gets the gold question list (number + stem + options) and the whole
               video as its search window, so extraction errors and screen timing play no part.
"v1" is exercise_align.py at the baseline commit (run_all.BASELINE_COMMIT), applied to the same inputs.
Results are pooled (micro-averaged over questions) over the main set (Vietnamese sources), its lectures (a teacher
explains) and its practice videos (recorded test audio, no teacher). Lessons whose gold split starts with "extra"
(non-Vietnamese teachers, kept for reference) are pooled separately and left out of the main numbers.
--exercises results/frozen/exercises.json scores the question lists extracted before any change was made with
this test set in view (the "frozen" run), so they can be compared with the current exercises.py.
Usage: python eval/eval_multisource.py [lessons/<id> ...] [--json out.json] [--exercises results/frozen/exercises.json]"""
import argparse, difflib, glob, importlib.util, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from exercise_align import candidates, decode, question_pattern, start_times  # noqa: E402

_spec = importlib.util.spec_from_file_location("run_all", os.path.join(ROOT, "eval", "run_all.py"))
run_all = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_all)


def text_of(q):
    return (q.get("stem") or "") + " " + " ".join((q.get("options") or {}).values())


MIN_SIM = 0.4  # stem+options similarity a same-numbered pair needs (true pairs seen: 0.40-1.00; a Part 2 item vs a Part 3 OCR duplicate: 0.38)


def similarity(g, ex):
    """Best of stem-vs-stem and (stem + options)-vs-(stem + options) difflib ratios: OCR often loses the options
    (or the stem), and comparing a bare stem with stem + options would understate a correct pair."""
    r = lambda a, b: difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return max(r(g.get("stem") or "", ex.get("stem") or ""), r(text_of(g), text_of(ex)))


def match_extracted(gold, exercises):
    """gold question id -> extracted exercise index (or None). Pairs need the same number; the most similar pairs
    (see similarity) are taken first, each side at most once, and only from MIN_SIM up. Numbering
    restarts per part in many videos, so the number alone would pair e.g. Part 1 Q1 with Part 3 Q1."""
    pairs = sorted(((similarity(g, ex), gi, ei)
                    for gi, g in enumerate(gold) for ei, ex in enumerate(exercises) if ex["number"] == g["number"]),
                   reverse=True)
    out, used_g, used_e = {g["id"]: None for g in gold}, set(), set()
    for sim, gi, ei in pairs:
        if sim >= MIN_SIM and gi not in used_g and ei not in used_e:
            out[gold[gi]["id"]] = ei
            used_g.add(gi)
            used_e.add(ei)
    return out


def predict(method, exercises, transcript, v1=None):
    if not exercises:
        return []
    if method == "v1":
        recs = {r["id"]: r["start"] for r in v1.align_exercises(exercises, transcript)}
        return [recs.get(ex["id"], ex["start"]) for ex in exercises]
    if method == "trigger_first":
        out = []
        for ex in exercises:
            pat = question_pattern(ex["number"])
            hit = next((transcript[j]["start"] for j in candidates(ex, transcript) if pat.search(transcript[j]["text"])),
                       None)
            out.append(hit if hit is not None else ex["start"])
        return out
    base, _, refine = method.partition("+")
    return start_times(exercises, transcript, decode(exercises, transcript, base, refine == "refine"))


def errors(pred, gold_starts):
    return [abs(p - g) for p, g in zip(pred, gold_starts)]


def summarise(err, n_total, inversions=None):
    """err: absolute errors of the questions that got a prediction; n_total: all gold questions."""
    r = {"n": n_total, "predicted": len(err),
         "acc_10s": round(sum(e <= 10 for e in err) / n_total, 3) if n_total else None,
         "acc_30s": round(sum(e <= 30 for e in err) / n_total, 3) if n_total else None,
         "median_abs_err_s": round(statistics.median(err), 1) if err else None,
         "mean_abs_err_s": round(statistics.mean(err), 1) if err else None}
    if inversions is not None:
        r["order_inversions"] = inversions
    return r


def evaluate(lesson, v1, exercises_file="exercises.json"):
    L = lambda f: os.path.join(lesson, f)
    doc = json.load(open(L("gold/questions_gold.json")))
    gold = [q for q in doc["questions"] if q.get("start") is not None]
    transcript = json.load(open(L("transcript.json")))
    exercises = json.load(open(L(exercises_file))) if os.path.exists(L(exercises_file)) else []
    meta = json.load(open(L("lesson.json")))
    g_start = [q["start"] for q in gold]
    res = {"lesson": os.path.basename(lesson.rstrip("/")), "platform": meta.get("platform"),
           "channel": meta.get("channel"), "language": meta["language"]["instruction"],
           "genre": doc.get("genre"), "split": doc.get("split"), "gold_verified": doc.get("verified", False), "n_gold": len(gold),
           "n_extracted": len(exercises)}

    # extraction
    m = match_extracted(gold, exercises)
    found = [g for g in gold if m[g["id"]] is not None]
    res["extraction"] = {"recall": round(len(found) / len(gold), 3) if gold else None,
                         "precision": round(len(found) / len(exercises), 3) if exercises else None,
                         "found": len(found)}

    # end-to-end: the full pipeline output, scored on every gold question
    res["end_to_end"] = {}
    for method in ("dp+refine", "v1"):
        pred = predict(method, exercises, transcript, v1)
        err = [abs(pred[m[g["id"]]] - g["start"]) for g in found]
        res["end_to_end"][method] = summarise(err, len(gold))
        res["end_to_end"][method]["_err"] = err

    # oracle question list, whole video as window
    end = max(s["end"] for s in transcript)
    oracle = [{"id": q["id"], "number": q["number"], "stem": q.get("stem") or "", "options": q.get("options") or {},
               "start": 0.0, "end": end, "screens": [None]} for q in gold]
    res["oracle"] = {}
    for method in ("trigger_first", "greedy+refine", "dp+refine", "v1"):
        pred = predict(method, oracle, transcript, v1)
        inv = sum(1 for a, b in zip(pred, pred[1:]) if a > b)
        err = errors(pred, g_start)
        res["oracle"][method] = summarise(err, len(gold), inv)
        res["oracle"][method]["_err"] = err
    return res


def pool(results, part, method):
    err = [e for r in results for e in r[part][method]["_err"]]
    return summarise(err, sum(r["n_gold"] for r in results))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("lessons", nargs="*")
    ap.add_argument("--json")
    ap.add_argument("--exercises", default="exercises.json",
                    help="extracted-question file inside each lesson, e.g. results/frozen/exercises.json")
    a = ap.parse_args()
    lessons = a.lessons or sorted(os.path.dirname(os.path.dirname(p))
                                  for p in glob.glob(os.path.join(ROOT, "lessons/*/gold/questions_gold.json")))
    v1 = run_all.module_from_git("exercise_align.py", "exercise_align_v1")
    results = [evaluate(l, v1, a.exercises) for l in lessons]
    if any(not r["gold_verified"] for r in results):
        print("note: gold/questions_gold.json are drafts (verified=false) — check them against the videos before citing")

    hdr = f"{'lesson':28s} {'genre':8s} {'lang':4s} {'gold':>4s} {'extr':>4s} {'recall':>6s} | {'e2e±10 now':>10s} {'v1':>6s} | {'oracle±10 dp':>12s} {'greedy':>6s} {'trig':>6s} {'v1':>6s} {'median':>7s}"
    print(hdr)
    pct = lambda x: "  -  " if x is None else f"{x:6.1%}"
    for r in results:
        e, o = r["end_to_end"], r["oracle"]
        print(f"{r['lesson'][:28]:28s} {str(r['genre'])[:8]:8s} {r['language']:4s} {r['n_gold']:4d} {r['n_extracted']:4d} {pct(r['extraction']['recall'])} | "
              f"{pct(e['dp+refine']['acc_10s']):>10s} {pct(e['v1']['acc_10s'])} | {pct(o['dp+refine']['acc_10s']):>12s} "
              f"{pct(o['greedy+refine']['acc_10s'])} {pct(o['trigger_first']['acc_10s'])} {pct(o['v1']['acc_10s'])} "
              f"{o['dp+refine']['median_abs_err_s']:6.1f}s")

    pooled = {}
    main = [r for r in results if not str(r["split"]).startswith("extra")]
    for name, rs in (("all", main), ("lecture", [r for r in main if r["genre"] == "lecture"]),
                     ("practice", [r for r in main if r["genre"] == "practice"]),
                     ("extra", [r for r in results if str(r["split"]).startswith("extra")])):
        if not rs:
            continue
        found = sum(r["extraction"]["found"] for r in rs)
        pooled[name] = {"lessons": len(rs), "n_gold": sum(r["n_gold"] for r in rs),
                        "extraction_recall": round(found / max(sum(r["n_gold"] for r in rs), 1), 3),
                        "end_to_end": {m: pool(rs, "end_to_end", m) for m in ("dp+refine", "v1")},
                        "oracle": {m: pool(rs, "oracle", m) for m in ("trigger_first", "greedy+refine", "dp+refine", "v1")}}
        p = pooled[name]
        print(f"POOLED {name:13s} lessons={p['lessons']} gold={p['n_gold']} extraction recall={p['extraction_recall']:.1%} | "
              f"e2e ±10s now {p['end_to_end']['dp+refine']['acc_10s']:.1%} v1 {p['end_to_end']['v1']['acc_10s']:.1%} | "
              f"oracle ±10s dp {p['oracle']['dp+refine']['acc_10s']:.1%} greedy {p['oracle']['greedy+refine']['acc_10s']:.1%} "
              f"trigger {p['oracle']['trigger_first']['acc_10s']:.1%} v1 {p['oracle']['v1']['acc_10s']:.1%}")

    for r in results:  # raw errors are only needed for pooling
        for part in ("end_to_end", "oracle"):
            for v in r[part].values():
                v.pop("_err")
    if a.json:
        os.makedirs(os.path.dirname(a.json) or ".", exist_ok=True)
        json.dump({"lessons": results, "pooled": pooled}, open(a.json, "w"), indent=2, ensure_ascii=False)
