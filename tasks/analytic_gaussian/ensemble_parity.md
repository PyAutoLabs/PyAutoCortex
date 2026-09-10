# analytic_gaussian — task 1: does autofit recover the closed form over an ensemble of draws

Project: analytic_gaussian
Summary: Do graphical and EP recover closed-form means and errors
State: awaiting-ruling
Gates:
Witness: over >= 200 independent dataset draws at N=5, the a/b error distributions and the empirical [q05, q95] coverage per column meet the pre-registered thresholds in the `## Witness` section below, committed as `results/ens_n5/{summary.json, parity_ensemble.md}`
Budget: 2:00
Runs: 342413
Ruling:
Review-minutes: 20
Epic: graphical-ep
Filed: 2026-09-09
Migrated-from: PyAutoMind/complete/2026/09/analytic-gaussian-benchmark.md

## Question

The `graphical-ep` campaign's end goal 1 is *"an analytic Gaussian model that statistically
demonstrates the graphical and EP source code is correct (means **and** errors against closed
form)"*. Phase 1 built the model and answered it at **one seed**, as a CI gate in
`autofit_workspace_test/scripts/graphical/`. That form did its job — it found six PyAutoFit
defects, D1–D6, all now shipped (#1558, #1560, #1562, #1572, #1573, #1574, #1576, #1578, #1580)
— but a single seed cannot demonstrate anything statistically: its 41-cell count moved 37/41 →
38/41 between two runs of identical code, because a verdict on a tolerance edge is a coin flip.

So: over many independent dataset draws of the same conjugate hierarchical Gaussian, does each
column recover the closed-form posterior — mean *and* error — and how often?

    mu ~ N(50, 10^2),   x_i | mu ~ N(mu, sigma^2),   y_ij | x_i ~ N(x_i, s_i^2)

    leg A   sigma = 10 fixed                          the graph is exactly Gaussian:
                                                      Laplace EP should be EXACT here
    leg B   sigma ~ TruncatedGaussian(10, 5, 0, 100)  the phase-2 scatter-collapse configuration

    columns   closed form | minimal EP | autofit graphical (joint DynestyStatic) | autofit EP

Three specific things this answers that the campaign has been carrying as assumptions:

- **Is leg A fixed?** The parked CI script failed leg A: `mu` never left its starting prior. The
  first local run on the post-fix library returns it exact (a = b = 0.000). Over 200 seeds, is
  that exactness the rule or the lucky draw?
- **How bad is leg B, really?** The Laplace-on-scatter caveat (`autofit/graphical/README.md`
  §3.5, PyAutoFit#1405) is documented but never quantified: the first local seed returns
  sigma 9.37 ± 3.57 against a reference 6.57 ± 2.88 — outside the cell tolerance, inside the
  closed-form [q05, q95], not collapsed. A rate with an interval turns that caveat into a
  measurement, and gives the moment-matching cure
  (`PyAutoMind draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`) a number to
  beat.
- **Is the collapse basin still reachable?** The scale-collapse rate (sigma < 0.1) over 200
  independent draws is the campaign's first unbiased estimate of how often PyAutoFit#1405's
  basin is entered.

The **minimal EP** column is the analytic ceiling, not a competitor: EP with a Gaussian site on
sigma is biased on this model by construction, so it — not zero — is what an autofit fix should
be judged against.

## Witness

Pre-registered before wave 1 was submitted, and mirrored machine-readably as `WITNESS` in
`scripts/aggregate_ensemble.py`. A missed criterion is a finding to rule on, never a number to
relax so a wave can pass; changing one is its own task, with the reason in the ruling.

| # | criterion | threshold |
|---|---|---|
| 1 | minimal EP, leg A | max a, b ≤ 1e-6 on every row of every seed — a deterministic identity |
| 2 | minimal EP, leg B (the analytic ceiling) | ≥ 95% of seeds within (scatter a 0.20 / b 0.30, other rows a 0.05 / b 0.16); E[sigma] coverage ≥ 0.90 |
| 3 | autofit EP, leg A | ≥ 95% of seeds within (a 0.01, b 0.02) on **every** row, and no seed worse than a = 0.10 |
| 4 | autofit EP, leg B | ≥ 90% of seeds within (a 0.15, b 0.25); E[sigma] inside the closed-form [q05, q95] for ≥ 90%; scale-collapse rate (sigma < 0.1) = 0 |
| 5 | autofit graphical | ≥ 90% of seeds within (a 0.10, b 0.15) on both legs; scatter coverage ≥ 0.85 |
| 6 | EP flag health | no seed in which any factor ends the run with zero SUCCESS updates — the STALE state #1562/#1574/#1576/#1580 taught the library to report |

Deliverable: `results/ens_n5/summary.json` (the witness file) and `parity_ensemble.md` committed
in `analytic_gaussian`, carrying every criterion's measured number — including a Wilson interval
on each coverage rate, so "3/3 covered" cannot be read as certainty.

Criterion 4 is **expected to miss**, on the campaign's own evidence. That is the point: the miss
becomes a measured rate rather than a documented caveat, and the ruling records it as the cure's
baseline.

## Where to look

- `analytic_gaussian` (this project's row): `scripts/ensemble_seed.py` (one seed per array task),
  `scripts/aggregate_ensemble.py` (the referee), `wiki/project/state.md`
- `autofit_workspace_test` @ `165a19e` — `scripts/graphical/analytic_{reference,ep_minimal,autofit}.py`,
  the modules this project borrows verbatim, and `analytic_gaussian.py`, the single-seed CI form
  parked NEEDS_FIX in `config/build/no_run.yaml`
- Mind `draft/research/graphical_ep/ep_campaign.md` — phase 1 and end goal 1
- PyAutoFit#1405 — the collapse basin, still open pending the moment-matching cure
- Mind `draft/bug/graphical_ep/analytic_gaussian_unseeded_graphical_column.md` — the CI script's
  unseeded graphical column; this project seeds dynesty's `rstate` from the seed instead, and
  records `graphical_seeded` in every sidecar
- `hpc/batch_cpu/submit_ensemble_n25` — the N=25 rung, written but **not submitted**: its cost is
  unmeasured (27 free parameters in the joint fit against 7 at N=5), and the local timing run was
  still going when wave 1 went out. Submit it once one seed has given a per-seed wall time; it
  runs the expensive graphical column on seeds 0-19 only

## Runs

- 342413_[0-199]: done — ral — submitted 2026-09-09 — wall 0:05 — the N=5 seed ensemble, 200 seeds, 50 concurrent, `hpc/batch_cpu/submit_ensemble_n5`, sample `ens_n5`. RAL PyAuto mirror verified at PyAutoFit `66f9f8d5d` before submission, which **contains** `08207bad0` (#1580) — unlike phase 3's EP arm, this wave carries the full D1–D6 wave plus the review bundle; sacct 200/200 COMPLETED exit 0:0, per-seed wall 63–303 s; pulled + aggregated 2026-09-10 → analytic_gaussian b44390d (WITNESS NOT MET: 7 met / 4 miss)
    pulled_to: /mnt/c/Users/Jammy/Science/analytic_gaussian/hpc/batch_cpu/output


## Ruling

(none)
