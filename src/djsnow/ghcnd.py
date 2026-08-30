# Copyright (c) 2026 Martial Systems LLC
"""GHCND daily SNOW, TAVG, PRCP. Values: SNOW mm, PRCP tenths of mm, TAVG tenths C."""

from __future__ import annotations

import csv
import gzip
import io
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable

import numpy as np

from djsnow.config import (
    COMPLETE_FRAC,
    CORE_STATIONS,
    GHCND_STATION_URL,
    GHCND_STATIONS_URL,
    IN_LAT,
    IN_LON,
    MIN_TRAIN_WINTERS,
    MM_PER_INCH,
    TRAIN_LAST_WINTER,
)
from djsnow.errors import FetchError
from djsnow.http import get_bytes
from djsnow.labels import complete_enough, winter_id_of


def parse_stations_txt(text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for line in text.splitlines():
        if len(line) < 41:
            continue
        st = line[38:40].strip()
        if st != "IN":
            continue
        sid = line[0:11].strip()
        try:
            lat = float(line[12:20])
            lon = float(line[21:30])
            elev = float(line[31:37])
        except ValueError:
            continue
        if not (IN_LAT[0] <= lat <= IN_LAT[1] and IN_LON[0] <= lon <= IN_LON[1]):
            continue
        name = line[41:71].strip() if len(line) >= 71 else sid
        out.append({"station_id": sid, "lat": lat, "lon": lon, "elev_m": elev, "name": name})
    if not out:
        raise FetchError("no Indiana GHCND stations")
    return out


def _parse_daily(text: str) -> list[tuple[date, str, float]]:
    rows: list[tuple[date, str, float]] = []
    for rec in csv.reader(io.StringIO(text)):
        if len(rec) < 4:
            continue
        elem = rec[2].strip()
        if elem not in {"SNOW", "PRCP", "TAVG", "TMAX", "TMIN"}:
            continue
        qflag = rec[5].strip() if len(rec) > 5 else ""
        if qflag:
            continue
        try:
            raw = int(rec[3])
        except ValueError:
            continue
        if raw == -9999:
            continue
        day = date.fromisoformat(f"{rec[1][0:4]}-{rec[1][4:6]}-{rec[1][6:8]}")
        rows.append((day, elem, float(raw)))
    return rows


def _to_in_c(elem: str, raw: float) -> float:
    if elem == "SNOW":
        return raw / MM_PER_INCH
    if elem == "PRCP":
        return (raw / 10.0) / MM_PER_INCH
    if elem in {"TAVG", "TMAX", "TMIN"}:
        return raw / 10.0
    return raw


def load_station_csv(sid: str, cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> list[tuple[date, str, float]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{sid}.csv.gz"
    if not path.is_file() or path.stat().st_size == 0:
        body = getter(GHCND_STATION_URL.format(sid=sid))
        if not body:
            raise FetchError(f"empty GHCND {sid}")
        path.write_bytes(body)
    raw = gzip.decompress(path.read_bytes()).decode("utf-8", errors="replace")
    return _parse_daily(raw)


def assemble_winters(
    *,
    stations: list[dict[str, Any]],
    daily: dict[str, list[tuple[date, str, float]]],
    normals: dict[str, float],
    nino_oct: dict[int, float],
) -> dict[str, np.ndarray]:
    buckets: dict[tuple[str, int], dict[str, Any]] = {}
    for st in stations:
        sid = st["station_id"]
        for day, elem, raw in daily.get(sid, []):
            if elem == "SNOW" and day.month in {12, 1, 2}:
                wid = winter_id_of(day)
                key = (sid, wid)
                b = buckets.setdefault(
                    key,
                    {
                        "snow": 0.0,
                        "n_snow": 0,
                        "oct_t": [],
                        "oct_p": [],
                        **st,
                    },
                )
                b["snow"] += _to_in_c("SNOW", raw)
                b["n_snow"] += 1
            elif elem in {"TAVG", "TMAX", "TMIN"} and day.month == 10:
                wid = day.year + 1
                key = (sid, wid)
                b = buckets.setdefault(
                    key,
                    {"snow": 0.0, "n_snow": 0, "oct_t": [], "oct_p": [], **st},
                )
                if elem == "TAVG":
                    b["oct_t"].append(_to_in_c("TAVG", raw))
                elif elem == "TMAX":
                    b.setdefault("oct_tx", []).append(_to_in_c("TMAX", raw))
                else:
                    b.setdefault("oct_tn", []).append(_to_in_c("TMIN", raw))
            elif elem == "PRCP" and day.month == 10:
                wid = day.year + 1
                key = (sid, wid)
                b = buckets.setdefault(
                    key,
                    {"snow": 0.0, "n_snow": 0, "oct_t": [], "oct_p": [], **st},
                )
                b["oct_p"].append(_to_in_c("PRCP", raw))

    keep_ids = {s for s, _ in CORE_STATIONS}
    counts: dict[str, int] = defaultdict(int)
    for (sid, wid), b in buckets.items():
        if complete_enough(int(b["n_snow"]), int(wid), floor=COMPLETE_FRAC) and int(wid) <= TRAIN_LAST_WINTER:
            counts[sid] += 1
    for sid, n in counts.items():
        if n >= MIN_TRAIN_WINTERS:
            keep_ids.add(sid)

    rows: dict[str, list] = defaultdict(list)
    last_snow: dict[str, float] = {}
    for (sid, wid) in sorted(buckets):
        if sid not in keep_ids:
            continue
        b = buckets[(sid, wid)]
        if not complete_enough(int(b["n_snow"]), int(wid), floor=COMPLETE_FRAC):
            continue
        if sid not in normals:
            continue
        if int(wid) not in nino_oct:
            continue
        tavg = b["oct_t"]
        if not tavg:
            tx = b.get("oct_tx") or []
            tn = b.get("oct_tn") or []
            if tx and tn:
                tavg = [0.5 * (float(np.mean(tx)) + float(np.mean(tn)))]
        if not tavg or not b["oct_p"]:
            continue
        prior = last_snow.get(sid, float(normals[sid]))
        snow = float(b["snow"])
        rows["winter_id"].append(int(wid))
        rows["station_id"].append(sid)
        rows["lat"].append(float(b["lat"]))
        rows["lon"].append(float(b["lon"]))
        rows["elev_m"].append(float(b["elev_m"]))
        rows["snow_in"].append(snow)
        rows["snow_normal_in"].append(float(normals[sid]))
        rows["prior_djf_in"].append(prior)
        rows["nino34_oct"].append(float(nino_oct[int(wid)]))
        rows["oct_tavg_c"].append(float(np.mean(tavg)))
        rows["oct_prcp_in"].append(float(np.sum(b["oct_p"])))
        rows["complete_frac"].append(float(b["n_snow"]) / float(31 + 28 + 31))
        last_snow[sid] = snow
    if not rows["winter_id"]:
        raise FetchError("no complete station-winters after GHCND QC")
    return {k: np.array(v) for k, v in rows.items()}


def load_indiana_stations(cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> list[dict[str, Any]]:
    path = cache_dir / "ghcnd-stations.txt"
    if not path.is_file():
        path.write_bytes(getter(GHCND_STATIONS_URL))
    text = path.read_text(encoding="utf-8", errors="replace")
    return parse_stations_txt(text)
