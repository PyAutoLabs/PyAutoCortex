# euclid_dr1 — Does the sep1 DR1 delivery reproduce the ten prelim lenses by eye

Project: euclid_dr1
Issue: none

## Now

342650 refits the ten euclid_dr1_prelim lenses from the sep1 delivery (dataset/dr1_sep1/, two-stage CPU route from the euclid_dr1 clone). Next: pull it, build the per-tile side-by-side sheet against prelim run 342629 and the Einstein-radius table (name any tile off by more than 10 %); the human judges by eye whether the same lenses come back — numerical parity is not the question (prelim's rerun scatter is z ≈ 15).

## Runs

- 342650 — open — ral — 2026-09-11 — euclid_dr1 sep1 reproduction: the ten euclid_dr1_prelim lenses refitted from the sep1 delivery through prelim's route (hpc/batch_cpu/submit_initial_lens_model_two_stage: vis_lp then vis_pix), array 0-9, wall budget 36:00; the by-eye reference is prelim run 342629

## Log

- 2026-09-18 — note — Bare-field pipeline prepared as PR #90 at 7fbdbe5: 230 local tests and 9 smoke scripts passed, independent review CLEAN. Not merged or synced: CI unit legs fail in jax-zero-contour with JAX 0.11.2. Local science remains d53b9ce; RAL PyAutoLens remains 7197380 and actual imported source lacks bare-field normalization. HPCPullPyAuto not run; read-only precondition check timed out during Galaxy after Nerves/Fit/Array passed. No SLURM submission; modelling-script approval hold remains.
- 2026-09-11 — run — 342650 submitted: euclid_dr1 sep1 reproduction: the ten euclid_dr1_prelim lenses refitted from the sep1 delivery through prelim's route (hpc/batch_cpu/submit_initial_lens_model_two_stage: vis_lp then vis_pix), array 0-9, wall budget 36:00; the by-eye reference is prelim run 342629
- 2026-09-11 — note — the delivery, and the ten tiles: Segmentation.zip (14.8 GB, three nested batch zips eclipse_catalogue_fits_sep1-segmentation_batch{1,2,3}, 15032 tile folders, every tile already in the pipeline dataset layout) was read in place with Python zipfile and the ten euclid_dr1_prelim tiles extracted into dataset/dr1_sep1/ (array index = list order). Three tiles keep the prelim name; seven are recentred by 0.8–2.2 arcsec and carry a new name (prelim → sep1: 102007899 → …RA0631697483678DECNEG0650586413593 0.88"; 102007903 → …RA0668824944366DECNEG0648906250124 1.88"; 102008165 → …RA0109661927007DECNEG0642904268129 0.79"; 102008219 → …RA0727857418392DECNEG0644388277074 2.19"; 102008468 → …RA3567393529734DECNEG0647169093056 1.13"; 102008532 → …RA0683486015030DECNEG0642073552911 1.43"; 102008848 → …RA0601371893270DECNEG0634606579714 0.91"). The regenerated info.json/positions.json differ from prelim's (102005065: mask radius 5.65" vs 3.32", 4 positions vs 2), which is why the comparison is by eye. The clone puts config/visualize back to the autoarray default colormap. Carried from the 2026-09-11 task file stranded on branch claude/euclid-dr1-birth-2026-09-11 under the pre-decision-60 schema.
- 2026-09-11 — note — ledger opened
