# analytic_gaussian — Graphical and EP against a closed-form Gaussian posterior, at ensemble scale

Project: analytic_gaussian
Issue: PyAutoCortex#34

## Now

Wave 1 (342413, 200 seeds at N=5) is accepted as the baseline: autofit EP is exact on the Gaussian leg, leg B sigma misses as pre-registered (78/200), collapse rate 0/200. On criterion 2, astra and an independent Opus review both favour an under-calibrated mu threshold (calibrated on five unrepresentative seeds) and found no defect in the minimal-EP control; both flag the per-site sigma>0 clip (analytic_ep_minimal.py:333) as the one audit target, and astra will not clear the control without an independent reconstruction of the EP fixed point. Next: run the planned diagnostic (archive/tasks/analytic_gaussian/minimal_ep_legb_mu_threshold.md) on a passing, an edge and the worst mu seed; the N=25 rung stays written but unsubmitted until it lands.

## Runs

## Log

- 2026-09-30 — note — astra (Codex gpt-6-astra) on criterion 2, verbatim: 'Neither is established as "wrong" by this result alone. I favour inadequate calibration of the threshold, with moderate confidence, but would not yet certify the control.' Decisive diagnostic: independently reconstruct the same EP factorisation at the fixed point on a passing, an edge and the worst mu seed and compare tilted vs q moments; audit the per-site sigma>0 clip (analytic_ep_minimal.py:333). Opus reviewer concurs independently (a_mu = 0.041*(E_ref[mu]-m0)/std_ref over 200 seeds, corr 0.98; calibration seeds 0-4 had |a_mu| 0.002-0.020 vs 95th pct 0.077). Full answer: PyAutoCortex#50 comment https://github.com/PyAutoLabs/PyAutoCortex/issues/50#issuecomment-5908448194
- 2026-09-10 — result — accepted ensemble_parity (R-20260910-04): ok accept and intake the things to address. we can do another run down the line so also achieve the results in the analytic_gaussian project for future comparison
- 2026-09-10 — note — question: Is criterion 2's mu threshold or the minimal-EP control wrong — planned, never run [archive/tasks/analytic_gaussian/minimal_ep_legb_mu_threshold.md]
- 2026-09-09 — run — 342413_[0-199] submitted (done, wall 0:05): ensemble_parity — the N=5 seed ensemble, 200 seeds, 50 concurrent, `hpc/batch_cpu/submit_ensemble_n5`, sample `ens_n5`.
  RAL PyAuto mirror verified at PyAutoFit `66f9f8d5d` before submission, which **contains** `08207bad0` (#1580) — unlike phase 3's EP arm, this wave carries the full D1–D6 wave plus the review bundle; sacct 200/200 COMPLETED exit 0:0, per-seed wall 63–303 s; pulled + aggregated 2026-09-10 → analytic_gaussian b44390d (WITNESS NOT MET: 7 met / 4 miss) pulled_to:
  /mnt/c/Users/Jammy/Science/analytic_gaussian/hpc/batch_cpu/output
- 2026-09-09 — note — question: Do graphical and EP recover closed-form means and errors [archive/tasks/analytic_gaussian/ensemble_parity.md]
