# Euclid_dr1_prelim — DR1 prelim science run — 10 real Euclid lenses in euclid_dr1_prelim on RAL

Project: euclid_dr1_prelim
Summary: Ten real DR1 lenses fitted from the pipeline repo alone
State: accepted
Gates: euclid_strong_lens_modeling_pipeline#48, euclid_strong_lens_modeling_pipeline#49
Witness: 10 lenses fitted end to end on RAL from the pipeline repo alone, with a complete catalogue folder (latents present) whose numerics match the 20260623 reference within the tolerance stated before the run
Budget: 48:00
Runs: 342301, 342314
Ruling: R-20260910-03
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
- Gates `euclid/resimulate_fitted_lens_simulator` (the resimulations need these
  results as their truth inputs).

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
- re-homed from `tasks/euclid/` on 2026-09-07 — the `euclid` row went dormant, superseded by
  `euclid_dr1_prelim`, which this phase births

## Notes

- 2026-09-05 — **`vis_pix` magnification column.** The archived `initial_lens_model/vis_pix`
  results (and the 20260623 reference this witness compares against) carry
  `magnification = 0.0` as a sentinel: the library latent was 0/0 for any pixelized source
  (PyAutoLens#726). PyAutoLens PR #727 (merged) and #728 (correction: per-data-pixel
  convention) fix it; euclid PR #51 adds the test. Until the reference is re-derived under
  the fixed library, the numerics witness must exclude the `vis_pix` magnification column,
  and any comparison of it is against a sentinel, not a measurement. Mind ledger:
  `PyAutoMind/draft/feature/euclid/euclid_dr1_prep_epic.md` item 8.

- 2026-09-07 — launched: sort key `sorted()` (plain Python, byte-wise ascending) over the
  directory names under `/mnt/c/Users/Jammy/Science/euclid/dataset/dr1_prelim_grade_ab/`
  (3097 entries, all directories), first 10 taken; datasets:
  `Tile102005065RA0135279431487DECNEG0701599765928`,
  `Tile102007299RA0702283866574DECNEG0660415308762`,
  `Tile102007899RA0631694872236DECNEG0650584220817`,
  `Tile102007903RA0668831429074DECNEG0648901814905`,
  `Tile102008165RA0109664211519DECNEG0642902327064`,
  `Tile102008219RA0727851454839DECNEG0644382776514`,
  `Tile102008468RA3567390985250DECNEG0647172046261`,
  `Tile102008475RA0039777627054DECNEG0637715426503`,
  `Tile102008532RA0683495100072DECNEG0642073858939`,
  `Tile102008848RA0601376380877DECNEG0634605061157`;
  jobs 342301_[0-9]; project born at `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`,
  RAL `/mnt/ral/jnightin/euclid_dr1_prelim`. Born by cloning
  `euclid_strong_lens_modeling_pipeline` (`dbdbe1d`) and nothing else; the only local
  adaptations are `hpc/sync.conf` and the project's own copy of
  `hpc/batch_cpu/submit_initial_lens_model_two_stage` (sample, the 10-entry `datasets`
  list, `--array=0-9`, `--partition=ral`, the mail address, and `PROJECT_PATH` /
  `PYAUTO_HPC_BASE` exported in-script because `hpc/sync submit` carries none). `config/`
  is exactly as committed — the configuration the 2026-09-03 RAL acceptance run used.

- 2026-09-07 — **task 3 resubmitted; the other nine run on under the pre-fix code.**
  `342301_3` (`Tile102007903RA0668831429074DECNEG0648901814905`) died at 03:52 when the first
  quick update built the max-likelihood instance from a source MGE `ell_comps` of magnitude
  1.009 — outside the unit disk, so `ModelParameterException`. Two merged fixes answer it:
  PyAutoFit `f6a991504` (PR #1568) makes the quick update tolerate an invalid instance, and
  pipeline `d78468b` (PR #53) bounds the source MGE `ell_comps` to [-0.7, 0.7] per component
  so the corner of the unit box is unreachable. Only PyAutoFit was pulled on RAL
  (`cdda28b5f` → `f6a991504`); PyAutoArray `e36a5af4`, PyAutoGalaxy `6d216c15`, PyAutoLens
  `146a3d725` and PyAutoNerves `fc9c474` were deliberately left alone so the nine live tasks'
  `vis_pix` stage — a fresh interpreter — picks up no unrelated library change mid-run. The
  nine were 1:20 in and were not cancelled, so this phase's evidence is provenance-split:
  `342301_[0-9]` minus task 3 under the pre-fix code, `342314_3` under the fix. That
  PyAutoFit fast-forward also carried two unrelated commits (`86cc1e182` deferring
  `scipy.special`, `e27eb8cbb` a recursion-walk skip), which the nine tasks' `vis_pix`
  interpreters will therefore also see.

## Runs

- 342301_[0,2,4-6,9]: done — ral — submitted 2026-09-07 — wall 6:54 — six of the ten tiles finished both stages (vis_lp JAX on CPU then vis_pix numba+pool) under the pre-fix code; walls 5:35, 6:54, 4:52, 6:50, 5:12, 5:23; sort key and dataset list in ## Notes
    pulled_to: /mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output_v1/dr1_prelim_grade_ab
- 342301_[1,7-8]: failed — ral — submitted 2026-09-07 — wall 1:59 — vis_lp finished, then the vis_pix stage aborted with "Run the light-profile stage first": the vis_lp result identifier changed when PyAutoFit was pulled on RAL mid-run; walls 1:39, 1:59, 1:56
- 342301_3: failed — ral — submitted 2026-09-07 — wall 0:02 — died at the first quick update on a source MGE ell_comps magnitude 1.009 (ModelParameterException), see ## Notes; resubmitted alone as 342314_3
- 342314_3: done — ral — submitted 2026-09-07 — wall 7:28 — task 3 (Tile102007903RA0668831429074DECNEG0648901814905) resubmitted under the ell_comps fix — PyAutoFit f6a991504 (#1568) + pipeline d78468b (#53); both stages finished (the other nine 342301 tasks ran on under the pre-fix code: RAL PyAutoFit was cdda28b5f; PyAutoArray e36a5af4 / PyAutoGalaxy 6d216c15 / PyAutoLens 146a3d725 / PyAutoNerves fc9c474 left untouched)
    pulled_to: /mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output_v1/dr1_prelim_grade_ab

## Ruling

R-20260910-03 — accept
