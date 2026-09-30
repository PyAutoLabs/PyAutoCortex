# ic50_workspace — EP against the graphical joint fit on IC50 dose-response data, scaling up

Project: ic50_workspace
Issue: PyAutoCortex#36

## Now

The scale ladder is in. EP passes N=5/10/25 with coef_mean within 3σ and cost growing about linearly per sweep (26/50/140 s). It died at N=50 on a projection assert the library should have recovered from (Mind bug prompt draft/bug/autofit/ep_project_nonfinite_suff_stats_ic50_n50.md, approved for start_dev; a local rerun converged, so the trigger is stochastic). Graphical is cheaper but overconfident beyond N=25, and the EP hill_coef widths are not yet comparable because util.py reports factor-message widths. Next: land the projection fix, rerun the EP ladder with output on and a fixed seed, report hill_coef from the mean field, then give ep_lbfgs_jax a witness as the scale lever.

## Runs


## Log

- 2026-09-30 — note — Ladder read: EP s/sweep 26/50/140/~300 s at N=5/10/25/50 vs graphical wall 21/42/119/281 s. EP hill_coef widths flat at ~0.8 because util.py reports factor-message (likelihood) widths and the global factor freezes hill_coef; graphical widths shrink but fall to 56/75 and 65/150 within 3 sigma at N=25/50 (overconfident). coef_mean passes 3 sigma for both methods on every completed rung.
- 2026-09-30 — note — 342411 N=50 failure diagnosed: AssertionError at autofit/messages/abstract.py:316 while projecting the global factor after EP sweep 4 (mirror 66f9f8d5d); the 4th global search had max logL -337 (vs -69 at sweep 3) and logz +/- nan. Library defect: project asserts on non-finite suff_stats and factor_step (optimiser.py:150) does not catch AssertionError, so one bad projection kills the run; no later commit touches the path. A local rerun at 66f9f8d5d converged in sweep 3 without failing (unseeded Dynesty, non-deterministic). Mind bug prompt draft/bug/autofit/ep_project_nonfinite_suff_stats_ic50_n50.md
- 2026-09-09 — run — 342411 failed — wall 0:38: ep_scale_up: EP scale ladder, sim rungs 5/10/25/50, nlive 150 max_steps 12 — finished 2026-09-09 23:19:29 BST (sacct COMPLETED 00:38:49, the ladder catches rung failures): rungs N=5/10/25 passed the global coef_mean assertions; rung N=50 FAILED — AssertionError: assert np.isfinite(suff_stats).all() in autofit/messages/abstract.py:316 project (via mapper/prior/abstract.py:237), error.342411.err
- 2026-09-09 — run — 342412 finished — wall 0:07: ep_scale_up: graphical scale ladder, sim rungs 5/10/25/50, nlive 150 — COMPLETED 2026-09-09 22:48:42 BST (sacct 00:07:59): all four rungs N=5/10/25/50 passed the global coef_mean assertions (within 3σ); results/graphical_ladder_n*_summary.json
- 2026-09-09 — run — 342408 finished — wall 0:01: ep_scale_up: EP sim, nlive 150, max_steps 12 — COMPLETED 2026-09-09 22:17:29 BST (sacct 00:01:03): N=5 EP parity, all global coef_mean assertions passed (within 3σ); results/ep_sim_summary.{txt,json}
- 2026-09-09 — run — 342409 finished — wall 0:00: ep_scale_up: graphical sim joint Dynesty, nlive 150 — COMPLETED 2026-09-09 22:16:54 BST (sacct 00:00:24): N=5 graphical parity, all global coef_mean assertions passed (within 3σ); results/graphical_sim_summary.{txt,json}
- 2026-09-09 — run — 342412 submitted: ep_scale_up — graphical scale ladder, sim rungs 5/10/25/50, nlive 150
- 2026-09-09 — run — 342411 submitted: ep_scale_up — EP scale ladder, sim rungs 5/10/25/50, nlive 150 max_steps 12
- 2026-09-09 — run — 342409 submitted: ep_scale_up — graphical sim joint Dynesty, nlive 150
- 2026-09-09 — run — 342408 submitted: ep_scale_up — EP sim, nlive 150, max_steps 12
- 2026-08-19 — note — question: Does EP match the graphical joint fit end to end [archive/tasks/ic50_workspace/ep_scale_up.md]
