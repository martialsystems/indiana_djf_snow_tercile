# Copyright (c) 2026 Martial Systems LLC
"""Fail closed: station DJF snow vs normal, not a warning, not a flood map."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from djsnow.errors import ClaimBanError

_BANS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("casualty", re.compile(r"\b(deaths?|fatalit(?:y|ies)|casualt(?:y|ies)|killed)\b", re.I)),
    ("p100", re.compile(r"\b100-year\s+exceedance\b", re.I)),
    ("flood_warning", re.compile(r"\bflood warning\b|\bemergency forecast\b", re.I)),
    ("blizzard", re.compile(r"\bexpected blizzard\b", re.I)),
    ("tornado", re.compile(r"\btornado\b", re.I)),
    ("hand_wet", re.compile(r"\bHAND wet mask\b", re.I)),
    ("flood_map", re.compile(r"\bflood map\b", re.I)),
    ("hero_in", re.compile(r"\bIndiana will get\s+\d+", re.I)),
    ("cmip", re.compile(r"\b(cmip\d*|downscal(?:e|ed|ing)|gcm)\b", re.I)),
)


def scan_text(text: str) -> list[str]:
    return [name for name, pat in _BANS if pat.search(text or "")]


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")
    if "\u2014" in (text or ""):
        raise ClaimBanError(f"{source}: em dash")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
