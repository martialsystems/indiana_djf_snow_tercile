# Copyright (c) 2026 Martial Systems LLC
"""Station-winter snowfall rows. Inches."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class WinterPack:
    winter_id: np.ndarray
    station_id: np.ndarray
    lat: np.ndarray
    lon: np.ndarray
    elev_m: np.ndarray
    snow_in: np.ndarray
    snow_normal_in: np.ndarray
    prior_djf_in: np.ndarray
    nino34_oct: np.ndarray
    oct_tavg_c: np.ndarray
    oct_prcp_in: np.ndarray
    complete_frac: np.ndarray
    source: str = "fixture"
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def n_rows(self) -> int:
        return int(self.winter_id.shape[0])

    @property
    def n_stations(self) -> int:
        return int(np.unique(self.station_id).shape[0])
