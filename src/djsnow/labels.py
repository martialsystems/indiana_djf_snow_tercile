# Copyright (c) 2026 Martial Systems LLC
"""Train-only tercile cuts. Completeness on DJF days."""

from __future__ import annotations

import calendar
from datetime import date

import numpy as np

from djsnow.config import COMPLETE_FRAC


def djf_ndays(winter_id: int) -> int:
    feb = 29 if calendar.isleap(int(winter_id)) else 28
    return 31 + feb + 31


def complete_enough(n_present: int, winter_id: int, *, floor: float = COMPLETE_FRAC) -> bool:
    return (n_present / float(djf_ndays(winter_id))) >= floor


def tercile_cuts(train_snow: np.ndarray) -> tuple[float, float]:
    y = np.asarray(train_snow, dtype=float)
    y = y[np.isfinite(y)]
    if y.size < 6:
        raise ValueError("not enough train winters for terciles")
    lo, hi = np.percentile(y, [100.0 / 3.0, 200.0 / 3.0])
    return float(lo), float(hi)


def assign_tercile(snow_in: np.ndarray, lo: float, hi: float) -> np.ndarray:
    y = np.asarray(snow_in, dtype=float)
    out = np.full(y.shape, 1, dtype=np.int32)
    out[y < lo] = 0
    out[y > hi] = 2
    return out


def winter_id_of(day: date) -> int:
    return day.year + 1 if day.month == 12 else day.year
