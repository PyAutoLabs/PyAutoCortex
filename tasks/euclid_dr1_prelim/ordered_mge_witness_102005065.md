# Euclid_dr1_prelim — Ordered lens-light MGE witness on tile 102005065

Project: euclid_dr1_prelim
Summary: Does ordering the MGE bases fix labelling on one tile
State: running
Gates: PyAutoFit#1586,PyAutoGalaxy#611,euclid_strong_lens_modeling_pipeline#58
Witness: Two independent unseeded vis_lp runs of the ordered model (mge_model_from order_bases=True, ell_comps_limit=0.5; pipeline#58) on tile 102005065, each in its own PYAUTO_OUTPUT_DIR, give set-A and set-B ell_comps that agree run-to-run to within 0.05 per component with no A<->B swap; log evidence within 1.0 of the unordered phase-4 vis_lp run of this tile (342301_0); per-set ell_comps marginal widths narrower than the unordered run's (the two-mode mixture collapses); wall time per run reported against 342301_0's 5:35 for the speed comparison.
Budget: 8:00
Runs: 342375
Ruling:
Review-minutes: 10
Epic:
Filed: 2026-09-08

## Question

The vis_lp lens light is two identical 20-Gaussian MGE bases with iid ell_comps priors and a
shared centre, so swapping the bases' ell_comps is an exact label symmetry and unseeded Nautilus
runs land on either labelling at random: 6 of 8 well-determined DR1 tiles swapped set A<->B
between jobs 306843 and 342301 (euclid_strong_lens_modeling_pipeline#54,
`docs/mge_label_degeneracy.md`). The fix chain is PyAutoFit#1583 (assertions enforceable on the
JAX path) + PyAutoFit#1586 (assertions enter the identifier) + PyAutoGalaxy#611
(`mge_model_from(order_bases=True)`, key `ell_comps_1`) + pipeline#58 (the pipeline turns it on).

Does the ordering fix the labelling on a real tile? Tile 102005065 is the cleanest phase-4 case:
its two sets sit at (0.007, -0.500) and (-0.023, 0.497), separated by 1.0 in `ell_comps_1`, so
the key cannot be blind here. Two independent unseeded runs, each in its own output root (an
unseeded ordered model is identical in both, so one root would make the second run resume the
first), are the test: agreement set by set is the ordering at work, not a seed.

Launch line (human's ask), from the science clone: `hpc/sync push --no-data`, then
`hpc/sync submit cpu submit_ordered_witness_vis_lp` (array 0-1, ral partition, 8 CPUs, 12 h
cap; writes `output_ordered_witness/run_<i>/`), then `cortex.py move <task> submitted --run <id>`.
Prerequisite on RAL: the shared PyAuto stack's PyAutoFit and PyAutoGalaxy mains pulled past the
three merged PRs.

## Witness

Two independent unseeded vis_lp runs of the ordered model (mge_model_from order_bases=True, ell_comps_limit=0.5; pipeline#58) on tile 102005065, each in its own PYAUTO_OUTPUT_DIR, give set-A and set-B ell_comps that agree run-to-run to within 0.05 per component with no A<->B swap; log evidence within 1.0 of the unordered phase-4 vis_lp run of this tile (342301_0); per-set ell_comps marginal widths narrower than the unordered run's (the two-mode mixture collapses); wall time per run reported against 342301_0's 5:35 for the speed comparison.

## Where to look

- `euclid_dr1_prelim` (project row): `output_ordered_witness/run_0/dr1_prelim_grade_ab/Tile102005065.../initial_lens_model/vis_lp/<id>/` and `run_1/...` (search.summary, model.results, samples)
- unordered baseline: `output/dr1_prelim_grade_ab/Tile102005065.../initial_lens_model/vis_lp/c8638aa7ec72dd3086b1c474c1979246/` (job 342301_0, wall 5:35)
- `hpc/batch_cpu/submit_ordered_witness_vis_lp` in the science clone (local, uncommitted like its two-stage sibling)
- `euclid_strong_lens_modeling_pipeline/docs/mge_label_degeneracy.md` section 7 (the ten-tile table and the key argument)

## Runs

- 342375_[0-1]: submitted — ral — submitted 2026-09-08 — wall 0:00 — two independent unseeded runs, own output roots output_ordered_witness/run_0,1; RAL PyAutoFit 84512bffa, PyAutoGalaxy 99cf7429, science clone 152d086

## Ruling

(none)
