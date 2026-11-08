"""Unit tests for teacher_analytics.py (Automated Pedagogical Quality & Action Plan Engine)."""
import json
import os
import sys
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from teacher_analytics import generate_teacher_report


def test_generate_teacher_report_real_lesson():
    lesson_dir = Path("lessons/ece-toeic-starter-u4")
    report = generate_teacher_report(lesson_dir)

    assert "class_meta" in report
    assert "interaction_health" in report
    assert "error_distribution" in report
    assert "weakest_concept" in report
    assert "next_lesson_action_plan" in report

    # Check interaction health
    health = report["interaction_health"]
    assert "teacher_talk_time_pct" in health
    assert "student_talk_time_pct" in health
    assert health["teacher_talk_time_pct"] >= 90.0

    # Check error distribution
    errors = report["error_distribution"]
    assert len(errors) >= 3
    err_types = [e["error_type"] for e in errors]
    assert "R:ADJ:PARTICIPLE" in err_types

    # Check action plan has at least 3 concrete steps
    plan = report["next_lesson_action_plan"]
    assert len(plan) >= 3
    for step in plan:
        assert len(step.strip()) > 10


def test_teacher_report_output_file_saved():
    out_file = Path("lessons/ece-toeic-starter-u4/teacher_report.json")
    assert out_file.is_file()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["class_meta"]["total_students_active"] == 5

