# Inference_programme — phase 8: the retro-adopted mge_fp64 InferenceRefs_v1 baseline

Project: inference_programme
Phase: 8
State: accepted
Gates:
Witness: the retro-adopted mge_fp64 baseline still stands under the redo standard — no fresh `_ref` run is needed for the InferenceRefs_v1 mge_fp64 row
Budget: 6:00
Runs: 339070
Ruling: R-20260901-02
Review-minutes: 4
Epic: jax-inference-profiling
Filed: 2026-08-24
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-09-01 — Batch 2026-08-31-pm review rulings (InferenceRefs_v1 legacy-reuse members)

## Question

`results/baselines/InferenceRefs_v1/mge_fp64/` was adopted **retroactively**
(`certified_by: "retro"`, 2026-08-24) from an existing Nautilus run rather than a fresh
long-run re-fit. Does that adoption still stand under the redo standard, or does the rewound
programme owe the row a fresh `_ref` run?

The run behind the row is RAL job **339070** (24 Aug 2026). Identified, not assumed: the
baseline's `reference.json` names `source_artifact:
results/searches/nautilus/imaging/mge/hst/hpc_hpc_a100_fp64.json`, and exactly one job log on
the mirror writes that file — `logs/output/output.339070.out` ("Results JSON saved to: …
hpc_hpc_a100_fp64.json"), whose `Total wall: 775.11 s` matches the baseline's
`total_wall_s: 775.11` and `sampler_wall_s: 706.50`.

## Witness

The adopted row reproduces the Nautilus MGE truth bar the programme used throughout Phases
0–3: `max_log_likelihood = 31786.63`, `log_evidence = 31690.50`, `likelihood_evals = 62208`,
version `2026.8.17.1`, `af.Nautilus` n_live=200 / n_batch=64.

A future Phase-1 refresh should still run at ≥ 2× this row's `n_live` for a tighter reference
posterior (`SUBMIT_LIST.md`).

## Where to look

- `autolens_profiling/results/baselines/InferenceRefs_v1/mge_fp64/{README.md,reference.json,target.json}`
- `inference_programme` (project row): `output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8`
- `logs/output/output.339070.out` on the mirror — the log that wrote the source artifact

## Runs

- 339070: legacy — gpu — submitted 2026-08-24 — wall 0:12 — pre-Cortex run, migrated
    where: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8

## Ruling

R-20260901-02 — accept
