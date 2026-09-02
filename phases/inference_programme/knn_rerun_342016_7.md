# Inference_programme — phase 3: knn reference re-run after the AdaptSplitPower stack boundary

Project: inference_programme
Phase: 3
State: dropped
Gates:
Witness: the re-run knn reference row replaces the withdrawn one and its logL deficit against the Prodigy arm bar is measured rather than inferred from a stale row
Budget: 6:00
Runs: 342016
Ruling: R-20260831-03
Lane: local-dev
Review-minutes: 15
Epic: jax-inference-profiling
Filed: 2026-08-30
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md

## Question

The `knn` reference row was withdrawn as a bar on 2026-08-29 (its 480-nat deficit is the
overflow pathology at lower amplitude) and queued to re-run under the capped
`al.reg.AdaptSplitPower` target. Does the re-run close the deficit, or is the knn cell
genuinely underperforming?

Hand-dispatched 2026-08-29 night, pre-framework; carried into the 2026-08-31-am packet.
A mesh cell, so the quarantine put it in `output/legacy_wrong/`.

## Witness

A fresh knn `hpc_a100_fp64_ref` result row on the current stack, comparable with the Prodigy
arm bar (30,557.03) — replacing the withdrawn one rather than being read beside it.

## Where to look

- `inference_programme` (project row): `output/legacy_wrong/searches/nautilus/imaging/knn/hst/hpc_a100_fp64_ref/39b5ccc228ad4b4389b1129a7e5cf605`
- `logs/output/output.342016_7.out` on the mirror
- `PyAutoMind/batches/reviews/2026-08-31-am.md` — the human's note on this member

## Runs

- 342016_7: legacy_wrong — gpu — submitted 2026-08-30 — wall 0:58 — pre-Cortex run, migrated
    where: output/legacy_wrong/searches/nautilus/imaging/knn/hst/hpc_a100_fp64_ref/39b5ccc228ad4b4389b1129a7e5cf605

## Ruling

R-20260831-03 — drop
