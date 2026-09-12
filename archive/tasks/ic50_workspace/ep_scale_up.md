# Ic50_workspace — IC50 use case — EP end to end with the existing derived-variable handling

Project: ic50_workspace
Summary: Does EP match the graphical joint fit end to end
State: submitted
Gates:
Witness: one committed EP-vs-graphical parity table (means ± errors) at small N, EP running at the largest N reached with per-rung timings committed, and any derived-variable or scaling blocker recorded as its own filed prompt
Budget: 48:00
Runs: 342408, 342409, 342411, 342412
Ruling:
Review-minutes: 25
Epic: graphical-ep
Filed: 2026-08-19
Migrated-from: PyAutoMind/draft/research/graphical_ep/ic50_ep_scale_up.md

## Question

Started 2026-09-09. Phases 1 and 2 of the campaign shipped on 2026-09-02 (the whole
D1–D6 PyAutoFit fix wave: #1558, #1560, #1562, #1572, #1573, #1574, #1576, #1578,
#1580), so the gate this task was waiting on is cleared and it went
`planned → ready → submitted` directly. The RAL PyAutoFit mirror was verified to
contain #1580 before submitting, so unlike phase 3's EP arm these runs carry the
stale-mask fixed-point fix.

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
- `scripts/compare_graphical_ep.py` (in the project) — writes the parity table this
  task's witness asks for, to `results/graphical_ep_comparison_<name>.{txt,json}`

## Runs

- 342408: submitted — ral — submitted 2026-09-09 — wall 0:00 — EP sim, nlive 150, max_steps 12
- 342409: submitted — ral — submitted 2026-09-09 — wall 0:00 — graphical sim joint Dynesty, nlive 150
- 342411: submitted — ral — submitted 2026-09-09 — wall 0:00 — EP scale ladder, sim rungs 5/10/25/50, nlive 150 max_steps 12
- 342412: submitted — ral — submitted 2026-09-09 — wall 0:00 — graphical scale ladder, sim rungs 5/10/25/50, nlive 150

## Ruling

(none)
