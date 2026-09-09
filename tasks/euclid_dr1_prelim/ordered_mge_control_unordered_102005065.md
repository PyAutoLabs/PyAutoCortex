# Euclid_dr1_prelim — Unordered control for the ordered-MGE witness on tile 102005065

Project: euclid_dr1_prelim
Summary: Is the ordered run's 8-nat gain ordering or library drift
State: running
Gates:
Witness: One unseeded vis_lp run of tile 102005065 with order_bases=False on today's stack (PyAutoFit 84512bffa, PyAutoGalaxy 99cf7429), own output root output_ordered_witness/control_unordered: if its log evidence lands within 1.0 of the unordered phase-4 baseline 9492.74 with the wide two-mode per-set ell_comps marginals, the ordered runs' log Z 9501.04 and narrow marginals are the ordering's doing; if it lands within 1.0 of 9501.04, the gain is library drift and the ordering's contribution is the collapsed marginals only; mass ell_comps_1 (-0.010 baseline vs -0.127 ordered) reported either way.
Budget: 8:00
Runs: 342377
Ruling:
Review-minutes: 10
Epic:
Filed: 2026-09-08

## Question

The ordered-MGE witness (task `ordered_mge_witness_102005065`, runs 342375_[0-1]) did what it was
asked: the two lens-light sets came back on the same labelling in both unseeded runs, and their
per-set ell_comps marginals collapsed from the two-mode mixture the unordered fit shows. But it
also came back with log Z 9501.04 against 9492.74 for the unordered phase-4 run of the same tile
(342301_0), and the mass `ell_comps_1` moved from -0.010 to -0.127. Eight nats and a shifted mass
ellipticity are more than a relabelling should buy: removing one of two exactly equal modes halves
the prior volume the posterior occupies, which cannot raise the evidence by eight nats. The
confound is that 342301_0 ran last week, before PyAutoFit#1583/#1586 and PyAutoGalaxy#611 landed
on the shared RAL stack, so "the ordering improved the search" and "the library moved" are not
separated by the pair of runs in hand.

This control separates them by changing exactly one thing against the witness: the same tile, the
same vis_lp model, the same stack, the same unseeded Nautilus, with `order_bases=False`. It runs
from `scripts/control_unordered_vis_lp.py` in the science clone, a thin wrapper that patches
`al.model_util.mge_model_from` to force `order_bases=False` and then calls
`initial_lens_model.vis_lp_model_from` / `fit` unchanged; it asserts the composed model carries
zero gathered assertions before the search starts. Its own output root keeps it clear of the
ordered runs, whose identifier it does not share. Launch line, from the science clone:
`hpc/sync push --no-data`, then `hpc/sync submit cpu submit_control_unordered_vis_lp` (array 0-0,
ral partition, 8 CPUs, 12 h cap; writes `output_ordered_witness/control_unordered/`).

## Witness

One unseeded vis_lp run of tile 102005065 with order_bases=False on today's stack (PyAutoFit 84512bffa, PyAutoGalaxy 99cf7429), own output root output_ordered_witness/control_unordered: if its log evidence lands within 1.0 of the unordered phase-4 baseline 9492.74 with the wide two-mode per-set ell_comps marginals, the ordered runs' log Z 9501.04 and narrow marginals are the ordering's doing; if it lands within 1.0 of 9501.04, the gain is library drift and the ordering's contribution is the collapsed marginals only; mass ell_comps_1 (-0.010 baseline vs -0.127 ordered) reported either way.

## Where to look

- `euclid_dr1_prelim` (project row): `output_ordered_witness/control_unordered/dr1_prelim_grade_ab/Tile102005065RA0135279431487DECNEG0701599765928/initial_lens_model/vis_lp/<id>/` (search.summary for log Z and wall time, model.results for the two sets' ell_comps and their marginal widths, samples)
- ordered runs to compare against: `output_ordered_witness/run_0/...` and `output_ordered_witness/run_1/...` (same tile, log Z 9501.04, job 342375_[0-1])
- unordered phase-4 baseline on last week's stack: `output/dr1_prelim_grade_ab/Tile102005065RA0135279431487DECNEG0701599765928/initial_lens_model/vis_lp/c8638aa7ec72dd3086b1c474c1979246/` (job 342301_0, log Z 9492.74, wall 5:35)
- `scripts/control_unordered_vis_lp.py` and `hpc/batch_cpu/submit_control_unordered_vis_lp` in the science clone (local, uncommitted like their ordered siblings)
- `euclid_strong_lens_modeling_pipeline/docs/mge_label_degeneracy.md` section 7 (the key argument and the ten-tile table)

## Runs

- 342377_0: submitted — ral — submitted 2026-09-08 — wall 0:00 — unordered control on today's stack; own output root output_ordered_witness/control_unordered

## Ruling

(none)
