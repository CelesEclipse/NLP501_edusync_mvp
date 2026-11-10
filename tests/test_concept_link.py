"""Unit tests for concept_link.py. Outputs go to tmp_path, never into lessons/."""
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import concept_link
from concept_link import link_exercises_to_concepts, speech_windows, tfidf_scores

REAL = Path("lessons/ece-toeic-starter-u4")


def test_no_hand_written_keyword_cues():
    assert not hasattr(concept_link, "KEYWORD_CUES")


def test_speech_window_stops_at_next_question():
    ex = [{"id": "a", "start": 0.0}, {"id": "b", "start": 0.0}]
    al = [{"id": "a", "start": 10.0}, {"id": "b", "start": 20.0}]
    tr = [{"start": 12.0, "text": "one"}, {"start": 25.0, "text": "two"}]
    assert speech_windows(ex, tr, al) == ["one", "two"]


def test_tfidf_fallback_prefers_matching_concept():
    S = tfidf_scores(["has his shoes shined"], ["công thức nhờ vả have cộng vật cộng verb 3"],
                     ["Causative have something done shined", "Passive voice be written"])
    assert S[0, 0] > S[0, 1]


def test_link_real_lesson_copy(tmp_path):
    pytest.importorskip("sentence_transformers")
    for f in ["exercises.json", "grammar_points.json", "transcript.json", "exercise_alignment.json"]:
        shutil.copy(REAL / f, tmp_path / f)
    links = link_exercises_to_concepts(tmp_path)
    assert len(links) == 34
    assert (tmp_path / "exercise_concept_links.json").is_file()
    for l in links:
        assert {"question_id", "grammar_point_id", "similarity_score", "confidence"} <= set(l)
        assert (l["grammar_point_id"] is None) == (l["confidence"] == "LOW")
