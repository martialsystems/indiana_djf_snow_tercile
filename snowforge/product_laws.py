# Copyright (c) 2026 Martial Systems LLC
"""Refuse laws. Verify-before-done is the finish gate."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from snowforge.graphs.claim_bans import build_graph as claim_bans
    from snowforge.graphs.fetch_ghcnd import build_graph as fetch_g
    from snowforge.graphs.no_p_sfha import build_graph as no_p_sfha
    from snowforge.graphs.temporal_split import build_graph as temporal_split

    return [
        {
            "id": "snow.no_p_sfha",
            "build": no_p_sfha,
            "state": {
                "p_sfha_feature": False,
                "p_sfha_label": False,
                "p_sfha_figure": False,
                "p_sfha_import": False,
                "hand_feature": False,
                "nora_q": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "snow.temporal_split",
            "build": temporal_split,
            "state": {
                "temporal_ok": True,
                "confirm_in_train": False,
                "random_split": False,
                "djf_in_features": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "snow.fetch_ghcnd",
            "build": fetch_g,
            "state": {
                "ghcnd_ok": True,
                "normals_ok": True,
                "nino_ok": True,
                "invented_points": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "snow.claim_bans",
            "build": claim_bans,
            "state": {
                "flood_warning": False,
                "blizzard": False,
                "hero_inches": False,
                "hand_wet": False,
                "n_figures": 2,
                "page_in_scope": False,
                "ridge_beats_normal": False,
            },
            "allow_decisions": ["allow"],
        },
    ]
