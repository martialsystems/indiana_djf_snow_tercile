# Copyright (c) 2026 Martial Systems LLC
"""Two figures: holdout scatter, station mean error bars."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from djsnow.claims import require_clean
from djsnow.config import (
    CORE_STATIONS,
    FIXTURE_MAP_SUBTITLE,
    FIXTURE_SCATTER_SUBTITLE,
    LIVE_MAP_SUBTITLE,
    LIVE_SCATTER_SUBTITLE,
    MAX_FIGURES,
    QUESTION,
)
from djsnow.errors import FigureCapError

_STATION_COLORS = {
    "USW00014848": "#1d4ed8",
    "USW00014827": "#b45309",
    "USW00093819": "#047857",
    "USW00093817": "#7c3aed",
}


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def live_scatter_subtitle(fit: dict[str, Any]) -> str:
    skill = fit.get("skill") or {}
    ridge = skill.get("ridge") or {}
    normal = skill.get("normal") or {}
    if "rmse_in" in ridge and "rmse_in" in normal:
        return (
            f"Holdout DJF inches. Ridge RMSE {float(ridge['rmse_in']):.2f} vs "
            f"normal {float(normal['rmse_in']):.2f}. "
            "October plus ENSO is a no. Seasonal, not a storm."
        )
    return LIVE_SCATTER_SUBTITLE


def live_map_subtitle(fit: dict[str, Any]) -> str:
    rows = {r["station_id"]: r for r in fit.get("station_err") or []}
    sb = rows.get("USW00014848")
    if sb is None:
        return LIVE_MAP_SUBTITLE
    return (
        "Holdout mean Ridge minus observed DJF inches by city. "
        f"South Bend {float(sb['bias_in']):+.0f} in. "
        "Seasonal error, not a storm, not water."
    )


def write_scatter(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    obs = np.asarray(fit["holdout_obs"], dtype=float)
    ridge = np.asarray(fit["holdout_ridge"], dtype=float)
    norm = np.asarray(fit["holdout_normal"], dtype=float)
    sids = [str(s) for s in (fit.get("holdout_station_id") or [])]
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    if sids and len(sids) == len(obs):
        sid_arr = np.asarray(sids)
        for sid, city in CORE_STATIONS:
            m = sid_arr == sid
            if not m.any():
                continue
            ax.scatter(
                obs[m],
                ridge[m],
                s=32,
                c=_STATION_COLORS.get(sid, "#b45309"),
                label=city,
                zorder=3,
            )
    else:
        ax.scatter(obs, ridge, s=28, c="#b45309", label="Ridge", zorder=3)
    ax.scatter(obs, norm, s=22, c="#64748b", marker="x", label="1991-2020 normal", zorder=2)
    lo = float(np.nanmin([obs.min(), ridge.min(), norm.min()]))
    hi = float(np.nanmax([obs.max(), ridge.max(), norm.max()]))
    pad = 0.05 * (hi - lo + 1.0)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#0f172a", lw=1.0, label="1:1")
    skill = fit.get("skill") or {}
    if skill.get("ridge") and skill.get("normal"):
        rr = float(skill["ridge"]["rmse_in"])
        nn = float(skill["normal"]["rmse_in"])
        ax.text(
            0.98,
            0.02,
            f"Ridge RMSE {rr:.2f} vs normal {nn:.2f}",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=8,
        )
    ax.set_xlabel("observed DJF snow (in)")
    ax.set_ylabel("predicted DJF snow (in)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=7, loc="upper left")
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

    by_id = {r["station_id"]: r for r in fit["station_err"]}
    cities: list[str] = []
    bias: list[float] = []
    for sid, city in CORE_STATIONS:
        row = by_id.get(sid)
        if row is None:
            continue
        cities.append(city)
        bias.append(float(row["bias_in"]))
    y = np.arange(len(cities), dtype=float)
    colors = ["#b45309" if v >= 0 else "#1d4ed8" for v in bias]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.barh(y, bias, color=colors, edgecolor="#0f172a", linewidth=0.4, height=0.62)
    ax.axvline(0.0, color="#0f172a", lw=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(cities, fontsize=10)
    ax.invert_yaxis()
    span = max(8.0, float(np.nanmax(np.abs(bias))) * 1.18) if bias else 8.0
    ax.set_xlim(-span * 0.15, span)
    for yi, val in zip(y, bias):
        ax.text(val + 0.35, yi, f"{val:+.1f} in", va="center", ha="left", fontsize=9)
    ax.set_xlabel("mean Ridge minus observed (in)")
    ax.set_title(title, fontsize=10)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.subplots_adjust(bottom=0.18, top=0.90, left=0.22, right=0.97)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any], live: bool = False) -> list[Path]:
    require_clean(QUESTION, source="question")
    scatter_sub = live_scatter_subtitle(fit) if live else FIXTURE_SCATTER_SUBTITLE
    map_sub = live_map_subtitle(fit) if live else FIXTURE_MAP_SUBTITLE
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
            title="Holdout mean Ridge minus observed",
            subtitle=map_sub,
        ),
    ]
    _cap(len(paths))
    return paths
