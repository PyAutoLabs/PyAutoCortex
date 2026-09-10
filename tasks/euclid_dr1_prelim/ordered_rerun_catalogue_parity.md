# Euclid_dr1_prelim — Ordered Nautilus rerun to catalogue parity

Project: euclid_dr1_prelim
Summary: Do ordered Nautilus reruns reproduce the euclid catalogue values?
State: awaiting-ruling
Gates: euclid_strong_lens_modeling_pipeline#60
Witness: The same ten dr1_prelim tiles are refitted on RAL with af.Nautilus through the two-stage vis_lp (n_live=750) / vis_pix (n_live=300) submit, from a science clone that has merged pipeline main so order_bases=True, hpc_mode on, quick updates off and samples.csv off are all in force, after output/ has been archived to output_v1 on both the laptop and RAL so the fresh runs write into a clean output/; all ten tiles complete, including the three that failed in 342301 (tasks 1, 7, 8); the Sersic and multi-wavelength follow-ups then run into output_sed; a catalogue built from output/ and output_sed reproduces the original euclid reference catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/ for those ten tiles, with tile identity and astrometry exact, effective Einstein radius and per-band magnitudes within combined 3 sigma, and MGE ell_comps agreeing up to a set swap; the same build then completes on RAL as it did for the original euclid project; and the fresh output/ holds no unzipped sibling directories and no samples.csv, coming in under 40% of the 130 MB zip payload the 2026-09-07 runs produced.
Budget: 36:00
Runs: 342398
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
- SED chain: `hpc/batch_gpu/submit_sersic_waveband`, which exports
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

## Runs

- 342398_[0-9]: done — ral — submitted 2026-09-09 — wall 13:12 — two-stage vis_lp(n_live=750)+vis_pix(n_live=300), array 0-9, ten dr1_prelim tiles; output/ archived to output_v1 on laptop and RAL; RAL libs refreshed BEFORE submit (PyAutoFit 66f9f8d5d, Array 35aa681f, Lens 7d1b04de8, Galaxy 99cf7429, Nerves 0e7163b) and must not be touched until it finishes - mid-run library drift is what broke 342301_1/_7/_8; pipeline main 93a389e (PR#61); all ten tiles finished both stages, .err files carry only the standard warnings
    pulled_to: /mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output/dr1_prelim_grade_ab

## Ruling

(none)
