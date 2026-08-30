# Methodology: DJF station snowfall vs 1991-2020 normal

Question: Can October features plus ENSO beat the 1991-2020 DJF snowfall normal at held-out Indiana GHCND stations?

## Label

GHCND `SNOW` summed 1 Dec through 28/29 Feb, inches. Drop a station-winter if fewer than 80% of DJF days are present. Tercile cuts are the 33rd and 67th percentiles of that station's **train** DJF totals. Confirmation winter 2025-26 does not set bins.

## Bars

Always-normal inches (official 1991-2020 DJF snowfall normal). Last year's DJF total. Ridge on the October vector. CPC Indiana precip tercile is descriptive only if the official GIS fetches.

## Features

Niño 3.4 October (CPC ERSSTv5, dated, mapped to the following DJF). Station 1991-2020 DJF snow normal. Prior DJF total. October mean temperature and October precipitation at the station. Latitude and elevation.

DJF rain, DJF radar, Stage IV, MRMS, HAND, and White River Q are refused as features.

## Split

Train DJF 1991-92 through 2018-19. Holdout DJF 2019-20 through 2024-25. Confirmation DJF 2025-26 out of train and out of tercile cuts. Station × winter rows. Spatial leak of the same winter across nearby stations is expected; report pooled RMSE and per-station bias.

Live holdout: Ridge RMSE 14.48, normal 13.00, last year 10.18. October plus ENSO lost to a table of averages; last winter beat both. Confirmation DJF 2025-26 Ridge 4.25 vs normal 7.04 does not reopen a page and does not set cuts.

## Figures

1. Holdout scatter of Ridge and the normal vs observed inches.
2. Station map of mean Ridge minus observed inches. Seasonal error, not a storm, not water.
