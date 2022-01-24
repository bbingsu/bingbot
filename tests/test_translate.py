import pytest
from ..module.translation import *

def test_translate():
    assert translate_google("안녕하세요", "ko", "en") == "Hello"
    assert translate_google("Hello", "en", "ko") == "안녕하세요"
    assert translate_google("반성해라 멍청이", "ko", "en") == "repent, you idiot"