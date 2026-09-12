# analytic_gaussian — Graphical and EP against a closed-form Gaussian posterior, at ensemble scale

Project: analytic_gaussian
Issue: PyAutoCortex#34

## Now

Wave 1 (342413, 200 seeds at N=5) is accepted as the baseline: autofit EP is exact on the Gaussian leg, leg B sigma misses as pre-registered (78/200), collapse rate 0/200. Follow-ups filed through /intake.
Next: settle whether criterion 2's mu threshold or the minimal-EP control is wrong before any rerun; the N=25 rung is written but not submitted.

## Runs

## Log

- 2026-09-10 — result — accepted ensemble_parity (R-20260910-04): ok accept and intake the things to address. we can do another run down the line so also achieve the results in the analytic_gaussian project for future comparison
- 2026-09-10 — note — question: Is criterion 2's mu threshold or the minimal-EP control wrong — planned, never run [archive/tasks/analytic_gaussian/minimal_ep_legb_mu_threshold.md]
- 2026-09-09 — run — 342413_[0-199] submitted (done, wall 0:05): ensemble_parity — the N=5 seed ensemble, 200 seeds, 50 concurrent, `hpc/batch_cpu/submit_ensemble_n5`, sample `ens_n5`.
  RAL PyAuto mirror verified at PyAutoFit `66f9f8d5d` before submission, which **contains** `08207bad0` (#1580) — unlike phase 3's EP arm, this wave carries the full D1–D6 wave plus the review bundle; sacct 200/200 COMPLETED exit 0:0, per-seed wall 63–303 s; pulled + aggregated 2026-09-10 → analytic_gaussian b44390d (WITNESS NOT MET: 7 met / 4 miss) pulled_to:
  /mnt/c/Users/Jammy/Science/analytic_gaussian/hpc/batch_cpu/output
- 2026-09-09 — note — question: Do graphical and EP recover closed-form means and errors [archive/tasks/analytic_gaussian/ensemble_parity.md]
