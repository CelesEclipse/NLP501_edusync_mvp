"""Align extracted exercise questions to the moment the teacher starts working on them in transcript.json.

Two decoders share one scoring function:
  - 'dp'     : monotonic dynamic programming (global optimum). Every question is either matched to a transcript
               segment or left unmatched, matched segments must have strictly increasing start times, and the total
               score over the lesson is maximised:
                   D[k][j] = s(k, j) + max(0, max{ D[k'][j'] : k' < k, t(j') < t(j) })
               computed with a prefix maximum over all earlier states sorted by time, then backtracked.
  - 'greedy' : the earlier left-to-right search (each question takes its best segment after the previous one).
               Kept as a baseline for eval/eval_alignment.py.

Score of question k at segment j (same for both decoders):
    s(k, j) = 25 * trigger(k, j) + 2 * |tokens(question k) ∩ tokens(segment j)| + 3 * on_screen(k, j)
trigger = the segment says "câu (số) N / question N / số N" (N in digits or Vietnamese words) and the number is not
preceded by "text", "page", "trang"; on_screen = the segment midpoint lies in the question's screen window.
Only segments within [screen start - 30 s, screen end + 120 s] are candidates and a segment needs s >= 3.
A "câu N" mention whose next 60 s share no word with the question only scores 2 instead of 25 (it usually refers to a
homonymous question of another exercise). After decoding, each start is moved back over the immediately preceding
segments that share a content word with the question (the teacher often reads the stem before naming the number).
Unmatched questions fall back to their screen start time, clamped between their neighbours ("matched": false).

Outputs <lesson>/exercise_alignment.json.
Usage: python exercise_align.py --lesson lessons/<id> [--method dp|greedy] [--out exercise_alignment.json]"""
import argparse, bisect, json, os, re

NUM_WORDS_VI = {
    1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm",
    6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười",
    11: "mười một", 12: "mười hai", 13: "mười ba", 14: "mười bốn", 15: "mười lăm",
    16: "mười sáu", 17: "mười bảy", 18: "mười tám", 19: "mười chín", 20: "hai mươi"
}

W_TRIGGER, W_OVERLAP, W_SCREEN = 25.0, 2.0, 3.0
W_TRIGGER_UNSUPPORTED = 2.0   # "câu N" with none of the question's words in the next CONTEXT_S seconds
CONTEXT_S = 60.0
MIN_SCORE = 3.0
WINDOW_BEFORE, WINDOW_AFTER = 30.0, 120.0


ORDINAL_VI = {1: "nhất", 4: "tư"}
STOPWORDS = set("""the and for are was were has have had with that this from you your our their its his her they she him
not but can will would should could may might must all any each into out per one two three four five what which who whom
whose when where why how than then them there these those very just also only most more some such own other about after
before over under again once here both few nor too off down shall does did doing being been được những các cái này thì
chúng mình một của cho với trong khi nếu như cũng đây đó rồi nhé nha thôi vậy""".split())


def question_pattern(num):
    """Regex for a spoken reference to question `num`: 'câu (số|thứ|hỏi số) N', 'question/number N', 'số N'.
    N may be digits or a Vietnamese number word; not preceded by 'text', 'page', 'part' or 'trang'."""
    words = [w for w in (NUM_WORDS_VI.get(num), ORDINAL_VI.get(num)) if w]
    word_clause = "".join(f"|{w}" for w in words)
    return re.compile(
        rf"(?<!text\s)(?<!page\s)(?<!part\s)(?<!trang\s)\b(?:câu\s+hỏi\s+số|câu\s+số|câu\s+thứ|câu|question|number|bài\s+tập|số)\s*({num}{word_clause})\b",
        re.I
    )


def token_set(text):
    """Lower-cased content words (length > 2, not a stopword)."""
    return set(w for w in (x.lower() for x in re.findall(r"\w+", text)) if len(w) > 2 and w not in STOPWORDS)


