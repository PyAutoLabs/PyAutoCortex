# Inference_programme — phase 5: slogdet A/B — Cholesky vs slogdet log-det on slam_source_pix_nn (overflow-flood rung 4)

Project: inference_programme
Phase: 5
State: dropped
Gates:
Witness: the Cholesky and slogdet log-det arms of the same slam_source_pix_nn cell differ (or do not) by more than the run-to-run scatter, giving a verdict on the log-det route
Budget: 6:00
Runs: 342017
Ruling: R-20260831-05
Review-minutes: 12
Epic: jax-inference-profiling
Filed: 2026-08-30
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md

## Question

Rung 4 of the overflow-flood fix wave: does swapping the regularization log-determinant from a
Cholesky factorisation to `slogdet` change the fit of the same `slam_source_pix_nn` cell by
more than run-to-run scatter — and is either arm immune to the non-PD flood?

Hand-dispatched 2026-08-29 night, pre-framework; carried into the 2026-08-31-am packet as
HEALTHY. Mesh rows, so the quarantine put them in `output/legacy_wrong/`.

## Witness

Two paired result rows, `ld_cholesky` and `ld_slogdet`, on the same cell and stack, whose
logZ / maxLL difference is readable against the arm's own scatter — enough for a written
slogdet verdict.

Ruled before the verdict was written: the rewound epic takes precedence, so no slogdet verdict
was recorded.

## Where to look

- `inference_programme` (project row): `output/legacy_wrong/searches/nautilus/imaging/slam_source_pix_nn/hst/ld_cholesky/…`
- `output/legacy_wrong/searches/nautilus/imaging/slam_source_pix_nn/hst/ld_slogdet/…`
- `logs/output/output.342017_{0,1}.out` on the mirror; RAL-only `slogdet_ab_harvest`
- `PyAutoMind/batches/reviews/2026-08-31-am.md` — the human's note on this member

## Runs

- 342017_0: legacy_wrong — gpu — submitted 2026-08-30 — wall 1:23 — pre-Cortex run, migrated
    where: output/legacy_wrong/searches/nautilus/imaging/slam_source_pix_nn/hst/ld_cholesky/hpc_a100_fp64_slogdet_ab_cholesky/ae454f54e14847ca62929c70033c11a5
- 342017_1: legacy_wrong — gpu — submitted 2026-08-30 — wall 1:14 — pre-Cortex run, migrated
    where: output/legacy_wrong/searches/nautilus/imaging/slam_source_pix_nn/hst/ld_slogdet/hpc_a100_fp64_slogdet_ab_slogdet/7eb80135de1db2112c5bb5383b32bc49

## Ruling

R-20260831-05 — drop
