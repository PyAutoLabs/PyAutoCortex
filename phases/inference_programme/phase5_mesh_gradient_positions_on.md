# Inference_programme — phase 16: Phase 5 — mesh global gradient searches with PositionsLH at factor 1e5 (the first mesh science since the rewind)

Project: inference_programme
Phase: 16
State: planned
Gates:
Witness: every arm delivers on its own artefacts — positions.info present in the run dir; .err free of Tracebacks; .out ends "Finished." with a .completed marker and zero "Fit Already Completed"; result row carries version 2026.8.17.1 and a target_id that recomputes from _targets.py; no overflow signature (no finite log_l above the 1e20 Fitness ceiling, no shell_log_l blow-up). Scoring: a cell's arm HITS when at least one lane's best point lands within 2 nats (the Phase-1 tolerance) of that cell's positions-on Nautilus reference maxLL — delaunay_pos 31,338.43, delaunay_nn_pos 31,351.39, slam_source_pix_pos 31,547.24, slam_source_pix_nn_pos 31,405.63, and pixelization_pos / knn_pos / delaunay_matern_pos at whatever phase 12 (RAL 342241) is ruled to; a lane best point with |e| >= 1 is non-physical and is never counted as a hit. Control: the one-cell Nautilus tauto0.2 f1e5 arm reproduces that cell's f1e8 reference logZ to within 0.1 nats (positions inert on the posterior at 1e5 as well as at 1e8). No legacy_wrong number is a bar.
Budget: 8:00
Runs:
Ruling:
Lane: local-dev
Review-minutes: 25
Epic: jax-inference-profiling
Filed: 2026-09-02

## Question

