"""WER of transcripts against corrected clips (gold/asr/clips.json from eval/asr_clips.py).
For each clip, the transcript segments whose midpoint falls in it are joined and aligned word by word with the
reference after normalization (lowercase, Unicode NFC, punctuation removed, Vietnamese diacritics kept).
'on-screen' = accuracy on reference words that are English content words of the screen on view, the words
the screen hints target.
Usage: python eval/wer.py --lesson lessons/<id> results/asr_none.json results/asr_words.json ..."""
import argparse, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcribe import screen_hints  # noqa: E402


def words(text):
    return re.findall(r"\w+", unicodedata.normalize("NFC", text.lower()))


def align(ref, hyp):
    """Levenshtein alignment -> (errors, set of ref positions matched exactly)."""
    n, m = len(ref), len(hyp)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    ok, i, j = set(), n, m
    while i and j:
        if D[i][j] == D[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            if ref[i - 1] == hyp[j - 1]:
                ok.add(i - 1)
            i, j = i - 1, j - 1
        elif D[i][j] == D[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    return D[n][m], ok


def screen_words(screens, t0, t1):
    """English content words of every screen on view during [t0, t1)."""
    out = set()
    for k, s in enumerate(screens):
        end = screens[k + 1]["start"] if k + 1 < len(screens) else float("inf")
        if s["start"] < t1 and end > t0:
            out |= set(w.lower() for w in screen_hints(s["text"], "words", max_words=10 ** 6).split())
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("transcripts", nargs="+")
    ap.add_argument("--lesson", default=".", help="lesson folder; the other paths are relative to it")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)
    meta = json.load(open(L("gold/asr/clips.json")))
    if not meta.get("corrected"):
        print("warning: clips.json says the references are not corrected yet; these numbers only compare to the draft")
    screens = json.load(open(L("screens.json"))) if os.path.exists(L("screens.json")) else []

    print(f"{'transcript':28s} {'ref words':>9s} {'WER':>7s} {'on-screen words':>16s}")
    for path in a.transcripts:
        tr = json.load(open(L(path)))
        err = n = hit = tot = 0
        for c in meta["clips"]:
            ref = words(open(L(c["ref"])).read())
            hyp = words(" ".join(s["text"] for s in tr if c["start"] <= (s["start"] + s["end"]) / 2 < c["end"]))
            e, ok = align(ref, hyp)
            target = screen_words(screens, c["start"], c["end"])
            idx = [i for i, w in enumerate(ref) if w in target]
            err, n, hit, tot = err + e, n + len(ref), hit + sum(i in ok for i in idx), tot + len(idx)
        print(f"{path:28s} {n:9d} {err / max(n, 1):7.1%} {hit:>9d}/{tot} = {hit / max(tot, 1):.0%}")
