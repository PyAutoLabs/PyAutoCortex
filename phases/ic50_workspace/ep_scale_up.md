# Ic50_workspace — phase 1: IC50 use case — EP end to end with the existing derived-variable handling

Project: ic50_workspace
Phase: 1
State: planned
Gates:
Witness: one committed EP-vs-graphical parity table (means ± errors) at small N, EP running at the largest N reached with per-rung timings committed, and any derived-variable or scaling blocker recorded as its own filed prompt
Budget: 48:00
Runs:
Ruling:
Review-minutes: 25
Epic: graphical-ep
Filed: 2026-08-19
Migrated-from: PyAutoMind/draft/research/graphical_ep/ic50_ep_scale_up.md

## Question

Ready when: graphical-ep phase 2 (Mind) is issued — add its ref to `Gates:` and move to `gated`.

The IC50 cancer use case is the scale target: the end goal is graphical + EP fits at 10 000+
datasets, with a clear demonstration that EP matches the graphical joint fit at small N before
anyone trusts it at large N.

The final model has a **derived variable**: the per-dataset factor results inform the priors on
the global model, currently through the declarative framework. **Scope decision, made at intake
on 2026-08-19: use the derived-variable handling exactly as it exists.** Formalising derived
variables as a first-class EP/API concept is explicitly out of scope — do not let it derail the
runs. If the existing handling blocks an EP fit outright, record the blocker and route it as its
own prompt; do not redesign inline.

The work, in order:

1. **Get an EP fit running end to end** on the real IC50 model, derived variable and all, at
   small N. The development half is the Mind prompt `feature/autofit/ep_lbfgs_jax.md` (swap
   DynestyStatic → LBFGS/JAX for the simple 3-parameter factor fits) — the speed lever for the
   per-factor fits; it can land before or alongside this and stays its own PR.
2. **EP-vs-graphical parity at small N** — same model both ways, compare parameter means and
   errors. This is the trust-building deliverable.
3. **Scale ladder** — grow N stepwise toward 10k, recording wall time, memory and disk at each
   rung. Expect the per-factor fits to be fast and the autofit wrapper overhead to dominate;
   that evidence feeds the EP-profiling epic rather than being fixed inline here.

## Witness

Acceptance, verbatim from the Mind prompt:

- One committed parity table (EP vs graphical, means ± errors) at small N.
- EP runs at the largest N reached, with per-rung timings committed.
- Any derived-variable or scaling blocker recorded as its own filed prompt, not patched ad hoc.

## Where to look

- `ic50_workspace` (project row) — external checkout, non-standard layout
- <https://github.com/Jammy2211/ic50_assistant> — scientific context and run help
- Mind `draft/feature/autofit/ep_lbfgs_jax.md` — the development half (the speed lever)
- Mind `research/graphical_ep/ep_campaign.md` phase 4 — the campaign row this feeds
- Mind `research/autofit/autofit_profiling_bootstrap.md` — where the wrapper-overhead evidence goes

## Runs

## Ruling

(none)
