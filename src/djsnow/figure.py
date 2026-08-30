# Copyright (c) 2026 Martial Systems LLC
"""Two figures: holdout scatter, station mean error map."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from djsnow.claims import require_clean
from djsnow.config import (
    FIXTURE_MAP_SUBTITLE,
    FIXTURE_SCATTER_SUBTITLE,
    LIVE_MAP_SUBTITLE,
    LIVE_SCATTER_SUBTITLE,
    MAX_FIGURES,
    QUESTION,
)
from djsnow.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_scatter(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    obs = np.asarray(fit["holdout_obs"], dtype=float)
    ridge = np.asarray(fit["holdout_ridge"], dtype=float)
    norm = np.asarray(fit["holdout_normal"], dtype=float)
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    ax.scatter(obs, ridge, s=28, c="#b45309", label="Ridge", zorder=3)
    ax.scatter(obs, norm, s=22, c="#64748b", marker="x", label="1991-2020 normal", zorder=2)
    lo = float(np.nanmin([obs.min(), ridge.min(), norm.min()]))
    hi = float(np.nanmax([obs.max(), ridge.max(), norm.max()]))
    pad = 0.05 * (hi - lo + 1.0)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#0f172a", lw=1.0, label="1:1")
    ax.set_xlabel("observed DJF snow (in)")
    ax.set_ylabel("predicted DJF snow (in)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.subplots_adjust(bottom=0.16, top=0.92)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_map(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = fit["station_err"]
    lon = np.array([r["lon"] for r in rows], dtype=float)
    lat = np.array([r["lat"] for r in rows], dtype=float)
    bias = np.array([r["bias_in"] for r in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(6.6, 6.8))
    mag = max(1.0, float(np.nanmax(np.abs(bias))))
    sc = ax.scatter(
        lon,
        lat,
        c=bias,
        cmap="RdBu_r",
        vmin=-mag,
        vmax=mag,
        s=48,
        edgecolors="#0f172a",
        linewidths=0.4,
    )
    cb = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("mean Ridge minus obs (in)", fontsize=8)
    ax.set_xlabel("lon")
    ax.set_ylabel("lat")
    ax.set_title(title, fontsize=10)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.subplots_adjust(bottom=0.16, top=0.92)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any], live: bool = False) -> list[Path]:
    require_clean(QUESTION, source="question")
    scatter_sub = LIVE_SCATTER_SUBTITLE if live else FIXTURE_SCATTER_SUBTITLE
    map_sub = LIVE_MAP_SUBTITLE if live else FIXTURE_MAP_SUBTITLE
    paths = [
        write_scatter(
            log_dir / "scatter.png",
            fit=fit,
            title="Holdout DJF snowfall",
            subtitle=scatter_sub,
        ),
        write_map(
            log_dir / "error_map.png",
            fit=fit,
            title="Holdout mean error",
            subtitle=map_sub,
        ),
    ]
    _cap(len(paths))
    return paths
