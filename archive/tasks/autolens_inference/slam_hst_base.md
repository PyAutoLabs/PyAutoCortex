# Autolens_inference — The HST SLaM base run — six backend legs, one parity row

Project: autolens_inference
Summary: Do six backend legs agree on the HST SLaM posterior?
State: ready
Gates:
Witness: All six legs of the 5-stage HST SLaM chain — {numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}, seeds 0 and 1 each — complete on RAL via the six `hpc/batch_{gpu,cpu}/submit_slam_hst_*` array submits: every stage of every leg carries `.completed` and `resumed: false`, every pixelized stage (source_pix[1], source_pix[2], light[1], mass_total[1]) carries `positions.info`, each leg writes `results/slam/imaging/hst/<config_name>/stages_seed<n>.json` with five stage rows and reject-inclusive `likelihood_evals`, `build_readme.py --check` renders the six-column parity view, and at the same seed the mass_total[1] posteriors agree across all six legs within 2 nats of log-evidence, 0.2σ on every median, and a σ-ratio inside [0.8, 1.25] on einstein_radius, slope and shear_magnitude; any leg outside those bands is the finding, not a rerun.
Budget: 120:00
Runs:
Ruling:
Review-minutes: 45
Epic: autolens-inference
Filed: 2026-09-11

## Question

The repo now has one driver — `scripts/imaging/slam/hst.py` over
`scripts/misc/slam/_runner.py`, merged in autolens_inference#3 — that runs the
workspace-default SLaM chain (source_lp[1] → source_pix[1] → source_pix[2] →
light[1] → mass_total[1], Nautilus throughout, RectangularBilinearAdaptDensity →
AdaptImage with reg.Adapt, MGE 20×2 lens / 20×1 source, Isothermal+shear →
PowerLaw) under any of three backends and either inversion path, on the
simulated HST cell whose truth is `dataset/imaging/hst/tracer.json`. Nothing has
yet been measured with it: `results/slam/` is empty and the only rates in
`wall/rates.py` are two partial `source_lp[1]` probes on the laptop.

This task is the first parity row the project exists for. Six legs — numba_cpu,
jax_cpu and jax_gpu (A100), each dense and sparse — run the identical chain at
seeds 0 and 1. The question is whether they land on the same answer: does
`mass_total[1]` reach the same posterior (log-evidence, medians, widths on the
Einstein radius, slope and shear) whichever backend computed the likelihood and
whichever inversion path was used, and what does each leg cost in wall-clock and
evaluations per stage? Agreement makes the backend a column of one table, as the
repo's AGENTS.md demands; a leg outside the bands is a bug in that leg's run, and
the ruling says which.

Secondary, recorded per stage but not part of the witness: compile_s on the JAX
legs, wall_s per stage per backend (these become the first measured rates for the
pixelized stages, replacing the containment `--time` limits), and whether the
~22 GB jax_cpu sparse footprint seen at source_pix[1] on the laptop holds on RAL.

## Witness

All six legs of the 5-stage HST SLaM chain — {numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}, seeds 0 and 1 each — complete on RAL via the six `hpc/batch_{gpu,cpu}/submit_slam_hst_*` array submits: every stage of every leg carries `.completed` and `resumed: false`, every pixelized stage (source_pix[1], source_pix[2], light[1], mass_total[1]) carries `positions.info`, each leg writes `results/slam/imaging/hst/<config_name>/stages_seed<n>.json` with five stage rows and reject-inclusive `likelihood_evals`, `build_readme.py --check` renders the six-column parity view, and at the same seed the mass_total[1] posteriors agree across all six legs within 2 nats of log-evidence, 0.2σ on every median, and a σ-ratio inside [0.8, 1.25] on einstein_radius, slope and shear_magnitude; any leg outside those bands is the finding, not a rerun.

## Where to look

- `/home/jammy/Code/PyAutoLabs/autolens_inference/results/slam/imaging/hst/` — one `stages_seed<n>.json` + PNG per leg after `hpc/sync pull`; the parity view lands in the root `README.md` via `build_readme.py`
- `/mnt/ral/jnightin/autolens_inference/output/slam/imaging/hst/<config_name>/seed_<n>/` — the kept run trees (`hpc_mode: false`); ~150 MB per leg per seed, ~1.8 GB total
- `/home/jammy/Code/PyAutoLabs/autolens_inference/hpc/batch_gpu/submit_slam_hst_jax_gpu_{dense,sparse}` and `hpc/batch_cpu/submit_slam_hst_{jax_cpu,numba_cpu}_{dense,sparse}` — the six array submits (`--array=0-1` = seeds); all carry `source: unmeasured` containment limits (12 h A100, 5 days `ral`)
- `/home/jammy/Code/PyAutoLabs/autolens_inference/wiki/project/state.md` — the project ledger; the phase-3 journal entry records the laptop OOM figures and the decisions the chain departs from the workspace on
- https://github.com/PyAutoLabs/autolens_inference/pull/3 — the driver; RAL job 342695 is the still-pending A100 `source_lp` rate probe (not part of this task's runs)
- Pre-flight before submitting: RAL clone on `main` with #3 merged and `HPCPullPyAuto` run so the library mains match the laptop (2026.8.17.1 at filing); submit the two GPU legs first (the `gpu` node is shared with the human's own 12-h jobs), then the four `ral` CPU legs (8 cores, 64 GB); pull with `hpc/sync pull`, then `cortex.py move … --run <jobid> --partition {gpu,cpu}` per submit

## Runs

## Ruling

(none)
