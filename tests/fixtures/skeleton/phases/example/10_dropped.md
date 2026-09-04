# Example — phase 10: the mesh-pix sweep, dropped

Project: example
Phase: 10
State: dropped
Witness: mesh-pix log-evidence beats the Delaunay anchor by 5.0
Budget: 6:00
Runs: 341950, 341960
Ruling: R-20260901-05
Review-minutes: 4
Epic: example-programme
Filed: 2026-08-31

## Question

Does the mesh-pix sweep beat the Delaunay anchor?

## Witness

`output/legacy_wrong/phase_10/*/samples_summary.json` log-evidence vs the anchor.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/legacy_wrong/phase_10/`

## Runs

- 341950_[0-3]: legacy_wrong — gpu — submitted 2026-08-22 — wall 6:00 — ran on the wrong regularisation
    where: /mnt/c/Users/Jammy/Science/example/output/legacy_wrong/phase_10
- 341960: void — gpu — submitted 2026-08-23 — wall 0:00 — cancelled before the first step

## Ruling

R-20260901-05 — drop
