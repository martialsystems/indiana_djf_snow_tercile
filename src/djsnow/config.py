# Copyright (c) 2026 Martial Systems LLC
"""Locked DJF station snowfall vs 1991-2020 normal. Pre-season October/ENSO only."""

from __future__ import annotations

from datetime import date
from pathlib import Path

QUESTION = (
    "Can October features plus ENSO beat the 1991-2020 DJF snowfall normal "
    "at held-out Indiana GHCND stations?"
)
USER_AGENT = "MartialSystemsResearch/indiana_djf_snow_tercile"
MAX_FIGURES = 2
MM_PER_INCH = 25.4
COMPLETE_FRAC = 0.80
MIN_TRAIN_WINTERS = 20
TRAIN_LAST_WINTER = 2019  # DJF 2018-19
HOLDOUT_FIRST_WINTER = 2020  # DJF 2019-20
HOLDOUT_LAST_WINTER = 2025  # DJF 2024-25
CONFIRM_WINTER = 2026  # DJF 2025-26
NORMAL_FIRST = 1991
NORMAL_LAST = 2020
CORE_STATIONS = (
    ("USW00014848", "South Bend"),
    ("USW00014827", "Fort Wayne"),
    ("USW00093819", "Indianapolis"),
    ("USW00093817", "Evansville"),
)
IN_LAT = (37.77, 41.76)
IN_LON = (-88.10, -84.78)
FEATURE_NAMES = (
    "nino34_oct",
    "snow_normal_in",
    "prior_djf_in",
    "oct_tavg_c",
    "oct_prcp_in",
    "lat",
    "elev_m",
)
BANNED_FEATURE_TOKENS = ("djf_prcp", "djf_tavg", "djf_snow", "mrms", "stageiv", "p_sfha", "hand")
GHCND_STATION_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/{sid}.csv.gz"
GHCND_STATIONS_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
NORMALS_URL = "https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/access/{sid}.csv"
NINO_URL = "https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices"
REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_GIST = "https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3"
AMOUNT_SHA = "ac36f0f"
JJA_MISS_SHA = "1416da1"
WINTER_LAKE_SHA = "6b47f21"
LIVE_SCATTER_SUBTITLE = (
    "Holdout DJF inches. Ridge RMSE 14.48 vs normal 13.00. "
    "October plus ENSO is a no. Seasonal, not a storm."
)
LIVE_MAP_SUBTITLE = (
    "Holdout mean Ridge minus observed DJF inches by city. "
    "South Bend +20 in. Seasonal error, not a storm, not water."
)
FIXTURE_SCATTER_SUBTITLE = "Fixture planted ENSO-snow. Does not rescue live skill."
FIXTURE_MAP_SUBTITLE = "Fixture mean error. Does not rescue live skill."
