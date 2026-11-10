import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neural_ie import format_time, fallback_rule_based_extraction, extract_neural_ie, MIN_CUE_HITS


def test_format_time():
    assert format_time(0.0) == "00:00"
    assert format_time(75.5) == "01:15"
    assert format_time(600) == "10:00"
    assert format_time(3605) == "60:05"


def _seg(t, text):
    return {"start": float(t), "end": float(t) + 3, "text": text}


def test_fallback_detects_topics_from_speech_only():
    transcript = [_seg(10 * i, "những phân từ này thêm ing hoặc thêm ed") for i in range(MIN_CUE_HITS)]
    transcript += [_seg(500, "đây là câu bị động"), _seg(600, "hello")]
    res = fallback_rule_based_extraction(transcript, [], [])
    titles = [g["title"] for g in res["grammar_points"]]
    assert any("Participle" in t for t in titles)
    assert not any("Passive" in t for t in titles)          # only one cue -> below MIN_CUE_HITS
    gp = res["grammar_points"][0]
    assert gp["timestamp"] == 0.0 and gp["source"] == "taxonomy_fallback"


def test_fallback_invents_nothing_on_empty_input():
    res = fallback_rule_based_extraction([], [], [])
    assert res == {"grammar_points": [], "vocab_deep": []}


def test_fallback_vocab_comes_from_vocab_json():
    vocab = [{"word": "prosperity", "level": "C1", "pos": "noun", "meaning_vi": "sự thịnh vượng", "timestamp": 12.0},
             {"word": "movie", "level": "A1", "timestamp": 3.0}]
    res = fallback_rule_based_extraction([], [], vocab)
    assert [v["word"] for v in res["vocab_deep"]] == ["prosperity"]


def test_extract_neural_ie_forced_fallback(tmp_path):
    (tmp_path / "transcript.json").write_text("[]", encoding="utf-8")
    (tmp_path / "exercises.json").write_text("[]", encoding="utf-8")
    res = extract_neural_ie(tmp_path, force_rule_based=True)
    assert res["grammar_points"] == []


def test_real_lesson_grammar_points_are_grounded():
    gps = json.loads(Path("lessons/ece-toeic-starter-u4/grammar_points.json").read_text(encoding="utf-8"))
    assert len(gps) >= 3
    assert any("participle" in gp["title"].lower() for gp in gps)
    for gp in gps:
        assert isinstance(gp["timestamp"], (int, float))


def test_fallback_accepts_vocab_without_timestamp():
    """vocab.py leaves timestamp None for words never spoken; the fallback must not crash on them."""
    vocab = [{"word": "negotiate", "level": "B2", "timestamp": None}, {"word": "retail", "level": "B1"}]
    out = fallback_rule_based_extraction([], [], vocab)
    assert [v["timestamp"] for v in out["vocab_deep"]] == [0.0, 0.0]
