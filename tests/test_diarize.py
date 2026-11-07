import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from diarize import assign_roles, match_speakers_to_transcript


def test_assign_roles_teacher_and_students():
    raw_turns = [
        {"raw_speaker": "Alice", "start": 0.0, "end": 100.0},
        {"raw_speaker": "Bob", "start": 102.0, "end": 112.0},
        {"raw_speaker": "Charlie", "start": 115.0, "end": 120.0},
        {"raw_speaker": "Alice", "start": 125.0, "end": 200.0},
    ]
    mapping, roles, turns = assign_roles(raw_turns)
    # Alice has 175s, Bob has 10s, Charlie has 5s
    assert mapping["Alice"] == "T"
    assert roles["T"] == "teacher"
    assert mapping["Bob"] == "S1"
    assert mapping["Charlie"] == "S2"
    assert len(turns) == 4
    assert turns[0]["speaker"] == "T"
    assert turns[1]["speaker"] == "S1"


def test_assign_roles_forced_teacher():
    raw_turns = [
        {"raw_speaker": "Alice", "start": 0.0, "end": 100.0},
        {"raw_speaker": "Bob", "start": 102.0, "end": 112.0},
    ]
    mapping, roles, turns = assign_roles(raw_turns, forced_teacher="Bob")
    assert mapping["Bob"] == "T"
    assert mapping["Alice"] == "S1"


def test_match_speakers_to_transcript():
    turns = [
        {"speaker": "T", "start": 0.0, "end": 10.0},
        {"speaker": "S1", "start": 10.5, "end": 15.0},
        {"speaker": "T", "start": 15.5, "end": 30.0},
    ]
    transcript = [
        {"start": 1.0, "end": 5.0, "text": "Good morning class"},
        {"start": 11.0, "end": 14.0, "text": "Teacher, I have a question"},
        {"start": 16.0, "end": 20.0, "text": "Yes, please ask"},
    ]
    updated = match_speakers_to_transcript(transcript, turns)
    assert updated[0]["speaker"] == "T"
    assert updated[1]["speaker"] == "S1"
    assert updated[2]["speaker"] == "T"
