# Inference_programme — phase 20: mass_pix gradient cost probe — forward vs value_and_grad on the A100, strict FD on all 7 params

Project: inference_programme
Phase: 20
State: gated
Gates: autolens_profiling#218
Witness: one A100 job on the `imaging/mass_pix/hst` cell writes a probe artifact carrying: the forward likelihood cost in ms/eval, the `value_and_grad` cost in ms/eval and their ratio; the jit compile time for each; and a strict finite-difference check of the analytic gradient on all 7 free parameters (Isothermal 5 + ExternalShear 2) that PASSES on every one of them — every FD/analytic pair agreeing to the probe's declared tolerance, no parameter skipped, no NaN or non-finite entry in either gradient; `.err` free of Tracebacks and `.out` ending "Finished."
Budget: 1:00
Runs:
Ruling:
Review-minutes: 10
Epic: gradient-slam-baseline
Filed: 2026-09-04

## Question

**Is a gradient evaluation on the `mass_pix` cell affordable on an A100, and is
the gradient correct?**

Nothing else in this epic is worth running if it is not. The only rectangular
kernel-CDF gradient cost datum that exists anywhere is a **CPU** one — the
`value_and_grad` ≈ **17× forward** anomaly of autolens_workspace_developer#117
(`searches_minimal/pix_prodigy_findings.md`) — and it has **never been
re-measured on an A100**. On the forward side the mesh likelihood already costs
**52.7 ms** against MGE's **6.09 ms**, and batching buys much less on a mesh
(vmap gain **1.6×** vs MGE's **15.8×**), so a 17× gradient would put a
multi-start gradient search out of reach before it starts.

Two things are settled here and nowhere else:

1. **The ratio.** `value_and_grad` / forward, measured on this cell. A ratio
   **≲ 4×** is sane and phase 22 is affordable. A ratio near **17×** means the
   CPU anomaly reproduces on the GPU, and that is a **library bug to file in the
   Mind before phase 22 runs**, not a cost to accept.
2. **The gradient itself.** A strict finite-difference check on all 7 free
   parameters — the same pattern as
   `autolens_workspace_test/scripts/imaging/jax_grad/pixelization.py`. A
   gradient search on an incorrect gradient measures nothing.

Compile time is recorded alongside, because on a mesh cell it is a real share of
a short run's wall.

**Ready when:** the development leg has landed —
`PyAutoMind/draft/feature/autolens_profiling/gradient_slam_mass_pix_target.md`
(the `mass_pix` target in `_setup.py` / `_targets.py`, the per-cell sampler rows,
the drivers and the probe script). That prompt was filed 2026-09-04 with its
issue opened at the same moment as this phase's gate ref —
**autolens_profiling#218** (Cortex schema decision 55: a `Gates:` line holds
GitHub refs only, so a Cortex-spawned dev prompt gets its issue at filing).
Reuse that issue in `/start_dev`; never open a second. When its PR merges,
`move` this phase to `ready`. Nothing here submits before then.

## Witness

one A100 job on the `imaging/mass_pix/hst` cell writes a probe artifact carrying: the forward likelihood cost in ms/eval, the `value_and_grad` cost in ms/eval and their ratio; the jit compile time for each; and a strict finite-difference check of the analytic gradient on all 7 free parameters (Isothermal 5 + ExternalShear 2) that PASSES on every one of them — every FD/analytic pair agreeing to the probe's declared tolerance, no parameter skipped, no NaN or non-finite entry in either gradient; `.err` free of Tracebacks and `.out` ending "Finished."

## Where to look

- `autolens_profiling/results/notes/gradient_slam/LEDGER.md` — the epic's ledger: the question, the inherited evidence and the exact `mass_pix` fixed values
- `PyAutoMind/draft/feature/autolens_profiling/gradient_slam_mass_pix_target.md` — the development leg this phase waits on
- `autolens_profiling/scripts/misc/searches/probe_mass_pix_gradient.py` — the probe script (written by the dev leg)
- `autolens_profiling/hpc/batch_gpu/` — the P1 submit script and its `WALL-BASIS` block
- `inference_programme` (project row): `output/searches/probe/imaging/mass_pix/hst/` — the probe run tree, and `logs/output/` + `logs/error/` on the mirror
- `autolens_workspace_developer#117` and `searches_minimal/pix_prodigy_findings.md` — the CPU 17× anomaly this probe re-measures
- `autolens_workspace_test/scripts/imaging/jax_grad/pixelization.py` — the FD-certification pattern

## Runs

## Ruling

(none)
