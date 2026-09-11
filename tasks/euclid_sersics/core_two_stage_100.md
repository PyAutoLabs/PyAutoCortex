# Euclid_sersics — the core two-stage run of the 100 Sersic-sample lenses

Project: euclid_sersics
Summary: Core two-stage run of the 100 sersic lenses
State: submitted
Gates:
Witness: 100/100 array tasks complete vis_lp and vis_pix within 36 h; aggregator yields 100 lens_mass rows; no task aborted
Budget: 36:00
Runs: 342696
Ruling:
Review-minutes: 25
Epic: euclid-sersics
Filed: 2026-09-11

## Question

The June `euclid` catalogue fits one `lp_linear.Sersic` per lens under `Uniform(0.8, 5.0)` with
hard limits, and the returned Sersic index **piles up against the top of the prior**: over 2983
lenses the median n is 4.80, 42 % sit above 4.9, and **nothing** sits at the lower edge. In the
unanimously-inspected subset the pile-up is *worse* (median 4.84), which is the opposite of what
a bad-fit signature does. `scripts/simulator.py` in the pipeline already names it: "Real Euclid
fits routinely return sersic_index = 5 … an artefact".

The project that settles it (`euclid_sersics`) will run **four Sersic-stage variants** —
`baseline` (today's prior), `wide_n` (n ∈ [0.5, 10]), `central_noise` (noise inflated inside the
seeing disk) and `sersic_point` (Sersic + point MGE) — on one fixed sample, to separate "the
prior is the bound" from "something biases n upward" (a too-broad model PSF or an unmodelled
nuclear point source both push n up; correct-PSF seeing pushes it *down*).

**This task is not that comparison.** It is the run every one of those variants stands on: the
**core two-stage fit of all 100 lenses**, `vis_lp` then `vis_pix`, on the route `euclid_dr1` is
already using. It produces the `vis_lp` result the variants reuse rather than re-derive, and the
`baseline` lens model the other three are read against. Its question is therefore an
*engineering* one, and it is asked first because a variant comparison built on a sample that
half-completed is worthless:

**Does the 100-lens sample run clean, end to end, on the sep1 delivery?**

D1 is resolved: **both stages run.** `vis_pix` is not skipped. The pixelized source is what makes
the lens-light Sersic honest — a variant that moves n by absorbing source flux into the lens
would be invisible on a `vis_lp`-only run.

## The sample

100 lenses, chosen by a rule written down so it cannot drift, because every variant must run on
**these exact lenses**: from `euclid`'s inspection set (2990 lenses, 1–7 human votes each, 1293
unanimous Success) — **unanimous Success, present in both `lens_sersic.csv` and `lens_mass.csv`,
sorted by `total_valid_votes` descending then `object_id` ascending, first 100**. That is 16
lenses at 7/7 votes and 84 at 6/6, median June n = 4.917, 22 of them interior (n < 4.5), min
0.859, max 4.999.

The data is the September-1 segmentation delivery, streamed out of `euclid_dr1`'s
`Segmentation.zip` into `dataset/dr1_sep1_sersics/` — 100 tile folders, 11 files each, all
verified present, two spot-checked through `util.load_vis_dataset`.

June `object_id` → sep1 tile is a **coordinate join, never a name match**: tile names were parsed
(`RA`/`DEC` as 3 integer + 10 decimal digits of degrees) and nearest-neighboured against all
15 032 sep1 names, a unique match required inside 3". **100/100 matched, 95 names identical, the
5 that moved by 0.68–0.92" (max 0.921")**. `sample/lens_map.csv` in the project is that table and
is the only legitimate join back to the June catalogue.

## Witness

100/100 array tasks complete vis_lp and vis_pix within 36 h; aggregator yields 100 lens_mass rows; no task aborted

## Where to look

- `euclid_sersics` (project row `euclid_sersics`): `output/dr1_sep1_sersics/<tile>/` once pulled
  — one subdirectory per stage per lens; the data is `dataset/dr1_sep1_sersics/` and the route is
  `hpc/batch_cpu/submit_initial_lens_model_two_stage` (array `0-99`, partition `ral`, 8 CPUs,
  64 GB, 36 h)
- `euclid_sersics` `sample/lens_map.csv` — the June `object_id` ↔ sep1 tile provenance table, and
  `sample/lenses_100_june.csv` — the June-side list with votes, θ_E, n and R_eff
- `euclid_sersics` `wiki/project/state.md` — this project's own ledger (the commentary; the
  ruling of record is the Cortex's)
- `euclid_dr1` (project row `euclid_dr1`): the same two-stage route on the same delivery, run
  342650 — the reference for what a healthy run of this script looks like
- `autolens_assistant/skills/euclid_prepare_data.md`, `euclid_setup_pipeline.md`,
  `euclid_model_lens.md`, `euclid_hpc_runs.md` — how this pipeline is driven

## Notes

- 2026-09-11 — **the project was born for this task.** `euclid_sersics` is a fresh clone of
  `euclid_strong_lens_modeling_pipeline` at **`dbbb2a5`** — deliberately the *same base commit* as
  `euclid_dr1`, plus that project's two local deltas (`activate.sh`'s `AUTOLENS_ASSISTANT` export;
  `config/visualize/general.yaml` back on the library default `colormap: autoarray`). Any
  difference between the two projects' fits is therefore the sample or the model, never the
  pipeline. The clone's `origin` is the pipeline repo and it has local commits that are never
  pushed.
- 2026-09-11 — **the submit script differs from `euclid_dr1`'s in five things and nothing else:**
  the job name, `PROJECT_PATH`, `sample=dr1_sep1_sersics`, `--array=0-99`, and the dataset list,
  which is read from the sample directory
  (`mapfile -t datasets < <(ls $PROJECT_PATH/dataset/$sample/ | grep '^Tile' | sort)`) instead of
  100 inline tile names, behind a guard that exits non-zero unless exactly 100 are found. The
  guard matters: a partial `hpc/sync push` would otherwise shift every array index and fit the
  wrong lens under each one, silently.
- 2026-09-11 — **the pipeline work the variants need does not exist yet**: a `--variant` flag in
  `scripts/sersic_lens_model.py`, a central-noise-inflation hook in `util.load_vis_dataset`, and
  an `mge_point_model_from` for the Sersic+point variant. That is a separate PR against the
  pipeline repo, and no variant can be submitted before it merges. This task is unblocked by none
  of it.

## Runs

- 342696: submitted — ral — submitted 2026-09-11 — wall 0:00

## Ruling

(none)
