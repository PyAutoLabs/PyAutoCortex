# Inference_programme — phase 22: MultiStartProdigy on mass_pix — does a gradient search beat Nautilus in a SLaM mass[1] shape?

Project: inference_programme
Phase: 22
State: planned
Gates:
Witness: five `MultiStartProdigy` autoconv seeds (0–4) on the `mass_pix` cell at `pos_tauto0.2_f1e5` each deliver on their own artefacts — `.completed`, `positions.info`, `.err` free of Tracebacks, `.out` ending "Finished.", a result row whose `target_id` recomputes from `_targets.py`, no overflow signature; a seed HITS when its best log-posterior lands within 2 nats of phase 21's `pos_tauto0.2_f1e5` max logL AND its best point is physical (`|ell_comps| < 1`, `einstein_radius` 1.60 ± 0.02); p_hit over the five seeds is reported with its Wilson-95 lower bound, and the per-seed wall is reported against phase 21's sampler wall on the same arm; a lane that ends NaN or pinned is counted and reported, never silently dropped
Budget: 4:00
Runs:
Ruling:
Review-minutes: 25
Epic: gradient-slam-baseline
Filed: 2026-09-04

## Question

**Dropped into a SLaM `mass[1]` search, does a gradient search beat Nautilus?**

**This is the headline ruling of the epic.** `MultiStartProdigy` autoconv,
n_starts 16, batch_size 4, n_steps ≤ 3000, `pos_tauto0.2_f1e5`, seeds 0–4, on the
same `mass_pix` cell phase 21 measured — lens light fixed to truth, mesh and
`reg.Adapt` fixed at the certified `slam_source_pix_pos` values, only mass +
shear free.

The comparison is against **phase 21's `f1e5` arm** (like for like), with the
`f1e8` arm as the tie to the certified set. Two numbers decide it: **p_hit** over
five seeds, and **wall against the Nautilus wall on the same arm**. The MGE
precedent is Prodigy n256 at 5/5 in 163–297 s against Nautilus's 939 s — 3.1–5.8×
under. Whether any of that survives a mesh likelihood is exactly what has never
been measured: **no gradient-search run exists on any rectangular mesh target,
anywhere.**

What would make this negative and still informative: lanes that NaN, lanes that
pin, or a p_hit that collapses while the wall advantage holds. All three are
counted and reported rather than absorbed, and any of them arms phase 23.

**Ready when:** phase 21 rules — its `f1e5` arm is the bar, and its own Nautilus
wall is the measured basis this phase's submit script inherits. Phase 21 is the
first science phase of the epic: phase 20, the gradient cost probe, was dropped
on 2026-09-04 (R-20260904-04) because the epic measures the number of inference
steps, not the cost of a gradient; the cost probe is now an ordinary
autolens_profiling prompt in the Mind
(`draft/feature/autolens_profiling/gradient_cost_probe.md`) and gates nothing
here.

## Witness

five `MultiStartProdigy` autoconv seeds (0–4) on the `mass_pix` cell at `pos_tauto0.2_f1e5` each deliver on their own artefacts — `.completed`, `positions.info`, `.err` free of Tracebacks, `.out` ending "Finished.", a result row whose `target_id` recomputes from `_targets.py`, no overflow signature; a seed HITS when its best log-posterior lands within 2 nats of phase 21's `pos_tauto0.2_f1e5` max logL AND its best point is physical (`|ell_comps| < 1`, `einstein_radius` 1.60 ± 0.02); p_hit over the five seeds is reported with its Wilson-95 lower bound, and the per-seed wall is reported against phase 21's sampler wall on the same arm; a lane that ends NaN or pinned is counted and reported, never silently dropped

## Where to look

- `autolens_profiling/results/notes/gradient_slam/LEDGER.md` — the question, the inherited MGE Prodigy evidence and the engine-split positions rule
- `autolens_profiling/scripts/imaging/searches/multi_start_prodigy_autoconv/mass_pix.py` — the driver (written by the dev leg)
- `autolens_profiling/scripts/misc/searches/_samplers.py` — the per-cell `imaging:mass_pix` rows (n_starts 16, batch 4, n_steps 3000)
- `autolens_profiling/hpc/batch_gpu/` — the seeds 0–4 array submit and its `WALL-BASIS` block
- `inference_programme` (project row): `output/searches/multi_start_prodigy_autoconv/imaging/mass_pix/hst/pos_tauto0.2_f1e5/` — the five run trees, each with `positions.info`
- `autolens_profiling/results/searches/multi_start_prodigy_autoconv/imaging/mass_pix/hst/` — the result rows
- `logs/output/` and `logs/error/` on the mirror
- phase 21 (`nautilus_mass_pix_baseline`) — the bar this is scored against

## Runs

## Ruling

(none)
