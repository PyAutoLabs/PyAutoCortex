# sdssj0946_subhalo — Reproduce He et al. 2025 SDSSJ0946+1006 luminous subhalo on RAL A100 GPUs

Project: sdssj0946_subhalo
Issue: none

## Now

Dark detection robust (+49 to +60); luminous beats dark by +1 to +12 per chain; light only ties luminous on h25. Running: mock none/dark/luminous/light_only on 4 repeats; luminous solution tests (415576).

## Runs

- 415569 — open — gpu — 2026-11-16 — H25 mock rep1: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415568
- 415571 — open — gpu — 2026-11-16 — H25 mock rep2: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415570
- 415573 — open — gpu — 2026-11-16 — H25 mock rep3: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415572
- 415575 — open — gpu — 2026-11-16 — H25 mock rep4: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415574
- 415576 — open — gpu — 2026-11-16 — Luminous solution tests on h25 (n_live 2400): h25mass (m200 limited to H25's 8.4-10.2), masspos / lightpos (centre limited around the mass / light solution), tuned (Nautilus n_networks 16, enlarge_per_dim 1.3, split_threshold 25, f_live 0.001). Sampling or likelihood?

## Log

- 2026-11-17 — result — Within-chain comparison (pulled 2026-11-17): dark - none +49 to +60 on all five real chains with the same H25-consistent dark subhalo; luminous - dark +6.2, +5.1, +11.8, +1.0, +11.2 (H25 +16), so luminous wins on every chain but the chain scatter is as large as the effect. On h25, light_only ties luminous (log Z -850.86 vs -850.02): the mass is not needed once the light is in. The H25 mock input reads log L 8.08 in our conversion (our light solution 8.02-8.08), so the 2x fainter gap is probably the conversion. On the h25 mock chain, luminous - dark is only +1.8 and the luminous c is too high (2.17 vs true 1.51). Details: journal section 8.
- 2026-11-17 — run — 415574 finished — wall 4:03: H25 mock rep4: fresh SLaM chain (UNIQUE_TAG h25_rep4)
- 2026-11-17 — run — 415572 finished — wall 3:56: H25 mock rep3: fresh SLaM chain (UNIQUE_TAG h25_rep3)
- 2026-11-17 — run — 415570 finished — wall 3:53: H25 mock rep2: fresh SLaM chain (UNIQUE_TAG h25_rep2)
- 2026-11-17 — run — 415568 finished — wall 3:48: H25 mock rep1: fresh SLaM chain (UNIQUE_TAG h25_rep1)
- 2026-11-17 — run — 415567 finished — wall 7:58: Real data rep4: none + dark (array 0-1, n_live 2400)
- 2026-11-17 — run — 415566 finished — wall 8:46: Real data rep3: none + dark (array 0-1, n_live 2400)
- 2026-11-17 — run — 415564 finished — wall 8:28: Real data rep2: none + dark (array 0-1, n_live 2400)
- 2026-11-17 — run — 415562 finished — wall 11:23: Real data rep1: none + dark (array 0-1, n_live 2400), within-chain luminous - dark
- 2026-11-17 — run — 415521 finished — wall 7:40: light_only rerun on the h25 chain (n_live 2400), galaxy renamed satellite after 415458_4 failed on the PyAutoLens subhalo-name assumption — light_only on h25: log Z -850.86 vs luminous -850.02
- 2026-11-16 — run — 415576 submitted: Luminous solution tests on h25 (n_live 2400): h25mass (m200 limited to H25's 8.4-10.2), masspos / lightpos (centre limited around the mass / light solution), tuned (Nautilus n_networks 16, enlarge_per_dim 1.3, split_threshold 25, f_live 0.001). Sampling or likelihood?
- 2026-11-16 — run — 415575 submitted: H25 mock rep4: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415574
- 2026-11-16 — run — 415574 submitted: H25 mock rep4: fresh SLaM chain (UNIQUE_TAG h25_rep4)
- 2026-11-16 — run — 415573 submitted: H25 mock rep3: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415572
- 2026-11-16 — run — 415572 submitted: H25 mock rep3: fresh SLaM chain (UNIQUE_TAG h25_rep3)
- 2026-11-16 — run — 415571 submitted: H25 mock rep2: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415570
- 2026-11-16 — run — 415570 submitted: H25 mock rep2: fresh SLaM chain (UNIQUE_TAG h25_rep2)
- 2026-11-16 — run — 415569 submitted: H25 mock rep1: none / dark / luminous / light_only (array 0,1,2,4, n_live 2400), afterok:415568
- 2026-11-16 — run — 415568 submitted: H25 mock rep1: fresh SLaM chain (UNIQUE_TAG h25_rep1)
- 2026-11-16 — run — 415567 submitted: Real data rep4: none + dark (array 0-1, n_live 2400)
- 2026-11-16 — run — 415566 submitted: Real data rep3: none + dark (array 0-1, n_live 2400)
- 2026-11-16 — run — 415564 submitted: Real data rep2: none + dark (array 0-1, n_live 2400)
- 2026-11-16 — run — 415562 submitted: Real data rep1: none + dark (array 0-1, n_live 2400), within-chain luminous - dark
- 2026-11-16 — result — Comparison with H25 at matched 95% intervals (H25 Table 2 errors are 95%, not 68%): our dark fit reproduces H25; no luminous fit does. H25: bright light (log L 8.4 [8.2,8.5]) with a bounded mass (log m200 8.4-10.2). Ours is either the light solution (mass does no lensing, unbounded to 10^7, light ~2x fainter than H25, luminosity conversion unchecked) or the mass solution (mass does all the lensing, light 5-13x fainter); at most 3% of any posterior lies in H25's region. Simona was right; the 2026-11-14 note that our luminous mass matches H25 was wrong (68% vs 95%). Details: journal section 5.
- 2026-11-16 — note — Correction to the 2026-11-16 result: the mass solution (NFW ~10^9.6-9.9 near the dark position) is only found on rep3 (tied with the light solution, posterior 59%) and rep1 (11 below in log L). On h25, rep2 and rep4 Nautilus barely explored it, so the earlier statement that the light solution wins by 3-15 on four chains was wrong. Both the chain and the sampler's mode-finding decide which solution appears.
- 2026-11-16 — run — 415521 submitted: light_only rerun on the h25 chain (n_live 2400), galaxy renamed satellite after 415458_4 failed on the PyAutoLens subhalo-name assumption
- 2026-11-16 — result — Repeats and tests (pulled 2026-11-16): the luminous posterior has two solutions, a light solution (bright Sersic at y 0.47, mass unconstrained) and a mass solution (NFW ~10^9.9 at the dark-fit position y 0.66, faint light). Which wins depends on the chain: light on h25 and reps 1, 2, 4; tied on rep3 (posterior 59% mass). Chain log Z varies by ~10-30 per search, so luminous - dark must be measured within each chain (none/dark only on h25 so far). Extra subhalo over-sampling changes nothing (log Z -850.02 both); independent centres on h25 leave the mass unconstrained (log Z -851.05). Details: wiki/project/2026-11-14-luminous-convergence-and-repeats.md sections 3-4
- 2026-11-16 — run — 415458 finished — wall 15:11: Subhalo tests on the h25 chain, n_live 2400: luminous_oversample (subhalo light added to the adaptive over-sampling centres), light_only (no NFW), luminous_two_centre (independent mass and light centres) — luminous_oversample and luminous_two_centre completed; light_only FAILED at start (PyAutoLens reads subhalo.mass.centre for any galaxy named subhalo)
- 2026-11-16 — run — 415448 finished — wall 27:10: Luminous end-to-end repeat experiment: array 0-3, each a fresh SLaM chain + luminous subhalo (n_live 2400) into h25_rep1..4, to measure how much the luminous result depends on the earlier phases (e.g. source_pix[2] regularization) — all 4 completed (walls 21:11, 14:53, 27:10, 15:34); pulled 2026-11-16
- 2026-11-14 — note — Simona's question (2026-11-14): something in the new run gives an unbound luminous satellite mass not seen in Qiuhan's paper, same priors, maybe a code change. Checked: her plot is our run; the projected lensing mass of the luminous NFW within 0.1-0.5 arcsec spans ~2 dex (dark fit: ~0.1 dex), so it is a real 2D non-constraint, not a projection effect. Candidate code difference: subhalo light over-sampled at only 2x2; tested by 415458_3.
- 2026-11-14 — run — 415458 submitted: Subhalo tests on the h25 chain, n_live 2400: luminous_oversample (subhalo light added to the adaptive over-sampling centres), light_only (no NFW), luminous_two_centre (independent mass and light centres)
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
