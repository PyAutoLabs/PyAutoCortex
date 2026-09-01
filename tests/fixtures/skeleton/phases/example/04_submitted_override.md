# Example — phase 4: the two-band fit, submitted under a gate override

Project: example
Phase: 4
State: submitted
Gates: PyAutoLens#900
Gate-override: the fix is verified locally on the branch; not waiting for the merge
Witness: both bands converge to the same source centre within 0.02 arcsec
Budget: 6:00
Runs: 342001, 342010
Lane: local-dev
Review-minutes: 6
Epic: example-programme
Filed: 2026-08-28

## Question

Do the two bands agree on the source centre once fitted jointly?

## Witness

`output/phase_04/joint/samples_summary.json` — source centres within 0.02 arcsec.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/phase_04/`

## Runs

- 342001: failed — gpu — submitted 2026-08-31 — wall 0:00 — node failure before the first step
- 342010: submitted — gpu — submitted 2026-09-01 — wall 0:00

## Ruling

(none)
