# ic50_workspace — EP against the graphical joint fit on IC50 dose-response data, scaling up

Project: ic50_workspace
Issue: PyAutoCortex#36

## Now

Parity at N=5 achieved on RAL (33/33 within 3σ for both methods, runs 342408 / 342409); the scale ladder runs 342411 and 342412 are submitted.
Next: pull the ladder and see where EP's cost and hill_coef width go as N grows; ep_lbfgs_jax is the scale lever.

## Runs

- 342408 — open — ral — 2026-09-09 — ep_scale_up: EP sim, nlive 150, max_steps 12
- 342409 — open — ral — 2026-09-09 — ep_scale_up: graphical sim joint Dynesty, nlive 150
- 342411 — open — ral — 2026-09-09 — ep_scale_up: EP scale ladder, sim rungs 5/10/25/50, nlive 150 max_steps 12
- 342412 — open — ral — 2026-09-09 — ep_scale_up: graphical scale ladder, sim rungs 5/10/25/50, nlive 150

## Log

- 2026-09-09 — run — 342412 submitted: ep_scale_up — graphical scale ladder, sim rungs 5/10/25/50, nlive 150
- 2026-09-09 — run — 342411 submitted: ep_scale_up — EP scale ladder, sim rungs 5/10/25/50, nlive 150 max_steps 12
- 2026-09-09 — run — 342409 submitted: ep_scale_up — graphical sim joint Dynesty, nlive 150
- 2026-09-09 — run — 342408 submitted: ep_scale_up — EP sim, nlive 150, max_steps 12
- 2026-08-19 — note — question: Does EP match the graphical joint fit end to end [archive/tasks/ic50_workspace/ep_scale_up.md]
