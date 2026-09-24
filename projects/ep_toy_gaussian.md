# ep_toy_gaussian — NUTS versus three EP fits on the #1405 collapse toy at N=50

Project: ep_toy_gaussian
Issue: ep_toy_gaussian#1

## Now

Wave 1 (n50_seed42: 342639 + 342640_[0-2]) failed on infrastructure — NUTS OOM at the 8 GB cap, EP x3 EMFILE (fixed upstream by PyAutoFit#1632/#1634, RAL mirror now a73684012). The collapse question at N=50 is unanswered. Only n5_smoke speaks so far: EP RECOVER 3/3 (parent sigma 10.14/9.96/9.83 vs truth 10, no collapse, no BIASED-TIGHT), NUTS 49.89/11.14. Next: wave 2 needs a human go, a NEW sample name (e.g. n50_seed42_w2 — never re-run into an existing sample directory) and the NUTS SBATCH memory raised above 8 GB.

## Runs


## Log

- 2026-09-24 — note — per-search overhead profile on this toy (2026-09-24, laptop, N=5, max_steps=3): 2.45 s per Dynesty factor search, ~1.47 s dynesty run_nested + ~0.98 s autofit wrapper (plots, a redundant second run_nested pass, samples writes); inside run_nested instance_from_vector is 57 % of the likelihood callback for a 1-parameter model. Speed-up prompt filed in the Mind: draft/refactor/autofit/ep_factor_search_wrapper_overhead.md
- 2026-09-24 — run — 342640 failed — wall 0:14: nuts_vs_ep_x3_n50: EP x3 on identical data, array 0-2 — all three array tasks [0-2] CRASH OSError [Errno 24] Too many open files after ~126 Dynesty factor fits each (wall ~860-880 s), no ep_history.csv; results/n50_seed42/comparison.md scores WITNESS NOT MET 0/7 on infrastructure, not science. Cause: RAL mirror PyAutoFit e354dbb6b built a Pool(1) per single-core Dynesty fit (~+8 fds per fit vs 1024 soft ulimit); fixed by PyAutoFit#1632 (merged 2026-09-15) + #1634 (merged 2026-09-17); RAL mirror now a73684012 (2026-09-19) contains both; local check 2026-09-24 on a73684012: fd count flat at 7 across 15 EP factor searches (N=5, max_steps=3)
- 2026-09-24 — run — 342639 failed: nuts_vs_ep_x3_n50: one_by_one + BlackJAX NUTS, partition ral — one_by_one completed 50/50 in 319 s (naive parent 52.470 ± 1.260, deconvolved scatter 3.142); NUTS leg OUT_OF_MEMORY at the 8 GB SBATCH cap during window adaptation, no nuts.json
- 2026-09-10 — run — 342640 submitted: nuts_vs_ep_x3_n50 — EP x3 on identical data, array 0-2
- 2026-09-10 — run — 342639 submitted: nuts_vs_ep_x3_n50 — one_by_one + BlackJAX NUTS, partition ral
- 2026-09-10 — note — question: Do three EP fits agree with NUTS at N=50 [archive/tasks/ep_toy_gaussian/nuts_vs_ep_x3_n50.md]
