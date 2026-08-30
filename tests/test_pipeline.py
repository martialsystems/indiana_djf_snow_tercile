# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from djsnow.config import QUESTION
from djsnow.errors import FigureCapError
from djsnow.figure import _cap
from djsnow.pipeline import stage0_fixture


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["figures"] == ["scatter.png", "error_map.png"]
    assert (tmp_path / "scatter.png").is_file()
    assert (tmp_path / "error_map.png").is_file()
    assert report["p_sfha_feature"] is False
    assert report["djf_in_features"] is False
    assert report["skill"]["ridge"]["rmse_in"] < report["skill"]["normal"]["rmse_in"]


def test_third_figure_refused() -> None:
    try:
        _cap(3)
        raise AssertionError("cap allowed 3")
    except FigureCapError:
        pass
