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


def _cats(text):
    edits, corrected = GECRuleEngine().check_sentence(text)
    return [e["category"] for e in edits], [e["error_type"] for e in edits], corrected


def test_gec_unnecessary_be():
    cats, types, corrected = _cats("I am agree with teacher.")
    assert cats == ["BE_VERB"] and types == ["U:VERB:TENSE"]
    assert "I agree" in corrected


def test_gec_be_verb_generalises():
    assert _cats("She is not understand the question")[2] == "She does not understand the question"
    assert _cats("I'm think the answer is B")[0] == ["BE_VERB"]


def test_gec_participle_confusion():
    cats, types, corrected = _cats("The movie was moved.")
    assert cats == ["PARTICIPLE"] and types == ["R:VERB:FORM"]
    assert "moving" in corrected


def test_gec_participle_generalises():
    assert _cats("I am so confusing")[2] == "I am so confused"
    assert _cats("This noise is very annoy")[2] == "This noise is very annoying"
    assert _cats("The lesson was bored")[2] == "The lesson was boring"


def test_gec_causative_verb():
    cats, types, corrected = _cats("He has his shoes shine.")
    assert cats == ["CAUSATIVE"] and types == ["R:VERB:FORM"]
    assert "shined" in corrected
    assert _cats("I will have my car repair tomorrow")[2] == "I will have my car repaired tomorrow"


def test_gec_modal_bare_infinitive():
    cats, types, corrected = _cats("Sales should to increase by 200%.")
    assert cats == ["MODAL_TO"] and types == ["U:VERB:FORM"]
    assert "should increase" in corrected
    assert _cats("I can't to hear you")[2] == "I can't hear you"


def test_gec_subject_verb_agreement():
    cats, types, corrected = _cats("It make me feel happy.")
    assert cats == ["SVA"] and types == ["R:VERB:SVA"]
    assert "makes" in corrected
    assert _cats("she don't like it")[2] == "she doesn't like it"


def test_gec_missing_auxiliary():
    cats, types, corrected = _cats("Why we use this word?")
    assert cats == ["WH_DO"] and types == ["M:VERB:TENSE"]
    assert "Why do we use" in corrected
    assert _cats("How she know the answer?")[2] == "How does she know the answer?"


@pytest.mark.parametrize("ok", [
    "I am interested in this topic", "She had her hair cut yesterday", "Does it make sense?",
    "I know why we use it", "Make it work", "He has to go", "You ought to study", "I was bored",
    "The movie was moving", "He's like his father", "Can I ask a question?", "We are agreed on the plan",
])
def test_gec_no_false_alarm_on_correct_sentences(ok):
    assert _cats(ok)[0] == []


def test_answer_choice_parsed():
    linked, _ = anonymize_and_link([{"sender": "A", "timestamp": 5.0, "time_str": "00:00:05",
                                     "message": "Câu 1 em chọn C, central luxury hotel."}])
    assert linked[0]["answer_choice"] == "C"


def test_chat_links_to_latest_question_with_that_number():
    exercises = [{"id": "q_1", "number": 1, "start": 100.0}, {"id": "q_5", "number": 1, "start": 800.0}]
    linked, _ = anonymize_and_link([{"sender": "A", "timestamp": 900.0, "time_str": "00:15:00", "message": "Câu 1 em chọn B"}],
                                   exercises)
    assert linked[0]["exercise_id"] == "q_5"
