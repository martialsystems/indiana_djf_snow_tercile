# Copyright (c) 2026 Martial Systems LLC

from djsnow.enso import parse_nino34_october


def test_october_maps_to_next_winter() -> None:
    text = (
        "YR MON  NINO1+2   ANOM   NINO3    ANOM   NINO4    ANOM NINO3.4    ANOM\n"
        "2018  10   21.00    0.10   25.00    0.10   28.00    0.10   26.50    0.72\n"
    )
    out = parse_nino34_october(text)
    assert out[2019] == 0.72
