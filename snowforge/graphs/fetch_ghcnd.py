# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from snowforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("ghcnd_ok"):
        v.append("ghcnd_empty")
    if not state.get("normals_ok"):
        v.append("normals_empty")
    if not state.get("nino_ok"):
        v.append("nino_empty")
    if state.get("invented_points"):
        v.append("invented_points")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="snow.fetch_ghcnd",
        evaluate=_evaluate,
        extra=["ghcnd_ok", "normals_ok", "nino_ok", "invented_points"],
    )
