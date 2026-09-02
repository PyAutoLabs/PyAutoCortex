# Subhalo_validation — phase 5: rectangular_adapt on pl_eff_0 — the clumpy-source lens on the RectangularBilinear comparison

Project: subhalo_validation
Phase: 5
State: submitted
Gates:
Witness: evidence_increase < 5 in results/rectangular_adapt/pl_eff_0_no_subhalo.json (test_mode false; grid-derived, subhalo_stage subhalo[1])
Budget: 48:00
Runs: 342237, 342240
Ruling:
Lane: local-dev
Review-minutes: 8
Epic:
Filed: 2026-09-02

## Question

Does `rectangular_adapt` (RectangularBilinearAdaptImage + Adapt regularization) report a
false subhalo detection on `pl_eff_0` — the clumpy-source lens — now that the source adapt image is
capped at S/N 3 and the adaptive over-sampling puts sub-size 4 only on the bright lensed
source? The RectangularBilinear comparison asked for under R-20260831-06, run under the
corrected settings of R-20260902-04..07 alongside the Delaunay reruns.

## Witness

evidence_increase < 5 in results/rectangular_adapt/pl_eff_0_no_subhalo.json (test_mode false; grid-derived, subhalo_stage subhalo[1])

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/rectangular_adapt/pl_eff_0_no_subhalo/`
- `results/rectangular_adapt/pl_eff_0_no_subhalo.json` — the witness (untracked in git by the human's ruling; laptop only)
- `wiki/project/results_summary.md`, `wiki/project/state.md`

## Runs

- 342237_1: submitted — ral — submitted 2026-09-02 — wall 0:00 — job A, source_lp[1] on JAX
- 342240_1: submitted — ral — submitted 2026-09-02 — wall 0:00 — job B, the full chain from source_pix[1]; reloads job A
    after: 342237_1

## Ruling

(none)
