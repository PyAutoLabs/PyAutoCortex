# Euclid — phase 5: resimulate a fitted Euclid lens, and resimulate the 10 prelim lenses with true magnifications recorded

Project: euclid
Phase: 5
State: planned
Gates:
Witness: a user with a fit result resimulates it in one command; 10 resimulations exist with recorded truths including magnifications, and the prior-edge rule's inferred and simulated Sersic index is recorded per lens
Budget: 24:00
Runs:
Ruling:
Lane: local-dev
Review-minutes: 20
Epic: euclid-dr1-prep
Filed: 2026-08-28
Migrated-from: PyAutoMind/draft/feature/euclid/resimulate_fitted_lens_simulator.md

## Question

Ready when: euclid 4 accepted (it needs the 10 real fits as truth inputs).

Can a Euclid lens we have a result for be resimulated, so the simulated data can be fitted
and PyAutoLens tested for recovery of the correct values? Two artefacts, two homes:

- **`scripts/simulator.py` in `euclid_strong_lens_modeling_pipeline`** — a general,
  documented example: *"I have fitted a lens; resimulate it."* The script already exists
  (shipped 2026-08-29, PR #46) with a `--from-result` mode in place, though its SED is flat
  for now. **Extend that script; do not write a second one.** That real PR is filed as a Mind
  development prompt when this phase opens.
- **The 10 resimulations in `euclid_dr1_prelim`** — science outputs built from phase 4's
  results; they live in the science project, not the public repo.

Recipe: Sersic lens light, Sersic source (deliberately over-simple for some of the 10, and
that is explicitly fine — phase 6 tests recovery under a *matched* model first). Record the
true magnification of every simulated lens as a first-class output stored alongside the
dataset — phase 7's entire question depends on that ground truth, so it must not be
reconstructible-only-by-rerunning, and it must record enough to distinguish the point and
area magnification definitions. Prior-edge correction: many real fits pin `sersic_index = 5`
at the prior edge; when a lens's inferred lens-light Sersic index is at that edge, lower it to
a value in [2, 4], record both values, and document the rule for choosing the replacement
(fixed 3.0? drawn? population median?) — phase 6's interpretation depends on it. Match the
real data's PSF, noise and exposure characteristics, and be explicit about which aspect is
idealised and which is faithful.

## Witness

Acceptance, verbatim from the Mind prompt:

- A user with a fit result can resimulate it in one command.
- All 10 resimulations exist with recorded truths, including magnifications.
- The prior-edge rule is applied and both values recorded per lens.
- Gates 6a and 6b.

(6a and 6b are Cortex phases 6 and 7.)

## Where to look

- `euclid_strong_lens_modeling_pipeline`: `scripts/simulator.py`, `smoke_tests.txt`
- `euclid_dr1_prelim` (project row): the 10 simulated datasets and their truth table
- `phases/euclid/dr1_prelim_10_lens_science_run.md` — the fits these resimulations start from

## Runs

## Ruling

(none)
