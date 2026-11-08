"""Grammatical Error Correction (GEC) & Diagnostic Feedback Engine for student chat messages.
Analyzes student English text, classifies errors under ERRANT taxonomy, and provides Vietnamese explanations.
Outputs <lesson>/chat_feedback.json.
Usage: python feedback.py --lesson lessons/<id> [--out chat_feedback.json]"""
import argparse, json, os, re

VI_CHARS = re.compile(r"[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)


class GECRuleEngine:
    """Diagnostic GEC rule engine with standard ERRANT taxonomy tags."""

    def __init__(self):
        # Compiled patterns: (regex, error_type, replacement_fn, explanation_vi)
        self.rules = [
            # 1. U:VERB:BE - Unnecessary 'be' before lexical verb (L1 transfer: "I am agree")
            (
                re.compile(r"\bI\s+am\s+agree\b", re.I),
                "U:VERB:BE",
                lambda m: "I agree",
                "Trong tiếng Anh, 'agree' đã là một động từ mang nghĩa 'đồng ý', không dùng kèm trợ động từ to be ('I am agree' -> 'I agree')."
            ),
            # 2. R:ADJ:PARTICIPLE - Confusing active (-ing) and passive (-ed) participles
            (
                re.compile(r"\b(the\s+)?(movie|film|story|book|show)\s+(?:was|is)\s+(moved)\b", re.I),
                "R:ADJ:PARTICIPLE",
                lambda m: f"{m.group(1) or ''}{m.group(2)} {m.group(0).split()[-2]} moving",
                "Chủ ngữ chỉ vật/bộ phim có bản chất gây xúc động cho người xem (chủ động), nên dùng hiện tại phân từ V-ing ('moving'), không dùng quá khứ phân từ V-ed ('moved' chỉ người bị cảm động)."
            ),
            # 3. R:ADJ:PARTICIPLE - Missing participle suffix on predicate adjective
            (
                re.compile(r"\b(this\s+)?(noise|sound)\s+is\s+(?:very\s+)?(annoy)\b", re.I),
                "R:ADJ:PARTICIPLE",
                lambda m: m.group(0).replace(m.group(3), "annoying"),
                "Sau động từ to be cần một tính từ bổ nghĩa cho danh từ 'noise'. Cần dùng hiện tại phân từ 'annoying' (gây bực mình/khó chịu), thay vì động từ nguyên mẫu 'annoy'."
            ),
            # 4. R:VERB:FORM - Causative structure: have something done (V3)
            (
                re.compile(r"\b(ha(?:s|ve|d)\s+(?:his|her|my|their|the)\s+\w+\s+)(shine)\b", re.I),
                "R:VERB:FORM",
                lambda m: m.group(1) + "shined",
                "Cấu trúc nhờ vả (Causative form): Have/Has + Tân ngữ chỉ vật (shoes) + Quá khứ phân từ V3/V-ed ('have his shoes shined' = có giày được đánh bóng)."
            ),
            # 5. U:PREP / R:VERB:FORM - Modal verb + 'to' infinitive (should to increase -> should increase)
            (
                re.compile(r"\b(should|can|could|will|would|must|may|might)\s+to\s+([a-z]+)\b", re.I),
                "U:PREP",
                lambda m: f"{m.group(1)} {m.group(2)}",
                f"Sau động từ khiếm khuyết (modal verb) như '{re.compile(r'should|can|could|will|would|must', re.I).pattern}', bắt buộc dùng động từ nguyên mẫu không 'to' (bare infinitive)."
            ),
            # 6. R:VERB:SVA - Subject-Verb Agreement: it make -> it makes
            (
                re.compile(r"\b(it|he|she)\s+(make)\b", re.I),
                "R:VERB:SVA",
                lambda m: f"{m.group(1)} makes",
                "Chủ ngữ ngôi thứ ba số ít ('it/he/she') ở thì hiện tại đơn yêu cầu động từ thêm đuôi '-s' hoặc '-es' ('it makes')."
            ),
            # 7. M:VERB:AUX - Missing auxiliary in wh-question (Why we use -> Why do we use)
            (
                re.compile(r"\bWhy\s+we\s+use\b", re.I),
                "M:VERB:AUX",
                lambda m: "Why do we use",
                "Trong câu hỏi trực tiếp ở thì hiện tại đơn, cần có trợ động từ 'do' đứng trước chủ ngữ 'we' ('Why do we use...')."
            ),
            # 8. R:ADJ:PARTICIPLE - Confusing bored vs boring
            (
                re.compile(r"\b(he|she|it|they|we)\s+felt\s+(boring)\b", re.I),
                "R:ADJ:PARTICIPLE",
                lambda m: f"{m.group(1)} felt bored",
                "Khi miêu tả cảm xúc của người/động vật bị tác động, dùng tính từ quá khứ phân từ '-ed' ('bored'), tính từ '-ing' ('boring') chỉ bản chất gây chán."
            )
        ]

    def extract_english_clauses(self, text):
        """Extract continuous English spans from bilingual Vietnamese-English text."""
        # Split by typical Vietnamese conversational markers
        parts = re.split(r"(?:^|[,\.\?!]|\bcâu\s+\d+\b|\btext\s+\d+\b|\bem\s+(?:chọn|nghĩ|thấy)\b|\bcô\s+ơi\b|\bạ\b)", text, flags=re.I)
        clauses = []
        for p in parts:
            p_strip = p.strip()
            # If contains at least 2 English words and little Vietnamese diacritics
            words = re.findall(r"[A-Za-z]+", p_strip)
            if len(words) >= 2 and not VI_CHARS.search(p_strip):
                clauses.append(p_strip)
        return clauses

    def check_sentence(self, text):
        """Run GEC rules on message and return detected edits."""
        edits = []
        corrected = text

        for pat, err_type, rep_fn, exp_vi in self.rules:
            m = pat.search(corrected)
            if m:
                orig_span = m.group(0)
                rep_span = rep_fn(m)
                edits.append({
                    "error_type": err_type,
                    "original": orig_span,
                    "replacement": rep_span,
                    "explanation_vi": exp_vi
                })
                # Apply replacement
                corrected = corrected[:m.start()] + rep_span + corrected[m.end():]

        return edits, corrected


def generate_feedback(chat_entries):
    """Analyze chat messages and produce GEC diagnostic feedback."""
    engine = GECRuleEngine()
    feedbacks = []

    for c in chat_entries:
        msg = c.get("message", "")
        edits, corrected = engine.check_sentence(msg)

        has_error = len(edits) > 0
        fb_item = {
            "chat_id": c["id"],
            "timestamp": c["timestamp"],
            "time_str": c["time_str"],
            "speaker_id": c["speaker_id"],
            "speaker_name": c["speaker_name"],
            "original_message": msg,
            "question_number": c.get("question_number"),
            "exercise_id": c.get("exercise_id"),
            "has_error": has_error,
            "corrected_message": corrected if has_error else msg,
            "edits": edits,
            "status": "needs_correction" if has_error else "correct_or_general"
        }
        feedbacks.append(fb_item)

    return feedbacks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", default=".", help="lesson folder; all paths are relative to it")
    ap.add_argument("--chat", default="chat.json", help="parsed chat json filename")
    ap.add_argument("--out", default="chat_feedback.json", help="output feedback json filename")
    a = ap.parse_args()
    L = lambda f: os.path.join(a.lesson, f)

    chat_file = L(a.chat)
    if not os.path.exists(chat_file):
        print(f"[feedback] Missing {chat_file}; skipping.")
        exit(0)

    chat_entries = json.load(open(chat_file, encoding="utf-8"))
    feedbacks = generate_feedback(chat_entries)

    err_count = sum(1 for f in feedbacks if f["has_error"])
    out_path = L(a.out)
    json.dump(feedbacks, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[feedback] Processed {len(feedbacks)} messages ({err_count} with GEC errors) -> {out_path}")
