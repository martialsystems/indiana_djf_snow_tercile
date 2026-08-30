# Copyright (c) 2026 Martial Systems LLC
"""Live GHCND + normals + ENSO. Empty SNOW or normals stops."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from djsnow.config import CORE_STATIONS
from djsnow.enso import load_nino34
from djsnow.errors import FetchError
from djsnow.ghcnd import assemble_winters, load_indiana_stations, load_station_csv
from djsnow.http import get_bytes
from djsnow.normals import load_normal
from djsnow.pack import WinterPack


def fetch_live(*, cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> tuple[WinterPack, dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    stations = load_indiana_stations(cache_dir, getter=getter)
    core = {s for s, _ in CORE_STATIONS}
    cands = [s for s in stations if s["station_id"] in core or s["station_id"].startswith("USW000")]
    if len(cands) < 4:
        raise FetchError("fewer than 4 Indiana first-order GHCND stations")
    nino = load_nino34(cache_dir, getter=getter)
    normals: dict[str, float] = {}
    daily: dict[str, list] = {}
    used: list[dict[str, Any]] = []
    for st in cands:
        sid = st["station_id"]
        try:
            normals[sid] = load_normal(sid, cache_dir, getter=getter)
            daily[sid] = load_station_csv(sid, cache_dir, getter=getter)
        except FetchError:
            if sid in core:
                raise
            continue
        if not any(el == "SNOW" for _, el, _ in daily[sid]):
            if sid in core:
                raise FetchError(f"core station {sid} has no SNOW")
            continue
        used.append(st)
    if not used:
        raise FetchError("no GHCND SNOW after QC")
    arrays = assemble_winters(stations=used, daily=daily, normals=normals, nino_oct=nino)
    pack = WinterPack(
        winter_id=arrays["winter_id"].astype(int),
        station_id=arrays["station_id"],
        lat=arrays["lat"].astype(float),
        lon=arrays["lon"].astype(float),
        elev_m=arrays["elev_m"].astype(float),
        snow_in=arrays["snow_in"].astype(float),
        snow_normal_in=arrays["snow_normal_in"].astype(float),
        prior_djf_in=arrays["prior_djf_in"].astype(float),
        nino34_oct=arrays["nino34_oct"].astype(float),
        oct_tavg_c=arrays["oct_tavg_c"].astype(float),
        oct_prcp_in=arrays["oct_prcp_in"].astype(float),
        complete_frac=arrays["complete_frac"].astype(float),
        source="live",
        extra={"n_station_files": len(used), "nino_source": "CPC sstoi.indices"},
    )
    meta = {
        "n_stations": pack.n_stations,
        "n_rows": pack.n_rows,
        "product": "GHCND SNOW",
        "cache_dir": str(cache_dir),
        "nino_dated": "October Niño 3.4 for winter Y (CPC ERSSTv5)",
    }
    return pack, meta
