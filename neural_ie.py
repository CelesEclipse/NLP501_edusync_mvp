#!/usr/bin/env python3
"""
neural_ie.py — Hybrid Neural Information Extraction (Neural IE) for EduSync.

Extracts:
1. grammar_points.json: Core grammar rules, formulas, timestamps in speech,
   pedagogical Vietnamese explanations, examples, and TOEIC tips.
2. vocab_deep.json: Deep bilingual vocabulary profiling with contextual definitions,
   collocations, CEFR levels, and links to speech audio clips.

Architecture:
- Tier 1: Gemini API (gemini-3.5-flash-lite) in JSON mode (responseMimeType=application/json); required fields are
  checked after parsing. The LLM sees ~30 sampled transcript segments, so its timestamps are only guesses.
- Tier 2 / Fallback (no API key or network error): a generic TOEIC grammar taxonomy matched against cue phrases in
  the transcript; deep vocabulary taken from vocab.json.
- Grounding (both tiers): each grammar point's timestamp is re-anchored to the most similar transcript window under
  multilingual-e5-small (ground_theory_timestamps). `--ground-only` applies this to an existing grammar_points.json.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


def load_env_key():
    """Load GEMINI_API_KEY from environment or .env file."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key.strip()
    
    # Check .env in current directory or repo root
    for env_path in [Path(".env"), Path(__file__).resolve().parent / ".env"]:
        if env_path.is_file():
            try:
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
            except Exception:
                pass
    return None


def format_time(seconds: float) -> str:
    """Format seconds into MM:SS string."""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"


