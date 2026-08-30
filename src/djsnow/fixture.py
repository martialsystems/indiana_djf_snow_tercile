# Copyright (c) 2026 Martial Systems LLC
"""Synthetic winters. Planted ENSO-snow so CI recovers a link. Does not rescue live."""

from __future__ import annotations

import numpy as np

from djsnow.config import CONFIRM_WINTER, FEATURE_NAMES, HOLDOUT_LAST_WINTER
from djsnow.pack import WinterPack


def build_fixture(*, seed: int = 3) -> WinterPack:
    rng = np.random.default_rng(seed)
    stations = [
        ("USW00014848", 41.71, -86.32, 236.0, 36.0),
        ("USW00014827", 41.12, -85.19, 248.0, 33.0),
        ("USW00093819", 39.72, -86.29, 241.0, 22.0),
        ("USW00093817", 38.04, -87.53, 118.0, 12.0),
        ("USW00014827B", 41.00, -85.00, 250.0, 30.0),
        ("USW00014848B", 41.50, -86.50, 220.0, 34.0),
    ]
    winters = np.arange(1992, CONFIRM_WINTER + 1)
    nino = rng.normal(0.0, 0.9, size=winters.size)
    nino_map = {int(w): float(nino[i]) for i, w in enumerate(winters)}
    rows: dict[str, list] = {k: [] for k in (
        "winter_id", "station_id", "lat", "lon", "elev_m", "snow_in", "snow_normal_in",
        "prior_djf_in", "nino34_oct", "oct_tavg_c", "oct_prcp_in", "complete_frac",
    )}
    last: dict[str, float] = {}
    for sid, lat, lon, elev, normal in stations:
        for w in winters:
            n34 = nino_map[int(w)]
            snow = normal + 6.0 * n34 + rng.normal(0.0, 2.5)
            snow = float(max(0.0, snow))
            prior = last.get(sid, normal)
            oct_t = 10.0 - 1.5 * n34 + rng.normal(0.0, 1.0)
            oct_p = 3.0 + rng.normal(0.0, 0.6)
            rows["winter_id"].append(int(w))
            rows["station_id"].append(sid)
            rows["lat"].append(lat)
            rows["lon"].append(lon)
            rows["elev_m"].append(elev)
            rows["snow_in"].append(snow)
            rows["snow_normal_in"].append(normal)
            rows["prior_djf_in"].append(prior)
            rows["nino34_oct"].append(n34)
            rows["oct_tavg_c"].append(oct_t)
            rows["oct_prcp_in"].append(max(0.0, oct_p))
            rows["complete_frac"].append(0.95)
            last[sid] = snow
    pack = WinterPack(
        winter_id=np.array(rows["winter_id"], dtype=int),
        station_id=np.array(rows["station_id"], dtype=object),
        lat=np.array(rows["lat"], dtype=float),
        lon=np.array(rows["lon"], dtype=float),
        elev_m=np.array(rows["elev_m"], dtype=float),
        snow_in=np.array(rows["snow_in"], dtype=float),
        snow_normal_in=np.array(rows["snow_normal_in"], dtype=float),
        prior_djf_in=np.array(rows["prior_djf_in"], dtype=float),
        nino34_oct=np.array(rows["nino34_oct"], dtype=float),
        oct_tavg_c=np.array(rows["oct_tavg_c"], dtype=float),
        oct_prcp_in=np.array(rows["oct_prcp_in"], dtype=float),
        complete_frac=np.array(rows["complete_frac"], dtype=float),
        source="fixture",
        extra={"planted_enso": True, "feature_names": list(FEATURE_NAMES), "n_holdout_last": HOLDOUT_LAST_WINTER},
    )
    return pack
