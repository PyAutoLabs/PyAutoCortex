# Subhalo_validation — rectangular_adapt on pl_eff_1_outer — the outer-component lens on the RectangularBilinear comparison

Project: subhalo_validation
Summary: Does rectangular_adapt false-detect a subhalo on the outer-component lens
State: running
Gates:
Witness: evidence_increase < 5 in results/rectangular_adapt/pl_eff_1_outer_no_subhalo.json (test_mode false; grid-derived, subhalo_stage subhalo[1])
Budget: 48:00
Runs: 342237, 342240, 342311
Ruling:
Review-minutes: 8
Epic:
Filed: 2026-09-02

## Question

Does `rectangular_adapt` (RectangularBilinearAdaptImage + Adapt regularization) report a
false subhalo detection on `pl_eff_1_outer` — the outer-component lens — now that the source adapt image is
capped at S/N 3 and the adaptive over-sampling puts sub-size 4 only on the bright lensed
source? The RectangularBilinear comparison asked for under R-20260831-06, run under the
corrected settings of R-20260902-04..07 alongside the Delaunay reruns.

## Witness

evidence_increase < 5 in results/rectangular_adapt/pl_eff_1_outer_no_subhalo.json (test_mode false; grid-derived, subhalo_stage subhalo[1])

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/rectangular_adapt/pl_eff_1_outer_no_subhalo/`
- `results/rectangular_adapt/pl_eff_1_outer_no_subhalo.json` — the witness (untracked in git by the human's ruling; laptop only)
- `wiki/project/results_summary.md`, `wiki/project/state.md`

## Runs

- 342237_2: done — ral — submitted 2026-09-02 — wall 1:52 — job A, source_lp[1] on JAX
- 342240_2: void — ral — submitted 2026-09-02 — wall 0:00 — job B, cancelled 2026-09-02 while pending afterok, to wait for the numba likelihood speed-ups
    after: 342237_2
- 342311_2: submitted — ral — submitted 2026-09-07 — wall 0:00 — job B, numba chain (8c / 96gb / 48 h) at the standard 1250-pixel mesh under PIPELINE=rectangular_adapt; reloads job A 342237_2; the 09-07 ask: submit the rectangular runs too

## Ruling

(none)