def call_gemini_api(prompt: str, api_key: str, model_name: str = "gemini-3.5-flash-lite") -> dict:
    """Call Google Generative Language API with JSON schema enforcement."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        candidate = res.get("candidates", [{}])[0]
        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "{}")
        return json.loads(text)


# Generic TOEIC grammar taxonomy for the offline fallback: a topic is reported when its cue phrases are spoken at
# least MIN_CUE_HITS times in the lesson. Nothing here is specific to one lesson.
GRAMMAR_TAXONOMY = [
    {"key": "participle_adj", "title": "Participles as Adjectives (-ing vs. -ed) (Phân từ làm tính từ)",
     "formula": "V-ing (gây ra tính chất/cảm xúc) / V-ed (người chịu cảm xúc)",
     "explanation_vi": "Phân từ hiện tại (-ing) mô tả tính chất của sự vật gây ra cảm xúc; phân từ quá khứ (-ed) mô tả cảm xúc của người chịu tác động.",
     "cues": ["phân từ", "participle", "động tính từ", "thêm ing", "thêm ed"]},
    {"key": "causative", "title": "Causative have/get + object + V3 (Cấu trúc nhờ vả)",
     "formula": "have/get + vật + V3/ed; have + người + V nguyên mẫu",
     "explanation_vi": "Diễn tả việc nhờ/thuê người khác làm gì; tân ngữ chỉ vật đi với phân từ hai.",
     "cues": ["nhờ vả", "sai khiến", "causative"]},
    {"key": "passive", "title": "Passive Voice (Câu bị động)", "formula": "be + V3/ed",
     "explanation_vi": "Chủ ngữ là đối tượng chịu tác động của hành động.", "cues": ["bị động", "passive"]},
    {"key": "subjunctive", "title": "Subjunctive after require/suggest that (Câu giả định)",
     "formula": "require/suggest/demand + that + S + (should) + V nguyên mẫu",
     "explanation_vi": "Sau các động từ yêu cầu/đề nghị, mệnh đề that dùng động từ nguyên mẫu.",
     "cues": ["giả định", "require cộng that", "suggest cộng that", "demand cộng that"]},
    {"key": "noun_modifier", "title": "Word Form before a Noun (Tính từ bổ nghĩa cho danh từ)",
     "formula": "(Det) + Adjective + Noun", "explanation_vi": "Vị trí trước danh từ cần tính từ để bổ nghĩa.",
     "cues": ["bổ nghĩa cho danh từ", "loại từ"]},
    {"key": "relative_clause", "title": "Relative Clauses (Mệnh đề quan hệ)", "formula": "N + who/which/that + clause",
     "explanation_vi": "Mệnh đề bổ nghĩa cho danh từ đứng trước.", "cues": ["mệnh đề quan hệ", "đại từ quan hệ", "relative clause"]},
    {"key": "comparison", "title": "Comparatives and Superlatives (So sánh)", "formula": "adj-er/more adj than; the adj-est/most adj",
     "explanation_vi": "So sánh hơn và so sánh nhất.", "cues": ["so sánh hơn", "so sánh nhất", "comparative", "superlative"]},
    {"key": "gerund_infinitive", "title": "Gerunds and Infinitives (Danh động từ và động từ nguyên mẫu)",
     "formula": "V + V-ing / V + to V", "explanation_vi": "Một số động từ theo sau bởi V-ing, một số bởi to V.",
     "cues": ["danh động từ", "gerund", "to infinitive", "nguyên mẫu có to"]},
    {"key": "conditional", "title": "Conditional Sentences (Câu điều kiện)", "formula": "If + clause, clause",
     "explanation_vi": "Câu điều kiện loại 1, 2, 3.", "cues": ["câu điều kiện", "conditional"]},
    {"key": "tense", "title": "Verb Tenses (Thì động từ)", "formula": "present / past / perfect",
     "explanation_vi": "Chia thì theo mốc thời gian và dấu hiệu nhận biết.",
     "cues": ["hiện tại hoàn thành", "quá khứ đơn", "present perfect", "past simple", "dấu hiệu nhận biết"]},
]
MIN_CUE_HITS = 3
GROUNDING_MODEL = ("intfloat/multilingual-e5-small", "query: ", "passage: ")
GROUNDING_WINDOW = 6  # transcript segments per window (about 10-20 s of speech)


def fallback_rule_based_extraction(transcript: list, exercises: list, vocab_items: list) -> dict:
    """Offline fallback (no API key / network): report the taxonomy topics whose cue phrases the teacher says at least
    MIN_CUE_HITS times, timestamped at the first cue (later replaced by ground_theory_timestamps), and take the deep
    vocabulary from vocab.json (B1+ words with their mined Vietnamese meaning). Examples are left empty rather than
    invented."""
    low = [(s["start"], s["text"].lower()) for s in transcript]
    found = []
    for topic in GRAMMAR_TAXONOMY:
        hits = [t for t, txt in low for c in topic["cues"] if c in txt]
        if len(hits) >= MIN_CUE_HITS:
            found.append((len(hits), min(hits), topic))
    found.sort(key=lambda x: x[1])
    grammar_points = []
    for i, (n, t0, topic) in enumerate(sorted(found, key=lambda x: -x[0])[:5]):
        grammar_points.append({
            "id": f"gp_{i + 1}", "title": topic["title"], "formula": topic["formula"],
            "explanation_vi": topic["explanation_vi"], "examples": [], "timestamp": float(t0),
            "time_str": format_time(t0), "toeic_tips": "", "source": "taxonomy_fallback", "cue_hits": n,
        })
    vocab_deep = []
    for v in vocab_items:
        if v.get("level") in ("B1", "B2", "C1", "C2"):
            ts = float(v.get("timestamp") or 0.0)
            vocab_deep.append({"word": v["word"], "pos": v.get("pos", ""), "level": v["level"],
                               "meaning_vi": v.get("meaning_vi", ""), "collocations": [],
                               "example": v.get("example_context", ""), "timestamp": ts, "time_str": format_time(ts)})
    return {"grammar_points": grammar_points, "vocab_deep": vocab_deep[:12]}


def ground_theory_timestamps(grammar_points: list, transcript: list) -> list:
    """Replace each grammar point's timestamp by the transcript window most similar to the concept
    (title + formula + English examples + Vietnamese explanation) under a multilingual bi-encoder.
    The LLM only sees a sample of the transcript, so its own timestamps are guesses; they are kept as
    'llm_timestamp'. Without sentence-transformers the timestamps are left unchanged."""
    if not grammar_points or not transcript:
        return grammar_points
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("[neural_ie] sentence-transformers not installed; theory timestamps not grounded.", flush=True)
        return grammar_points
    name, qp, pp = GROUNDING_MODEL
    model = SentenceTransformer(name)
    W = GROUNDING_WINDOW
    windows = [" ".join(s["text"] for s in transcript[i:i + W]) for i in range(len(transcript))]
    E = model.encode([pp + w for w in windows], normalize_embeddings=True, batch_size=64)
    for g in grammar_points:
        ex = " ".join(x.get("en", "") for x in g.get("examples", []) if isinstance(x, dict))
        text = f"{g.get('title', '')}. Formula: {g.get('formula', '')}. Examples: {ex}. {g.get('explanation_vi', '')}"
        c = model.encode([qp + text], normalize_embeddings=True)[0]
        sims = E @ c
        best = int(sims.argmax())
        if "llm_timestamp" not in g and g.get("source") != "taxonomy_fallback":
            g["llm_timestamp"] = g.get("timestamp")
        g["timestamp"] = float(transcript[best]["start"])
        g["time_str"] = format_time(g["timestamp"])
        g["timestamp_source"] = "grounded:" + name.split("/")[-1]
        g["grounding_score"] = round(float(sims[best]), 3)
    return grammar_points


def extract_neural_ie(lesson_dir: Path, force_rule_based: bool = False) -> dict:
    """
    Main extraction function. Reads lesson assets, calls Gemini API or fallback,
    and returns validated grammar_points and vocab_deep.
    """
    # 1. Load inputs
    transcript_path = lesson_dir / "transcript.json"
    exercises_path = lesson_dir / "exercises.json"
    vocab_path = lesson_dir / "vocab.json"
    chat_path = lesson_dir / "chat_feedback.json"

    transcript = json.loads(transcript_path.read_text(encoding="utf-8")) if transcript_path.is_file() else []
    exercises = json.loads(exercises_path.read_text(encoding="utf-8")) if exercises_path.is_file() else []
    vocab_items = json.loads(vocab_path.read_text(encoding="utf-8")) if vocab_path.is_file() else []
    chat_feedback = json.loads(chat_path.read_text(encoding="utf-8")) if chat_path.is_file() else []
    lesson_meta_path = lesson_dir / "lesson.json"
    lesson_title = (json.loads(lesson_meta_path.read_text(encoding="utf-8")).get("title", lesson_dir.name)
                    if lesson_meta_path.is_file() else lesson_dir.name)

    api_key = None if force_rule_based else load_env_key()

    if not api_key:
        print("[neural_ie] No GEMINI_API_KEY found or forced. Using the taxonomy-based fallback.", flush=True)
        return fallback_rule_based_extraction(transcript, exercises, vocab_items)

    print("[neural_ie] GEMINI_API_KEY detected. Calling Gemini (JSON mode)...", flush=True)

    # 2. Build representative context prompt
    # Sample transcript every N segments to fit comfortably
    stride = max(1, len(transcript) // 30)
    sampled_speech = [{"start": round(s["start"], 1), "text": s["text"]} for s in transcript[::stride]]
    sampled_ex = [{"num": e.get("number"), "stem": e.get("stem"), "options": e.get("options")} for e in exercises[:10]]
    sampled_errors = [
        {"student": c.get("speaker_id"), "original": c.get("original_message"), "error": [ed.get("error_type") for ed in c.get("edits", [])]}
        for c in chat_feedback if c.get("has_error")
    ]

    prompt = f"""Bạn là chuyên gia giảng dạy tiếng Anh TOEIC và chuyên gia Xử lý Ngôn ngữ Tự nhiên (NLP).
