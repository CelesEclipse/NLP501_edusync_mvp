import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcribe import text_lang


def test_text_lang_pure_vietnamese():
    assert text_lang("Chào các bạn, hôm nay chúng ta sẽ chữa đề thi thử.") == "vi"
    assert text_lang("Đáp án chính xác cho câu này là phương án B.") == "vi"


def test_text_lang_pure_english():
    assert text_lang("BERT is a pre-trained language model from Google.") == "en"
    assert text_lang("Choose the correct option between A and B.") == "en"


def test_text_lang_mixed():
    # When a sentence has some Vietnamese diacritics but low ratio (e.g. short code-switching)
    # text_lang returns "vi" if vi > 0.3 else "en" if vi == 0 else "mixed"
    # "Chúng ta học present perfect tense."
    res = text_lang("Học sinh chọn past continuous.")
    assert res in ["vi", "mixed"]

