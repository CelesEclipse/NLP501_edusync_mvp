"""Extract structured exercise questions (question number, stem, options A/B/C/D) from OCR screen text or worksheet.
Supports both Part 5 (isolated sentences) and Part 6 (reading passages with in-text blanks).
Usage: python exercises.py --lesson lessons/<id> [--out exercises.json]"""
import argparse, difflib, json, os, re, sys

# a line that starts a question: "<label> N" (label = question / number / câu [hỏi] [số] / q) or a bare "N." / "N)".
# N has up to 3 digits because real TOEIC tests number Part 5-7 as 101-200 (the ECE book restarts at 1).
QUESTION_LINE = re.compile(
    r"^(?:(?:question|number|câu(?:\s+hỏi)?(?:\s+số)?|q)\s*(\d{1,3})\b[\.\):]?|(\d{1,3})[\.\)])\s*(.*)", re.I)


def extract_stem_and_options(raw_text):
    """Split raw question block into stem and option dictionary."""
    opts = {}
    cleaned = raw_text.strip()
    
    # Try pattern with parentheses: (A) ... (B) ...
    pats = re.findall(r"\(([A-D])\)\s*([^(\n]+)", cleaned)
    if len(pats) >= 2:
        for k, v in pats:
            opts[k.upper()] = v.strip()
        stem = re.sub(r"\([A-D]\).*", "", cleaned, flags=re.DOTALL).strip()
    else:
        # Try pattern with dot: A. ... B. ...
        pats = re.findall(r"\b([A-D])[\.\)]\s*([^A-D\n]+)", cleaned)
        if len(pats) >= 2:
            for k, v in pats:
                opts[k.upper()] = v.strip()
            stem = re.sub(r"\b[A-D][\.\)].*", "", cleaned, flags=re.DOTALL).strip()
        else:
            stem = cleaned

    stem = re.sub(r"\s+", " ", stem).strip()
    return stem, opts


def extract_passage_exercises(raw_text, screen_id, s_start, s_end):
    """Extract in-text cloze questions (Part 6) where blanks appear inside reading passages."""
    splits = list(re.finditer(r"(?:^|\n)\s*(\d+)[\.\)]\s*(?=(?:\([A-D]\)|[A-D][\.\)]))", raw_text))
    if len(splits) < 2:
        return []

    questions = []
    for i, m in enumerate(splits):
        num = int(m.group(1))
        opt_start = m.end()
        next_m = splits[i + 1] if i + 1 < len(splits) else None
        chunk_after = raw_text[opt_start: next_m.start() if next_m else len(raw_text)]
        
        opt_lines = []
        is_opt = True
        for line in chunk_after.strip().splitlines():
            l = line.strip()
            if re.match(r"^(?:\([A-D]\)|[A-D][\.\)])", l) or (is_opt and re.findall(r"(?:\([A-D]\)|[A-D][\.\)])", l)):
                opt_lines.append(l)
            else:
                is_opt = False

        opt_text = " ".join(opt_lines)
        pats = re.findall(r"(?:\(([A-D])\)|([A-D])[\.\)])\s*([^A-D(\n]+)", opt_text)
        options = {}
        for k1, k2, v in pats:
            k = (k1 or k2).upper()
            options[k] = v.strip()

        prev_end = splits[i - 1].end() if i > 0 else 0
        preceding = raw_text[prev_end: m.start()].strip()
        pre_lines = [l.strip() for l in preceding.splitlines() if not re.match(r"^(?:\([A-D]\)|[A-D][\.\)])", l.strip())]
        stem = " ".join(pre_lines[-3:]) if pre_lines else ""
        stem = re.sub(r"\s+", " ", stem).strip()

        questions.append({
            "number": num,
            "stem": stem,
            "options": options,
            "screen": screen_id,
            "start": s_start,
            "end": s_end
        })
    return questions


def parse_screen_text(screen):
    """Parse a single screen OCR text into candidate questions."""
    text = screen.get("text", "")
    lines = text.splitlines()
    candidates = []
    cur_q = None

    for line in lines:
        l = line.strip()
        if not l:
            continue
        # Check if line begins with a question number: "1.", "15)", TOEIC's 101-200 ("147."), or a labelled
        # number ("Number 7", "Question 2:", "Câu 12", "Q3") as on practice-test slides
        m = QUESTION_LINE.match(l)
        if m and (len(l) > 2):
            if cur_q:
                candidates.append(cur_q)
            cur_q = {
                "num": int(m.group(1) or m.group(2)),
                "lines": [m.group(3)] if m.group(3) else [],
                "screen": screen["id"],
                "start": screen["start"],
                "end": screen["end"]
            }
        elif cur_q:
            cur_q["lines"].append(l)

    if cur_q:
        candidates.append(cur_q)

    parsed = []
    for c in candidates:
        full_text = " ".join(c["lines"]).strip()
        if len(full_text) < 4:
            continue
        stem, opts = extract_stem_and_options(full_text)
        if stem or opts:
            parsed.append({
                "number": c["num"],
                "stem": stem,
                "options": opts,
                "screen": c["screen"],
                "start": c["start"],
                "end": c["end"]
            })
    return parsed


def deduplicate_exercises(items):
    """Merge questions across consecutive screens using smart recency window."""
    if not items:
        return []

    merged = []
    for it in items:
        matched = False
        # Look back up to 8 recent items to handle multi-question screens
        for prev in reversed(merged[-8:]):
            same_num = (prev["number"] == it["number"])
            screen_near = (it["screen"] - max(prev["screens"]) <= 2)
            stem_sim = difflib.SequenceMatcher(None, prev["stem"], it["stem"]).ratio() if (prev["stem"] and it["stem"]) else 0.5
            opts_shared = len(set(prev["options"].values()) & set(it["options"].values())) if (prev["options"] and it["options"]) else 1

            if same_num and screen_near and (stem_sim > 0.3 or opts_shared >= 1):
                prev["screens"].append(it["screen"])
                prev["end"] = max(prev["end"], it["end"])
                if len(it["stem"]) > len(prev["stem"]):
                    prev["stem"] = it["stem"]
                if len(it["options"]) > len(prev["options"]):
                    prev["options"] = it["options"]
                matched = True
                break

        if not matched:
            merged.append({
                "id": f"q_{len(merged) + 1}",
                "number": it["number"],
                "stem": it["stem"],
                "options": it["options"],
                "screens": [it["screen"]],
                "start": it["start"],
                "end": it["end"]
            })
    return merged


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--out", default="exercises.json")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    screens_file = L("screens.json")
    if not os.path.exists(screens_file):
        print(f"[exercises] No screens.json in {a.lesson}; skipping exercise extraction.")
        sys.exit(0)

    screens = json.load(open(screens_file))
    all_raw = []
    for s in screens:
        passage_items = extract_passage_exercises(s["text"], s["id"], s["start"], s["end"])
        if passage_items:
            all_raw.extend(passage_items)
        else:
            all_raw.extend(parse_screen_text(s))

    exercises = deduplicate_exercises(all_raw)
    out_path = L(a.out)
    json.dump(exercises, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(f"[exercises] Extracted {len(exercises)} structured exercises across {len(screens)} screens -> {out_path}")
