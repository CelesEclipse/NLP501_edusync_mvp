#!/usr/bin/env python3
"""
concept_link.py — Question-to-Concept Linking via Dense Semantic Embeddings.

Maps exercise questions to core grammar topics using Sentence-Transformers (all-MiniLM-L6-v2)
and Cosine Similarity.
"""
import argparse
import json
import os
import sys
from pathlib import Path
import numpy as np

try:
    from sentence_transformers import SentenceTransformer, util
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


# Fallback keyword associations if sentence_transformers cannot load
KEYWORD_CUES = {
    "gp_1": ["participle", "adjective", "bored", "boring", "moving", "moved", "annoying", "annoyed", "pleased", "pleasing", "-ing", "-ed", "fall asleep", "noise"],
    "gp_2": ["causative", "have", "has", "had", "get", "shoes", "shine", "shined", "repair", "cut", "hair"],
    "gp_3": ["passive", "require", "demand", "suggest", "written", "papers", "ink", "modal", "be written", "should be"],
    "gp_4": ["modifier", "adjective", "noun", "central", "luxury", "hotel", "retail", "wholesale", "sales"]
}


def link_exercises_to_concepts(lesson_dir: Path, threshold: float = 0.12) -> list:
    ex_path = lesson_dir / "exercises.json"
    gp_path = lesson_dir / "grammar_points.json"

    if not ex_path.is_file() or not gp_path.is_file():
        print(f"[concept_link] Warning: Missing {ex_path} or {gp_path}. Skipping.", file=sys.stderr)
        return []

    exercises = json.loads(ex_path.read_text(encoding="utf-8"))
    grammar_points = json.loads(gp_path.read_text(encoding="utf-8"))

    if not exercises or not grammar_points:
        return []

    print(f"[concept_link] Linking {len(exercises)} questions to {len(grammar_points)} grammar topics...")

    links = []

    if HAS_SENTENCE_TRANSFORMERS:
        try:
            model = SentenceTransformer("all-MiniLM-L6-v2")

            # 1. Prepare Question text representations
            q_texts = []
            for ex in exercises:
                opts_str = " ".join([f"{k}. {v}" for k, v in ex.get("options", {}).items()])
                q_texts.append(f"{ex.get('stem', '')} Options: {opts_str}")

            # 2. Prepare Grammar representations enriched with cues and examples
            gp_texts = []
            for gp in grammar_points:
                gp_id = gp.get("id", "")
                cues = " ".join(KEYWORD_CUES.get(gp_id, []))
                ex_str = " ".join([x.get("en", "") for x in gp.get("examples", []) if isinstance(x, dict)])
                text = f"{gp.get('title', '')}. Formula: {gp.get('formula', '')}. Explanation: {gp.get('explanation_vi', '')}. Keywords: {cues}. Examples: {ex_str}"
                gp_texts.append(text)

            # 3. Dense Vector Encoding
            Q_emb = model.encode(q_texts, convert_to_tensor=True, normalize_embeddings=True)
            GP_emb = model.encode(gp_texts, convert_to_tensor=True, normalize_embeddings=True)

            # 4. Matrix Cosine Similarity
            sim_matrix = util.cos_sim(Q_emb, GP_emb).cpu().numpy()

            for i, ex in enumerate(exercises):
                best_idx = int(np.argmax(sim_matrix[i]))
                best_score = float(sim_matrix[i][best_idx])

                if best_score >= threshold:
                    best_gp = grammar_points[best_idx]
                    links.append({
                        "question_id": ex["id"],
                        "question_number": ex["number"],
                        "grammar_point_id": best_gp["id"],
                        "grammar_title": best_gp["title"],
                        "similarity_score": round(best_score, 3),
                        "confidence": "HIGH" if best_score >= 0.25 else "MEDIUM",
                        "practice_timestamp": ex["start"],
                        "theory_timestamp": best_gp.get("timestamp", 49.0),
                        "theory_time_str": best_gp.get("time_str", "00:49")
                    })
                else:
                    links.append({
                        "question_id": ex["id"],
                        "question_number": ex["number"],
                        "grammar_point_id": None,
                        "grammar_title": "General TOEIC Practice",
                        "similarity_score": round(best_score, 3),
                        "confidence": "LOW",
                        "practice_timestamp": ex["start"],
                        "theory_timestamp": None,
                        "theory_time_str": None
                    })
            print(f"[concept_link] Dense Embedding linking completed with SentenceTransformers.")
        except Exception as e:
            print(f"[concept_link] Warning: Neural inference failed ({e}), falling back to keyword heuristic.", file=sys.stderr)
            links = []

    # Heuristic Fallback if not HAS_SENTENCE_TRANSFORMERS or model failure
    if not links:
        for ex in exercises:
            text = (ex.get("stem", "") + " " + " ".join(ex.get("options", {}).values())).lower()
            best_gp = None
            max_matches = 0
            for gp in grammar_points:
                gp_id = gp.get("id", "")
                cues = KEYWORD_CUES.get(gp_id, [])
                matches = sum(1 for c in cues if c in text)
                if matches > max_matches:
                    max_matches = matches
                    best_gp = gp
            
            if best_gp and max_matches > 0:
                links.append({
                    "question_id": ex["id"],
                    "question_number": ex["number"],
                    "grammar_point_id": best_gp["id"],
                    "grammar_title": best_gp["title"],
                    "similarity_score": 0.5 + 0.1 * min(max_matches, 4),
                    "confidence": "MEDIUM",
                    "practice_timestamp": ex["start"],
                    "theory_timestamp": best_gp.get("timestamp", 49.0),
                    "theory_time_str": best_gp.get("time_str", "00:49")
                })
            else:
                links.append({
                    "question_id": ex["id"],
                    "question_number": ex["number"],
                    "grammar_point_id": None,
                    "grammar_title": "General TOEIC Practice",
                    "similarity_score": 0.0,
                    "confidence": "LOW",
                    "practice_timestamp": ex["start"],
                    "theory_timestamp": None,
                    "theory_time_str": None
                })

    out_path = lesson_dir / "exercise_concept_links.json"
    out_path.write_text(json.dumps(links, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[concept_link] Generated {len(links)} links -> {out_path}")
    return links


def main():
    parser = argparse.ArgumentParser(description="Link exercise questions to grammar concepts via Dense Semantic Embeddings.")
    parser.add_argument("lesson_pos", nargs="?", default=None, help="Path to lesson directory (positional)")
    parser.add_argument("--lesson", default=None, help="Path to lesson directory (flag)")
    parser.add_argument("--threshold", type=float, default=0.12, help="Cosine similarity threshold")
    args = parser.parse_args()

    target_lesson = args.lesson or args.lesson_pos or "lessons/ece-toeic-starter-u4"
    lesson_dir = Path(target_lesson)
    if not lesson_dir.is_dir():
        print(f"Error: {lesson_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    link_exercises_to_concepts(lesson_dir, threshold=args.threshold)


if __name__ == "__main__":
    main()
