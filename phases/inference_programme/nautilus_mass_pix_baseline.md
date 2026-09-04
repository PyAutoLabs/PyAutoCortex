# Inference_programme — phase 21: the Nautilus bar on mass_pix — f1e8 (refs convention) and f1e5 (like-for-like)

Project: inference_programme
Phase: 21
State: planned
Gates:
Witness: both Nautilus arms deliver on their own artefacts — a `.completed` marker and a `positions.info` file in each run dir; `.err` free of Tracebacks; `.out` ends "Finished." with zero "Fit Already Completed"; a result row per arm carrying a `target_id` that recomputes from `_targets.py`; no overflow signature (no finite `log_l` above the Fitness ceiling); each arm physical — `einstein_radius` recovered at 1.60 ± 0.02 with `|ell_comps| < 1`; and max logL, log evidence, likelihood evals and sampler wall recorded for both arms
Budget: 4:00
Runs:
Ruling:
Review-minutes: 15
Epic: gradient-slam-baseline
Filed: 2026-09-04

## Question

**What does Nautilus achieve on the `mass_pix` cell, and what does it cost?**

This is the bar phase 22 has to beat. Two arms, both n_live 300, seed 0, fp64,
A100, the `InferenceRefs_v1` settings otherwise:

- **`pos_tauto0.2_f1e8`** — the reference convention every certified mesh
  baseline uses. Nautilus is measured inert to the factor (Δ logZ ≤ 0.022 nats,
  R-20260902-10), so this arm is comparable with the whole certified set.
- **`pos_tauto0.2_f1e5`** — the *like-for-like* arm. The gradient search in phase
  22 must run at 1e5 (Gate B pt 2: on MGE, factor 1e8 gives Prodigy 0/4 and 1e5
  gives 5/5), so without this arm the headline comparison would be
  cross-objective. Whether MGE's 1e5 transfers to a mesh likelihood scale is
  **unmeasured**; the two arms agreeing here is the first evidence either way.

The target itself is fixed by the ledger: lens light = the `Sersic` truth
instance from `dataset/imaging/hst/tracer.json`; source = `RectangularRTUAdaptImage`
`shape=(39,39)`, `weight_power` 0.001, `weight_floor` 0.248, with `reg.Adapt`
`inner_coefficient` 0.140, `outer_coefficient` 226.169, `signal_scale` 0.004 —
all instances at the certified `slam_source_pix_pos_fp64` maximum likelihood
(R-20260902-01, run identifier `4323a2ffcb3e50a71f229e46032d9e95`). Free = 7
parameters, Isothermal (5) + ExternalShear (2).

**Ready when:** phase 20 rules, and its measured cost has been written into this
phase's submit script as the `WALL-BASIS` block (the wall basis is measured on
this cell, never transferred).

## Witness

both Nautilus arms deliver on their own artefacts — a `.completed` marker and a `positions.info` file in each run dir; `.err` free of Tracebacks; `.out` ends "Finished." with zero "Fit Already Completed"; a result row per arm carrying a `target_id` that recomputes from `_targets.py`; no overflow signature (no finite `log_l` above the Fitness ceiling); each arm physical — `einstein_radius` recovered at 1.60 ± 0.02 with `|ell_comps| < 1`; and max logL, log evidence, likelihood evals and sampler wall recorded for both arms

## Where to look

- `autolens_profiling/results/notes/gradient_slam/LEDGER.md` — the `mass_pix` target definition and the provenance of every fixed value
- `autolens_profiling/scripts/imaging/searches/nautilus/mass_pix.py` — the driver (written by the dev leg)
- `autolens_profiling/hpc/batch_gpu/` — the two-arm submit script and its `WALL-BASIS` block
- `inference_programme` (project row): `output/searches/nautilus/imaging/mass_pix/hst/pos_tauto0.2_f1e8/` and `.../pos_tauto0.2_f1e5/` — the two run trees, each with `positions.info`
- `autolens_profiling/results/searches/nautilus/imaging/mass_pix/hst/` — the result rows
- `logs/output/` and `logs/error/` on the mirror
- `autolens_profiling/results/baselines/InferenceRefs_v1/pixelization_pos_fp64/` — the nearest certified neighbour (12 free parameters vs this cell's 7)

## Runs

## Ruling

(none)
