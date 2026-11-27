# galaxy_sightlines — Full line of sight of a strong lens: dark halos, galaxies, environment; external shear budget

Project: galaxy_sightlines
Issue: none

## Now

Just opened — nothing submitted yet.

## Runs

- 417554 — open — gpu — 2026-11-27 — stage 1 step A at full image size: refits from offset starts, recovery of injected shears, one perturbing halo at five distances, three redshifts and three masses; one A100, one job
- 417555 — open — gpu — 2026-11-27 — stage 1 step B pilot: fitted shear of 100 sightlines (2 tasks x 50), three cases each, power law + shear refits from three starts; GPU array 0-1, one A100 each
- 417564 — open — ral — 2026-11-27 — stage 1 step A at full image size on a CPU node: offset starts, injected shears, one perturbing halo at five distances, three redshifts and three masses (part 3 at fit tolerance 1e-7); 8 cores, one job
- 417565 — open — ral — 2026-11-27 — stage 1 step B CPU pilot: fitted shear of 50 full-size sightlines (5 tasks x 10), three cases each, fit tolerance 1e-7; CPU array 0-4, 8 cores each

## Log

- 2026-11-27 — run — 417565 submitted: stage 1 step B CPU pilot: fitted shear of 50 full-size sightlines (5 tasks x 10), three cases each, fit tolerance 1e-7; CPU array 0-4, 8 cores each
- 2026-11-27 — run — 417564 submitted: stage 1 step A at full image size on a CPU node: offset starts, injected shears, one perturbing halo at five distances, three redshifts and three masses (part 3 at fit tolerance 1e-7); 8 cores, one job
- 2026-11-27 — run — 417561 finished — wall 0:44: stage 1 timing on a CPU node: two full-size sightlines and the injected-shear check, 16 cores, one job; decides whether the population can run as a CPU array while the gpu partition is full — 1/1 task completed; one full-size sightline took 29 min on 16 cores (ray traces 37 s each, model evaluations 1.6 s each, fits up to 200 evaluations), the second sightline failed on a NaN fixed since; 21/21 injected-shear fits completed
- 2026-11-27 — run — 417561 submitted: stage 1 timing on a CPU node: two full-size sightlines and the injected-shear check, 16 cores, one job; decides whether the population can run as a CPU array while the gpu partition is full
- 2026-11-27 — run — 417555 submitted: stage 1 step B pilot: fitted shear of 100 sightlines (2 tasks x 50), three cases each, power law + shear refits from three starts; GPU array 0-1, one A100 each
- 2026-11-27 — run — 417554 submitted: stage 1 step A at full image size: refits from offset starts, recovery of injected shears, one perturbing halo at five distances, three redshifts and three masses; one A100, one job
- 2026-11-27 — note — Follow-up to check, separate from stage 1 (human): "my feeling is that we do need to be wary of big luminous galaxies being within 10″ to 20″ contributing to shears, albeit if this was really whats happening on real lenses we would have seen them but we should double check that."
- 2026-11-27 — note — ledger opened
