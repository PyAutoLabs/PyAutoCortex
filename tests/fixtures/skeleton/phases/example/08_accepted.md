# Example — phase 8: the anchor comparison, accepted

Project: example
Phase: 8
State: accepted
Gates: PyAutoFit#1400
Gates-cleared: 2026-08-25
Witness: anchor theta_E within 0.01 arcsec of the published value on the new sampler
Budget: 6:00
Runs: 342050
Ruling: R-20260901-02
Lane: local-dev
Review-minutes: 6
Epic: example-programme
Filed: 2026-08-24

## Question

Does the new sampler reproduce the anchor within the published error?

## Witness

`output/phase_08/anchor/samples_summary.json` — `theta_E` within 0.01 arcsec.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/phase_08/`

## Runs

- 342050: done — gpu — submitted 2026-08-28 — wall 5:10
    pulled_to: /mnt/c/Users/Jammy/Science/example/output/phase_08
    ruled: R-20260901-02

## Ruling

R-20260901-02 — accept (supersedes R-20260901-01)
