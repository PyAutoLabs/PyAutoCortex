# adapt_snr_cap — Real-data test of the S/N 3 adapt-image cap: cap3 vs uncapped SLaM, 14 lenses

Project: adapt_snr_cap
Issue: none

## Now

Just opened — nothing submitted yet.

## Runs

- 416418 — running — gpu — 2026-11-25 — rerun Euclid tasks 10-13 after positions.json fix
- 416981 — open — ral — 2026-11-25 — cap3, uncapped and peak_share_unified on ral CPU (24 workers) for the 10 HST and 10 COWLS datasets, array 0-9,14-23, results in output_cpu

## Log

- 2026-11-25 — note — 416941 correction: tasks 0 and 1 (slacs0216-0813, slacs0252+0039) completed all four searches on the A100 before the cancel; task 2 was 4 min 45 s in; tasks 3-9 never started. CPU pilot 416972 (ral, slacs1430 uncapped arm) finished in 0:53 with peak memory 45 GB; its own ledger branch has not merged.
- 2026-11-25 — run — 416981 submitted: cap3, uncapped and peak_share_unified on ral CPU (24 workers) for the 10 HST and 10 COWLS datasets, array 0-9,14-23, results in output_cpu
- 2026-11-25 — run — 416571 failed: cap3 vs uncapped SLaM baseline on 5 COWLS M25 lenses x F150W + F277W (10 datasets), gpu array 14-23%4 — cancelled by request before any task started; COWLS moved to the CPU array 416981
- 2026-11-25 — run — 416941 failed: peak_share_unified arm (peak_share Hilbert mesh, AdaptSplit on the same soft S/N transform) on the 10 HST lenses, gpu array 0-9%4 — cancelled by request to move the fits to CPU; task 2 had run 4 min 45 s
- 2026-11-25 — run — 416941 submitted: peak_share_unified arm (peak_share Hilbert mesh, AdaptSplit on the same soft S/N transform) on the 10 HST lenses, gpu array 0-9%4
- 2026-11-25 — run — 416884 failed: weighting arms budget, rank, peak_share + control cap3_mesh on the 10 HST lenses (SLACS, BELLS), gpu array 0-9%4; phase 2 of PyAutoArray#714 — cancelled by request before any task started; replaced by 416941
- 2026-11-25 — run — 416884 submitted: weighting arms budget, rank, peak_share + control cap3_mesh on the 10 HST lenses (SLACS, BELLS), gpu array 0-9%4; phase 2 of PyAutoArray#714
- 2026-11-25 — run — 416571 submitted: cap3 vs uncapped SLaM baseline on 5 COWLS M25 lenses x F150W + F277W (10 datasets), gpu array 14-23%4
- 2026-11-25 — run — 416362 finished — wall 3:42: cap3 vs uncapped SLaM, 14 lenses (5 SLACS, 5 BELLS, 4 Euclid), gpu array 0-13%4 — 10/14 lenses complete (SLACS + BELLS, both arms); Euclid tasks 10-13 failed in 5 s on the positions.json format, fixed and rerun as 416418
- 2026-11-25 — run — 416418 submitted: rerun Euclid tasks 10-13 after positions.json fix
- 2026-11-24 — run — 416362 submitted: cap3 vs uncapped SLaM, 14 lenses (5 SLACS, 5 BELLS, 4 Euclid), gpu array 0-13%4
- 2026-11-24 — note — ledger opened
