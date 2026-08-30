# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from snowforge.graphs._common import binary_graph

_FLAGS = ("flood_warning", "blizzard", "hero_inches", "hand_wet")


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [k for k in _FLAGS if state.get(k)]
    n = int(state.get("n_figures") or 0)
    if n > 2:
        v.append("figure_cap")
    if state.get("page_in_scope") and not state.get("ridge_beats_normal"):
        v.append("page_without_skill")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="snow.claim_bans",
        evaluate=_evaluate,
        extra=[*_FLAGS, "n_figures", "page_in_scope", "ridge_beats_normal"],
    )
