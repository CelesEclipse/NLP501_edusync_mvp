"""Extract structured exercise questions (question number, stem, options A/B/C/D) from OCR screen text or worksheet.
Usage: python exercises.py --lesson lessons/<id> [--out exercises.json]"""
import argparse, difflib, json, os, re

NUM_WORDS = {
    1: ["một", "one"],
    2: ["hai", "two"],
    3: ["ba", "three"],
    4: ["bốn", "four"],
    5: ["năm", "five"],
    6: ["sáu", "six"],
    7: ["bảy", "seven"],
    8: ["tám", "eight"],
    9: ["chín", "nine"],
    10: ["mười", "ten"],
}


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
        # Check if line begins with a question number e.g. "1.", "2.", "15."
        m = re.match(r"^(\d{1,2})[\.\)]\s*(.*)", l)
        if m and (len(l) > 2):
            if cur_q:
                candidates.append(cur_q)
            cur_q = {
                "num": int(m.group(1)),
                "lines": [m.group(2)] if m.group(2) else [],
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


def deduplicate_exercises(raw_items):
    """Merge items with the same number appearing across consecutive screens."""
    if not raw_items:
        return []

    merged = []
    for it in raw_items:
        # Check if can merge with last item if same number and adjacent screen
        if merged and merged[-1]["number"] == it["number"] and it["screen"] - merged[-1]["screens"][-1] <= 2:
            prev = merged[-1]
            prev["screens"].append(it["screen"])
            prev["end"] = max(prev["end"], it["end"])
            # Keep richer stem or options
            if len(it["stem"]) > len(prev["stem"]):
                prev["stem"] = it["stem"]
            if len(it["options"]) > len(prev["options"]):
                prev["options"] = it["options"]
        else:
            merged.append({
                "id": f"q_{len(merged)+1}",
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
        all_raw.extend(parse_screen_text(s))

    exercises = deduplicate_exercises(all_raw)
    out_path = L(a.out)
    json.dump(exercises, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(f"[exercises] Extracted {len(exercises)} structured exercises across {len(screens)} screens -> {out_path}")

