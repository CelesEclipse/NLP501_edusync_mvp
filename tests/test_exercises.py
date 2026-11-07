import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from exercises import extract_stem_and_options, deduplicate_exercises
from exercise_align import align_exercises


def test_extract_stem_and_options_parentheses():
    text = "Professor Miller requires that all papers be in ink. (A) formatted (B) copied (C) written (D) made"
    stem, opts = extract_stem_and_options(text)
    assert "Professor Miller" in stem
    assert opts["A"] == "formatted"
    assert opts["B"] == "copied"
    assert opts["C"] == "written"
    assert opts["D"] == "made"


def test_extract_stem_and_options_dot_notation():
    text = "Choose the best option. A. center B. located C. central D. best"
    stem, opts = extract_stem_and_options(text)
    assert "Choose the best option" in stem
    assert opts["A"] == "center"
    assert opts["B"] == "located"
    assert opts["C"] == "central"
    assert opts["D"] == "best"


def test_deduplicate_exercises():
    raw = [
        {"number": 1, "stem": "Short stem", "options": {"A": "yes"}, "screen": 3, "start": 10.0, "end": 20.0},
        {"number": 1, "stem": "Longer stem with more words", "options": {"A": "yes", "B": "no"}, "screen": 4, "start": 20.0, "end": 30.0},
        {"number": 2, "stem": "Question 2 stem", "options": {"A": "opt"}, "screen": 4, "start": 20.0, "end": 30.0},
    ]
    merged = deduplicate_exercises(raw)
    assert len(merged) == 2
    assert merged[0]["number"] == 1
    assert merged[0]["screens"] == [3, 4]
    assert merged[0]["end"] == 30.0
    assert "Longer stem" in merged[0]["stem"]
    assert merged[1]["number"] == 2


def test_align_exercises_monotonic():
    exercises = [
        {"id": "q1", "number": 1, "stem": "First question stem", "options": {}, "screens": [1], "start": 0.0, "end": 100.0},
        {"id": "q2", "number": 2, "stem": "Second question stem", "options": {}, "screens": [1], "start": 0.0, "end": 100.0},
    ]
    transcript = [
        {"start": 10.0, "end": 15.0, "text": "Chúng ta bắt đầu làm câu số 1."},
        {"start": 25.0, "end": 30.0, "text": "Bây giờ chuyển sang câu số 2."},
    ]
    aligned = align_exercises(exercises, transcript)
    assert len(aligned) == 2
    assert aligned[0]["number"] == 1
    assert aligned[0]["start"] == 10.0
    assert aligned[1]["number"] == 2
    assert aligned[1]["start"] == 25.0

