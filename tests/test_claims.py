# Copyright (c) 2026 Martial Systems LLC

from djsnow.claims import scan_text
from djsnow.config import LIVE_MAP_SUBTITLE, LIVE_SCATTER_SUBTITLE, QUESTION


def test_question_and_bans() -> None:
    assert scan_text(QUESTION) == []
    assert scan_text(LIVE_SCATTER_SUBTITLE) == []
    assert scan_text(LIVE_MAP_SUBTITLE) == []
    assert "October" in QUESTION
    assert "1991-2020" in QUESTION
    assert "blizzard" in scan_text("expected blizzard tonight")
    assert "hero_in" in scan_text("Indiana will get 25 inches this winter")
    assert "hand_wet" in scan_text("HAND wet mask")
