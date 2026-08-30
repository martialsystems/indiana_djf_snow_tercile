# Copyright (c) 2026 Martial Systems LLC
"""Normal, last-year, Ridge inches. Not a deeper net if Ridge loses."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from djsnow.config import FEATURE_NAMES
from djsnow.features import matrix_x
from djsnow.labels import assign_tercile, tercile_cuts
from djsnow.pack import WinterPack
from djsnow.split import assert_split, row_masks


def _rmse(y: np.ndarray, p: np.ndarray) -> float:
    d = np.asarray(y, dtype=float) - np.asarray(p, dtype=float)
    d = d[np.isfinite(d)]
    return float(np.sqrt(np.mean(d * d))) if d.size else float("nan")


def _mae(y: np.ndarray, p: np.ndarray) -> float:
    d = np.abs(np.asarray(y, dtype=float) - np.asarray(p, dtype=float))
    d = d[np.isfinite(d)]
    return float(np.mean(d)) if d.size else float("nan")


def _hit(y: np.ndarray, p: np.ndarray) -> float:
    m = np.isfinite(y.astype(float)) & np.isfinite(p.astype(float))
    if not m.any():
        return float("nan")
    return float(np.mean(y[m] == p[m]))


def fit_pack(pack: WinterPack) -> dict[str, Any]:
    train, hold, confirm = row_masks(pack)
    assert_split(pack, train, hold, confirm)
    x = matrix_x(pack)
    y = np.asarray(pack.snow_in, dtype=float)
    ok = np.isfinite(x).all(axis=1) & np.isfinite(y)
    train = train & ok
    hold = hold & ok
    confirm = confirm & ok
    x_tr, y_tr = x[train], y[train]
    x_ho, y_ho = x[hold], y[hold]
    ridge = Pipeline(
        [("scale", StandardScaler()), ("reg", Ridge(alpha=1.0))]
    )
    ridge.fit(x_tr, y_tr)
    p_ridge = ridge.predict(x_ho)
    p_norm = np.asarray(pack.snow_normal_in, dtype=float)[hold]
    p_last = np.asarray(pack.prior_djf_in, dtype=float)[hold]
    skill = {
        "normal": {"rmse_in": _rmse(y_ho, p_norm), "mae_in": _mae(y_ho, p_norm)},
        "last_year": {"rmse_in": _rmse(y_ho, p_last), "mae_in": _mae(y_ho, p_last)},
        "ridge": {"rmse_in": _rmse(y_ho, p_ridge), "mae_in": _mae(y_ho, p_ridge)},
    }
    ridge_beats = skill["ridge"]["rmse_in"] < skill["normal"]["rmse_in"]
    cuts: dict[str, tuple[float, float]] = {}
    for sid in np.unique(pack.station_id[train].astype(str)):
        m = train & (pack.station_id.astype(str) == sid)
        cuts[sid] = tercile_cuts(y[m])
    def _terc(snow: np.ndarray, sids: np.ndarray) -> np.ndarray:
        out = np.zeros(snow.shape, dtype=np.int32)
        for i, sid in enumerate(sids.astype(str)):
            lo, hi = cuts[str(sid)]
            out[i] = assign_tercile(np.array([snow[i]]), lo, hi)[0]
        return out

    y_t = _terc(y_ho, pack.station_id[hold])
    near = np.full(y_ho.shape, 1, dtype=np.int32)
    t_norm = _terc(p_norm, pack.station_id[hold])
    t_ridge = _terc(p_ridge, pack.station_id[hold])
    t_last = _terc(p_last, pack.station_id[hold])
    tercile = {
        "always_near": _hit(y_t, near),
        "normal": _hit(y_t, t_norm),
        "last_year": _hit(y_t, t_last),
        "ridge": _hit(y_t, t_ridge),
    }
    st = pack.station_id[hold].astype(str)
    lat_ho = pack.lat[hold]
    lon_ho = pack.lon[hold]
    station_err = []
    for sid in np.unique(st):
        m = st == sid
        station_err.append(
            {
                "station_id": str(sid),
                "lat": float(lat_ho[m][0]),
                "lon": float(lon_ho[m][0]),
                "n": int(m.sum()),
                "bias_in": float(np.mean(p_ridge[m] - y_ho[m])),
                "rmse_in": _rmse(y_ho[m], p_ridge[m]),
                "normal_rmse_in": _rmse(y_ho[m], p_norm[m]),
            }
        )
    confirm_rmse = None
    if confirm.any():
        p_c = ridge.predict(x[confirm])
        confirm_rmse = {
            "n": int(confirm.sum()),
            "ridge_rmse_in": _rmse(y[confirm], p_c),
            "normal_rmse_in": _rmse(y[confirm], pack.snow_normal_in[confirm]),
        }
    return {
        "n_train": int(train.sum()),
        "n_holdout": int(hold.sum()),
        "n_confirm": int(confirm.sum()),
        "n_train_stations": int(np.unique(pack.station_id[train]).shape[0]),
        "n_holdout_stations": int(np.unique(st).shape[0]),
        "feature_names": list(FEATURE_NAMES),
        "skill": skill,
        "tercile": tercile,
        "ridge_beats_normal": bool(ridge_beats),
        "page_in_scope": bool(ridge_beats),
        "station_err": station_err,
        "holdout_obs": y_ho.tolist(),
        "holdout_ridge": p_ridge.tolist(),
        "holdout_normal": p_norm.tolist(),
        "confirm": confirm_rmse,
        "djf_in_features": False,
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "random_split": False,
        "confirm_in_train": False,
        "gauge_as_feature": False,
    }
