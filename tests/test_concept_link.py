"""Unit tests for concept_link.py (Dense Semantic Embeddings for Question-to-Concept Linking)."""
import json
import os
import sys
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from concept_link import link_exercises_to_concepts


def test_link_exercises_to_concepts_real_lesson():
    lesson_dir = Path("lessons/ece-toeic-starter-u4")
    assert (lesson_dir / "exercises.json").is_file()
    assert (lesson_dir / "grammar_points.json").is_file()

    links = link_exercises_to_concepts(lesson_dir, threshold=0.10)
    assert len(links) == 34, f"Expected 34 links, got {len(links)}"

    for link in links:
        assert "question_id" in link
        assert "question_number" in link
        assert "grammar_title" in link
        assert "similarity_score" in link
        assert isinstance(link["similarity_score"], (int, float))
        assert "practice_timestamp" in link


def test_concept_link_output_file_exists():
    out_file = Path("lessons/ece-toeic-starter-u4/exercise_concept_links.json")
    assert out_file.is_file()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert len(data) == 34
    
    # Check that high confidence links have valid grammar IDs
    high_conf = [d for d in data if d.get("confidence") in ("HIGH", "MEDIUM")]
    assert len(high_conf) > 0
    assert any("Participles" in d["grammar_title"] for d in high_conf)
