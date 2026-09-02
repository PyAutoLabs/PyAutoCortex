# Subhalo_validation — phase 3: delaunay_adapt_split on pl_eff_1_outer — the outer-component lens, plus the AdaptSplit fix rerun

Project: subhalo_validation
Phase: 3
State: running
Gates:
Witness: evidence_increase < 5 in results/delaunay_adapt_split/pl_eff_1_outer_no_subhalo.json (test_mode false)
Budget: 48:00
Runs: 342027, 342093, 342231, 342234
Ruling: R-20260902-04
Lane: local-dev
Review-minutes: 8
Epic:
Filed: 2026-08-29
Migrated-from: PyAutoMind/batches/reviews/2026-08-31-am.md; PyAutoMind/active/follow_up_wave_adapt_split_and_rectangular.md

## Question

Two questions on one lens — `pl_eff_1_outer`, which is `pl_eff_0` plus a compact component at
(0.0, −0.4) outside the tangential caustic, doubly imaged at x ≈ +1.5" / −2.3".

1. Does `delaunay_adapt_split` report a false subhalo detection on it (`342027_2`)?
2. Was the poor `pix[1]` solution the am review flagged caused by `ConstantSplit`
   regularization at `source_pix[1]`? The `_adapt_split_fix` rerun (`342093_0`) swaps it for
   `AdaptSplit` on the same lens, same mesh, same free parameters — the human inspects the
   reconstruction and decides the default recipe's `pix[1]` regularization from it. Nothing
   downstream moves until that judgement lands.

Three simulated HST-like lenses (0.05" pixels, 301×301, PSF sigma 0.05", 300 s), identical
`PowerLaw` + shear mass and bulge+disk lens light, differing only in the source. The pipeline is
the full SLaM chain (source_lp → source_pix → light → mass → subhalo grid search), source mesh
at 1250 pixels, subhalo grid 3.0" across 2 steps per axis, then a single-plane refine.

Every dataset contains **no** subhalo, so a large `evidence_increase` is a false positive;
≳ 5 is conventionally a detection.

## Witness

`evidence_increase < 5` in `results/delaunay_adapt_split/pl_eff_1_outer_no_subhalo.json`, with
`test_mode: false`.

Landed 2026-08-31 20:59 local (2026-09-01 01:59 BST): **+2.7361** (logL +15.3716, M200 8.196e8
M⊙ at (1.4117, 1.4193)"). Under the < 5 null, but the least emphatic of the three — +2.7361
against a +15.37 likelihood increase — and the largest false positive on the board so far.

The `_adapt_split_fix` rerun has no witness JSON by design (`--stop_after=source_pix_1`). Its
readout, like for like against the ConstantSplit baseline `source_pix[1]` (same lens, 600-px
Delaunay, `areas_factor` 0.5, 10 free parameters, same dataset): log evidence **18,312.473 →
19,390.673 (+1,078.20)**, maxLL **18,377.142 → 19,462.741 (+1,085.60)**; regularization goes
from a flat 1.321 to `inner_coefficient` 1.0e-4 / `outer_coefficient` 79.76 (3σ 44.3–113.6) /
`signal_scale` 0.0164. The compact source is **not** smoothed away. Caveat, recorded honestly:
the coherent ring residuals persist in *both* fits at comparable amplitude (±7.40 → ±7.95;
chi² map max 54.69 → 63.20), so the +1,078 nats come from the adaptive smoothing prior, not
from resolving the ring residuals away.

## Where to look

- `subhalo_validation` (project row): `output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo/`
- `output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo_adapt_split_fix/source_pix[1]/085f85ba6970436a1b8b115b6c9b3fbf`
- `results/delaunay_adapt_split/pl_eff_1_outer_no_subhalo.json` — the witness
- `results/figures/adapt_split_fix_{regularization,source_plane,residuals}_before_after.jpg`
- `wiki/project/2026-08-31-adapt-split-fix-and-rectangular.md`, `wiki/project/state.md`

## Runs

- 342027_2: legacy — ral — submitted 2026-08-29 — wall 47:05 — pre-Cortex run, migrated; COMPLETED 0:0 in 1-23:05:05, ended 01:59:36 BST 2026-09-01 with 55 min of wall to spare; witness predates the subhalo_stage key
    where: output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo/
    pulled_to: output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo/
- 342093_0: legacy — ral — submitted 2026-08-31 — wall 1:16 — pre-Cortex run, migrated; the source_pix[1] AdaptSplit rerun the am review asked for — recipe delaunay_adapt_split_fix, --output_suffix=_adapt_split_fix --stop_after=source_pix_1, so it writes no witness JSON by design; awaiting the human's judgement
    where: output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo_adapt_split_fix/
    pulled_to: output/subhalo/detect/delaunay_adapt_split/pl_eff_1_outer_no_subhalo_adapt_split_fix/
- 342231_2: submitted — ral — submitted 2026-09-02 — wall 0:00 — job A, source_lp[1] on JAX; rerun with the S/N-3 adapt-image cap and fixed over-sampling (R-20260902-04..07)
- 342234_2: submitted — ral — submitted 2026-09-02 — wall 0:00 — job B, the full chain from source_pix[1]; reloads job A
    after: 342231_2

## Ruling

R-20260831-08 — leave-to-finish
R-20260902-04 — rerun
