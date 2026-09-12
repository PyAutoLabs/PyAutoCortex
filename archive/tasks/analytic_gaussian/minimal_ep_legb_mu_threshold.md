# analytic_gaussian — is criterion 2's `mu` threshold too tight, or is the minimal EP control biased

Project: analytic_gaussian
Summary: Is criterion 2's mu threshold or the minimal-EP control wrong
State: planned
Gates:
Witness: on the 34 leg-B seeds whose minimal EP `mu` cell failed in wave 1, the minimal EP `mu` posterior is re-derived against the closed form and the displacement is attributed — either it matches the independently derived Gaussian-site bias (the threshold is wrong) or it exceeds it (the control is wrong), decided by the pre-registered numbers in the `## Witness` section
Budget:
Runs:
Ruling:
Review-minutes: 20
Epic: graphical-ep
Filed: 2026-09-10

## Question

Criterion 2 of the `ensemble_parity` witness — the **minimal EP column on leg B**, the campaign's
*analytic ceiling* — missed its own bar in wave 1: **166/200 seeds** pass every row against a
pre-registered **0.95**, ruled 2026-09-10 as `rulings/2026/09/R-20260910-04.md`.

The miss is one row. Of the 34 failing seeds, **33 fail on `mu` alone**; the `sigma` row that the
Laplace-on-scatter caveat predicts would be the problem passes **199/200**, and every `x_i` row
passes 200/200. And it is the *mean* statistic, not the error: 33 of the 34 `mu` cells fail on
`a = |dmean| / std_ref > 0.05` (a med 0.0237, a p90 0.0656, a max 0.1303), exactly one on
`b = |std / std_ref - 1| > 0.16` (b 0.205; that seed's a is 0.0323 and passes).

So the minimal EP column places the `mu` posterior *mean* a few percent of a reference standard
deviation away from the closed form, systematically enough that ~17% of seeds land outside a
5%-of-sigma tolerance. On leg A — where `sigma` is fixed and the graph is exactly Gaussian — the
same code is exact to `max a = 4.25e-14`. So whatever this is, it is created by the leg-B
`sigma ~ TruncatedGaussian(10, 5, 0, 100)` level.

Two mutually exclusive explanations, and this task decides which:

1. **The threshold is wrong.** EP with a Gaussian site on `sigma` is biased on this model *by
   construction*; the campaign has always said so. If that construction-level bias propagates into
   `mu` at the observed magnitude, then a 0.05 `a` tolerance on the `mu` row was simply set too
   tight for a column that is *defined* to be biased — the ceiling was mis-measured, not breached.
2. **The control is wrong.** The hand-rolled minimal EP carries an implementation defect (a
   mis-formed cavity, a moment update taken on the wrong parameterisation, a convergence criterion
   that stops before the `mu` site has settled) that displaces `mu` beyond what the Gaussian-site
   approximation alone accounts for.

**Why this must be settled before the cure is judged.** The moment-matching cure filed as
PyAutoMind `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md` is to be judged
*against this column* — criterion 4's autofit-EP leg-B miss (78/200) has the minimal EP column as
its reference ceiling, on the campaign's own logic that "EP with a Gaussian site on sigma is biased
on this model by construction, so it — not zero — is what an autofit fix should be judged against".
A ceiling that is itself off by an unexplained amount cannot referee a cure. Either the number the
cure must beat moves, or the reference implementation it is compared to is repaired.

## Witness

Pre-registered here, before any re-derivation is run.

**This task must not relax the existing `WITNESS` block in `scripts/aggregate_ensemble.py`.**
Changing criterion 2's threshold is this task's *outcome*, not its method: the aggregator's
pre-registered numbers stay exactly as wave 1 ran them until a ruling on this task says otherwise
and records the reason. Wave 1's 166/200 stands as the measured number either way.

The re-derivation runs on the **34 leg-B seeds whose minimal EP `mu` cell failed in wave 1**,
named by seed id so the set cannot drift:

    8, 10, 12, 14, 16, 29, 38, 40, 44, 47, 48, 57, 58, 62, 68, 72, 76, 83, 92,
    106, 125, 127, 137, 138, 145, 151, 152, 153, 156, 169, 171, 175, 181, 183

(the set is reproducible from `results/ens_n5/parity_ensemble.csv` and the per-seed sidecars:
a seed is in it iff some `legs.B.rows[*].columns["minimal EP"].passed` is false.)

For each of those seeds, recompute the minimal EP `mu` posterior and, independently of the EP
code path, compute the displacement that the Gaussian-site-on-`sigma` approximation *alone*
predicts for `E[mu]` — by marginalising `mu` under the closed form and under a graph in which the
`sigma` level is replaced by its best Gaussian site, using no code from
`scripts/analytic_ep_minimal.py`. Call the observed displacement `a_obs` and the predicted one
`a_pred`, both in units of `std_ref` as the aggregator defines `a`.

| # | claim | number that decides it |
|---|---|---|
| 1 | the control is faithful | on ≥ 32 of the 34 seeds, `\|a_obs − a_pred\| ≤ 0.01`, and the signed residual `a_obs − a_pred` has median `\|·\| ≤ 0.005` — no systematic excess beyond the analytic bias |
| 2 | the control is biased | claim 1 fails, i.e. ≥ 3 seeds with `\|a_obs − a_pred\| > 0.01` or a signed-residual median beyond ±0.005 — the excess is an implementation defect, and the defect is named with the line that causes it |
| 3 | if claim 1 holds, the replacement threshold is derived, not chosen | the smallest `a` tolerance on the `mu` row at which ≥ 95% of all 200 wave-1 seeds pass, reported with its Wilson 95% interval, together with `a_pred`'s p95 over all 200 seeds — the new threshold must be ≥ that p95, so it is set by the analytic bias and not by the sample |
| 4 | leg A is untouched | re-running the same re-derivation on leg A returns `a_obs ≤ 1e-6` on every row of every seed — the exactness criterion 1 already measured is not a casualty of any change made here |

Deliverable: a written finding in `analytic_gaussian` carrying the per-seed `a_obs`, `a_pred` and
residual table, and — only if claim 1 holds — the derived replacement threshold from claim 3, as
the proposal a ruling may then apply to `WITNESS`. Claims 1 and 2 are exhaustive: exactly one is
recorded, and criterion 2 is amended only under claim 1 with the derivation as its reason.

## Where to look

- `rulings/2026/09/R-20260910-04.md` — the ruling that opened this; criterion 2's bullet carries
  the 166/200, the `mu` attribution and the 199/200 `sigma` row that rules out the obvious culprit
- `tasks/analytic_gaussian/ensemble_parity.md` — the parent task; its `## Witness` table is the
  pre-registration this one may not edit unilaterally
- `analytic_gaussian` @ `b44390d` (`/mnt/c/Users/Jammy/Science/analytic_gaussian`, git main, no
  remote):
  - `results/ens_n5/parity_ensemble.md` — the leg-B table: `minimal EP | mu | 0.0237 | 0.0656 |
    0.1303 | 0.0526 | 0.0663 | 0.2050 | 166/200`, against `minimal EP | sigma | … | 199/200`
  - `results/ens_n5/parity_ensemble.csv` — the same per row, machine-readable; the 34 failing
    seed ids come from the sidecars it summarises
  - `results/ens_n5/seed_NNNN.json` — per-seed `legs.B.rows[*].columns["minimal EP"]`
    (`mean`, `std`, `a`, `b`, `tol_a`, `tol_b`, `passed`)
  - `scripts/analytic_ep_minimal.py` — the control under suspicion; borrowed verbatim from
    `autofit_workspace_test/scripts/graphical/analytic_ep_minimal.py` @ `165a19e`
  - `scripts/analytic_reference.py` — the closed form to re-derive against
  - `scripts/aggregate_ensemble.py` — the `WITNESS` block (line ~58) and `MAX_STALE_FRACTION`;
    the pre-registration in machine-readable form, and the file this task may not relax
  - `scripts/ensemble_seed.py` — `--seed`, `--legs`, `--columns` for a single-seed re-run
- PyAutoMind `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md` — the cure that
  this column is meant to referee, and the reason this cannot wait
- PyAutoFit#1405 — the open Laplace-on-scatter caveat this column quantifies

## Runs

## Ruling

(none)
