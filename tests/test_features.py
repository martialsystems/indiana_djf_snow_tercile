# Copyright (c) 2026 Martial Systems LLC

import numpy as np
import pytest

from djsnow.config import BANNED_FEATURE_TOKENS, FEATURE_NAMES
from djsnow.errors import LeakError
from djsnow.features import matrix_x
from djsnow.fixture import build_fixture


def test_no_djf_in_feature_names() -> None:
    blob = " ".join(FEATURE_NAMES).lower()
    for tok in BANNED_FEATURE_TOKENS:
        assert tok not in blob


def test_matrix_shape() -> None:
    pack = build_fixture()
    x = matrix_x(pack)
    assert x.shape[1] == 7
    assert np.isfinite(x).all()


def test_leak_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    import djsnow.features as feat

    monkeypatch.setattr(feat, "FEATURE_NAMES", FEATURE_NAMES + ("djf_snow",))
    with pytest.raises(LeakError):
        matrix_x(build_fixture())
