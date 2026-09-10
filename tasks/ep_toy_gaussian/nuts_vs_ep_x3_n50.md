# Ep_toy_gaussian — do three EP fits agree with NUTS on the #1405 collapse toy at N=50

Project: ep_toy_gaussian
Summary: Do three EP fits agree with NUTS at N=50
State: ready
Gates:
Witness: over one 50-dataset draw (seed 42), NUTS is healthy and every one of 3 EP repeats on identical data recovers the NUTS parent mean and sigma within the pre-registered thresholds in `## Witness`, committed as `results/n50_seed42/{summary.json, comparison.md}`
Budget: 24:00
Runs:
Ruling:
Review-minutes: 20
Epic: graphical-ep
Filed: 2026-09-10

## Question

The `graphical-ep` campaign has three independent lines of evidence that graphical and EP are
sound after the D1-D6 wave: the cosmology run (`slope_hierarchy_scale`, N=25), IC50 (33/33 at
N=5) and the analytic Gaussian ensemble (200 seeds, ruling R-20260910-04). What none of them is,
is the toy on which the hierarchical-parameter collapse was *first* found. This task is the last
confidence test before the campaign scales up: run **that** model, at 50 datasets, with a joint
**JAX + NUTS** reference, and fit it with EP **three times on identical data**. Do all three EP
fits agree with each other and with NUTS?

### What the earlier "collapse" runs actually were

The "the toy collapsed" memory is a composite of four different runs, none of which is the run
this task performs. Recorded here so nobody re-derives it:

| run | what it was | collapse seen |
|---|---|---|
| `PyAutoMind/complete/2026/07/ep_scale_collapse_assets/ep_toy_diagnostic.py` + `EP_TOY_FINDINGS.md` (2026-07-21, PyAutoFit `f83f2f493`) | **The original.** HowToFit `gaussian_x1__hierarchical` toy: N=5 Gaussians, `centre_i ~ N(50, 10)`, `normalization=0.5`, `sigma=5` fixed, `centre` prior `TruncatedGaussian(50, 20, 0, 100)`, `HierarchicalFactor(GaussianPrior, mean=TG(50,10,0,100), sigma=TG(10,5,0,100))`, per-factor `DynestyStatic(nlive=100, sample="rwalk")`, `LaplaceOptimiser`, `EPHistory(kl_tol=0.05)`, `max_steps=20`. Joint reference = **Dynesty** on `global_prior_model`, not NUTS. | 30 identical runs: 70% RECOVER / 7% COLLAPSE (`scatter=0.0030 +/- 0.0000`, mean -> 54.4) / 23% CRASH. The joint fit was stable every time. |
| `PyAutoMind/complete/2026/09/ep-scale-collapse-leg2-assets/{toy.py,run_once.py,classify.py,results_baseline.txt}` | Self-contained rebuild of the same model (data regenerated in memory; `TOY_N`, `TOY_SEED`, `TOY_MAX_STEPS`, `TOY_OPT`, `TOY_UPDATER`), noise `TOY_NOISE=0.05`. | 20 seeds at N=5: 13 COLLAPSE / 7 RECOVER (`scatter=0.0000 err=1e-11`) — harsher than the original. Three-state classifier PATHOLOGICAL / BIASED-TIGHT / RECOVER. |
| `autofit_workspace_test/scripts/graphical/analytic_gaussian_collapse.py` | The closed-form referee's collapse configuration (N=5, 5 seeds, `max_steps=20`). | pre-fix FAIL 3/5 (STALE `10.00 +/- 3.69`, BIASED-TIGHT `7.78 +/- 0.51`); post #1558/#1560/#1562 RECOVER 5/5. |
| `Science/z_projects_complete/slope_hierarchy` (lensing, N=5) | The only **NUTS-vs-EP** hierarchical comparison to date. | NUTS sigma `0.143 [0.117, 0.185]` vs EP `0.026 +/- 0.00001` — 4x low, errors ~1000x too tight. |
| "50 datasets" | `autofit_workspace/scripts/simulators/simulators_sample.py:29` and `Science/concr/simulators/toy.py` — the **fixed-centre** low-SNR sample, shared-centre EP, no hierarchy. | not a collapse run |

**Nothing has ever run this toy with a NUTS joint fit, at N=50, or with repeated EP fits on
identical data.** The project is new in exactly those three respects, and keeps the original
model and EP settings verbatim.

### The fixes that might have cured it

