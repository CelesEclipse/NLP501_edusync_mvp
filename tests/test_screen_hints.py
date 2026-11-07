import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcribe import screen_hints


def test_screen_hints_chunks_returns_empty():
    ocr = "Exercise 1: Choose the correct answer.\n(A) has gone (B) have went"
    assert screen_hints(ocr, "chunks") == ""


def test_screen_hints_words_filters_stopwords_and_duplicates():
    ocr = "The quick brown fox jumps over the lazy dog.\n(A) is (B) are"
    hints = screen_hints(ocr, "words")
    words = hints.split()
    # Check that stopwords like 'the', 'is', 'are' are not in words
    for sw in ["the", "is", "are"]:
        assert sw not in [w.lower() for w in words]
    # Check content words are preserved
    assert "quick" in words
    assert "brown" in words
    assert "jumps" in words
    # Check no duplicate words
    assert len(words) == len(set(w.lower() for w in words))


def test_screen_hints_words_filters_vietnamese_lines():
    ocr = "Học sinh chọn đáp án đúng nhất.\n(A) application (B) applicant"
    hints = screen_hints(ocr, "words")
    # 'học', 'sinh', 'chọn', 'đáp', 'án', 'đúng', 'nhất' should be filtered out
    assert "application" in hints
    assert "applicant" in hints
    for vi_word in ["học", "sinh", "chọn", "đáp", "án"]:
        assert vi_word not in hints.lower()


def test_screen_hints_lines_cleans_options():
    ocr = "Question 101. Please submit your application.\n(A) before (B) after"
    hints = screen_hints(ocr, "lines")
    # (A) and (B) options cleaned
    assert "(A)" not in hints
    assert "(B)" not in hints
    assert "Question" in hints
    assert "application" in hints

