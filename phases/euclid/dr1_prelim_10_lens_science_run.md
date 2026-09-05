# Euclid — phase 4: DR1 prelim science run — 10 real Euclid lenses in euclid_dr1_prelim on RAL

Project: euclid
Phase: 4
State: ready
Gates: euclid_strong_lens_modeling_pipeline#48, euclid_strong_lens_modeling_pipeline#49
Witness: 10 lenses fitted end to end on RAL from the pipeline repo alone, with a complete catalogue folder (latents present) whose numerics match the 20260623 reference within the tolerance stated before the run
Budget: 48:00
Runs:
Ruling:
Review-minutes: 25
Epic: euclid-dr1-prep
Filed: 2026-08-28
Migrated-from: PyAutoMind/draft/research/euclid/dr1_prelim_10_lens_science_run.md

## Question

Can everything delivered for the DR1 runs out of `Science/euclid` now be delivered from
`euclid_strong_lens_modeling_pipeline` alone? A new science project at
`/mnt/c/Users/Jammy/Science/euclid_dr1_prelim` takes the first 10 lenses alphanumerically from
`/mnt/c/Users/Jammy/Science/euclid`, fits them with the two-stage CPU route on RAL (`vis_lp`
JAX → reset → `vis_pix` numba + multiprocessing, submitted from the pipeline repo's own
`hpc/batch_cpu` scripts), and produces a catalogue folder with the full latent-variable output.

This is a science run on RAL, not a software task: it is human-driven, runs on wall-clock
timescales of days, and its deliverable is a result and a written verdict. It must never be
handed to an autonomous ship gate.

The run goes through the `autolens_assistant` euclid skill family — `euclid_prepare_data`,
`euclid_setup_pipeline`, `euclid_model_lens`, `euclid_hpc_runs`. (There is no literal
`euclid_mode` in the assistant; the skills are what the request meant.)

State the sort key explicitly and list the 10 chosen datasets by name in the issue before
running, so the selection is reproducible and auditable.

## Witness

Acceptance, verbatim from the Mind prompt:

- 10 lenses fitted end to end on RAL from the pipeline repo alone.
- Catalogue folder complete, latents present, numerics approximately matching the
  20260623 reference within a stated tolerance.
- A written verdict: **can everything delivered for the DR1 runs out of
  `Science/euclid` now be delivered from `euclid_strong_lens_modeling_pipeline`?**
  Any "no" is itself a finding and should feed back into phase 1.
- Gates phase 5 (the resimulations need these results as their truth inputs).

The catalogue product set is the reference tile's: `lens_mass.csv`, `lens_sersic.csv`,
`source_sersic.csv`, `magnitudes.csv`, `model.fits`, `pre_psf.fits`, and the PNG set
(`fit_sersic.png`, `fit_multi_wavelength.png`, `rgb.png`, `segmentation.png`,
`vis_lp_fit.png`, `vis_lp_image_with_positions.png`, `vis_pix_fit.png`).

## Where to look

- `euclid_dr1_prelim` (project row `euclid_dr1_prelim`): the new project tree, once created
- `euclid` (project row `euclid`): `catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/`
  — the numerical comparison reference for the same 10 lenses
- `autolens_assistant/skills/euclid_{prepare_data,setup_pipeline,model_lens,hpc_runs}.md`
- `euclid_strong_lens_modeling_pipeline`: `catalogue/scripts/`, `hpc/batch_cpu/`

## Notes

- 2026-09-05 — **`vis_pix` magnification column.** The archived `initial_lens_model/vis_pix`
  results (and the 20260623 reference this witness compares against) carry
  `magnification = 0.0` as a sentinel: the library latent was 0/0 for any pixelized source
  (PyAutoLens#726). PyAutoLens PR #727 (merged) and #728 (correction: per-data-pixel
  convention) fix it; euclid PR #51 adds the test. Until the reference is re-derived under
  the fixed library, the numerics witness must exclude the `vis_pix` magnification column,
  and any comparison of it is against a sentinel, not a measurement. Mind ledger:
  `PyAutoMind/draft/feature/euclid/euclid_dr1_prep_epic.md` item 8.

## Runs

## Ruling

(none)
