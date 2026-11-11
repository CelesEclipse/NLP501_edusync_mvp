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



# ---- monotonic DP alignment -----------------------------------------------------------------------------------
from exercise_align import align_dp, align_greedy, start_times, question_pattern


def _ex(i, num, stem, start=0.0, end=100.0):
    return {"id": f"q{i}", "number": num, "stem": stem, "options": {}, "screens": [1], "start": start, "end": end}


def _seg(t, text):
    return {"start": t, "end": t + 4.0, "text": text}


def test_dp_finds_global_optimum_where_greedy_fails():
    # q1's strongest cue comes late (t=50), q2 is only discussed at t=30. Greedy takes q1@50 and loses q2;
    # DP takes q1@10 + q2@30 (higher total, both matched, still monotonic).
    exercises = [_ex(1, 1, "hotel luxury central"), _ex(2, 2, "package massage weekend")]
    transcript = [_seg(10.0, "luxury hotel central"), _seg(30.0, "câu số 2 package massage"),
                  _seg(50.0, "câu số 1 hotel luxury")]
    assert align_greedy(exercises, transcript) == {0: 2}
    assert align_dp(exercises, transcript) == {0: 0, 1: 1}


def test_unsupported_number_mention_is_demoted():
    # "câu số 1" at t=5 is followed (within 60 s) by unrelated words only; the real question is discussed at t=90
    exercises = [_ex(1, 1, "plaza hotel located heart city")]
    transcript = [_seg(5.0, "câu số 1 news"), _seg(9.0, "danh từ news"), _seg(90.0, "located plaza hotel heart city")]
    assert align_dp(exercises, transcript) == {0: 2}


def test_ordinal_and_spelled_numbers_are_triggers():
    assert question_pattern(4).search("Sang câu thứ 4.")
    assert question_pattern(4).search("câu thứ tư")
    assert not question_pattern(2).search("text 2 nói về")
    assert not question_pattern(5).search("part 5 incomplete sentences")


def test_unmatched_fallback_keeps_order():
    exercises = [_ex(1, 1, "a", start=0.0), _ex(2, 2, "b", start=5.0), _ex(3, 3, "c", start=50.0)]
    transcript = [_seg(40.0, "x"), _seg(60.0, "y")]
    times = start_times(exercises, transcript, {0: 0, 2: 1})   # q2 unmatched, its screen start (5) < q1 (40)
    assert times == sorted(times) and times[1] == 40.0


from exercises import parse_screen_text


def test_toeic_part7_numbers_are_extracted():
    """Real TOEIC tests number Part 5-7 as 101-200; the multi-source test set showed 0/7 found with 1-2 digits only."""
    screen = {"id": 3, "start": 10.0, "end": 60.0,
              "text": "147. What type of event is the invitation for?\n(A) A community food fair\n(B) An annual banquet\n"
                      "148. What is true about Ricardo's Corner?\n(A) It operates multiple stores.\n(B) It will not sell goods"}
    assert [q["number"] for q in parse_screen_text(screen)] == [147, 148]


def test_labelled_question_numbers_are_extracted():
    screen = {"id": 1, "start": 0.0, "end": 30.0,
              "text": "Number 7 Can I help you?\nA. Yes, it is.\nB. No, he doesn't mind.\n"
                      "Question 8: Where is the meeting?\n(A) Room 2\n(B) At noon"}
    qs = parse_screen_text(screen)
    assert [q["number"] for q in qs] == [7, 8]
    assert qs[0]["stem"].startswith("Can I help you")


def test_years_and_quantities_are_not_question_numbers():
    screen = {"id": 1, "start": 0.0, "end": 30.0, "text": "2016, Test 1 review\n200 customers will get a discount"}
    assert parse_screen_text(screen) == []
