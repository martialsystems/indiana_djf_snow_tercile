# Copyright (c) 2026 Martial Systems LLC
"""Temporal winter split. Confirmation winter never trains."""

from __future__ import annotations

import numpy as np

from djsnow.config import CONFIRM_WINTER, HOLDOUT_FIRST_WINTER, HOLDOUT_LAST_WINTER, TRAIN_LAST_WINTER
from djsnow.errors import SplitError
from djsnow.pack import WinterPack


def row_masks(pack: WinterPack) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    w = np.asarray(pack.winter_id, dtype=int)
    train = w <= TRAIN_LAST_WINTER
    hold = (w >= HOLDOUT_FIRST_WINTER) & (w <= HOLDOUT_LAST_WINTER)
    confirm = w == CONFIRM_WINTER
    return train, hold, confirm


def assert_split(pack: WinterPack, train: np.ndarray, hold: np.ndarray, confirm: np.ndarray) -> None:
    w = np.asarray(pack.winter_id, dtype=int)
    train = np.asarray(train, dtype=bool)
    hold = np.asarray(hold, dtype=bool)
    confirm = np.asarray(confirm, dtype=bool)
    if not train.any():
        raise SplitError("train is empty")
    if not hold.any():
        raise SplitError("holdout is empty")
    if np.any(train & hold) or np.any(train & confirm) or np.any(hold & confirm):
        raise SplitError("train/holdout/confirm overlap")
    if np.any(train & (w == CONFIRM_WINTER)):
        raise SplitError("confirmation winter in train")
    if int(w[train].max()) >= int(w[hold].min()):
        raise SplitError("not a temporal winter cut")
