# Example — phase 7: the second half of the shared array, awaiting a ruling

Project: example
Phase: 7
State: awaiting-ruling
Witness: five faint lenses' checkpoint.hdf5 sane after the checkpoint resubmit
Budget: 8:00
Runs: 342110, 342120
Lane: local-dev
Review-minutes: 5
Epic: example-programme
Filed: 2026-08-30

## Question

Do the five faint lenses converge once resumed from the timed-out checkpoint?

## Witness

`output/phase_07/*/checkpoint.hdf5` sane for all five.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/phase_07/`

## Runs

- 342110: timeout — gpu — submitted 2026-08-30 — wall 8:00 — hit the budget; resubmitted from checkpoint
- 342120_[5-9]: done — gpu — submitted 2026-08-31 — wall 3:55 — array shared with phase 6
    resumes: 342110
    pulled_to: /mnt/c/Users/Jammy/Science/example/output/phase_07

## Ruling

(none)
