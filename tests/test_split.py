# Copyright (c) 2026 Martial Systems LLC

import numpy as np
import pytest

from djsnow.config import CONFIRM_WINTER, TRAIN_LAST_WINTER
from djsnow.errors import SplitError
from djsnow.fixture import build_fixture
from djsnow.split import assert_split, row_masks


def test_temporal_cut() -> None:
    pack = build_fixture()
    train, hold, confirm = row_masks(pack)
    assert_split(pack, train, hold, confirm)
    assert int(pack.winter_id[train].max()) <= TRAIN_LAST_WINTER
    assert not np.any(train & (pack.winter_id == CONFIRM_WINTER))


def test_confirm_in_train_refused() -> None:
    pack = build_fixture()
    train, hold, confirm = row_masks(pack)
    train = train.copy()
    train[np.where(confirm)[0][0]] = True
    with pytest.raises(SplitError, match="overlap"):
        assert_split(pack, train, hold, confirm)
