# Inference_programme — phase 11: cluster extended-source inference — gradient-based fitting building on JAX knowledge

Project: inference_programme
Phase: 11
State: planned
Gates:
Witness: a written feasibility verdict with profiling numbers and a go/no-go for a follow-up implementation prompt — not shipped inference machinery
Budget: 24:00
Runs:
Ruling:
Lane: local-dev
Review-minutes: 25
Epic: cluster-strong-lensing
Filed: 2026-08-19
Migrated-from: PyAutoMind/draft/research/autolens/cluster_extended_source_inference.md

## Question

Ready when: cluster phase 10 (Mind draft `draft/feature/workspaces/cluster_pixelized_analysisfactor.md`)
is issued — add its ref to `Gates:` and move to `gated`.

Part of the Source & Cluster arc (phase 11 of 12). User request, verbatim: "Once this is
robust begin to extend inference with extended sources, build on JAX gradient knowledge."

Research-first. Phase 10 delivers post-inference refinement (mass model mostly fixed); this
phase asks whether full joint inference of cluster mass + pixelized sources is tractable with
the JAX gradient stack (MultiStart / gradient samplers, the SMC warm-start work, implicit-diff
PointSolver gradients from #657).

Known constraints from the JAX campaign memory: pixelized-source gradient sampling was
previously found infeasible (reg/logdet NaN localisation, Delaunay `sqrt(dual_area)` NaN
gradients, Delaunay needs `custom_jvp`); factor-graph fits multiply the cost by `n_sources`.
The research question is what changed and what is needed — which mesh (rectangular uniform is
the gradient-safest), which sampler tier, what the per-iteration cost is at cluster scale, and
whether positions-likelihood + imaging-likelihood factor graphs are jointly jit-able.

## Witness

A written feasibility verdict with profiling numbers and a go/no-go for a follow-up
implementation prompt — not shipped inference machinery.

## Where to look

- Mind `draft/feature/autolens/source_cluster_arc.md` — the arc ledger (this is its line 11)
- Mind `draft/feature/workspaces/cluster_pixelized_analysisfactor.md` — cluster phase 10, the gate
- `inference_programme` (project row): `output/searches/*/cluster/` — the cluster trees the
  REWIND left in the active tree

## Runs

## Ruling

(none)
