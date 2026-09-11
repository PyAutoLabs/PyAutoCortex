# Euclid_dr1_prelim — Ordered Nautilus rerun to catalogue parity

Project: euclid_dr1_prelim
Summary: Do ordered Nautilus reruns reproduce the euclid catalogue values?
State: awaiting-ruling
Gates: euclid_strong_lens_modeling_pipeline#60
Witness: The same ten dr1_prelim tiles are refitted on RAL with af.Nautilus through the two-stage vis_lp (n_live=750) / vis_pix (n_live=300) submit, from a science clone that has merged pipeline main so order_bases=True, hpc_mode on, quick updates off and samples.csv off are all in force, after output/ has been archived to output_v1 on both the laptop and RAL so the fresh runs write into a clean output/; all ten tiles complete, including the three that failed in 342301 (tasks 1, 7, 8); the Sersic and multi-wavelength follow-ups then run into output_sed; a catalogue built from output/ and output_sed reproduces the original euclid reference catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/ for those ten tiles, with tile identity and astrometry exact, effective Einstein radius and per-band magnitudes within combined 3 sigma, and MGE ell_comps agreeing up to a set swap; the same build then completes on RAL as it did for the original euclid project; and the fresh output/ holds no unzipped sibling directories and no samples.csv, coming in under 40% of the 130 MB zip payload the 2026-09-07 runs produced.
Budget: 36:00
Runs: 342398, 342629, 342648, 342668
Ruling:
Review-minutes: 25
Epic:
Filed: 2026-09-09

## Question

The ten DR1-prelim tiles were fitted on 2026-09-07 (SLURM 342301) before the
MGE label degeneracy was fixed, and only seven survived: tasks 1, 7 and 8
failed at exit 1 after 1h39-1h59 with their logs still unread, and task 3 died
at 3:52 on an ell_comps magnitude of 1.009 before being resubmitted alone as
342314_3. Those runs also predate the disk work: `output/` is 505 MB on RAL for
ten tiles, of which most is extracted copies beside the zips and `samples.csv`.

The ordering fix has since been validated on one tile (witness 342375_[0-1]
against control 342377_0, all COMPLETED), and the pipeline defaults it depends
on are being merged upstream. This task is the science half: run the *same ten
lenses* again, properly, and see whether the catalogue that comes out of them
matches what the original `euclid` project published.

So: with the pipeline defaults in force, do all ten tiles complete under
Nautilus on RAL, do the Sersic and multi-wavelength follow-ups then run cleanly
into `output_sed`, and does a catalogue built from the result reproduce the
original euclid values for those same ten tiles - first locally, then on RAL?

MGE ordering is expected to change the *labelling* of the two lens bases, not
the physics, so `ell_comps` is compared up to a set swap and everything else on
value. A disagreement outside that is the finding.

## Witness

The same ten dr1_prelim tiles are refitted on RAL with af.Nautilus through the two-stage vis_lp (n_live=750) / vis_pix (n_live=300) submit, from a science clone that has merged pipeline main so order_bases=True, hpc_mode on, quick updates off and samples.csv off are all in force, after output/ has been archived to output_v1 on both the laptop and RAL so the fresh runs write into a clean output/; all ten tiles complete, including the three that failed in 342301 (tasks 1, 7, 8); the Sersic and multi-wavelength follow-ups then run into output_sed; a catalogue built from output/ and output_sed reproduces the original euclid reference catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/ for those ten tiles, with tile identity and astrometry exact, effective Einstein radius and per-band magnitudes within combined 3 sigma, and MGE ell_comps agreeing up to a set swap; the same build then completes on RAL as it did for the original euclid project; and the fresh output/ holds no unzipped sibling directories and no samples.csv, coming in under 40% of the 130 MB zip payload the 2026-09-07 runs produced.

## Where to look

Project row `euclid_dr1_prelim`: laptop `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim`,
RAL `/mnt/ral/jnightin/euclid_dr1_prelim`, both clones of
`PyAutoLabs/euclid_strong_lens_modeling_pipeline`.

Pre-flight, in order - none of the run work is meaningful until these hold:

