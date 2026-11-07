import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval.wer import align, words


def test_wer_exact_match():
    ref = words("hôm nay chúng ta học thì hiện tại hoàn thành")
    hyp = words("hôm nay chúng ta học thì hiện tại hoàn thành")
    err, ok = align(ref, hyp)
    assert err == 0
    assert len(ok) == len(ref)


def test_wer_substitution():
    ref = words("chọn đáp án B")
    hyp = words("chọn đáp án C")
    err, ok = align(ref, hyp)
    assert err == 1
    # 2 matched words ('chọn', 'đáp', 'án' is 3 tokens)
    assert len(ok) == 3


def test_wer_deletion():
    ref = words("bài tập về nhà số một")
    hyp = words("bài tập số một")
    err, ok = align(ref, hyp)
    assert err == 2  # 'về', 'nhà' deleted


def test_wer_insertion():
    ref = words("câu số hai")
    hyp = words("và đây là câu số hai")
    err, ok = align(ref, hyp)
    assert err == 3  # 'và', 'đây', 'là' inserted


def test_words_normalizes_case_and_punctuation():
    w = words("Hello, World! This is TOEIC...")
    assert w == ["hello", "world", "this", "is", "toeic"]