def candidates(ex, transcript):
    """Indices of transcript segments inside the question's search window."""
    lo, hi = ex["start"] - WINDOW_BEFORE, ex["end"] + WINDOW_AFTER
    return [j for j, seg in enumerate(transcript) if lo <= seg["start"] <= hi and seg["end"] >= lo]


def segment_score(ex, seg, pat=None, ex_tokens=None, context_tokens=None):
    """Score of question `ex` starting at `seg`. `context_tokens` = content words spoken in the CONTEXT_S seconds
    from this segment on; a "câu N" mention only gets the full trigger weight when that context shares a word with
    the question (verifies that the announced number refers to this question and not to a homonymous one in another
    exercise, e.g. the book's Exercise A while Exercise B is on screen)."""
    pat = pat or question_pattern(ex["number"])
    ex_tokens = ex_tokens if ex_tokens is not None else token_set(ex["stem"] + " " + " ".join(ex["options"].values()))
    score = 0.0
    if pat.search(seg["text"]):
        supported = context_tokens is None or bool(ex_tokens & context_tokens)
        score += W_TRIGGER if supported else W_TRIGGER_UNSUPPORTED
    score += W_OVERLAP * len(ex_tokens & token_set(seg["text"]))
    mid = (seg["start"] + seg["end"]) / 2
    if ex["start"] <= mid <= ex["end"]:
        score += W_SCREEN
    return score


def context_tokens(transcript, j):
    t0 = transcript[j]["start"]
    out = set()
    for seg in transcript[j:]:
        if seg["start"] > t0 + CONTEXT_S:
            break
        out |= token_set(seg["text"])
    return out


def scored_candidates(ex, transcript):
    """[(segment index, score)] for candidates with score >= MIN_SCORE. A tiny earliness bonus breaks ties toward
    the first mention (a teacher announces a question before referring back to it)."""
    pat = question_pattern(ex["number"])
    ex_tokens = token_set(ex["stem"] + " " + " ".join(ex["options"].values()))
    out = []
    span = max(ex["end"] + WINDOW_AFTER - (ex["start"] - WINDOW_BEFORE), 1.0)
    for j in candidates(ex, transcript):
        s = segment_score(ex, transcript[j], pat, ex_tokens, context_tokens(transcript, j))
        if s >= MIN_SCORE:
            rel = (transcript[j]["start"] - (ex["start"] - WINDOW_BEFORE)) / span
            out.append((j, s - 0.01 * rel))
    return out


def align_greedy(exercises, transcript):
    """Baseline: each question takes its best segment that starts after the previous match. -> {k: j}"""
    picks, last_t = {}, -1.0
    for k, ex in enumerate(exercises):
        best = None
        for j, s in scored_candidates(ex, transcript):
            if transcript[j]["start"] > last_t and (best is None or s > best[1]):
                best = (j, s)
        if best:
            picks[k] = best[0]
            last_t = transcript[best[0]]["start"]
    return picks


def align_dp(exercises, transcript):
    """Monotonic DP over (question, segment) states; questions may stay unmatched. -> {k: j}"""
    states = []          # (time, value, k, j, back_index)
    times, prefix = [], []  # states from earlier questions sorted by time, with running max (value, index)
    for k, ex in enumerate(exercises):
        new = []
        for j, s in scored_candidates(ex, transcript):
            t = transcript[j]["start"]
            pos = bisect.bisect_left(times, t)          # earlier states with time strictly < t
            best_prev, back = (prefix[pos - 1] if pos else (0.0, None))
            if best_prev <= 0.0:
                best_prev, back = 0.0, None
            new.append((t, s + best_prev, k, j, back))
        start = len(states)
        states.extend(new)
        # rebuild the sorted prefix-max table including this question's states
        order = sorted(range(len(states)), key=lambda i: states[i][0])
        times, prefix, run = [], [], (float("-inf"), None)
        for i in order:
            if states[i][1] > run[0]:
                run = (states[i][1], i)
            times.append(states[i][0])
            prefix.append(run)
    if not states:
        return {}
    i = max(range(len(states)), key=lambda x: states[x][1])
    picks = {}
    while i is not None:
        _, _, k, j, back = states[i]
        picks[k] = j
        i = back
    return picks


