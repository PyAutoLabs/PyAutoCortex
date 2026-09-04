# Inference_programme — phase 23: likelihood-term levers on mass_pix — slogdet vs cholesky, relative jitter on reg.Adapt

Project: inference_programme
Phase: 23
State: planned
Gates:
Witness: each lever arm runs the same `mass_pix` gradient configuration as phase 22 and delivers on its own artefacts — `.completed`, `positions.info`, `.err` free of Tracebacks, `.out` ending "Finished.", a result row whose `target_id` recomputes from `_targets.py`; and each arm reports, against the phase 22 control it is paired with, the change in NaN-lane count, the change in p_hit against phase 21's `f1e5` max logL, and the change in wall — so that a lever is judged on whether it removes the failure phase 22 measured, not on whether it changes a number
Budget: 4:00
Runs:
Ruling:
Review-minutes: 20
Epic: gradient-slam-baseline
Filed: 2026-09-04

## Question

**If the gradient search fails on `mass_pix`, is it the likelihood terms?**

**This phase arms only if phase 22 shows NaN lanes or misses.** If phase 22 hits
5/5 cleanly there is nothing here to run and the phase is dropped.

Two levers, both already suspected, neither ever tested on this target:

1. **The log-determinant method.** `SEARCHES_LOG_DET_METHOD=slogdet` against
   `cholesky` on the `mass_pix` cell. Phase 8A of the retired programme found
   slogdet rescues 64–73 % of NaNs on Delaunay+AdaptSplit but failed its own
   pre-registered test, and the residual population was the genuinely singular
   λ⁴ one. This target's regularization is fixed `reg.Adapt`, not a free λ⁴
   AdaptSplit, so the failure mode may simply not be present — which is itself
   the answer. This folds **autolens_profiling#166** (make slogdet the
   PyAutoArray default), which stays open for it.
2. **Relative jitter on `reg.Adapt`.** Today only the kernel schemes carry
   `jitter_relative`; `constant.py:53` and `adapt.py` still apply the absolute
   `1e-8` lift, which is scale-dependent and therefore wrong at this target's
   `signal_scale` 0.004. If it fires, that is a **PyAutoArray task filed in the
   Mind**, not a change made here.

**Ready when:** phase 22 rules, and its ruling names a NaN or miss population for
a lever to act on. Absent that, this phase is dropped rather than run.

## Witness

each lever arm runs the same `mass_pix` gradient configuration as phase 22 and delivers on its own artefacts — `.completed`, `positions.info`, `.err` free of Tracebacks, `.out` ending "Finished.", a result row whose `target_id` recomputes from `_targets.py`; and each arm reports, against the phase 22 control it is paired with, the change in NaN-lane count, the change in p_hit against phase 21's `f1e5` max logL, and the change in wall — so that a lever is judged on whether it removes the failure phase 22 measured, not on whether it changes a number

## Where to look

- `autolens_profiling/results/notes/gradient_slam/LEDGER.md` — the phase table and the inherited rules
- phase 22 (`prodigy_mass_pix`) — the control this phase is paired against; its ruling decides whether this arms at all
- `autolens_profiling#166` — the slogdet-as-PyAutoArray-default reminder this lever folds
- `autolens_profiling/results/notes/inference/phase_08_regularization/RESULTS.md` — the retired programme's slogdet A/B, for what was already learned
- `PyAutoArray` `constant.py:53` and the `adapt.py` regularization schemes — the absolute `1e-8` lift vs `jitter_relative`
- `inference_programme` (project row): `output/searches/multi_start_prodigy_autoconv/imaging/mass_pix/hst/` — the lever arms land beside the phase 22 control
- `logs/output/` and `logs/error/` on the mirror

## Runs

## Ruling

(none)
