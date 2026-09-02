# Inference_programme — phase 7: reuse 340210_9 as the mge_pos_fp64 InferenceRefs_v1 reference

Project: inference_programme
Phase: 7
State: accepted
Gates:
Witness: the quarantined-but-reusable 340210_9 run is at the same target/config as the `mge_pos_fp64` reference and can be adopted rather than resubmitted
Budget: 6:00
Runs: 340210
Ruling: R-20260901-01
Lane: local-dev
Review-minutes: 5
Epic: jax-inference-profiling
Filed: 2026-08-25
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-09-01 — Batch 2026-08-31-pm review rulings (InferenceRefs_v1 legacy-reuse members)

## Question

The MGE reuse rule binds the redo: before submitting any MGE run, check `output/legacy/searches/`
(RAL **and** the mirror) for an existing result at the same target/config. If one is present and
has not been ruled on in a batch review packet, do not resubmit — surface it as a packet member
for a human ruling.

`340210_9` (2026-08-25) is such a run: the `mge_pos_fp64` cell, positions on at
`tauto0.2_f1e8`, fp64. Is it adopted as the InferenceRefs_v1 `mge_pos_fp64` reference, or does
the redo need a fresh `_ref` run?

It is why array task 9 was held back from the 342091 refs wave.

## Witness

The run's result row matches the `mge_pos_fp64` target/config, on a stack the redo standard
accepts — enough that adopting it costs the programme no evidence a fresh run would add.

If accepted, the laptop action is to cite it and `mv` it from `output/legacy/searches/…` back
into the active tree on RAL and on the mirror; array task 9 stays excluded from the refs array.

## Where to look

- `inference_programme` (project row): `output/legacy/searches/nautilus/imaging/mge/hst/pos_tauto0.2_f1e8/hpc_a100_fp64_ref_pos_tauto0.2_f1e8/dc42087fb0524e78fd43eced7706b365`
- `logs/output/output.340210_9.out` on the mirror
- `autolens_profiling/results/notes/inference/DECISIONS.md` — the MGE reuse rule in the 2026-08-31 REWIND entry
- autolens_profiling#201 — the Phase-1 redo leg that routed this as a ruling member

## Runs

- 340210_9: legacy — gpu — submitted 2026-08-25 — wall 0:16 — pre-Cortex run, migrated
    where: output/legacy/searches/nautilus/imaging/mge/hst/pos_tauto0.2_f1e8/hpc_a100_fp64_ref_pos_tauto0.2_f1e8/dc42087fb0524e78fd43eced7706b365
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/pos_tauto0.2_f1e8/hpc_a100_fp64_ref_pos_tauto0.2_f1e8/dc42087fb0524e78fd43eced7706b365

## Ruling

R-20260901-01 — accept