REFINE_MAX_BACK, REFINE_MAX_GAP = 30.0, 3.0


def refine_starts(exercises, transcript, picks):
    """Episode-start refinement: a teacher often reads a question's stem aloud before naming its number, so from each
    matched segment step back over the immediately preceding segments (gap <= 3 s, at most 30 s back) that share a
    content word with the question, never crossing the previous question's match. Keeps the order strictly monotonic."""
    out, floor_t = {}, -1.0
    for k in sorted(picks):
        ex, j = exercises[k], picks[k]
        toks = token_set(ex["stem"] + " " + " ".join(ex["options"].values()))
        i = j
        while i > 0:
            prev, cur = transcript[i - 1], transcript[i]
            if (prev["start"] <= floor_t or transcript[j]["start"] - prev["start"] > REFINE_MAX_BACK
                    or cur["start"] - prev["end"] > REFINE_MAX_GAP or not toks & token_set(prev["text"])):
                break
            i -= 1
        out[k] = i
        floor_t = transcript[i]["start"]
    return out


def decode(exercises, transcript, method="dp", refine=True):
    """{question index: segment index} for the chosen decoder, optionally with episode-start refinement."""
    picks = (align_dp if method == "dp" else align_greedy)(exercises, transcript)
    return refine_starts(exercises, transcript, picks) if refine else picks


def start_times(exercises, transcript, picks):
    """Start time per question. Unmatched questions fall back to their screen start, clamped between the
    neighbouring matched questions so the output order stays monotonic."""
    matched = {k: transcript[j]["start"] for k, j in picks.items()}
    out, prev_t = [], float("-inf")
    for k, ex in enumerate(exercises):
        if k in matched:
            t = matched[k]
        else:
            nxt = min((matched[i] for i in matched if i > k), default=float("inf"))
            t = min(max(ex["start"], prev_t), nxt)
        out.append(t)
        prev_t = t
    return out


def align_exercises(exercises, transcript, method="dp", refine=True):
    """Align exercises with transcript segments. Returns one record per exercise, in exercise order."""
    if not exercises or not transcript:
        return []
    picks = decode(exercises, transcript, method, refine)
    times = start_times(exercises, transcript, picks)
    out = []
    for k, ex in enumerate(exercises):
        j = picks.get(k)
        rec = {
            "id": ex["id"], "number": ex["number"], "stem": ex["stem"], "options": ex["options"],
            "screen": ex["screens"][0] if ex.get("screens") else None,
        }
        if j is not None:
            seg = transcript[j]
            rec.update(start=seg["start"], end=seg["end"],
                       score=round(segment_score(ex, seg, context_tokens=context_tokens(transcript, j)), 2),
                       trigger_text=seg["text"],
                       speaker=seg.get("speaker", "T"), matched=True)
        else:
            rec.update(start=times[k], end=max(times[k], ex["end"]), score=0.0, trigger_text="",
                       speaker="T", matched=False)
        rec["method"] = method
        out.append(rec)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--method", default="dp", choices=["dp", "greedy"])
    ap.add_argument("--out", default="exercise_alignment.json")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    ex_file = L("exercises.json")
    tr_file = L("transcript.json")

    if not os.path.exists(ex_file) or not os.path.exists(tr_file):
        print(f"[exercise_align] Missing {ex_file} or {tr_file}; skipping.")
        exit(0)

    exercises = json.load(open(ex_file))
    transcript = json.load(open(tr_file))

    aligned = align_exercises(exercises, transcript, a.method)
    out_path = L(a.out)
    json.dump(aligned, open(out_path, "w"), ensure_ascii=False, indent=2)
    n = sum(r["matched"] for r in aligned)
    print(f"[exercise_align] {a.method}: matched {n}/{len(exercises)} questions to speech "
          f"({len(exercises) - n} fall back to screen time) -> {out_path}")
