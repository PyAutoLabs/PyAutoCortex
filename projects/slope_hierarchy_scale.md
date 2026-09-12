# slope_hierarchy_scale — Hierarchical slope recovery with graphical and EP at N=25 to 50

Project: slope_hierarchy_scale
Issue: none

## Now

The N=25 scale-up is running: graphical array 342348_[0-24], joint fits 342350_0 / 342351_0, and the EP rerun 342410 on the mirror that carries #1580.
Next: pull wave 1 and compare EP against the NUTS parent sigma; then decide whether to go to N=50.

## Runs

- 342348_[0-24] — open — gpu — 2026-09-08 — n25_scale_up: one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 342350_0 — open — gpu — 2026-09-08 — n25_scale_up: joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 342351_0 — open — ral — 2026-09-08 — n25_scale_up: EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 342410 — open — ral — 2026-09-09 — n25_scale_up: EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0

## Log

- 2026-09-09 — run — 342410 submitted: n25_scale_up — EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0
- 2026-09-08 — run — 342351_0 submitted: n25_scale_up — EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 2026-09-08 — run — 342350_0 submitted: n25_scale_up — joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 2026-09-08 — run — 342348_[0-24] submitted: n25_scale_up — one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 2026-07-22 — note — question: Does hierarchical slope recovery hold at N=25 to 50 [archive/tasks/slope_hierarchy_scale/n25_scale_up.md]
