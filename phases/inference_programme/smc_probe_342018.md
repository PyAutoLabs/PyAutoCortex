# Inference_programme — phase 2: SMC probe on MGE — warm-start MALA, warm-start HMC, cold MALA

Project: inference_programme
Phase: 2
State: dropped
Gates:
Witness: the SMC arm's warm-start MALA/HMC rows on MGE reach the Nautilus logZ bar and the acceptance rates are ingestable as a PROGRAMME Phase-7 readout
Budget: 6:00
Runs: 342018
Ruling: R-20260831-02
Review-minutes: 25
Epic: jax-inference-profiling
Filed: 2026-08-30
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md

## Question

Does the `af.SMC` arm — warm-start MALA, warm-start HMC and cold MALA at n=256 on the MGE
cell — reach the Nautilus bar, and are its acceptance rates worth ingesting as a PROGRAMME
Phase-7 readout?

Hand-dispatched on 2026-08-29 night, before the batch framework shipped; carried into the
2026-08-31-am packet as a review member. The runs are MGE, so the quarantine put them in
`output/legacy/` (reusable) rather than `output/legacy_wrong/`.

## Witness

The three SMC rows write result JSONs under `output/legacy/searches/smc/imaging/mge/hst/`
with acceptance rates and logZ readable against the Nautilus MGE truth bar.

Ruled before the readout was ingested: the rewound epic takes precedence, so no rates were
ingested and no ledger write was made.

## Where to look

- `inference_programme` (project row): `output/legacy/searches/smc/imaging/mge/hst/`
- `logs/output/output.342018_{0,1,2}.out` on the mirror
- `PyAutoMind/batches/reviews/2026-08-31-am.md` — the human's note on this member

## Runs

- 342018_0: legacy — gpu — submitted 2026-08-30 — wall 0:10 — pre-Cortex run, migrated
    where: output/legacy/searches/smc/imaging/mge/hst/n256_mala_m5_seed0_warmebe2e28d_massprior_scaled/hpc_a100_fp64_n256_mala_warm/7fe1b8d8baee5edc4a5c485a8d48b45b
- 342018_1: legacy — gpu — submitted 2026-08-30 — wall 0:12 — pre-Cortex run, migrated
    where: output/legacy/searches/smc/imaging/mge/hst/n256_hmc_m5_i8_seed0_warmebe2e28d_massprior_scaled/hpc_a100_fp64_n256_hmc_warm/3b4ab5e2d6ff3b453680eee171bb6f4b
- 342018_2: legacy — gpu — submitted 2026-08-30 — wall 0:31 — pre-Cortex run, migrated
    where: output/legacy/searches/smc/imaging/mge/hst/n256_mala_m5_seed0_cold/hpc_a100_fp64_n256_mala_cold/1e3dea2f7a4d385eac93f5bbc80de7cf

## Ruling

R-20260831-02 — drop
