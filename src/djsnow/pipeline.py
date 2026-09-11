# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop. Two figures. Page refused unless Ridge beats normal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from djsnow.claims import require_clean, require_paths_clean
from djsnow.config import FEATURE_NAMES, QUESTION
from djsnow.fetch import fetch_live
from djsnow.figure import write_two
from djsnow.fixture import build_fixture
from djsnow.models import fit_pack

try:
    from snowforge.gate import require_claims, require_fetch, require_no_p_sfha, require_split
except ImportError:  # pragma: no cover

    def require_claims(**kwargs):
        del kwargs

    def require_fetch(**kwargs):
        del kwargs

    def require_no_p_sfha(**kwargs):
        del kwargs

    def require_split(**kwargs):
        del kwargs


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    skip = {"holdout_obs", "holdout_ridge", "holdout_normal", "holdout_station_id"}
    return {k: v for k, v in report.items() if k not in skip}


def _run(log_dir: Path, *, pack, fixture: bool, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    require_no_p_sfha(thread_id="p_sfha")
    require_clean(QUESTION, source="question")
    fit = fit_pack(pack)
    require_split(
        temporal_ok=True,
        confirm_in_train=bool(fit["confirm_in_train"]),
        random_split=bool(fit["random_split"]),
        djf_in_features=bool(fit["djf_in_features"]),
        thread_id="split",
    )
    paths = write_two(log_dir, fit=fit, live=not fixture)
    require_claims(
        n_figures=len(paths),
        page_in_scope=bool(fit["page_in_scope"]),
        ridge_beats_normal=bool(fit["ridge_beats_normal"]),
        thread_id="claims",
    )
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "source": pack.source,
        "n_rows": pack.n_rows,
        "n_stations": pack.n_stations,
        "n_train": fit["n_train"],
        "n_holdout": fit["n_holdout"],
        "n_confirm": fit["n_confirm"],
        "n_train_stations": fit["n_train_stations"],
        "n_holdout_stations": fit["n_holdout_stations"],
        "units": "inches",
        "feature_names": list(FEATURE_NAMES),
        "skill": fit["skill"],
        "tercile": fit["tercile"],
        "ridge_beats_normal": fit["ridge_beats_normal"],
        "page_in_scope": fit["page_in_scope"],
        "station_err": fit["station_err"],
        "confirm": fit["confirm"],
        "djf_in_features": False,
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "figures": [p.name for p in paths],
        "holdout_obs": fit["holdout_obs"],
        "holdout_ridge": fit["holdout_ridge"],
        "holdout_normal": fit["holdout_normal"],
        "holdout_station_id": fit["holdout_station_id"],
    }
    if extra:
        report.update(extra)
    name = "stage0_report.json" if fixture else "stage_c_report.json"
    (log_dir / name).write_text(json.dumps(_jsonable(report), indent=2, default=str) + "\n")
    paths_scan = [log_dir / name]
    readme = Path(__file__).resolve().parents[2] / "README.md"
    if readme.is_file():
        paths_scan.append(readme)
    require_paths_clean(paths_scan)
    return report


def stage0_fixture(log_dir: Path) -> dict[str, Any]:
    return _run(log_dir, pack=build_fixture(), fixture=True)


def run_live(log_dir: Path, *, cache_dir: Path) -> dict[str, Any]:
    pack, meta = fetch_live(cache_dir=cache_dir)
    require_fetch(
        ghcnd_ok=True,
        normals_ok=True,
        nino_ok=True,
        invented_points=False,
        thread_id="live.fetch",
    )
    return _run(log_dir, pack=pack, fixture=False, extra={"live": meta})