Everything below landed in PyAutoFit after the 2026-07-21 original run (local source checkout
`PyAutoFit` main `81927cce9`, version string still 2026.8.17.1 — cite the SHA, not the version):
**#1465** (collapse guard), **#1558** (D1 id-0 gradient), **#1560** (D4 message limits),
**#1562** (D2/D3 fd-Hessian + skip-not-write), **#1572 / #1573 / #1574 / #1576** (the review wave,
per-variable stale tracking), **#1578 / #1580** (stale-mask fixed point), plus the 2026-08-05
`InitializerException` no-abort commit, which is the 23% CRASH mode of the original run. The RAL
PyAuto mirror was verified at PyAutoFit `66f9f8d5d` (contains `08207bad0`, #1580) on 2026-09-09;
re-verify before submitting.

### What is new here

1. A **joint NUTS reference** (`af.BlackJAXNUTS`, `use_jax=True`) instead of Dynesty — the first
   time this toy has had a gradient-based joint posterior to be judged against.
2. **N=50**, ten times the original's N=5, which is where the campaign wants to scale to.
3. **Three EP repeats on identical data**, differing only in RNG — so EP's run-to-run spread is
   measured directly rather than inferred across seeds. A pass on criteria 2-5 is the evidence
   that the phase-2 / analytic-Gaussian fixes cured #1405 on its own toy; a failure isolates it
   to the Dynesty-per-factor EP path, since the analytic ensemble used Laplace factors.

## Witness

Pre-registered before submission and mirrored machine-readably as `WITNESS` in
`scripts/compare.py`. Reference = the NUTS posterior on `n50_seed42`; truth = the parent
`(50, 10)` and the realised sample statistics of the 50 drawn centres. **A missed criterion is a
finding to rule on, never a number to relax so a run can pass**; changing one is its own task,
with the reason in the ruling.

| # | criterion | threshold |
|---|---|---|
| 1 | NUTS health | 0 divergences; r-hat <= 1.01 and ESS >= 400 on parent mean and sigma; realised sample mean/std inside the NUTS 3 sigma interval |
| 2 | No collapse | every EP repeat: parent sigma >= 1.0 (10% of truth) and the #1465 guard silent — PATHOLOGICAL count 0/3 |
| 3 | EP-NUTS parity | every repeat: \|mean_EP - mean_NUTS\| <= 2 sigma_NUTS(mean) and \|sigma_EP - sigma_NUTS\| <= 2 sigma_NUTS(sigma) |
| 4 | EP self-agreement | max pairwise spread across the 3 repeats <= 1 sigma_NUTS, for parent mean and for sigma |
| 5 | Honest widths | every repeat: sigma_EP / sigma_NUTS within [1/3, 3] on parent mean and sigma — BIASED-TIGHT count 0/3 |
| 6 | Per-dataset centres | >= 95% of the 50 centres within 3 sigma_NUTS of the NUTS median, in every repeat |
| 7 | EP flag health | no factor ends any repeat with zero SUCCESS updates; no CRASH; no NaN `RuntimeWarning` |

Deliverable: `results/n50_seed42/summary.json` (the witness file) + `comparison.md`, committed in
`ep_toy_gaussian`, carrying every criterion's measured number.

## Where to look

- `ep_toy_gaussian` (this project's row): `/mnt/c/Users/Jammy/Science/ep_toy_gaussian` —
  `scripts/{toy.py, one_by_one.py, graphical_nuts.py, ep_repeat.py, compare.py}`,
  `hpc/batch_cpu/{submit_nuts, submit_ep}`, `wiki/project/state.md`
- `results/n50_seed42/` — `nuts.json`, `one_by_one.json`, `ep_r{0,1,2}.json`, and the two
  deliverables `summary.json` + `comparison.md`. The local smoke sample is `n5_smoke`
- `PyAutoMind/complete/2026/07/ep_scale_collapse_assets/` — the original run: `ep_toy_diagnostic.py`
  and `EP_TOY_FINDINGS.md`, the source of the model and the EP settings used verbatim here
- `PyAutoMind/complete/2026/09/ep-scale-collapse-leg2-assets/` — `toy.py` (borrowed for
  `scripts/toy.py`), `run_once.py`, `classify.py` (the three-state labels), `results_baseline.txt`
- `PyAutoMind/draft/research/graphical_ep/ep_campaign.md` — the campaign ledger; this task is
  phase 1's confidence test
- Cortex `tasks/analytic_gaussian/ensemble_parity.md` (ruling R-20260910-04) — the 200-seed
  closed-form ensemble whose fixes this task tests on the original toy
- `Science/z_projects_complete/slope_hierarchy` — the only prior NUTS-vs-EP hierarchical comparison
- PyAutoFit#1405 — the collapse basin, still open pending the moment-matching cure

## Runs

## Ruling

(none)
