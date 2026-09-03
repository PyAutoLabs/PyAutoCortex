# Inference_programme — phase 17: cluster-scale gradient-search benchmark (Prodigy vs Nautilus, point-source)

Project: inference_programme
Phase: 17
State: planned
Gates:
Witness: a cluster point-source sweep whose `results/searches/…` JSONs carry, per arm, best logL against the truth-instance logL, per-parameter recovery, wall time and evals/steps — the same truth-anchored shape as the 2026-07-31 galaxy-scale rows
Budget: 24:00
Runs:
Ruling:
Review-minutes: 20
Filed: 2026-07-31
Migrated-from: PyAutoMind/draft/research/autolens_profiling/cluster_gradient_search_benchmark.md

## Question

Does the Nautilus-vs-MultiStartProdigy comparison hold at CLUSTER scale for point
sources — the regime the solved variants target (many sources, big dimensionality
win: −2 params/source with `PointSolved`)?

> **ABSORBED 2026-07-31 (same day it was filed)** into the Mind prompt
> `draft/feature/autolens/point_source_defaults_campaign.md` (phase B, cluster
> tier, on RAL A100s). Do not dispatch this phase standalone — it is carried here
> so the context literals below survive the Cortex split and so the campaign's
> cluster tier has a phase to rule against when it runs.

Human-requested follow-up (2026-07-31, #657 wrap-up): once the galaxy-scale
point_source benchmark cells wrap, extend the comparison to a cluster-scale
point-source model in autolens_profiling.

### Scope (autolens_profiling)

- New sweep cells: `nautilus` + `multi_start_prodigy` on a cluster point-source dataset
  (multi-plane tracer, multiple sources; reuse/extend the profiling simulators — the
  workspace `cluster/simulator.py` family CSV conventions are the model source).
- Model: dPIE/Isothermal members + host halo as in the workspace cluster examples;
  sources as `al.ps.PointSolved` + `FitPositionsSourceSolved` (recommended search config)
  with an image-plane-solved arm if runtime permits.
- KNOWN CONSTRAINT: free cosmology cannot cross the solver custom_jvp boundary
  (Tracer aux; see the Mind's `ideas.md` follow-up) — pin cosmology, or benchmark
  source-plane solved only (no solver in chain) until the flattening follow-up lands.
- Compare: best logL vs truth-instance logL, per-parameter recovery, wall time,
  evals/steps; same truth-anchored methodology as the 2026-07-31 galaxy-scale runs.

### Context literals (2026-07-31 galaxy-scale runs, results/searches/)

- image_plane truth logL +7.20: nautilus +9.56 (739.7s) converged; prodigy 64x300 −79.9
  (852.8s) missed the 5mas basin (PairAll −inf underflow plateaus suspected; 256-start
  rerun pending at filing time).
- source_plane truth logL −33788: BOTH found better-than-truth wrong models (nautilus
  −313, prodigy −110 at 8.7x less wall) — scalar-mu^2 free-centre source-plane bias
  displayed; gradients work, likelihood flavour is the problem.

## Witness

Per arm, a `results/searches/…` JSON carrying best logL against the truth-instance
logL, per-parameter recovery, wall time and evals/steps — the same shape as the
galaxy-scale rows above, so the two tiers are directly comparable.

## Where to look

- `/home/jammy/Code/PyAutoLabs/autolens_profiling/results/searches/`
- `/mnt/ral/jnightin/autolens_profiling/`

## Runs

## Ruling
