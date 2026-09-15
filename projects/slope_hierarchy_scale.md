# slope_hierarchy_scale — Hierarchical slope recovery with graphical and EP at N=25 to 50

Project: slope_hierarchy_scale
Issue: slope_hierarchy_scale#2

## Now

N=25 scale-up: graphical array 342348_[0-24] and joint fit 342350_0 still open; the EP arm 342410 died at ~EP step 3 on LLVM compile memory (one jit per factor search, 64 GB). slope_hierarchy_scale#4 decouples --use_cpu from the JAX likelihood; once merged, submit the EP witness rerun with MAX_STEPS=2 (human's choice 2026-09-15). Next: pull wave 1, compare EP vs NUTS parent sigma once the compile-memory fix lands.

## Runs

- 342348_[0-24] — open — gpu — 2026-09-08 — n25_scale_up: one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 342350_0 — open — gpu — 2026-09-08 — n25_scale_up: joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 342351_0 — open — ral — 2026-09-08 — n25_scale_up: EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix

## Log

- 2026-09-15 — run — 342410 failed — wall 11:05: n25_scale_up: EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0 — JAX-on-CPU path, no pool: 76 factor searches (~3 EP steps of 25) then LLVM JIT section memory exhausted 64 GB; aborted 2026-09-10 09:29 (slope_hierarchy_scale#3 phase; compile-memory bug filed against PyAutoFit)
- 2026-09-09 — run — 342410 submitted: n25_scale_up — EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0
- 2026-09-08 — run — 342351_0 submitted: n25_scale_up — EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 2026-09-08 — run — 342350_0 submitted: n25_scale_up — joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 2026-09-08 — run — 342348_[0-24] submitted: n25_scale_up — one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 2026-07-22 — note — question: Does hierarchical slope recovery hold at N=25 to 50 [archive/tasks/slope_hierarchy_scale/n25_scale_up.md]