Nhiệm vụ: Phân tích sâu bài giảng "{lesson_title}" (bài giảng luyện thi tiếng Anh, giảng song ngữ Việt - Anh).

Dữ liệu bài tập trắc nghiệm mẫu của bài:
{json.dumps(sampled_ex, ensure_ascii=False)}

Dữ liệu các đoạn lời giảng mẫu của giáo viên (kèm mốc thời gian start tính bằng giây):
{json.dumps(sampled_speech, ensure_ascii=False)}

Các lỗi ngữ pháp thực tế học viên mắc phải trong chat:
{json.dumps(sampled_errors, ensure_ascii=False)}

Yêu cầu xuất ra cấu trúc JSON hợp lệ duy nhất có đúng 2 trường:
1. "grammar_points": danh sách 4-5 chủ điểm ngữ pháp cốt lõi nhất được giảng viên truyền đạt.
   Mỗi phần tử gồm:
   - "id": chuỗi id dạng "gp_1", "gp_2"...
   - "title": tên chủ điểm (song ngữ Anh - Việt, ví dụ: "Participles as Adjectives (Phân từ làm Tính từ)")
   - "formula": công thức ngữ pháp rút gọn, súc tích
   - "explanation_vi": giải thích sư phạm chi tiết bằng tiếng Việt
   - "examples": danh sách 2-3 câu ví dụ (mỗi ví dụ có "en" và "vi")
   - "timestamp": mốc thời gian số (giây) gần nhất trong bài giảng mà giảng viên đang giải thích cấu trúc này
   - "time_str": chuỗi thời gian định dạng "MM:SS" (ví dụ: "14:15")
   - "toeic_tips": lời khuyên, mẹo làm bài hoặc bẫy đề thi TOEIC thường gặp

