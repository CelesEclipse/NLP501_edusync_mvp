"""Unit tests for vocab.py: CEFR profiling, lemmatization, teacher definition mining."""
import os, sys, pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vocab import resolve_lemma, extract_meanings_from_speech, extract_vocabulary, VI_HOMOPHONES


SAMPLE_LEXICON = {
    "shoe": {"level": "A1", "pos": "noun"},
    "movie": {"level": "A1", "pos": "noun"},
    "actor": {"level": "A1", "pos": "noun"},
    "write": {"level": "A1", "pos": "verb"},
    "increase": {"level": "B1", "pos": "verb"},
    "prosperity": {"level": "B1", "pos": "noun"},
    "determine": {"level": "B1", "pos": "verb"},
    "retirement": {"level": "B2", "pos": "noun"},
    "economic": {"level": "B1", "pos": "adjective"},
    "economical": {"level": "B2", "pos": "adjective"},
    "hay": {"level": "B2", "pos": "noun"},
    "con": {"level": "C1", "pos": "verb"},
}


def test_resolve_lemma_exact():
    lemma, info = resolve_lemma("prosperity", SAMPLE_LEXICON)
    assert lemma == "prosperity"
    assert info["level"] == "B1"
    assert info["pos"] == "noun"


def test_resolve_lemma_plural():
    lemma, info = resolve_lemma("shoes", SAMPLE_LEXICON)
    assert lemma == "shoe"
    assert info["level"] == "A1"


def test_resolve_lemma_irregular_verb():
    lemma, info = resolve_lemma("wrote", SAMPLE_LEXICON)
    assert lemma == "write"
    assert info["level"] == "A1"


def test_resolve_lemma_unknown():
    lemma, info = resolve_lemma("xyznotaword", SAMPLE_LEXICON)
    assert info is None


def test_extract_meanings_from_speech_single_segment():
    transcript = [
        {"start": 10.0, "end": 12.0, "text": "Chúng ta có từ prosperity là sự thịnh vượng."},
        {"start": 20.0, "end": 22.0, "text": "Động từ determine là quyết tâm hoặc quyết định."},
    ]
    meanings = extract_meanings_from_speech(transcript, SAMPLE_LEXICON)
    assert "prosperity" in meanings
    assert "thịnh vượng" in meanings["prosperity"][0]
    assert "determine" in meanings
    assert "quyết tâm" in meanings["determine"][0]


def test_extract_meanings_from_speech_consecutive_segments():
    transcript = [
        {"start": 30.0, "end": 30.8, "text": "Actor."},
        {"start": 31.0, "end": 32.2, "text": "Diễn viên nam."},
    ]
    meanings = extract_meanings_from_speech(transcript, SAMPLE_LEXICON)
    assert "actor" in meanings
    assert "diễn viên nam" in meanings["actor"][0].lower()


def test_vi_homophones_filtered():
    # 'hay' and 'con' exist in English dictionaries (B2/C1) but are common Vietnamese words
    assert "hay" in VI_HOMOPHONES
    assert "con" in VI_HOMOPHONES

    screens = [{"id": 1, "text": "Watch this movie."}]
    # Teacher speaks: "Hay là chúng ta chọn con này"
    transcript = [
        {"start": 5.0, "end": 7.0, "text": "Hay là chúng ta chọn con số 1."}
    ]
    vocab = extract_vocabulary(screens, transcript, SAMPLE_LEXICON, max_vocab=10, min_score=1.0)
    words = {v["word"] for v in vocab}
    assert "movie" in words
    assert "hay" not in words
    assert "con" not in words


def test_extract_vocabulary_cefr_levels():
    screens = [
        {"id": 1, "text": "Welcome to the movie. Look at the economic performance."}
    ]
    transcript = [
        {"start": 1.0, "end": 3.0, "text": "Movie."},
        {"start": 4.0, "end": 6.0, "text": "Economic là thuộc về kinh tế."},
    ]
    vocab = extract_vocabulary(screens, transcript, SAMPLE_LEXICON, max_vocab=10, min_score=1.0)
    v_dict = {v["word"]: v for v in vocab}
    assert "movie" in v_dict
    assert v_dict["movie"]["level"] == "A1"
    assert "economic" in v_dict
    assert v_dict["economic"]["level"] == "B1"
    assert "thuộc về kinh tế" in v_dict["economic"]["meaning_vi"]

