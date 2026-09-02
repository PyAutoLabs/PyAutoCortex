# Subhalo_validation — phase 4: rectangular_adapt on pl_sersic_0 — the RectangularBilinear comparison

Project: subhalo_validation
Phase: 4
State: running
Gates:
Witness: evidence_increase < 5 in results/rectangular_adapt/pl_sersic_0_no_subhalo.json (test_mode false)
Budget: 48:00
Runs: 342094, 342095, 342237, 342240
Ruling: R-20260902-06
Lane: local-dev
Review-minutes: 15
Epic:
Filed: 2026-08-31
Migrated-from: PyAutoMind/active/follow_up_wave_adapt_split_and_rectangular.md

## Question

The mesh/regularization comparison the am review asked for: does `RectangularBilinear` (recipe
`rectangular_adapt`) behave like `delaunay_adapt_split` on the lens that already gave a clean
null, `pl_sersic_0`?

Run as the mandatory two-job split — job A (`342094_0`) refits `source_lp[1]` under JAX in the
rectangular tree, job B (`342095_0`) runs the numba chain `afterok`. It is the first run with
`subhalo[2]` gated off behind `--subhalo_refine`, so its witness comes from the `subhalo[1]`
grid rather than a refine and is **not** like-for-like with the three delaunay rows.

The second `rectangular_adapt` lens stays PARKED: which `pl_eff` (if either) goes next is a
human decision that follows the rulings on phases 2 and 3.

Three simulated HST-like lenses (0.05" pixels, 301×301, PSF sigma 0.05", 300 s), identical
`PowerLaw` + shear mass and bulge+disk lens light, differing only in the source. The pipeline is
the full SLaM chain (source_lp → source_pix → light → mass → subhalo grid search), source mesh
at 1250 pixels, subhalo grid 3.0" across 2 steps per axis, then a single-plane refine.

Every dataset contains **no** subhalo, so a large `evidence_increase` is a false positive;
≳ 5 is conventionally a detection.

## Witness

`evidence_increase < 5` in `results/rectangular_adapt/pl_sersic_0_no_subhalo.json`, with
`test_mode: false`.

Landed 2026-09-01 12:54 local (17:54 BST): **+0.2538** (logL +4.1732, M200 2.360e10 M⊙ at
(1.5843, −0.0448)"), `subhalo_stage: subhalo[1]_[search_lens_plane]` — the first grid-derived
witness in the project. Under the < 5 null.

Its results JSON is deliberately **untracked** in git (the human's ruling), so it lives only on
the laptop at `results/rectangular_adapt/pl_sersic_0_no_subhalo.json`.

Indicative only, not a like-for-like comparison: `source_pix[2]` confirms
`RectangularBilinearAdaptImage` 32×32 + Adapt (N=3) at evidence 21,418.501 against the delaunay
column's 21,386.823 — different mesh size and free-parameter count.

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/`
- `output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/source_lp[1]/3e9ced20d8180a15d972b1874636c5c1` — job A
- `results/rectangular_adapt/pl_sersic_0_no_subhalo.json` — the witness (untracked; laptop only)
- `wiki/project/2026-08-31-adapt-split-fix-and-rectangular.md`, `wiki/project/results_summary.md`

## Runs

- 342094_0: legacy — ral — submitted 2026-08-31 — wall 1:44 — pre-Cortex run, migrated; job A, JAX source_lp[1] under the rectangular tree (4c / 32gb / 12 h) — COMPLETED 0:0 in 01:44:40, ended 23:52:17 BST
    where: output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/
    pulled_to: output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/
- 342095_0: legacy — ral — submitted 2026-08-31 — wall 18:01 — pre-Cortex run, migrated; job B, the numba chain (8c / 96gb / 48 h) with subhalo[2] off — witness landed 2026-09-01 12:54 local (17:54 BST)
    where: output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/
    after: 342094_0
    pulled_to: output/subhalo/detect/rectangular_adapt/pl_sersic_0_no_subhalo/
- 342237_0: submitted — ral — submitted 2026-09-02 — wall 0:00 — job A, source_lp[1] on JAX; rerun with the S/N-3 adapt-image cap and fixed over-sampling (R-20260902-04..07)
- 342240_0: submitted — ral — submitted 2026-09-02 — wall 0:00 — job B, the full chain from source_pix[1]; reloads job A
    after: 342237_0

## Ruling

R-20260902-03 — accept
R-20260902-06 — rerun (supersedes R-20260902-03)
