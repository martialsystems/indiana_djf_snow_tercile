# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

import pytest

from djsnow.errors import FetchError
from djsnow.fetch import fetch_live


def test_empty_ghcnd_stops(tmp_path: Path) -> None:
    def getter(url: str) -> bytes:
        if "ghcnd-stations" in url:
            return (
                b"USW00014848  41.7072  -86.3164  235.6 IN SOUTH BEND                          \n"
            )
        raise FetchError("empty in this test")

    with pytest.raises(FetchError):
        fetch_live(cache_dir=tmp_path, getter=getter)
