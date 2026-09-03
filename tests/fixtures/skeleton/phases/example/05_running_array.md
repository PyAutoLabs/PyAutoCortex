# Example — phase 5: the nine-lens array

Project: example
Phase: 5
State: running
Gates: PyAutoArray#431
Witness: nine of ten array tasks write a sane checkpoint.hdf5 within 8:00 wall
Budget: 8:00
Runs: 342091, 342102
Ruling: R-20260901-03
Review-minutes: 8
Epic: example-programme
Filed: 2026-08-29

## Question

Does the Delaunay pipeline reach the same theta_E basin on all ten lenses?

## Witness

`output/phase_05/*/checkpoint.hdf5` present for nine lenses, `.err` clean.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/phase_05/`

## Runs

- 342091_[0-8,10]: done — gpu — submitted 2026-08-30 — wall 6:12
    pulled_to: /mnt/c/Users/Jammy/Science/example/output/phase_05
- 342091_9: failed — gpu — submitted 2026-08-30 — wall 0:00 — OOM before the first step
- 342102: running — gpu — submitted 2026-09-01 — wall 0:00 — task 9 resubmitted alone
    after: 342091_9

## Ruling

R-20260901-03 — leave-to-finish
