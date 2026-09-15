# slope_hierarchy_scale — Hierarchical slope recovery with graphical and EP at N=25 to 50

Project: slope_hierarchy_scale
Issue: slope_hierarchy_scale#2

## Now

N=25 scale-up: graphical array 342348_[0-24] and joint fit 342350_0 still open; EP witness rerun 343299 (MAX_STEPS=2, --use_cpu on the decoupled script from slope_hierarchy_scale#4) submitted 2026-09-15 after 342410 died at ~EP step 3 on LLVM compile memory. Next: pull 343299 and confirm the first factor_step ran JAX-vectorised with no pool; the full EP arm waits on the PyAutoFit compile-memory fix (draft/bug/autofit/ep_re_jit_compiles_the_vmapped_likelihood.md).

## Runs

- 342348_[0-24] — open — gpu — 2026-09-08 — n25_scale_up: one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 342350_0 — open — gpu — 2026-09-08 — n25_scale_up: joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 342351_0 — open — ral — 2026-09-08 — n25_scale_up: EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 343299 — open — ral — 2026-09-15 — n25_scale_up: EP witness rerun on the decoupled --use_cpu script (slope_hierarchy_scale#4), JAX vectorised likelihood on the CPU backend, no pool, MAX_STEPS=2 via sbatch --export; stale 342410 output parked as ep_dead_342410

## Log

- 2026-09-15 — run — 343299 submitted: n25_scale_up: EP witness rerun on the decoupled --use_cpu script (slope_hierarchy_scale#4), JAX vectorised likelihood on the CPU backend, no pool, MAX_STEPS=2 via sbatch --export; stale 342410 output parked as ep_dead_342410
- 2026-09-15 — run — 342410 failed — wall 11:05: n25_scale_up: EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0 — JAX-on-CPU path, no pool: 76 factor searches (~3 EP steps of 25) then LLVM JIT section memory exhausted 64 GB; aborted 2026-09-10 09:29 (slope_hierarchy_scale#3 phase; compile-memory bug filed against PyAutoFit)
- 2026-09-09 — run — 342410 submitted: n25_scale_up — EP arm rerun on the JAX-on-CPU path (no multiprocessing pool); replaces 342351_0
- 2026-09-08 — run — 342351_0 submitted: n25_scale_up — EP arm on the CPU partition, hpc/batch_cpu/submit_ep, max_steps 12; RAL PyAutoFit mirror 68ff9bd57 predates PyAutoFit#1580, so this arm runs without the stale-mask fixed-point fix
- 2026-09-08 — run — 342350_0 submitted: n25_scale_up — joint hierarchical NUTS fit, hpc/batch_gpu/submit_graphical
- 2026-09-08 — run — 342348_[0-24] submitted: n25_scale_up — one lens per array task, hpc/batch_gpu/submit_one_by_one, sample_n25_seed42
- 2026-07-22 — note — question: Does hierarchical slope recovery hold at N=25 to 50 [archive/tasks/slope_hierarchy_scale/n25_scale_up.md]
