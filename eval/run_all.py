"""Reproduce every number quoted in docs/10_evaluation_results.md and the slides.

Writes eval/results/*.json (metrics only, no lesson content) and eval/results/summary.md.
Baseline "v1" = the code at git commit BASELINE_COMMIT (before the evaluation-driven fixes); its outputs are
recomputed from that commit where possible, otherwise read from lessons/<id>/results/v1/ (gitignored).
Usage: python eval/run_all.py [--skip-concepts]   (concepts loads 3 embedding models, ~1-2 min)"""
import argparse, importlib.util, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
BASELINE_COMMIT = "73d9a62"
U4, U5 = "lessons/ece-toeic-starter-u4", "lessons/ece-toeic-starter-u5"
RES = os.path.join(ROOT, "eval", "results")
PY = sys.executable


def sh(*args):
    out = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"failed: {' '.join(args)}\n{out.stderr[-2000:]}")
    return out.stdout


def module_from_git(path, name):
    src = subprocess.run(["git", "show", f"{BASELINE_COMMIT}:{path}"], cwd=ROOT, capture_output=True, text=True).stdout
    if not src:
        return None
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
    f.write(src)
    f.close()
    spec = importlib.util.spec_from_file_location(name, f.name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def v1_alignment(lesson):
    mod = module_from_git("exercise_align.py", "exercise_align_v1")
    out = os.path.join(ROOT, lesson, "results", "v1", "exercise_alignment.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L = lambda f: os.path.join(ROOT, lesson, f)
    json.dump(mod.align_exercises(json.load(open(L("exercises.json"))), json.load(open(L("transcript.json")))),
              open(out, "w"), ensure_ascii=False)
    return out


def v1_gec():
    mod = module_from_git("feedback.py", "feedback_v1")
    items = json.load(open(os.path.join(ROOT, "eval/gold/gec_heldout.json")))["items"]
    targets = {"BE_VERB", "PARTICIPLE", "CAUSATIVE", "MODAL_TO", "SVA", "WH_DO"}
    eng = mod.GECRuleEngine()
    tp = fp = fn = 0
    for it in items:
        pred, gold = bool(eng.check_sentence(it["text"])[0]), bool(set(it["tags"]) & targets)
        tp += pred and gold
        fp += pred and not gold
        fn += gold and not pred
    p, r = tp / max(tp + fp, 1), tp / max(tp + fn, 1)
    return {"precision": round(p, 3), "recall": round(r, 3), "f1": round(2 * p * r / max(p + r, 1e-9), 3),
            "tp": tp, "fp": fp, "fn": fn}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-concepts", action="store_true")
    a = ap.parse_args()
    os.makedirs(RES, exist_ok=True)
    summary = {"baseline_commit": BASELINE_COMMIT}

    # 1. alignment (u4 = development, u5 = held-out test; the multi-source test set is step 5)
    for lesson, split in ((U4, "dev"), (U5, "test")):
        v1 = v1_alignment(lesson)
        out = os.path.join(RES, f"alignment_{split}.json")
        print(sh("eval/eval_alignment.py", "--lesson", lesson, "--file", v1, "--json", out))
        r = json.load(open(out))["results"]
        r["v1 (commit %s)" % BASELINE_COMMIT] = r.pop(next(k for k in r if k.startswith("file:")))
        summary[f"alignment_{split}"] = {"lesson": os.path.basename(lesson), **r}
        json.dump({"lesson": os.path.basename(lesson), "split": split, "results": r}, open(out, "w"), indent=2)

    # 2. concept linking + theory timestamps (u4)
    if not a.skip_concepts:
        out = os.path.join(RES, "concepts_dev.json")
        v1_links = os.path.join(U4, "results/v1/exercise_concept_links.json")
        v1_gp = os.path.join(U4, "results/v1/grammar_points.json")
        args = ["eval/eval_concepts.py", "--lesson", U4, "--json", out,
                "--file", os.path.join(U4, "exercise_concept_links.json"),
                "--theory", os.path.join(U4, "grammar_points.json")]
        if os.path.exists(os.path.join(ROOT, v1_links)):
            args += ["--file", v1_links, "--theory", v1_gp]
        print(sh(*args))
        summary["concepts_dev"] = json.load(open(out))

    # 3. learner-error detector
    out = os.path.join(RES, "gec_heldout.json")
    print(sh("eval/eval_gec.py", "--json", out))
    summary["gec_heldout"] = json.load(open(out))
    summary["gec_heldout"]["v1 (commit %s) sentence-level" % BASELINE_COMMIT] = v1_gec()

    # 4. ASR proxy (no corrected reference yet, so no WER)
    txt = sh("eval/asr_screen_terms.py", "--lesson", U4, "results/asr_none.json", "results/asr_chunks.json",
             "results/asr_words.json", "results/asr_lines.json")
    summary["asr_proxy_u4"] = txt
    open(os.path.join(RES, "asr_proxy_dev.txt"), "w").write(txt)
    print(txt)

    # 5. multi-source test set: Vietnamese TOEIC videos from other teachers/channels (gold/questions_gold.json).
    #    "frozen" = question lists extracted before any change made with this set in view (results/frozen/, kept
    #    locally like the lessons' other outputs); the second run uses the current exercises.json.
    for name, extra in (("alignment_multisource_frozen", ["--exercises", "results/frozen/exercises.json"]),
                        ("alignment_multisource", [])):
        out = os.path.join(RES, f"{name}.json")
        print(sh("eval/eval_multisource.py", "--json", out, *extra))
        summary[name] = json.load(open(out))["pooled"]

    json.dump(summary, open(os.path.join(RES, "summary.json"), "w"), indent=2, ensure_ascii=False)
    print("wrote eval/results/summary.json")
