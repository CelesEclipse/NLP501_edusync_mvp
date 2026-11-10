#!/usr/bin/env python3
"""
concept_link.py — link each exercise question to the grammar concept it practises (or to none).

Method (chosen with eval/eval_concepts.py on Unit 4, see docs/10_evaluation_results.md):
  score(q, c) = ( cos(E(question q), E(concept c)) + cos(E(speech of q), E(concept c)) ) / 2
  - E = intfloat/multilingual-e5-small (multilingual bi-encoder, 384-d, L2-normalised; "query:"/"passage:" prefixes)
  - question = OCR stem + options; speech = what the teacher says from the aligned start of q to the next question
    (max 90 s, from exercise_alignment.json) — the multimodal signal: the teacher names the concept in Vietnamese
    while solving ("thêm ing hay ed để làm tính từ", "công thức nhờ vả"...).
  - concept = title + formula + English examples + Vietnamese explanation from grammar_points.json.
  q is linked to argmax_c score when that score >= THRESHOLD, otherwise to none.
  No hand-written keywords: the previous version appended lesson-specific cue words (incl. answer words such as
  "central", "luxury", "shined") to the concept text, which leaked the answer into the representation.
Fallback without sentence-transformers: TF-IDF cosine between question+speech and concept.

Outputs <lesson>/exercise_concept_links.json.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

MODEL_NAME = "intfloat/multilingual-e5-small"
QUERY_PREFIX, PASSAGE_PREFIX = "query: ", "passage: "
THRESHOLD = 0.835          # middle of the 0.830-0.840 plateau on Unit 4; recalibrate for a new lesson set
HIGH_MARGIN = 0.01         # linked and ahead of the runner-up by this much -> confidence HIGH
TFIDF_THRESHOLD = 0.10
SPEECH_MAX_S = 90.0


def question_text(ex):
    return f"{ex.get('stem', '')} Options: " + " ".join(f"{k}. {v}" for k, v in ex.get("options", {}).items())


def concept_text(gp):
    examples = " ".join(x.get("en", "") for x in gp.get("examples", []) if isinstance(x, dict))
    return f"{gp.get('title', '')}. Formula: {gp.get('formula', '')}. Examples: {examples}. {gp.get('explanation_vi', '')}"


def speech_windows(exercises, transcript, alignment):
    """Teacher speech from each question's aligned start to the next question's start (max SPEECH_MAX_S)."""
    starts_by_id = {a["id"]: a["start"] for a in alignment}
    starts = [starts_by_id.get(ex["id"], ex["start"]) for ex in exercises]
    out = []
    for k, t0 in enumerate(starts):
        nxt = starts[k + 1] if k + 1 < len(starts) and starts[k + 1] > t0 else t0 + SPEECH_MAX_S
        t1 = min(nxt, t0 + SPEECH_MAX_S)
        out.append(" ".join(s["text"] for s in transcript if t0 <= s["start"] < t1))
    return out


def dense_scores(q_texts, s_texts, c_texts, model_name=MODEL_NAME):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    enc = lambda xs, p: model.encode([p + x for x in xs], normalize_embeddings=True)
    C = enc(c_texts, PASSAGE_PREFIX)
    return (enc(q_texts, QUERY_PREFIX) @ C.T + enc(s_texts, QUERY_PREFIX) @ C.T) / 2


def tfidf_scores(q_texts, s_texts, c_texts):
    from sklearn.feature_extraction.text import TfidfVectorizer
    docs = [q + " " + s for q, s in zip(q_texts, s_texts)]
    vec = TfidfVectorizer(token_pattern=r"(?u)\b\w\w+\b").fit(docs + c_texts)
    return (vec.transform(docs) @ vec.transform(c_texts).T).toarray()


def link_exercises_to_concepts(lesson_dir: Path, threshold: float = None, out_name: str = "exercise_concept_links.json") -> list:
    lesson_dir = Path(lesson_dir)
    ex_path, gp_path = lesson_dir / "exercises.json", lesson_dir / "grammar_points.json"
    if not ex_path.is_file() or not gp_path.is_file():
        print(f"[concept_link] Warning: Missing {ex_path} or {gp_path}. Skipping.", file=sys.stderr)
        return []
    exercises = json.loads(ex_path.read_text(encoding="utf-8"))
    grammar_points = json.loads(gp_path.read_text(encoding="utf-8"))
    if not exercises or not grammar_points:
        return []
    tr_path, al_path = lesson_dir / "transcript.json", lesson_dir / "exercise_alignment.json"
    transcript = json.loads(tr_path.read_text(encoding="utf-8")) if tr_path.is_file() else []
    alignment = json.loads(al_path.read_text(encoding="utf-8")) if al_path.is_file() else []

    q_texts = [question_text(e) for e in exercises]
    s_texts = speech_windows(exercises, transcript, alignment)
    c_texts = [concept_text(g) for g in grammar_points]
    print(f"[concept_link] Linking {len(exercises)} questions to {len(grammar_points)} grammar topics...")
    try:
        S = dense_scores(q_texts, s_texts, c_texts)
        method, theta = MODEL_NAME.split("/")[-1] + "+speech", THRESHOLD if threshold is None else threshold
    except Exception as e:  # sentence-transformers missing or model unavailable offline
        print(f"[concept_link] Dense model unavailable ({e}); using TF-IDF fallback.", file=sys.stderr)
        S = tfidf_scores(q_texts, s_texts, c_texts)
        method, theta = "tfidf+speech", TFIDF_THRESHOLD if threshold is None else threshold

    links = []
    for i, ex in enumerate(exercises):
        order = np.argsort(-S[i])
        best, second = int(order[0]), (int(order[1]) if len(order) > 1 else None)
        score = float(S[i, best])
        margin = score - float(S[i, second]) if second is not None else score
        rec = {
            "question_id": ex["id"], "question_number": ex["number"],
            "similarity_score": round(score, 3), "margin": round(margin, 3), "method": method,
            "threshold": theta, "practice_timestamp": next((a["start"] for a in alignment if a["id"] == ex["id"]), ex["start"]),
        }
        if score >= theta:
            gp = grammar_points[best]
            rec.update(grammar_point_id=gp["id"], grammar_title=gp["title"],
                       confidence="HIGH" if margin >= HIGH_MARGIN else "MEDIUM",
                       theory_timestamp=gp.get("timestamp"), theory_time_str=gp.get("time_str"))
        else:
            rec.update(grammar_point_id=None, grammar_title="Không gắn chủ điểm (từ vựng / đọc hiểu)",
                       confidence="LOW", theory_timestamp=None, theory_time_str=None)
        links.append(rec)

    out_path = lesson_dir / out_name
    out_path.write_text(json.dumps(links, ensure_ascii=False, indent=2), encoding="utf-8")
    n = sum(1 for l in links if l["grammar_point_id"])
    print(f"[concept_link] {method}: {n}/{len(links)} questions linked (threshold {theta}) -> {out_path}")
    return links


def main():
    parser = argparse.ArgumentParser(description="Link exercise questions to grammar concepts.")
    parser.add_argument("lesson_pos", nargs="?", default=None, help="Path to lesson directory (positional)")
    parser.add_argument("--lesson", default=None, help="Path to lesson directory (flag)")
    parser.add_argument("--threshold", type=float, default=None, help="override the link threshold")
    args = parser.parse_args()

    target_lesson = args.lesson or args.lesson_pos or "lessons/ece-toeic-starter-u4"
    lesson_dir = Path(target_lesson)
    if not lesson_dir.is_dir():
        print(f"Error: {lesson_dir} is not a directory", file=sys.stderr)
        sys.exit(1)
    link_exercises_to_concepts(lesson_dir, threshold=args.threshold)


if __name__ == "__main__":
    main()
