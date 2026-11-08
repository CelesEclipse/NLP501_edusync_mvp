"""Unit tests for chat_parser.py and feedback.py (GEC Diagnostic Engine)."""
import os, sys, pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chat_parser import parse_timestamp, parse_chat_log, anonymize_and_link
from feedback import GECRuleEngine, generate_feedback


def test_parse_timestamp():
    assert parse_timestamp("00:03:12") == 192.0
    assert parse_timestamp("01:00:00") == 3600.0
    assert parse_timestamp("02:30") == 150.0


def test_parse_zoom_chat():
    raw_chat = """00:03:12 From Nguyen Hoang Minh to Everyone:
Em chào cô và cả lớp ạ!
00:03:22 From Tran Thi Mai to Everyone:
Câu 1 em chọn C, central luxury hotel.
"""
    entries = parse_chat_log(raw_chat)
    assert len(entries) == 2
    assert entries[0]["sender"] == "Nguyen Hoang Minh"
    assert entries[0]["timestamp"] == 192.0
    assert "Em chào cô" in entries[0]["message"]
    assert entries[1]["sender"] == "Tran Thi Mai"
    assert "Câu 1 em chọn C" in entries[1]["message"]


def test_anonymize_student_names():
    raw_entries = [
        {"sender": "Nguyen Hoang Minh", "timestamp": 10.0, "time_str": "00:00:10", "message": "Hi"},
        {"sender": "Tran Thi Mai", "timestamp": 20.0, "time_str": "00:00:20", "message": "Hello"},
        {"sender": "Nguyen Hoang Minh", "timestamp": 30.0, "time_str": "00:00:30", "message": "Again"}
    ]
    linked, spk_map = anonymize_and_link(raw_entries)
    assert len(spk_map) == 2
    assert linked[0]["speaker_id"] == "S1"
    assert linked[1]["speaker_id"] == "S2"
    assert linked[2]["speaker_id"] == "S1"  # Same student keeps same ID


def test_link_chat_to_exercises():
    raw_entries = [
        {"sender": "Student A", "timestamp": 190.0, "time_str": "00:03:10", "message": "Câu 1 em chọn C"}
    ]
    exercises = [
        {"id": "q_1", "number": 1, "start": 189.11, "end": 230.0}
    ]
    linked, _ = anonymize_and_link(raw_entries, exercises)
    assert linked[0]["question_number"] == 1
    assert linked[0]["exercise_id"] == "q_1"


def test_gec_unnecessary_be():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("I am agree with teacher.")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "U:VERB:BE"
    assert "I agree" in corrected


def test_gec_participle_confusion():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("The movie was moved.")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "R:ADJ:PARTICIPLE"
    assert "moving" in corrected


def test_gec_causative_verb():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("He has his shoes shine.")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "R:VERB:FORM"
    assert "shined" in corrected


def test_gec_modal_bare_infinitive():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("Sales should to increase by 200%.")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "U:PREP"
    assert "should increase" in corrected


def test_gec_subject_verb_agreement():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("It make me feel happy.")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "R:VERB:SVA"
    assert "makes" in corrected


def test_gec_missing_auxiliary():
    engine = GECRuleEngine()
    edits, corrected = engine.check_sentence("Why we use this word?")
    assert len(edits) == 1
    assert edits[0]["error_type"] == "M:VERB:AUX"
    assert "Why do we use" in corrected
