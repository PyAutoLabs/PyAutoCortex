# Euclid — phase 6: do we recover Sersic indices? 10 simulated Euclid lenses vs the real prior-edge pile-up

Project: euclid
Phase: 6
State: planned
Gates:
Witness: 10 simulated fits complete with a recovered-vs-input Sersic index table and plot, the same 10 real lenses' prior-edge status established from phase 4, and a written verdict naming the likely cause
Budget: 24:00
Runs:
Ruling:
Review-minutes: 20
Epic: euclid-dr1-prep
Filed: 2026-08-28
Migrated-from: PyAutoMind/draft/research/euclid/sersic_index_recovery.md

## Question

Ready when: euclid 5 accepted.

Real Euclid fits pile up at `sersic_index = 5` — the prior's upper edge. Two competing
explanations:

- **Real signal.** These lenses genuinely have high-index light profiles and the prior is
  simply too narrow.
- **Artefact.** A defective PSF model (or another data-side systematic) drives the fit to
  absorb the mismatch into a high Sersic index.

The phase-5 resimulations are built with indices in [2, 4] and without whatever data defect is
suspected. If the fits to the *simulated* data recover the input index, the pile-up is an
artefact of the real data; if they *also* pile up at 5, the problem is in the model or the
fitting, not the data.

Do **not** implement the fix here — the request is explicit that we get to the point where we
have results for 10 lenses and then work out what changes we want to make.

Interpretation hazards to respect: N = 10 is small, and a pile-up in 2 of 10 does not
distinguish the hypotheses — say up front what fraction would count as a result. Note which
phase-5 replacement-index rule was used and what it costs the inference. Confirm the simulated
fits use the **same** prior as the real fits, or the comparison is not like-for-like.

## Witness

Acceptance, verbatim from the Mind prompt:

- 10 simulated fits complete, recovered-vs-input table and plot produced.
- The real-lens prior-edge status of the same 10 lenses established from phase 4 output.
- A written verdict naming the likely cause and the recommended change, filed as a
  follow-up prompt if a change is warranted. No fix implemented here.

## Where to look

- `euclid` (project row): `catalogue/scripts/plot_lens_sersic_index.py` — already plots this
  population; reuse it rather than hand-rolling a new plot
- `euclid_dr1_prelim` (project row): the phase-5 simulated datasets and their truth table
- `euclid_strong_lens_modeling_pipeline`: the `sersic_lens_model.py` family used on the real data

## Runs

## Ruling

(none)