2. "vocab_deep": danh sách 8-12 từ vựng trọng tâm nhất trình độ B1-C1 trong bài giảng.
   Mỗi phần tử gồm:
   - "word": từ tiếng Anh
   - "pos": từ loại (noun, verb, adj...)
   - "level": bậc CEFR ("B1", "B2", "C1")
   - "meaning_vi": nghĩa tiếng Việt chính xác theo ngữ cảnh bài học
   - "collocations": danh sách 2-3 cụm từ hay đi kèm (ví dụ: ["economic depression", "severe depression"])
   - "example": câu ví dụ thực tế có trong bài học hoặc đề thi
   - "timestamp": mốc thời gian (giây) từ xuất hiện trong video
   - "time_str": chuỗi "MM:SS"

Trả về JSON thuần túy, không có văn bản giải thích phụ bên ngoài.
"""

    try:
        data = call_gemini_api(prompt, api_key, model_name="gemini-3.5-flash-lite")
        gps = data.get("grammar_points", [])
        vds = data.get("vocab_deep", [])
        if gps and vds:
            # Ensure timestamps and time_str are sanitized
            for g in gps:
                ts = float(g.get("timestamp") or 0.0)
                g["timestamp"] = ts
                if "time_str" not in g or not g["time_str"]:
                    g["time_str"] = format_time(ts)
            for v in vds:
                ts = float(v.get("timestamp") or 0.0)
                v["timestamp"] = ts
                if "time_str" not in v or not v["time_str"]:
                    v["time_str"] = format_time(ts)

            print(f"[neural_ie] Gemini Neural IE success: {len(gps)} grammar points, {len(vds)} deep vocab words.", flush=True)
            return {"grammar_points": gps, "vocab_deep": vds}
        else:
            print("[neural_ie] Gemini returned incomplete structure, falling back to rule-based.", flush=True)
            return fallback_rule_based_extraction(transcript, exercises, vocab_items)
    except Exception as e:
        print(f"[neural_ie] Gemini API call failed ({e}). Gracefully falling back to rule-based IE.", flush=True)
        return fallback_rule_based_extraction(transcript, exercises, vocab_items)


def main():
    parser = argparse.ArgumentParser(description="Extract grammar points and deep vocabulary via Hybrid Neural IE.")
    parser.add_argument("lesson_pos", nargs="?", default=None, help="Path to lesson directory (positional)")
    parser.add_argument("--lesson", default=None, help="Path to lesson directory (flag)")
    parser.add_argument("--force-rule-based", action="store_true", help="Force the offline taxonomy fallback")
    parser.add_argument("--ground-only", action="store_true",
                        help="Do not extract: re-ground the timestamps of the existing grammar_points.json")
    parser.add_argument("--no-ground", action="store_true", help="Skip timestamp grounding")
    args = parser.parse_args()

    target_lesson = args.lesson or args.lesson_pos or "lessons/ece-toeic-starter-u4"
    lesson_dir = Path(target_lesson)
    if not lesson_dir.is_dir():
        print(f"Error: {lesson_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    gp_path = lesson_dir / "grammar_points.json"
    vd_path = lesson_dir / "vocab_deep.json"
    transcript = json.loads((lesson_dir / "transcript.json").read_text(encoding="utf-8"))

    if args.ground_only:
        gps = ground_theory_timestamps(json.loads(gp_path.read_text(encoding="utf-8")), transcript)
        gp_path.write_text(json.dumps(gps, ensure_ascii=False, indent=2), encoding="utf-8")
        for g in gps:
            print(f"[neural_ie] {g['id']}: {g.get('llm_timestamp')} -> {g['timestamp']} ({g['time_str']})")
        return

    result = extract_neural_ie(lesson_dir, force_rule_based=args.force_rule_based)
    if not args.no_ground:
        result["grammar_points"] = ground_theory_timestamps(result["grammar_points"], transcript)

    gp_path.write_text(json.dumps(result["grammar_points"], ensure_ascii=False, indent=2), encoding="utf-8")
    vd_path.write_text(json.dumps(result["vocab_deep"], ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[neural_ie] Written {len(result['grammar_points'])} grammar points -> {gp_path}")
    print(f"[neural_ie] Written {len(result['vocab_deep'])} deep vocab words -> {vd_path}")


if __name__ == "__main__":
    main()
