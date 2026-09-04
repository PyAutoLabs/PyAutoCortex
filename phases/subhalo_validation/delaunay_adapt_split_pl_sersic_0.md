# Subhalo_validation — phase 1: delaunay_adapt_split on pl_sersic_0 — the false-positive null

Project: subhalo_validation
Phase: 1
State: ready
Gates:
Reset: job B (342234 / 342240) cancelled 2026-09-02 after 12 min at the human's request: the chain waits for the numba likelihood speed-ups in progress; source_lp[1] (job A) is complete and kept; the partial source_pix[1] outputs were removed on RAL
Witness: evidence_increase < 5 in results/delaunay_adapt_split/pl_sersic_0_no_subhalo.json (test_mode false)
Budget: 48:00
Runs: 342027, 342231, 342234
Ruling: R-20260902-07
Review-minutes: 10
Epic:
Filed: 2026-08-29
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md

## Question

Does the `delaunay_adapt_split` SLaM chain report a false subhalo detection on `pl_sersic_0`,
a simulated lens with a single `SersicCore` source and no subhalo?

Three simulated HST-like lenses (0.05" pixels, 301×301, PSF sigma 0.05", 300 s), identical
`PowerLaw` + shear mass and bulge+disk lens light, differing only in the source. The pipeline is
the full SLaM chain (source_lp → source_pix → light → mass → subhalo grid search), source mesh
at 1250 pixels, subhalo grid 3.0" across 2 steps per axis, then a single-plane refine.

Every dataset contains **no** subhalo, so a large `evidence_increase` is a false positive;
≳ 5 is conventionally a detection.

## Witness

`evidence_increase < 5` in `results/delaunay_adapt_split/pl_sersic_0_no_subhalo.json`, with
`test_mode: false`.

Landed: **−0.3009** — a textbook null. The subhalo buys +0.9668 nats of likelihood for 3 extra
parameters and the evidence falls; the nuisance subhalo parks at (2.1457, −0.2410)", outside
the ring, M200 1.493e9 M⊙. All four subhalo[1] grid cells sit below the no-subhalo baseline
(−0.60 to −0.79) — a uniform null.

Measured stage costs (the reason subhalo[2] was later switched off): `source_lp[1]` 1 h 10 m,
`source_pix[1]` 29 min, `source_pix[2]` 10 min, `light[1]` 74 min, `mass_total[1]` 168 min,
`subhalo[1]` grid 21.2 h, `subhalo[2]` refine 8.25 h — 29.4 h of the 34 h chain.

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/delaunay_adapt_split/pl_sersic_0_no_subhalo/`
- `results/delaunay_adapt_split/pl_sersic_0_no_subhalo.json` — the witness
- `wiki/project/results_summary.md` — the scientific commentary and the provenance row

## Runs

- 342027_0: legacy — ral — submitted 2026-08-29 — wall 34:08 — pre-Cortex run, migrated; MaxRSS 27.0 GB, autolens 2026.8.17.1 + PyAutoFit 56fb8b63b (the PR #1548 pool fix); witness predates the subhalo_stage key — read it as subhalo[2]_[single_plane_refine]
    where: output/subhalo/detect/delaunay_adapt_split/pl_sersic_0_no_subhalo/
    pulled_to: output/subhalo/detect/delaunay_adapt_split/pl_sersic_0_no_subhalo/
- 342231_0: done — ral — submitted 2026-09-02 — wall 0:02 — job A, source_lp[1] on JAX; rerun with the S/N-3 adapt-image cap and fixed over-sampling (R-20260902-04..07)
- 342234_0: void — ral — submitted 2026-09-02 — wall 0:12 — job B, cancelled 2026-09-02 at 12 min inside source_pix[1] to wait for the numba likelihood speed-ups; partial source_pix[1] output removed on RAL
    after: 342231_0

## Ruling

R-20260831-06 — accept
R-20260902-07 — rerun (supersedes R-20260831-06)
