# Copyright (c) 2026 Martial Systems LLC
"""Call sites for refuse laws."""

from __future__ import annotations

from typing import Any

from snowforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from snowforge.graphs.claim_bans import build_graph as build_claims
from snowforge.graphs.fetch_ghcnd import build_graph as build_fetch
from snowforge.graphs.no_p_sfha import build_graph as build_p
from snowforge.graphs.temporal_split import build_graph as build_split


def require_no_p_sfha(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "snow_p"))
    state = {
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "p_sfha_figure": False,
        "p_sfha_import": False,
        "hand_feature": False,
        "nora_q": False,
    }
    state.update(flags)
    require_law(build_p(), state, allow_decisions=["allow"], law_id="snow.no_p_sfha", thread_id=thread_id, raise_error=True)


def require_split(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "snow_split"))
    state = {
        "temporal_ok": True,
        "confirm_in_train": False,
        "random_split": False,
        "djf_in_features": False,
    }
    state.update(flags)
    require_law(
        build_split(),
        state,
        allow_decisions=["allow"],
        law_id="snow.temporal_split",
        thread_id=thread_id,
        raise_error=True,
    )


def require_fetch(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "snow_fetch"))
    state = {
        "ghcnd_ok": False,
        "normals_ok": False,
        "nino_ok": False,
        "invented_points": False,
    }
    state.update(flags)
    require_law(
        build_fetch(),
        state,
        allow_decisions=["allow"],
        law_id="snow.fetch_ghcnd",
        thread_id=thread_id,
        raise_error=True,
    )


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "snow_claims"))
    state = {
        "flood_warning": False,
        "blizzard": False,
        "hero_inches": False,
        "hand_wet": False,
        "n_figures": 2,
        "page_in_scope": False,
        "ridge_beats_normal": False,
    }
    state.update(flags)
    require_law(
        build_claims(),
        state,
        allow_decisions=["allow"],
        law_id="snow.claim_bans",
        thread_id=thread_id,
        raise_error=True,
    )
