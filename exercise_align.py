"""Align extracted exercise questions to teacher speech segments in transcript.json using Monotonic DP.
Outputs <lesson>/exercise_alignment.json.
Usage: python exercise_align.py --lesson lessons/<id> [--out exercise_alignment.json]"""
import argparse, json, os, re

NUM_WORDS_VI = {
    1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm",
    6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười",
    11: "mười một", 12: "mười hai", 13: "mười ba", 14: "mười bốn", 15: "mười lăm"
}


def question_pattern(num):
    vi_word = NUM_WORDS_VI.get(num, "")
    word_clause = f"|{vi_word}" if vi_word else ""
    return re.compile(rf"\b(câu|câu số|number|question)\s*({num}{word_clause})\b", re.I)


def token_set(text):
    return set(w.lower() for w in re.findall(r"\w+", text) if len(w) > 2)


def align_exercises(exercises, transcript):
    """Align exercises with transcript segments using monotonic forward search."""
    if not exercises or not transcript:
        return []

    alignments = []
    last_seg_idx = 0
    N_trans = len(transcript)

    for ex in exercises:
        num = ex["number"]
        pat = question_pattern(num)
        
        # Screen boundaries
        t_screen_start = ex["start"]
        t_screen_end = ex["end"]

        # Search window in transcript: prefer forward progression
        # Look from last_seg_idx up to segments within screen display + buffer
        cands = []
        for idx in range(last_seg_idx, N_trans):
            seg = transcript[idx]
            if seg["start"] > t_screen_end + 45.0:
                break
            # consider segments near screen time
            if seg["end"] >= t_screen_start - 20.0:
                cands.append((idx, seg))

        if not cands:
            # Fallback to local search around screen start
            cands = [(i, s) for i, s in enumerate(transcript) if t_screen_start - 10.0 <= s["start"] <= t_screen_end + 30.0 and i >= last_seg_idx]

        best_idx, best_seg, best_score = None, None, -1.0
        ex_tokens = token_set(ex["stem"] + " " + " ".join(ex["options"].values()))

        for idx, seg in cands:
            score = 0.0
            text = seg["text"]

            # 1. Explicit question mention
            if pat.search(text):
                score += 20.0

            # 2. Token overlap with stem/options
            seg_tokens = token_set(text)
            overlap = len(ex_tokens & seg_tokens)
            score += overlap * 2.0

            # 3. Screen display temporal alignment
            if t_screen_start <= (seg["start"] + seg["end"]) / 2 <= t_screen_end:
                score += 3.0

            if score > best_score and score >= 3.0:
                best_score = score
                best_idx = idx
                best_seg = seg

        if best_seg is not None:
            last_seg_idx = best_idx
            alignments.append({
                "id": ex["id"],
                "number": num,
                "stem": ex["stem"],
                "options": ex["options"],
                "screen": ex["screens"][0],
                "start": best_seg["start"],
                "end": best_seg["end"],
                "score": round(best_score, 2),
                "trigger_text": best_seg["text"],
                "speaker": best_seg.get("speaker", "T")
            })

    return alignments


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
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

    aligned = align_exercises(exercises, transcript)
    out_path = L(a.out)
    json.dump(aligned, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(f"[exercise_align] Successfully aligned {len(aligned)}/{len(exercises)} questions to speech -> {out_path}")

