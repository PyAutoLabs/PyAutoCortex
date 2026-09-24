# slope_hierarchy_scale — Hierarchical slope recovery with graphical and EP at N=25 to 50

Project: slope_hierarchy_scale
Issue: slope_hierarchy_scale#2

## Now

343299 (EP witness rerun, MAX_STEPS=2) completed: dataset factors all SUCCESS and JAX-vectorised with one compile per factor search, but the hierarchical factor never updated (0/50 SUCCESS: 27 BAD_PROJECTION + 23 FAILURE), so the parent came back as the prior. The EP arm cannot estimate the slope scatter with the Laplace projection; the moment-matching cure (draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md) is the gate — human decision. Still open: graphical array 342348_[0-24], joint fit 342350_0, EP arm 342351_0.

## Runs

- 342348_[0-24] — open — gpu — 2026-09-08 — n25_scale_up: one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 342350_0 — open — gpu — 2026-09-08 — n25_scale_up: joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 342351_0 — open — ral — 2026-09-08 — n25_scale_up: EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix

## Log

- 2026-09-24 — note — 343299 finding: BAD_PROJECTION = Hessian at the mode not finite or not negative-definite (scale parameter driven to a limit); FAILURE = line search failed and the mean field was handed back unchanged. This is the Laplace-on-scatter caveat (autofit/graphical/README.md §3.5, analytic_gaussian leg B) at 100 % on the lensing model: per-lens slope widths 0.002-0.05 are far tighter than the scatter prior, so the tilted density in sigma sits at the boundary.
- 2026-09-24 — run — 343299 finished — wall 5:20: n25_scale_up: EP witness rerun on the decoupled --use_cpu script (slope_hierarchy_scale#4), JAX vectorised likelihood on the CPU backend, no pool, MAX_STEPS=2 via sbatch --export; stale 342410 output parked as ep_dead_342410 — COMPLETED 2026-09-16 02:03 BST, MAX_STEPS=2, 25 lenses, JAX-on-CPU, no pool: 50 'jit compiling vectorized' lines = one compile per factor search (2 steps x 25), confirming draft/refactor/autofit/ep_analysis_level_compile_cache.md. Every dataset factor SUCCESS (2/2 each) BUT the hierarchical factor is fully STALE: HierarchicalFactor0 50 rows = 27 BAD_PROJECTION + 23 FAILURE, zero SUCCESS (PriorFactor239 and PriorFactor263 also stale); library STALE FACTORS warning fired. Parent recovery printed exactly the prior: mean 2.0000 ± 0.7071, sigma 0.5000 ± 0.3536 (prior TG(2,1) / TG(0.5,0.5); truth sigma 0.1). EP output local at output/sample_n25_seed42/ep/expectation_propagation/a7ec60f07f4261afcb98b2adef484199/ (ep_history.csv, ep_diagnostics.results)
- 2026-09-15 — run — 343299 submitted: n25_scale_up: EP witness rerun on the decoupled --use_cpu script (slope_hierarchy_scale#4), JAX vectorised likelihood on the CPU backend, no pool, MAX_STEPS=2 via sbatch --export; stale 342410 output parked as ep_dead_342410
- 2026-09-15 — run — 342410 failed — wall 11:05: n25_scale_up: EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0 — JAX-on-CPU path, no pool: 76 factor searches (~3 EP steps of 25) then LLVM JIT section memory exhausted 64 GB; aborted 2026-09-10 09:29 (slope_hierarchy_scale#3 phase; compile-memory bug filed against PyAutoFit)
- 2026-09-09 — run — 342410 submitted: n25_scale_up — EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0
- 2026-09-08 — run — 342351_0 submitted: n25_scale_up — EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 2026-09-08 — run — 342350_0 submitted: n25_scale_up — joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 2026-09-08 — run — 342348_[0-24] submitted: n25_scale_up — one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 2026-07-22 — note — question: Does hierarchical slope recovery hold at N=25 to 50 [archive/tasks/slope_hierarchy_scale/n25_scale_up.md]
