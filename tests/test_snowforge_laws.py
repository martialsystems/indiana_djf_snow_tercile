# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from snowforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from snowforge.gate import require_claims, require_fetch, require_no_p_sfha, require_split
from snowforge.product_laws import laws


def test_laws() -> None:
    require_no_p_sfha(thread_id="t.p.ok")
    with pytest.raises(LawBlockedError):
        require_no_p_sfha(p_sfha_feature=True, thread_id="t.p.bad")
    require_split(thread_id="t.s.ok")
    with pytest.raises(LawBlockedError):
        require_split(djf_in_features=True, thread_id="t.s.djf")
    with pytest.raises(LawBlockedError):
        require_split(confirm_in_train=True, thread_id="t.s.conf")
    require_fetch(ghcnd_ok=True, normals_ok=True, nino_ok=True, thread_id="t.f.ok")
    with pytest.raises(LawBlockedError):
        require_fetch(ghcnd_ok=True, normals_ok=True, nino_ok=True, invented_points=True, thread_id="t.f.inv")
    require_claims(n_figures=2, page_in_scope=False, thread_id="t.c.ok")
    with pytest.raises(LawBlockedError):
        require_claims(n_figures=3, thread_id="t.c.fig")
    with pytest.raises(LawBlockedError):
        require_claims(page_in_scope=True, ridge_beats_normal=False, thread_id="t.c.page")
    assert {row["id"] for row in laws()} == {
        "snow.no_p_sfha",
        "snow.temporal_split",
        "snow.fetch_ghcnd",
        "snow.claim_bans",
    }