Programme Phase 5 (`PROGRAMME.md` "Phase 5 — Pixelized / mesh global searches with
PositionsLH"), restated under the redo and under the design note of
[R-20260902-10](../../rulings/2026/09/R-20260902-10.md):

**With `PositionsLH` on at factor `1e5` / threshold `auto` (the `pos_tauto0.2_f1e5` arm), does
`MultiStartProdigy(n=256, prior_box, autoconv)` — the Gate B pt 1 config — reach the physical
basin on the mesh cells, at what hit rate across seeds, and at what wall against those cells'
positions-on Nautilus reference rows?** This is the first mesh science since the 2026-08-31
REWIND, and Phase 5's own first check is whether MGE's `1e5` transfers to a mesh likelihood
scale at all — R-20260902-10 says that is unmeasured.

**The engine split, stated so it is not re-derived.** The reference rows are Nautilus at
`pos_tauto0.2_f1e8`, and R-20260902-10 measured Nautilus *inert* under the penalty
(Δ logZ ≤ 0.022 nats on/off across 5 seeds). The gradient arms run at `f1e5` because
R-20260902-10 rejected `f1e8` for fixed-step gradient MAP (Prodigy n=256 on MGE: `t0.3 f1e5`
5/5, `t0.3 f1e8` 2/5, `tauto0.2 f1e8` 0/4 — stiffness, not tightness). The two engines are
therefore compared *across* penalty factors, and that is sound only because **the penalty is
zero at the recovered model**: at the physical solution the traced positions sit inside the
threshold, the `PositionsLH` term contributes nothing, and the objective the gradient arm
maximises equals the objective the reference row's maxLL was read off. The comparison is a
comparison of maxLL at the solution, not of penalised objectives along the way.

**The control that makes that argument checkable on a mesh rather than on MGE.** One extra
task: Nautilus, one mesh cell, `pos_tauto0.2_f1e5`, otherwise identical to that cell's
reference row (n_live 2× fiducial, seed 0, fp64). If its logZ reproduces the cell's `f1e8`
reference logZ to within 0.1 nats, Nautilus is inert at `1e5` on a mesh too and the reference
row is usable as the bar for an `f1e5` gradient arm. If it does not, the cross-factor
comparison fails on its own terms and the phase says so rather than scoring the arms.

**The bars.** The only bars are the positions-on Nautilus reference rows — `delaunay_pos`
31,338.43, `delaunay_nn_pos` 31,351.39, `slam_source_pix_pos` 31,547.24, `slam_source_pix_nn_pos`
31,405.63 (R-20260902-01), and `pixelization_pos` / `knn_pos` / `delaunay_matern_pos` once
phase 12 (RAL 342241) is ruled. **No `legacy_wrong` number is a bar.** In particular the
Phase 8A/8B mesh arms and the 8B "Prodigy arm 30,557.03" reading are quarantined
(`output/legacy_wrong/`) and are read here only for run *design* — lane counts, batching, step
rates — never as a comparison. R-20260902-01's binding rule also applies to every arm this
phase produces: a mesh run dir without `positions.info` is unreliable and cannot be cited.

---

### Dispatch plan

**Cells.** Only cells that have *both* a `multi_start_prodigy` leaf script and a positions-on
Nautilus reference are in scope. The intersection is smaller than the programme text assumes,
and it is entirely phase-12 rows:

| cell (`model_type`) | gradient leaf script | positions-on Nautilus reference | in scope? |
|---|---|---|---|
| `pixelization` | `scripts/imaging/searches/multi_start_prodigy/pixelization.py` | `pixelization_pos_fp64` — phase 12, 342241_11, **not yet ruled** | **IN** (bar arrives with phase 12) |
| `knn` | `.../multi_start_prodigy/knn.py` | `knn_pos_fp64` — phase 12, 342241_12, **not yet ruled** | **IN** (bar arrives with phase 12) |
| `delaunay_matern` | `.../multi_start_prodigy/delaunay.py` (its `model_type` is `delaunay_matern`, **not** `delaunay`) | `delaunay_matern_pos_fp64` — phase 12, 342241_13, **not yet ruled** | **IN** (bar arrives with phase 12) |
| `delaunay_adapt_split` | `.../multi_start_prodigy/delaunay_adapt_split.py` | none — there is no `scripts/imaging/searches/nautilus/delaunay_adapt_split.py`, so the cell has no reference row of any kind | **DEFERRED** — no bar exists |
| `delaunay` (plain) | none | `delaunay_pos` 31,338.43 (ruled) | **DEFERRED** — no gradient leaf |
| `delaunay_nn` | none | `delaunay_nn_pos` 31,351.39 (ruled) | **DEFERRED** — no gradient leaf |
| `slam_source_pix` | none | `slam_source_pix_pos` 31,547.24 (ruled) | **DEFERRED** — no gradient leaf |
| `slam_source_pix_nn` | none | `slam_source_pix_nn_pos` 31,405.63 (ruled) | **DEFERRED** — no gradient leaf |

So the four *ruled* reference rows have no gradient leaf, and the three cells that have one are
waiting on phase 12. That is the whole reason this phase is `planned` and gated on phase 12
being ruled: filed today it has no bar to score against. H5.2's DelaunayNN/kernel-CDF ranking
cannot be answered at all until `delaunay_nn` (and, for the SLaM cells, `slam_source_pix*`)
gain gradient leaves — a separate dev leg, not this phase.

**Arms.**

| arm | cells | seeds | config |
|---|---|---|---|
| primary — `pos_tauto0.2_f1e5` | `pixelization`, `knn`, `delaunay_matern` | 0–4 | `MultiStartProdigy` n=256, `prior_box`, `scaler=none`, autoconv, `batch_size=4` (mandatory on pixelized cells), fp64, viz off |
| bridge — `pos_t0.3_f1e5` | `knn` only | 0–4 | as above; the *only* threshold/factor pair with a 5/5 Prodigy result on MGE (R-20260902-10), so it is the arm that carries Phase 4's evidence onto a mesh; `tauto0.2` was measured on MGE only at `f1e8`, where it was 0/4 |
| control — Nautilus `pos_tauto0.2_f1e5` | `knn` only | 0 | `nautilus`, n_live 2× fiducial (300), fp64, `--config-name hpc_a100_fp64_ref` — the reference-row recipe with the factor changed |

**Array size: 21 tasks** — 15 primary (3 cells × 5 seeds) + 5 bridge + 1 Nautilus control.
`--array=0-20`, one task per arm/seed, `--requeue` (the `_gpu_preflight.sh` MIG bounce).

**Cost, and the one number this phase must not invent.** There is **no measured step rate for
any mesh cell at 256 lanes** (`scripts/misc/wall/rates.py`): the only mesh rows are 16 lanes /
`batch_size=4` — `knn` 2.20 s/step, `delaunay_adapt_split` 4.85 s/step, `delaunay_matern`
unmeasured entirely. Holding `batch_size=4`, 16 → 256 lanes is 16× the chunks per step, so the
naive scaling is ~35 s/step on `knn` and ~29 A100-h for a 3000-step arm — past any single job.
Quoting a rate across a configuration is exactly what killed RAL 340576 (35 of 39 arms lost at
~12 % of budget), so:

- **Budget 8:00 per task** — the array's `--time`, being the slowest *measured* mesh arm
  (8B `delaunay_adapt_split`, 14,540 s = 4:02) rounded up with headroom for the unmeasured lane
  scaling. **Ceiling: 21 × 8:00 = 168 A100-h.**
- **Step 0 is a probe, not an assumption.** Before the array is sized, one short truncated arm
  per in-scope cell at the dispatch lane tier measures s/step, the row goes into
  `wall/rates.py` with its job id, and the submit's `WALL-BASIS` block cites `source: rates`
  (`wall/check_submits.py` enforces this). Autoconv early-stopping is what makes n=256 plausible
  at all — the 3000 steps are a ceiling, not a cost — and its stopping step on a mesh is
  unmeasured.
- **If the probe says n=256 does not fit 8:00,** the human's call at dispatch is a lower lane
  tier (n=64 is ~4× cheaper) with the caveat recorded that Gate B pt 1 ratified n=256 *only*,
  so a lower tier measures a different thing and cannot inherit Phase 3's reliability claim.

**What must exist first.**

1. **Phase 12 ruled.** All three in-scope cells take their bar from it; without it the witness
   has no numbers.
2. **The dev leg merged** (PyAutoMind prompt filed 2026-09-02, `autolens_profiling` target):
   verify the `multi_start_prodigy` leaves honour `SEARCHES_POSITIONS` / `_THRESHOLD` /
   `_FACTOR` through `scripts/misc/searches/_setup.py`; add
   `hpc/batch_gpu/submit_search_multi_start_prodigy_phase5_positions_array.sh` with the 21-task
   mapping above and the Nautilus control task; dry-run one task under
   `AUTOLENS_PROFILING_SMOKE=1`. **No submission** — dispatch is an act of this phase.
3. **A decision on `autoconv`.** The Gate B pt 1 config is `multi_start_prodigy_autoconv`, and
   the only leaf under that sampler is `mge.py` — there is no autoconv leaf for any mesh cell.
   Either the dev leg adds `multi_start_prodigy_autoconv/{pixelization,knn,delaunay}.py`, or the
   arms run the genuinely fixed-step `multi_start_prodigy` cell and this phase is **not** the
   Gate B1 config and must say so in its ruling. This is a human decision at dispatch, recorded
   here so it is not made silently.

## Witness

every arm delivers on its own artefacts — positions.info present in the run dir; .err free of Tracebacks; .out ends "Finished." with a .completed marker and zero "Fit Already Completed"; result row carries version 2026.8.17.1 and a target_id that recomputes from _targets.py; no overflow signature (no finite log_l above the 1e20 Fitness ceiling, no shell_log_l blow-up). Scoring: a cell's arm HITS when at least one lane's best point lands within 2 nats (the Phase-1 tolerance) of that cell's positions-on Nautilus reference maxLL — delaunay_pos 31,338.43, delaunay_nn_pos 31,351.39, slam_source_pix_pos 31,547.24, slam_source_pix_nn_pos 31,405.63, and pixelization_pos / knn_pos / delaunay_matern_pos at whatever phase 12 (RAL 342241) is ruled to; a lane best point with |e| >= 1 is non-physical and is never counted as a hit. Control: the one-cell Nautilus tauto0.2 f1e5 arm reproduces that cell's f1e8 reference logZ to within 0.1 nats (positions inert on the posterior at 1e5 as well as at 1e8). No legacy_wrong number is a bar.

## Where to look

- `inference_programme` (project row): `output/searches/multi_start_prodigy/imaging/{pixelization,knn,delaunay_matern}/hst/hpc_a100_fp64_n256_seed{0..4}_pos_tauto0.2_f1e5/` — the 15 primary run trees, each of which must carry `positions.info` (R-20260902-01)
- `output/searches/multi_start_prodigy/imaging/knn/hst/hpc_a100_fp64_n256_seed{0..4}_pos_t0.3_f1e5/` — the 5 bridge-arm run trees
- `output/searches/nautilus/imaging/knn/hst/pos_tauto0.2_f1e5/hpc_a100_fp64_ref_pos_tauto0.2_f1e5/` — the Nautilus inertness control
- `logs/output/output.<job>_{0-20}.out` and the matching `logs/error/error.<job>_{0-20}.err` on the mirror
- Result rows: `autolens_profiling/results/searches/multi_start_prodigy/imaging/<cell>/hst/hpc_hpc_a100_fp64_n256_seed<N>_pos_tauto0.2_f1e5.json` (and `_pos_t0.3_f1e5.json` for the bridge arm); the control at `results/searches/nautilus/imaging/knn/hst/hpc_hpc_a100_fp64_ref_pos_tauto0.2_f1e5.json`
- The bars: `autolens_profiling/results/baselines/InferenceRefs_v1/<key>/` plus `INDEX.json` / `INDEX.md` / `SUBMIT_LIST.md` — `pixelization_pos_fp64`, `knn_pos_fp64`, `delaunay_matern_pos_fp64` once phase 12 is ruled, and the four rows ruled by R-20260902-01
- `autolens_profiling/results/notes/inference/PROGRAMME.md` — "### Phase 5 — Pixelized / mesh global searches with PositionsLH" (the pre-registered design) and the "2026-08-31 REWIND" section
- `autolens_profiling/scripts/misc/wall/rates.py` — the step-rate rows the probe must add before the array is sized; `hpc/batch_gpu/submit_search_multi_start_prodigy_phase5_positions_array.sh` once the dev leg lands
- `PyAutoCortex/phases/inference_programme/refs_v1_positions_on_completion.md` (phase 12) — the prerequisite

## Runs

## Ruling

(none)