1. `euclid_strong_lens_modeling_pipeline` main carries the defaults:
   `order_bases=True` + `ell_comps_limit` on every two-basis MGE builder
   (shipped for `initial_lens_model.py` in PR #58; `full_model.py` and
   `mge_lens_only.py` in PR #61), `hpc.hpc_mode: true`,
   `hpc.iterations_per_quick_update: 1e99`, `samples: false`,
   `unzip_temporary=True` on every aggregator (PR #61).
2. The science clone has merged that main. It carries local uncommitted work
   (`hpc/batch_cpu/submit_initial_lens_model_two_stage` modified, plus
   untracked `submit_ordered_witness_vis_lp`, `submit_control_unordered_vis_lp`,
   `scripts/control_unordered_vis_lp.py`, `dataset/dr1_prelim_grade_ab/`) and
   two unpushed commits adding `AGENTS.md` and `wiki/project/`; `config/` is
   clean, so the merge is conflict-free.
3. `hpc/sync push` carries the clone to RAL, and `HPCPullPyAuto` refreshes the
   library mains there - `unzip_temporary` is merged but unreleased, so RAL must
   track PyAutoFit main.
4. `output/` is archived to `output_v1` on the laptop AND on RAL (505 MB each)
   so the reruns write into a clean `output/`. `PYAUTO_OUTPUT_DIR` stays unset
   for the reruns, so the catalogue build needs no path change.
5. The unread failure logs of 342301 tasks 1, 7 and 8 are read before
   relaunching, so the rerun does not repeat whatever killed them.

Then:

- Reruns: `hpc/batch_cpu/submit_initial_lens_model_two_stage` (partition cpu,
  8 CPU, 64 GB, 36 h, `--array=0-9`), `af.Nautilus` - `vis_lp` n_live=750 then
  `vis_pix` n_live=300 in a second interpreter. Results land in
  `output/dr1_prelim_grade_ab/<Tile>/initial_lens_model/{vis_lp,vis_pix}/`.
- SED chain: `hpc/batch_cpu/submit_sersic_waveband` (CPU default, partition ral,
  8 CPU, 64 GB, 12 h, JAX pinned to the CPU backend; `hpc/batch_gpu/submit_sersic_waveband`
  is the optional GPU route and is what 342648 ran), which exports
  `PYAUTO_OUTPUT_DIR=output_sed`; the per-band results are what
  `catalogue/scripts/multi_wavelength.py` and `magnitudes.py` read.
- Catalogue: `scripts/build_inspection_bundle.sh`, locally first, then on RAL
  (the submit script for it does not exist yet - it is phase 2 of #60).
- Reference to match: the original euclid project's
  `catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/`
  (2990 rows; all ten dr1_prelim tiles confirmed present).
- Archive of the pre-ordering runs, once moved: `output_v1/dr1_prelim_grade_ab/`
  (17 zips, 18 searches, one incomplete at
  `Tile102007903.../initial_lens_model/vis_lp/df990a0fe949bdc2888cb7fddf532e26`).
- Already-scored inputs: `ordered_mge_witness_102005065` (342375_[0-1]) and
  `ordered_mge_control_unordered_102005065` (342377_0).
- laptop bundle from the ordered runs:
  `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim/inspect/dr1_prelim_grade_ab_ordered_v2/`
  (10 tiles of PNGs, 5-row `lens_mass.csv` — see Notes 2026-09-10)

## Notes

- 2026-09-10 — **laptop-side scoring of 342398; RAL unreachable** (the SSH jump host
  refuses the key, so the SED chain, the RAL catalogue build and the RAL `output_v1`
  check did not run). All ten tiles finished both stages, task walls 6:41–13:12, `.err`
  clean. Findings: (1) `vis_lp` on 102007299 / 102007903 / 102008475 is pinned by the
  positions penalty — log Z −7.9e7 / −5.1e7 / −5.1e6, max source-plane separation
  0.99 / 0.71 / 0.25 against `positions_threshold` 0.2 — completed searches, not usable
  fits, and the same tiles that failed in 342301. (2) 15 unzipped `<hash>/` directories
  sit beside their zips (19.1 MB, RAL mtimes inside the job window: `hpc_mode` removed
  the tree and the pre-fit file set was re-emitted at the stage boundary; no
  `.completed`). A sibling directory makes
  `Aggregator.from_directory(completed_only=True)` take the directory, never open the
  zip, and drop the search silently (controlled test: 1 vs 4 search outputs) —
  `lens_mass.csv` came out with 5 of 10 rows and the bundle build aborted at stage 4.
  (3) `effective_einstein_radius` is blank on every row: the `latent.<name>` argument
  path no longer matches the unprefixed keys the latent summary merges in, a silent
  `None`. (4) Parity against `dr1_prelim_grade_ab_catalogue_csvs_20260623` on a zip-only
  rebuild: tile identity 10/10; astrometry exact 0/10; `einstein_radius` within combined
  3σ 6/10; mass `ell_comps` 3/10 and 6/10; shear 4/10 and 7/10. A three-way control on
  `samples_summary.json` medians shows the 2026-09-07 `output_v1` runs miss the June
  reference by the same or larger margins, so the disagreement is rerun scatter, not the
  ordering. (5) MGE ordering key `A_ec1 > B_ec1` holds 10/10; sets agree with
  `output_v1` up to a swap on 9/10 (clean swaps on 102005065, 102007903, 102008532);
  102008165 is undetermined (key separation 0.0125, 1σ overlap) and 102007299 marginal.
  (6) Disk: zips 61.54 MB = 47.3 % of the 130.05 MB `output_v1` zip baseline (fails the
  <40 % clause); whole tree 81 MB vs 526 MB (15.4 %); `samples.csv` 0 loose, 0 in-zip.
  (7) `output_v1` no longer loads under the installed stack
  (`autoarray/inversion/mesh/mesh/delaunay.py:97` `zeroed_pixels` array-truth error on
  the 09-07 `model.json`). Prepared, not submitted:
  `hpc/batch_gpu/submit_sersic_waveband` in the science clone (uncommitted; ten tiles,
  array 0-9, `output_sed`), with the RAL seed-copy sequence in the session report.
  Laptop bundle: `inspect/dr1_prelim_grade_ab_ordered_v2/` (stage 1 PNGs for all ten,
  5-row `lens_mass.csv`).
- 2026-09-10 (evening) — **library and pipeline fixes shipped, confirmation rerun 342629 submitted.**
  pipeline#65 fixed the `latent.<name>` prefix so `effective_einstein_radius` is no longer a silent
  `None`; PyAutoFit#1598 corrected the 3σ / `max_lh` aggregate-CSV paths; PyAutoLens#734 +
  PyAutoFit#1600 + pipeline#67 trace `LatentEuclid.variables` under the latent engine's `jax.jit` so
  `vis_lp` writes latents (12 keys on 102005065). PyAutoFit#1602 found the aggregator sibling-dir
  root cause: post-completion caches recreate `<hash>/` via `_files_path` mkdir plus a
  `preserve_in_zip` loose copy — fixed, and aggregator output order is now path-sorted.
  The 14-file laptop residue dirs were rsync-without-`--delete` mid-run pulls, not a library bug.
- 2026-09-11 — **342629 scored on the eight tiles that finished; all four 09-10 defects
  confirmed fixed; parity fails on rerun scatter, not ordering.** `sacct`: tasks 0,2,4,5,6,7,8,9
  COMPLETED (walls 5:45–9:42, MaxRSS 7.6–10.9 GB); tasks 1 (`Tile102007299…`) and 3
  (`Tile102007903…`) still RUNNING in **stage 1 `vis_lp`** at 15:52 of 36:00 — alive, not hung
  (`checkpoint.hdf5` 72.5/76.9 MB written minutes ago; first checkpoint only at 7.6 h / 9.9 h in).
  Those are two of the three positions-penalty-pinned tiles. Fixes verified: (1) every one of the
  16 zips carries `.completed` and a **12-key** `files/latent/latent_summary.json` in *both*
  stages, all finite, and no `search.log` says "latent function raised" or "no finite latent
  samples" (PyAutoLens#734 + PyAutoFit#1600); (2) `lens_mass.csv` has **0 blank cells across all
  42 columns** including the `effective_einstein_radius` family (pipeline#65); (3) **0 of 64**
  (row, quantity) cells have 3σ exactly equal to 1σ, 62/64 strictly outside (PyAutoFit#1598);
  (4) `output/` holds **0** sibling `<hash>/` directories beside a zip and **0** `samples.csv`,
  the aggregator found 16/16 searches and the bundle has **8 rows** where 09-10 got 5 of 10
  (PyAutoFit#1602). The #1602 fix was also re-run against the tree that broke it:
  `output_v2_pre_refresh`, with its 15 residue dirs, now builds a **10-row, 0-blank**
  `lens_mass.csv` while emitting 60 warnings "…has no `.completed` file but ….zip does; the zip
  was used", and writing nothing into that tree (verified byte-identical). **Parity** (reports
  under `inspect/`): vs `20260623`, tile identity 8/8 exact, coverage 100 %,
  `effective_einstein_radius` 2/8 within combined 3σ (median z 4.94, max 27.3); vs **342398, the
  same code on the same data**, 2/8 with median z **15.4**, max **41.9** — three times worse, so
  the disagreement is Nautilus rerun scatter and the pre-registered "within combined 3σ" clause
  **cannot be met by any pair of these runs and needs restating**. "Astrometry exact" is likewise
  untestable today: `lens_mass.csv` has no astrometry column, and `magnitudes.csv` needs the SED
  chain, which has never run. **MGE ordering is clean**: key `A.ell_comps_1 > B.ell_comps_1`
  holds **8/8**, and the two lens-light bases agree with 342398 as a set **8/8** (7 same order,
  1 swap on `Tile102008165…`, whose key separation 0.0130 sits below its marginal width 0.0389 —
  the undetermined case the script documents). Note the comparator applies the basis-swap
  symmetry to `lens_mass.csv`'s `ell_comps`, which are the `Isothermal` **mass** ellipticity, so
  its `ell_comps` FAIL is a scatter row, not a labelling finding. **Disk**: 16 zips = **47.44 MB**
  (tree 49 MB) against the `output_v1` baseline 130.05 MB / 17 zips / 503 MB — **2.97 MB per
  search vs 7.65 = 38.8 %**, which clears the <40 % clause per search, while the eight-tile
  payload projected to ten is ≈59 MB = **45.6 %**, which does not; the clause needs a reading.
  New: latent 1σ **collapses** on some stages (the latent PDF is drawn from 100 samples, so both
  1σ percentiles can land on one sample — `Tile102008532…` `vis_lp` is degenerate on 12 of 12).
  `Tile102008475…` `vis_lp` is still pinned (log Z −5.07e6 → max source-plane separation ≈0.2507"
  against `threshold` 0.2); its `vis_pix` is healthy. Science clone merged to pipeline main
  (`a8529cb`, PR #68) and committed locally at `d481264`; nothing pushed, nothing submitted.

## Runs

- 342398_[0-9]: done — ral — submitted 2026-09-09 — wall 13:12 — two-stage vis_lp(n_live=750)+vis_pix(n_live=300), array 0-9, ten dr1_prelim tiles; output/ archived to output_v1 on laptop and RAL; RAL libs refreshed BEFORE submit (PyAutoFit 66f9f8d5d, Array 35aa681f, Lens 7d1b04de8, Galaxy 99cf7429, Nerves 0e7163b) and must not be touched until it finishes - mid-run library drift is what broke 342301_1/_7/_8; pipeline main 93a389e (PR#61); all ten tiles finished both stages, .err files carry only the standard warnings
    pulled_to: /mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output/dr1_prelim_grade_ab

- 342629_[0-9]: running — ral — submitted 2026-09-10 — wall 0:00 — two-stage vis_lp(n_live=750)+vis_pix(n_live=300), array 0-9, ten dr1_prelim tiles; libraries refreshed BEFORE submit (PyAutoNerves 0e7163bc2, PyAutoFit e354dbb6b, PyAutoArray 667deed3a, PyAutoGalaxy 6640a7494, PyAutoLens 0da06de63) carrying PyAutoFit#1598/#1600/#1602 and PyAutoLens#734; pipeline main 2a8b4db (PR#65 + #67); 342398 output archived to output_v2_pre_refresh on laptop and RAL; purpose: confirmation rerun — vis_lp latents written (12 keys on 102005065), catalogue rebuild with 0 blank cells, same-library rerun scatter vs 342398 for the restated parity witness

- 342648_[0,2,4-9]: submitted — gpu — submitted 2026-09-11 — wall 0:00 — SED chain `hpc/batch_gpu/submit_sersic_waveband_8tiles` (a copy of `submit_sersic_waveband` differing only in `--array=0,2,4-9`, because `hpc/sync submit` passes no sbatch arguments), `PYAUTO_OUTPUT_DIR=output_sed`: Sersic lens model on VIS then every non-VIS waveband fit (nir_y/j/h on all eight tiles, plus decam_g/r/i/z on the seven non-102005065 tiles), for the eight tiles 342629 completed; tiles 1 and 3 omitted because 342629_1/_3 are still fitting `vis_lp` and have no result to seed from. `output_sed/<sample>/<tile>/initial_lens_model/vis_lp/<hash>.zip` seeded by `cp -p` from `output/` for all eight tiles before submit so the upstream stage short-circuits; `output/` untouched (16 zips before and after). No library refresh on RAL, no push. Purpose: produce `sersic_lens_model/{vis,<band>}` so `catalogue/scripts/magnitudes.py` and `multi_wavelength.py` can run and the per-band magnitudes can be compared against `dr1_prelim_grade_ab_catalogue_csvs_20260623`. Progress at 15:40 on 2026-09-11: tasks 0, 2, 4, 5, 6 COMPLETED on `euclid-ral-gpu-2` in 13:34–20:15 each (13:43, 15:08, 15:42, 20:15, 13:34), task 7 RUNNING, task 8 PENDING. **Task `_9` (`Tile102008848RA0601376380877DECNEG0634605061157`) was cancelled while still PENDING on 2026-09-11**, on the human's authorisation, so that tile could be run instead on the CPU route as the verification run recorded below; it is the only array index removed and the other seven are unaffected

- 342668_9: submitted — ral — submitted 2026-09-11 — wall 0:00 — CPU verification of the SED chain via hpc/batch_cpu/submit_sersic_waveband (pipeline PR #70, sbatch --array=9): tile 102008848, JAX on the CPU backend, 8 CPU; same seeded vis_lp zip as the GPU tiles; purpose: verify the CPU setup the main experiment will use, and give a GPU-vs-CPU wall-time and result comparison. Started 15:37:49 BST on `euclid-ral-compute-10-2`, 8 CPUs, partition `ral`. First-log evidence, all four pre-registered PASS criteria met inside 30 s: `JAX backend: cpu` (the script's cpu-backend guard); `15:37:59 … Starting non-linear search with JAX (CPU: cpu)`; `15:38:02 vis_lp … output path … initial_lens_model/vis_lp/ac98229c0d67998215f1885157f8c5f4` — the seeded hash exactly — followed by `Fit Already Completed: skipping non-linear search`; then the Sersic VIS search `15:38:14 vis … Starting new Nautilus non-linear search` and `15:38:18 … JAX jit compilation of vectorized (vmap) likelihood function complete in 1.5 seconds`. The submitted script is PR #70's byte-for-byte apart from the four site lines this clone's other `batch_cpu/` scripts already carry (`PROJECT_PATH` / `PYAUTO_HPC_BASE` exports, `sample=dr1_prelim_grade_ab`, the ten-tile dataset list, the real `--mail-user`); the PR file is the generic pipeline version (`sample=q1_walsmley`, one-entry dataset list, no exports), so a byte-identical copy would have resolved array index 9 to an empty dataset. Every element under test — the `#SBATCH` resource directives, `PYAUTO_OUTPUT_DIR=output_sed`, the cpu-backend guard, the `env` line and `--number_of_cores=$THREADS` — is unchanged from PR #70

## Ruling

(none)
