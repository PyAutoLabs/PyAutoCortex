# autofit_inference — PyAutoFit search benchmark on gaussian_x3: which searches find the right answer fastest

Project: autofit_inference
Issue: autofit_inference#8

## Now

Wave 2 closed and judged under gaussian_x3@2 (B5b-2, 2026-10-15): 12,750 rows at PyAutoFit pin df6d218f10cd all admitted (11,580 rows + 1,170 failed + 0 missing + 250 deferred = 13,000); the 409930 probe-first legs close: NSS 50-step leads both evidence rankings (blend 158/250, separated 210/250), Zeus JAX 0/250 blend and 190/250 separated (first among separated posterior legs). Catalogue ranks only legs with success rate >= 50 % over >= 20 attempts, the rest listed unreliable (post-hoc presentation convention, protocol §8 note; autofit_inference#12 ruling 2). Summary records published as inference-summary@3 (101 record shards). Next: after the B5b-2 PRs merge, capture the Insight fit snapshot from main under @3 and run pyauto-insight check online; then B5c (a second model family).

## Runs


## Log

- 2026-10-15 — run — 409930_[0-19] finished — wall 1:30: wave-2 probe-first remainder (B5b): Zeus JAX + NSS n_live_200_mcmc_steps_50, both datasets, 980 runs after the probe under probe-derived @2 timeouts (NSS 600 s, Zeus 1168 s); %20; submit_wave2_remainder; pin df6d218f10cd; pulled in B5b-2 — 20/20 COMPLETED (16:08-17:38 UTC); 980 remainder rows pulled by per-directory tar (20 probe rows byte-identical); all admitted under gaussian_x3@2, 0 missing; judged B5b-2
- 2026-10-15 — run — 408367_[0-389] finished — wall 1:57: scored wave 2 separated jax_cpu: 3750 runs, %60, afterany 408346:408347 — 390/390 COMPLETED; 3750 separated jax_cpu rows admitted; judged B5b
- 2026-10-15 — run — 408366_[0-379] finished — wall 1:51: scored wave 2 separated numpy: 2250 runs, %60, afterany 408346:408347 — 380/380 COMPLETED; 2250 separated numpy rows admitted; judged B5b
- 2026-10-15 — run — 408365_[0-344] finished — wall 1:46: scored wave 2 blend jax_cpu: 3500 runs, %60, afterany 408346:408347 — 345/345 COMPLETED; 3500 blend jax_cpu rows admitted; judged B5b
- 2026-10-15 — run — 408348_[0-379] finished — wall 1:53: scored wave 2 (gaussian_x3@2) blend numpy: 2250 runs, 50 seeds x 5 realisations, %60, afterany 408346:408347; submit_wave2_scored_gaussian_x3_blend_numpy — 380/380 COMPLETED; 2250 blend numpy rows admitted under gaussian_x3@2; judged B5b
- 2026-10-15 — run — 408347_[0-7] finished — wall 0:01: wave-2 separated reference builds, afterany 408245; %8 — 8/8 COMPLETED; separated reference builds
- 2026-10-15 — run — 408346_[0-7] finished — wall 0:01: wave-2 blend reference builds (MAP + build_reference), afterany 408244; %8 — 8/8 COMPLETED; blend reference builds
- 2026-10-15 — run — 408246_[0-19] finished — wall 0:03: wave-2 probe: Zeus JAX + NSS n_live_200_mcmc_steps_50, both datasets, realisation 1, seeds 0-4 (timeouts for probe-first cells); %20; submit_wave2_probe — 20/20 COMPLETED; probe rows -> @2 timeouts NSS 50-step 600 s (median 26.6 s), Zeus JAX 1168 s (median 116.8 s); pulled B5b
- 2026-10-15 — run — 408245_[0-47] finished — wall 0:26: wave-2 separated references: realisations 1,3,4,5 x numpy/jax x 6 runs; %48; submit_wave2_reference_gaussian_x3_separated; pin df6d218f10cd — 48/48 COMPLETED; separated references realisations 1,3,4,5 complete (Nautilus-only); pulled B5b
- 2026-10-15 — run — 408244_[0-49] finished — wall 1:04: wave-2 blend references (gaussian_x3@2 freeze 72d6faaf1717): realisations 2-5 x numpy/jax x Nautilus n_live=2000 + DynestyStatic nlive=1000 seeds 0-2, + JAX Nautilus seed 1 realisation 1, + NSS ln 3!; %50; submit_wave2_reference_gaussian_x3_blend; pin PyAutoFit df6d218f10cd — 50/50 COMPLETED exit 0; blend references realisations 2-5 complete (Nautilus-only: DynestyStatic ln Z disagrees 2.2-7.3 nat), JAX Nautilus seed 1 realisation 1 pulled, NSS ln 3! validated (-1.728); pulled B5b
- 2026-10-15 — run — 409930_[0-19] submitted: wave-2 probe-first remainder (B5b): Zeus JAX + NSS n_live_200_mcmc_steps_50, both datasets, 980 runs after the probe under probe-derived @2 timeouts (NSS 600 s, Zeus 1168 s); %20; submit_wave2_remainder; pin df6d218f10cd; pulled in B5b-2
- 2026-10-14 — note — gaussian_x3@2 frozen (autofit_inference 72d6faaf1717, protocol 11 A2) before any scored run; A4 gate met (PyAutoFit df6d218f1). Dry run 408236 on ral: pin imports, RAL 4-7x faster than the laptop pilot (laptop-derived timeouts are lenient); zeus missing from shared venv, carried in the private pin. Survey correction: separated committed realisation is data_seed 2.
- 2026-10-14 — run — 408367_[0-389] submitted: scored wave 2 separated jax_cpu: 3750 runs, %60, afterany 408346:408347
- 2026-10-14 — run — 408366_[0-379] submitted: scored wave 2 separated numpy: 2250 runs, %60, afterany 408346:408347
- 2026-10-14 — run — 408365_[0-344] submitted: scored wave 2 blend jax_cpu: 3500 runs, %60, afterany 408346:408347
- 2026-10-14 — run — 408348_[0-379] submitted: scored wave 2 (gaussian_x3@2) blend numpy: 2250 runs, 50 seeds x 5 realisations, %60, afterany 408346:408347; submit_wave2_scored_gaussian_x3_blend_numpy
- 2026-10-14 — run — 408347_[0-7] submitted: wave-2 separated reference builds, afterany 408245; %8
- 2026-10-14 — run — 408346_[0-7] submitted: wave-2 blend reference builds (MAP + build_reference), afterany 408244; %8
- 2026-10-14 — run — 408246_[0-19] submitted: wave-2 probe: Zeus JAX + NSS n_live_200_mcmc_steps_50, both datasets, realisation 1, seeds 0-4 (timeouts for probe-first cells); %20; submit_wave2_probe
- 2026-10-14 — run — 408245_[0-47] submitted: wave-2 separated references: realisations 1,3,4,5 x numpy/jax x 6 runs; %48; submit_wave2_reference_gaussian_x3_separated; pin df6d218f10cd
- 2026-10-14 — run — 408244_[0-49] submitted: wave-2 blend references (gaussian_x3@2 freeze 72d6faaf1717): realisations 2-5 x numpy/jax x Nautilus n_live=2000 + DynestyStatic nlive=1000 seeds 0-2, + JAX Nautilus seed 1 realisation 1, + NSS ln 3!; %50; submit_wave2_reference_gaussian_x3_blend; pin PyAutoFit df6d218f10cd
- 2026-10-08 — result — wave-1 pilot (gaussian_x3@1, local CPU, PyAutoFit 0dbf258c4f5e pre-A2) stopped at 223 of 520 runs by the B3 wrap-up ruling; 297 deferred to wave 2 on RAL partition ral; ranks nothing — rows in autofit_inference results/searches/
- 2026-10-08 — note — ledger opened
