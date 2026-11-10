"""Unit tests for teacher_analytics.py. All tests write into tmp_path, never into lessons/."""
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from teacher_analytics import generate_teacher_report

REAL = Path("lessons/ece-toeic-starter-u4")
FILES = ["speakers.json", "chat_feedback.json", "exercise_concept_links.json", "lesson.json", "grammar_points.json"]


def _copy_lesson(tmp_path):
    for f in FILES:
        if (REAL / f).is_file():
            shutil.copy(REAL / f, tmp_path / f)
    return tmp_path


def test_report_on_real_lesson_copy(tmp_path):
    report = generate_teacher_report(_copy_lesson(tmp_path))
    assert (tmp_path / "teacher_report.json").is_file()
    assert set(report) >= {"class_meta", "interaction_health", "error_distribution", "weakest_concept",
                           "next_lesson_action_plan"}
    # single-speaker recording: TTT/STT must be reported as not measurable, not as 100 / 0
    ih = report["interaction_health"]
    assert ih["measured"] is False and ih["teacher_talk_time_pct"] is None
    cats = [e["category"] for e in report["error_distribution"]]
    assert "PARTICIPLE" in cats
    assert report["class_meta"]["total_students_active"] == 5
    assert all(len(step) > 10 for step in report["next_lesson_action_plan"])


def test_talk_time_measured_with_separate_tracks(tmp_path):
    (tmp_path / "speakers.json").write_text(json.dumps({"source": "tracks", "talk_time": {"T": 80.0, "S1": 20.0}}))
    ih = generate_teacher_report(tmp_path)["interaction_health"]
    assert ih["measured"] is True and ih["teacher_talk_time_pct"] == 80.0 and ih["student_talk_time_pct"] == 20.0


def test_no_evidence_means_no_weakest_concept_and_no_invented_students(tmp_path):
    (tmp_path / "chat_feedback.json").write_text("[]")
    report = generate_teacher_report(tmp_path)
    assert report["weakest_concept"] is None
    assert report["class_meta"]["total_students_active"] == 0
    assert report["error_distribution"] == []


def test_weakest_concept_uses_exercise_id(tmp_path):
    (tmp_path / "exercise_concept_links.json").write_text(json.dumps([
        {"question_id": "q_1", "question_number": 1, "grammar_point_id": "gp_a", "grammar_title": "A"},
        {"question_id": "q_9", "question_number": 1, "grammar_point_id": "gp_b", "grammar_title": "B"}]))
    err = {"has_error": True, "speaker_id": "S1", "question_number": 1,
           "edits": [{"category": "SVA", "error_type": "R:VERB:SVA"}]}
    (tmp_path / "chat_feedback.json").write_text(json.dumps([{**err, "exercise_id": "q_9"}]))
    report = generate_teacher_report(tmp_path)
    assert report["weakest_concept"]["concept_id"] == "gp_b"      # not confused by the repeated number 1
