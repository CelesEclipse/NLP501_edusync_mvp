"""Proxy check of transcripts without a reference transcript: on-screen word recall = share of the English
content words shown on a screen that the transcript has the teacher saying while that screen is up.
Screen hints raise this by design and can also make Whisper write words that were not said, so it is a proxy
only; judge with eval/wer.py on corrected clips. Also: segment count, English share, consecutive repeats,
mean log-probability (when the transcript has it).
Usage: python eval/asr_screen_terms.py --lesson lessons/<id> results/asr_none.json results/asr_words.json ..."""
import argparse, json, os, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcribe import screen_hints  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("transcripts", nargs="+")
ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
a = ap.parse_args()
L = lambda f: os.path.join(a.lesson, f)
screens = json.load(open(L("screens.json")))
shown = [set(w.lower() for w in screen_hints(s["text"], "words", max_words=10 ** 6).split()) for s in screens]

print(f"{'transcript':28s} {'segs':>5s} {'en':>5s} {'repeats':>7s} {'logprob':>8s} {'on-screen recall':>17s}")
for path in a.transcripts:
    tr = json.load(open(L(path)))
    said = [set() for _ in screens]
    for seg in tr:
        mid = (seg["start"] + seg["end"]) / 2
        k = max([i for i, s in enumerate(screens) if s["start"] <= mid] or [0])
        said[k] |= set(re.findall(r"[a-z][a-z'-]+", seg["text"].lower()))
    hit = sum(len(w & s) for w, s in zip(shown, said))
    total = sum(map(len, shown))
    repeats = sum(x["text"] == y["text"] for x, y in zip(tr, tr[1:]))
    lp = np.mean([s["logprob"] for s in tr]) if tr and "logprob" in tr[0] else float("nan")
    en = sum(s.get("lang") == "en" for s in tr) / max(len(tr), 1)
    print(f"{path:28s} {len(tr):5d} {en:5.0%} {repeats:7d} {lp:8.3f} {hit:>8d}/{total} = {hit / max(total, 1):.0%}")
