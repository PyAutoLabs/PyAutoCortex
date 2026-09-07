# Example — the pixel-scale sweep, gated on two dev fixes

Project: example
Summary: Does the pixel-scale sweep change the preferred model
State: gated
Gates: PyAutoArray#431, https://github.com/PyAutoLabs/PyAutoFit/pull/1436
Witness: three lenses reach log-evidence within 2.0 of the anchor at 0.05 arcsec
Budget: 6:00
Review-minutes: 6
Epic: example-programme
Filed: 2026-08-26

## Question

Does the pixel-scale sweep change the preferred model once the mask fix and the
prior-loading fix land?

## Witness

`output/task_02/*/samples_summary.json` — log-evidence within 2.0 of the anchor.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/task_02/`

## Runs

## Ruling

(none)
