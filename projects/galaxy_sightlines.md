# galaxy_sightlines — Full line of sight of a strong lens: dark halos, galaxies, environment; external shear budget

Project: galaxy_sightlines
Issue: none

## Now

Just opened — nothing submitted yet.

## Runs

- 417590 — open — gpu — 2026-11-28 — stage 1 step B, the rest of the 1,000 sightlines: fitted shear of 900 full-size sightlines (seeds 100-999, 18 tasks x 50), three cases each, power law + shear refits from three starts, fit tolerance 1e-7; GPU array 2-19, one A100 each, at most 4 at a time

## Log

- 2026-11-28 — run — 417590 submitted: stage 1 step B, the rest of the 1,000 sightlines: fitted shear of 900 full-size sightlines (seeds 100-999, 18 tasks x 50), three cases each, power law + shear refits from three starts, fit tolerance 1e-7; GPU array 2-19, one A100 each, at most 4 at a time
- 2026-11-27 — run — 417565 finished — wall 1:41: stage 1 step B CPU pilot: fitted shear of 50 full-size sightlines (5 tasks x 10), three cases each, fit tolerance 1e-7; CPU array 0-4, 8 cores each — 5/5 tasks completed, 50/50 sightlines fitted, none failed; median 421 s per sightline on 8 cores (tasks took 1:07 to 1:41)
- 2026-11-27 — run — 417564 finished — wall 1:55: stage 1 step A at full image size on a CPU node: offset starts, injected shears, one perturbing halo at five distances, three redshifts and three masses (part 3 at fit tolerance 1e-7); 8 cores, one job — 1/1 task completed, all three parts
- 2026-11-27 — run — 417555 finished — wall 0:26: stage 1 step B pilot: fitted shear of 100 sightlines (2 tasks x 50), three cases each, power law + shear refits from three starts; GPU array 0-1, one A100 each — 2/2 tasks completed, 100/100 sightlines fitted, none failed; median 22 s per sightline on one A100 (tasks took 0:26 and 0:24)
- 2026-11-27 — run — 417554 finished — wall 0:08: stage 1 step A at full image size: refits from offset starts, recovery of injected shears, one perturbing halo at five distances, three redshifts and three masses; one A100, one job — 1/1 task completed, all three parts; its validate_full.json was overwritten an hour later by the CPU job 417564 (same output path), the log is kept
- 2026-11-27 — run — 417565 submitted: stage 1 step B CPU pilot: fitted shear of 50 full-size sightlines (5 tasks x 10), three cases each, fit tolerance 1e-7; CPU array 0-4, 8 cores each
- 2026-11-27 — run — 417564 submitted: stage 1 step A at full image size on a CPU node: offset starts, injected shears, one perturbing halo at five distances, three redshifts and three masses (part 3 at fit tolerance 1e-7); 8 cores, one job
- 2026-11-27 — run — 417561 finished — wall 0:44: stage 1 timing on a CPU node: two full-size sightlines and the injected-shear check, 16 cores, one job; decides whether the population can run as a CPU array while the gpu partition is full — 1/1 task completed; one full-size sightline took 29 min on 16 cores (ray traces 37 s each, model evaluations 1.6 s each, fits up to 200 evaluations), the second sightline failed on a NaN fixed since; 21/21 injected-shear fits completed
- 2026-11-27 — run — 417561 submitted: stage 1 timing on a CPU node: two full-size sightlines and the injected-shear check, 16 cores, one job; decides whether the population can run as a CPU array while the gpu partition is full
- 2026-11-27 — run — 417555 submitted: stage 1 step B pilot: fitted shear of 100 sightlines (2 tasks x 50), three cases each, power law + shear refits from three starts; GPU array 0-1, one A100 each
- 2026-11-27 — run — 417554 submitted: stage 1 step A at full image size: refits from offset starts, recovery of injected shears, one perturbing halo at five distances, three redshifts and three masses; one A100, one job
- 2026-11-27 — note — Follow-up to check, separate from stage 1 (human): "my feeling is that we do need to be wary of big luminous galaxies being within 10″ to 20″ contributing to shears, albeit if this was really whats happening on real lenses we would have seen them but we should double check that."
- 2026-11-27 — note — ledger opened
