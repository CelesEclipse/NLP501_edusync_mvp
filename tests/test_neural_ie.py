import json
import os
import sys
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_ie import format_time, fallback_rule_based_extraction, extract_neural_ie, load_env_key


def test_format_time():
    assert format_time(0.0) == "00:00"
    assert format_time(75.5) == "01:15"
    assert format_time(600) == "10:00"
    assert format_time(3605) == "60:05"


def test_fallback_rule_based_structure():
    res = fallback_rule_based_extraction([], [], [])
    assert "grammar_points" in res
    assert "vocab_deep" in res
    gps = res["grammar_points"]
    vds = res["vocab_deep"]

    assert len(gps) >= 3
    for gp in gps:
        assert "id" in gp
        assert "title" in gp
        assert "formula" in gp
        assert "explanation_vi" in gp
        assert "examples" in gp and len(gp["examples"]) > 0
        assert "timestamp" in gp
        assert "toeic_tips" in gp
        assert isinstance(gp["timestamp"], (int, float))

    assert len(vds) >= 5
    for vd in vds:
        assert "word" in vd
        assert "pos" in vd
        assert "level" in vd
        assert "meaning_vi" in vd
        assert "collocations" in vd
        assert "timestamp" in vd


def test_extract_neural_ie_forced_fallback(tmp_path):
    # Create minimal lesson folder
    (tmp_path / "transcript.json").write_text("[]", encoding="utf-8")
    (tmp_path / "exercises.json").write_text("[]", encoding="utf-8")

    res = extract_neural_ie(tmp_path, force_rule_based=True)
    assert len(res["grammar_points"]) >= 3
    assert len(res["vocab_deep"]) >= 5


def test_real_lesson_has_neural_ie_outputs():
    lesson_dir = Path("lessons/ece-toeic-starter-u4")
    gp_path = lesson_dir / "grammar_points.json"
    vd_path = lesson_dir / "vocab_deep.json"

    assert gp_path.is_file(), "grammar_points.json should exist"
    assert vd_path.is_file(), "vocab_deep.json should exist"

    gps = json.loads(gp_path.read_text(encoding="utf-8"))
    vds = json.loads(vd_path.read_text(encoding="utf-8"))

    assert len(gps) >= 3
    assert any("participle" in gp["title"].lower() or "phân từ" in gp["title"].lower() for gp in gps)
    assert any("have" in gp["formula"].lower() or "sai khiến" in gp["title"].lower() or "causative" in gp["title"].lower() for gp in gps)

    assert len(vds) >= 5
    words = [v["word"].lower() for v in vds]
    assert "depression" in words or "retail" in words or "wholesale" in words
