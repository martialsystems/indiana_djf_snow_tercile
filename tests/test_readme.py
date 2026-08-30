# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from djsnow.claims import scan_text
from djsnow.config import INDEX_GIST, QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert "1991-2020" in text
    assert "14.48" in text
    assert "13.00" in text
    assert "does not beat the normal" in text
    assert "ac36f0f" in text
    assert "1416da1" in text
    assert INDEX_GIST.split("/")[-1] in text
    assert ".github/blob/main/RESEARCH.md" not in text
    assert "scatter.png" in text
    assert "error_map.png" in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
    assert "p_sfha" in text.lower() or "HAND" in text or "Nora" in text
    # parked hydro lives as an ops sentence, not a product identity section
