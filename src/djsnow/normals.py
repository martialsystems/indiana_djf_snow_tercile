# Copyright (c) 2026 Martial Systems LLC
"""1991-2020 monthly snowfall normals. DJF is Dec+Jan+Feb."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Callable

from djsnow.config import NORMALS_URL
from djsnow.errors import FetchError
from djsnow.http import get_bytes


def parse_djf_snow_normal(text: str) -> float:
    months: dict[int, float] = {}
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "MLY-SNOW-NORMAL" not in reader.fieldnames:
        raise FetchError("normals file missing MLY-SNOW-NORMAL")
    for rec in reader:
        try:
            month = int(float(rec.get("month") or rec.get("DATE") or "0"))
        except ValueError:
            continue
        raw = (rec.get("MLY-SNOW-NORMAL") or "").strip()
        if not raw or raw in {"-9999", ""}:
            continue
        try:
            months[month] = float(raw)
        except ValueError:
            continue
    if not {1, 2, 12}.issubset(months):
        raise FetchError("DJF snowfall normal incomplete")
    return float(months[12] + months[1] + months[2])


def load_normal(sid: str, cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> float:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{sid}_normals.csv"
    if not path.is_file() or path.stat().st_size == 0:
        body = getter(NORMALS_URL.format(sid=sid))
        if not body:
            raise FetchError(f"empty normals {sid}")
        path.write_bytes(body)
    return parse_djf_snow_normal(path.read_text(encoding="utf-8", errors="replace"))
