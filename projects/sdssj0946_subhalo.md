# sdssj0946_subhalo — Reproduce He et al. 2025 SDSSJ0946+1006 luminous subhalo on RAL A100 GPUs

Project: sdssj0946_subhalo
Issue: none

## Now

Luminous subhalo converged at n_live 2400; its broad mass matches H25 (shared centre, log10 m200 9.5 +0.7/-1.1). Open: luminous - dark +5.8 vs H25 +16. 4 end-to-end luminous repeats (415448) running.

## Runs

- 415448 — open — gpu — 2026-11-14 — Luminous end-to-end repeat experiment: array 0-3, each a fresh SLaM chain + luminous subhalo (n_live 2400) into h25_rep1..4, to measure how much the luminous result depends on the earlier phases (e.g. source_pix[2] regularization)

## Log

- 2026-11-14 — note — Correction to the 2026-11-14 result: H25 also share the subhalo mass and light centre (Sec. III.6), and their luminous mass is just as broad (log10 m200 9.5 +0.7/-1.1, c 1.7 +1.2/-0.9), so the unbounded luminous mass matches H25 rather than differing from it. Still different: luminous - dark +5.8 vs H25 +16.
- 2026-11-14 — result — Luminous convergence check (415324, n_live 2400 vs 1200): log Z -850.02 vs -850.44, log10 m200 9.07 vs 8.96, log10 c 1.68 vs 1.77, all within errors, so Nautilus is converged. The human's reading: the luminous subhalo removes the dark matter model rather than both being in the posterior, and its mass is unbounded, so it is not quite the same as H25. Checked: m200 95% range 10^7.3-10^10.5 (12% below 10^8, upper tail grew with n_live); the Sersic is tight; the shared centre (0.48,-1.12) sits 0.21 arcsec from the dark-only subhalo (0.66,-1.02; m200 10^9.69+-0.11). Details: wiki/project/2026-11-14-luminous-convergence-and-repeats.md
- 2026-11-14 — run — 415448 submitted: Luminous end-to-end repeat experiment: array 0-3, each a fresh SLaM chain + luminous subhalo (n_live 2400) into h25_rep1..4, to measure how much the luminous result depends on the earlier phases (e.g. source_pix[2] regularization)
- 2026-11-14 — run — 415324 finished — wall 11:59: Luminous subhalo rerun on real data with n_live 2400 (2x) to check Nautilus convergence; array task 2 only
- 2026-11-13 — run — 415324 submitted: Luminous subhalo rerun on real data with n_live 2400 (2x) to check Nautilus convergence; array task 2 only
- 2026-11-13 — note — shelved (status dormant) on the human's decision in the 2026-11-13 project review
- 2026-11-11 — run — 414912 finished — wall 4:24: H25 mock: subhalo array none/dark/luminous, afterok:414911
- 2026-11-11 — run — 414911 finished — wall 4:30: H25 mock (Table 3 luminous subhalo): SLaM chain
- 2026-11-10 — run — 414912 submitted: H25 mock: subhalo array none/dark/luminous, afterok:414911
- 2026-11-10 — run — 414911 submitted: H25 mock (Table 3 luminous subhalo): SLaM chain
- 2026-11-10 — run — 414821 finished — wall 5:06: Luminous subhalo resubmitted (414796_2 crashed at start-up: concurrent search_internal removal race)
- 2026-11-10 — run — 414796 finished — wall 4:18: Subhalo array none/dark/luminous, priors mapped y->-y from H25, afterok:414795
- 2026-11-10 — run — 414821 submitted: Luminous subhalo resubmitted (414796_2 crashed at start-up: concurrent search_internal removal race)
- 2026-11-10 — run — 414795 finished — wall 0:16: Source Tune rerun on current main (Sibson + AdaptSplit log-det fixes); SP..M reused
- 2026-11-10 — run — 414796 submitted: Subhalo array none/dark/luminous, priors mapped y->-y from H25, afterok:414795
- 2026-11-10 — run — 414795 submitted: Source Tune rerun on current main (Sibson + AdaptSplit log-det fixes); SP..M reused
- 2026-11-09 — run — 414452 finished — wall 4:58: Subhalo phase array 0-2 (none/dark/luminous, n_live 1200), afterok:414440
- 2026-11-09 — run — 414440 finished — wall 0:14: SLaM chain (SP→Pix1→Pix2→L→M→ST), RAL gpu A100, base PyAuto_wt/sdssj0946-h25
- 2026-11-06 — run — 414452 submitted: Subhalo phase array 0-2 (none/dark/luminous, n_live 1200), afterok:414440
- 2026-11-06 — run — 414440 submitted: SLaM chain (SP→Pix1→Pix2→L→M→ST), RAL gpu A100, base PyAuto_wt/sdssj0946-h25
- 2026-11-06 — note — ledger opened
