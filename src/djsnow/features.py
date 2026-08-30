# Copyright (c) 2026 Martial Systems LLC
"""October / ENSO vector. DJF weather is leakage."""

from __future__ import annotations

import numpy as np

from djsnow.config import BANNED_FEATURE_TOKENS, FEATURE_NAMES
from djsnow.errors import LeakError
from djsnow.pack import WinterPack


def matrix_x(pack: WinterPack) -> np.ndarray:
    names = " ".join(FEATURE_NAMES).lower()
    for tok in BANNED_FEATURE_TOKENS:
        if tok in names:
            raise LeakError(f"banned token {tok} in FEATURE_NAMES")
    x = np.column_stack(
        [
            np.asarray(pack.nino34_oct, dtype=float),
            np.asarray(pack.snow_normal_in, dtype=float),
            np.asarray(pack.prior_djf_in, dtype=float),
            np.asarray(pack.oct_tavg_c, dtype=float),
            np.asarray(pack.oct_prcp_in, dtype=float),
            np.asarray(pack.lat, dtype=float),
            np.asarray(pack.elev_m, dtype=float),
        ]
    )
    return x
