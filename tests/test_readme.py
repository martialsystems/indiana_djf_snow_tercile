# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from djsnow.claims import scan_text
from djsnow.config import QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert "1991-2020" in text
    assert "14.48" in text
    assert "13.00" in text
    assert "does not beat the normal" in text
    assert "does not reopen" in text
    assert "4.25" in text
    assert "Holdout is the product" in text
    assert "ac36f0f" in text
    assert "1416da1" in text
    assert "Research index: https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3" in text
    assert "Open_the_research_console" not in text
    assert "66b896b0a4a0b8cba2b478aef64312f3" in text
    assert "Precip writeup" in text or "b5f900aad37487bb8c0206a321c1ed5c" in text
    assert "b5f900aad37487bb8c0206a321c1ed5c" in text
    assert ".github/blob/main/RESEARCH.md" not in text
    assert "scatter.png" in text
    assert "error_map.png" in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
    assert "p_sfha" in text.lower() or "HAND" in text or "Nora" in text
    # parked hydro lives as an ops sentence, not a product identity section
