# Agent notes: indiana_djf_snow_tercile

Public GitHub. MIT. Question: Can October features plus ENSO beat the 1991-2020 DJF snowfall normal at held-out Indiana GHCND stations?

Live: Ridge RMSE 14.48 vs normal 13.00 vs last year 10.18. October plus ENSO does not beat the normal. Page stays out of scope. Do not train a deeper net.

Do not edit `indiana_cocorahs_mrms`, `indiana_radar_miss`, or `indiana_winter_lake_miss`. Do not start `indiana_winter_page` in this git. Do not read `p_sfha`, HAND, Nora Q, or NWM.

`snowforge/` is the GraphForge pin.

Research index: https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
