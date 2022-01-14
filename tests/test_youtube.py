import pytest
from ..youtube import *

def test_getYoutubeVideoId():
    assert getYoutubeVideoId("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert getYoutubeVideoId("https://www.youtube.com/watch?v=fApiH880T5o") == "fApiH880T5o"

def test_getYoutubeTitle():
    assert getYoutubeTitle("dQw4w9WgXcQ") == "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    assert getYoutubeTitle("fApiH880T5o") == "아이유 (IU) - 정거장 (Next Stop) | 가사"
    assert getYoutubeTitle("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    assert getYoutubeTitle("https://www.youtube.com/watch?v=fApiH880T5o") == "아이유 (IU) - 정거장 (Next Stop) | 가사"