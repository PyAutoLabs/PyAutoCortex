# Euclid_dr1_prelim — Ordered rerun to catalogue parity

Project: euclid_dr1_prelim
Summary: Do ordered reruns reproduce the euclid catalogue values?
State: gated
Gates: euclid_strong_lens_modeling_pipeline#60
Witness: Ten dr1_prelim tiles refitted with order_bases=True under the new low-disk config (hpc_mode on, quick updates off, samples.csv off), then the Sersic and multi-wavelength follow-ups run into output_sed, then a catalogue built from them: for those ten tiles the catalogue matches the original euclid reference catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/ with tile identity and astrometry exact, effective Einstein radius and per-band magnitudes within combined 3 sigma, and MGE ell_comps agreeing up to a set swap; the same build then completes on RAL as it did for the original euclid project; and the ten reruns' output/ holds no unzipped sibling directories and no samples.csv, coming in under 40% of the 130 MB zip payload the 2026-09-07 runs produced.
Budget: 12:00
Runs:
Ruling:
Review-minutes: 20
Epic:
Filed: 2026-09-09

## Question

The phase-4 array (342301) fitted ten DR1-prelim tiles before the MGE label
degeneracy was fixed, and only seven of them survived: 342301_1, _7 and _8
failed at exit 1 after 1h39-1h59 with their logs still unread, and _3 died at
3:52 on an ell_comps magnitude of 1.009 before being resubmitted alone as
342314_3. Those runs also predate the disk work: their `output/` is 501 MB for
ten tiles, of which ~371 MB is extracted copies sitting beside the zips and
79 MB of the remaining zip payload is `samples.csv`.

So: if the ten tiles are refitted with `order_bases=True` under the new
low-disk config, do the Sersic and multi-wavelength follow-ups then run
cleanly into `output_sed`, and does a catalogue built from the result
reproduce the values the original `euclid` project published for those same
ten tiles — first locally, then on RAL?

The MGE ordering is expected to change the *labelling* of the two lens bases,
not the physics, so `ell_comps` is compared up to a set swap while everything
else is compared on value. A disagreement outside that is the finding.

## Witness

Ten dr1_prelim tiles refitted with order_bases=True under the new low-disk config (hpc_mode on, quick updates off, samples.csv off), then the Sersic and multi-wavelength follow-ups run into output_sed, then a catalogue built from them: for those ten tiles the catalogue matches the original euclid reference catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/ with tile identity and astrometry exact, effective Einstein radius and per-band magnitudes within combined 3 sigma, and MGE ell_comps agreeing up to a set swap; the same build then completes on RAL as it did for the original euclid project; and the ten reruns' output/ holds no unzipped sibling directories and no samples.csv, coming in under 40% of the 130 MB zip payload the 2026-09-07 runs produced.

## Where to look

- Archive of the pre-ordering runs: `output_v1/dr1_prelim_grade_ab/` (the
  current `output/`, moved aside before the reruns; 501 MB, 17 zips, 18
  searches, one of them incomplete at
  `Tile102007903.../initial_lens_model/vis_lp/df990a0fe949bdc2888cb7fddf532e26`).
- Reruns: `output/dr1_prelim_grade_ab/<Tile>/initial_lens_model/{vis_lp,vis_pix}/`.
- SED chain: `output_sed/dr1_prelim_grade_ab/<Tile>/` via
  `PYAUTO_OUTPUT_DIR=output_sed` (`hpc/batch_gpu/submit_sersic_waveband`).
- Catalogue: `catalogue/` built by `scripts/build_inspection_bundle.sh`.
- Reference to match: the original euclid project's
  `catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/`
  (2990 rows; all ten dr1_prelim tiles confirmed present).
- Unread failure logs to read before relaunching: 342301_1, 342301_7, 342301_8.
- Already-scored inputs: the ordered witness 342375_[0-1] and the unordered
  control 342377_0 (all COMPLETED) — see
  `ordered_mge_witness_102005065` and `ordered_mge_control_unordered_102005065`.

## Runs

## Ruling

(none)
