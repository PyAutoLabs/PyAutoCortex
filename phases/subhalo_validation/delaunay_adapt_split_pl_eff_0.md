# Subhalo_validation — phase 2: delaunay_adapt_split on pl_eff_0 — the clumpy-source lens

Project: subhalo_validation
Phase: 2
State: awaiting-ruling
Gates:
Witness: evidence_increase < 5 in results/delaunay_adapt_split/pl_eff_0_no_subhalo.json (test_mode false)
Budget: 48:00
Runs: 342027
Ruling: R-20260831-07
Lane: local-dev
Review-minutes: 8
Epic:
Filed: 2026-08-29
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md

## Question

Does `delaunay_adapt_split` report a false subhalo detection on `pl_eff_0` — six
`ElsonFreeFall` clumps inside the tangential caustic, quadruply imaged, and no subhalo?

Three simulated HST-like lenses (0.05" pixels, 301×301, PSF sigma 0.05", 300 s), identical
`PowerLaw` + shear mass and bulge+disk lens light, differing only in the source. The pipeline is
the full SLaM chain (source_lp → source_pix → light → mass → subhalo grid search), source mesh
at 1250 pixels, subhalo grid 3.0" across 2 steps per axis, then a single-plane refine.

Every dataset contains **no** subhalo, so a large `evidence_increase` is a false positive;
≳ 5 is conventionally a detection.

## Witness

`evidence_increase < 5` in `results/delaunay_adapt_split/pl_eff_0_no_subhalo.json`, with
`test_mode: false`.

Landed 2026-08-31 19:04 local (2026-09-01 00:04 BST): **−0.2425** (logL +0.6093, M200 1.213e8
M⊙ at (−1.3016, −2.5132)"). Under the < 5 null. The witness came from `subhalo[2]` and
predates the `subhalo_stage` key.

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/delaunay_adapt_split/pl_eff_0_no_subhalo/`
- `results/delaunay_adapt_split/pl_eff_0_no_subhalo.json` — the witness
- `wiki/project/results_summary.md`, `wiki/project/state.md`

## Runs

- 342027_1: legacy — ral — submitted 2026-08-29 — wall 45:10 — pre-Cortex run, migrated; COMPLETED 0:0 in 1-21:10:24, ended 00:04:55 BST 2026-09-01 — inside the 2-day wall after all; witness predates the subhalo_stage key
    where: output/subhalo/detect/delaunay_adapt_split/pl_eff_0_no_subhalo/
    pulled_to: output/subhalo/detect/delaunay_adapt_split/pl_eff_0_no_subhalo/

## Ruling

R-20260831-07 — leave-to-finish
