# Inference_programme — phase 9: the retro-adopted delaunay_fp64 InferenceRefs_v1 baseline

Project: inference_programme
Phase: 9
State: dropped
Gates:
Witness: the retro-adopted delaunay_fp64 baseline is a physical solution — checkable by inspecting the run's source-plane reconstruction for the demagnified-source signature
Budget: 6:00
Runs: 339071
Ruling: R-20260901-03
Lane: local-dev
Review-minutes: 4
Epic: jax-inference-profiling
Filed: 2026-08-24
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-09-01 — Batch 2026-08-31-pm review rulings (InferenceRefs_v1 legacy-reuse members)

## Question

The twin of phase 8: `results/baselines/InferenceRefs_v1/delaunay_fp64/` was adopted
retroactively on the same day from an existing Nautilus run. Does *that* adoption stand?

The run behind the row is RAL job **339071** (24 Aug 2026) — same identification route as
phase 8: the baseline's `source_artifact` is
`results/searches/nautilus/imaging/delaunay/hst/hpc_hpc_a100_fp64.json`, and the only mirror
log that writes it is `logs/output/output.339071.out`, whose `Total wall: 1938.52 s` matches
the baseline's `total_wall_s: 1938.52`.

Its run tree is in `output/legacy_wrong/` — it is a mesh cell, quarantined by the REWIND.

## Witness

The reconstruction is a physical source, not the demagnified-source solution the Inversion
bias produces when no positions likelihood constrains the mass model.

See <https://pyautolens.readthedocs.io/en/latest/general/demagnified_solutions.html>.

## Where to look

- `autolens_profiling/results/baselines/InferenceRefs_v1/delaunay_fp64/{README.md,reference.json,target.json}`
- `inference_programme` (project row): `output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/` — the tree the human inspected
- `logs/output/output.339071.out` on the mirror — the log that wrote the source artifact

## Runs

- 339071: legacy_wrong — gpu — submitted 2026-08-24 — wall 0:32 — pre-Cortex run, migrated
    where: output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/b29ffe390c18e070b3eaba60270cb502

## Ruling

R-20260901-03 — drop
