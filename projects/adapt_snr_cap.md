# adapt_snr_cap — Real-data test of the S/N 3 adapt-image cap: cap3 vs uncapped SLaM, 14 lenses

Project: adapt_snr_cap
Issue: none

## Now

Just opened — nothing submitted yet.

## Runs

- 416418 — running — gpu — 2026-11-25 — rerun Euclid tasks 10-13 after positions.json fix
- 416571 — open — gpu — 2026-11-25 — cap3 vs uncapped SLaM baseline on 5 COWLS M25 lenses x F150W + F277W (10 datasets), gpu array 14-23%4
- 416941 — open — gpu — 2026-11-25 — peak_share_unified arm (peak_share Hilbert mesh, AdaptSplit on the same soft S/N transform) on the 10 HST lenses, gpu array 0-9%4

## Log

- 2026-11-25 — run — 416941 submitted: peak_share_unified arm (peak_share Hilbert mesh, AdaptSplit on the same soft S/N transform) on the 10 HST lenses, gpu array 0-9%4
- 2026-11-25 — run — 416884 failed: weighting arms budget, rank, peak_share + control cap3_mesh on the 10 HST lenses (SLACS, BELLS), gpu array 0-9%4; phase 2 of PyAutoArray#714 — cancelled by request before any task started; replaced by 416941
- 2026-11-25 — run — 416884 submitted: weighting arms budget, rank, peak_share + control cap3_mesh on the 10 HST lenses (SLACS, BELLS), gpu array 0-9%4; phase 2 of PyAutoArray#714
- 2026-11-25 — run — 416571 submitted: cap3 vs uncapped SLaM baseline on 5 COWLS M25 lenses x F150W + F277W (10 datasets), gpu array 14-23%4
- 2026-11-25 — run — 416362 finished — wall 3:42: cap3 vs uncapped SLaM, 14 lenses (5 SLACS, 5 BELLS, 4 Euclid), gpu array 0-13%4 — 10/14 lenses complete (SLACS + BELLS, both arms); Euclid tasks 10-13 failed in 5 s on the positions.json format, fixed and rerun as 416418
- 2026-11-25 — run — 416418 submitted: rerun Euclid tasks 10-13 after positions.json fix
- 2026-11-24 — run — 416362 submitted: cap3 vs uncapped SLaM, 14 lenses (5 SLACS, 5 BELLS, 4 Euclid), gpu array 0-13%4
- 2026-11-24 — note — ledger opened
