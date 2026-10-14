# autofit_inference — PyAutoFit search benchmark on gaussian_x3: which searches find the right answer fastest

Project: autofit_inference
Issue: autofit_inference#8

## Now

gaussian_x3@2 frozen in autofit_inference 72d6faaf1717 before any scored run (A2+A4 gate met: PyAutoFit df6d218f1). Scored wave 2 submitted 2026-10-14 on RAL ral (11,750 runs + 20-run probe; references first) against a private PyAutoFit pin df6d218f10cd (autofit_inference#9). Next: B5b pulls, builds the JAX blend realisation-1 reference on the laptop, judges under @2.

## Runs

- 408244_[0-49] — running — ral — 2026-10-14 — wave-2 blend references (gaussian_x3@2 freeze 72d6faaf1717): realisations 2-5 x numpy/jax x Nautilus n_live=2000 + DynestyStatic nlive=1000 seeds 0-2, + JAX Nautilus seed 1 realisation 1, + NSS ln 3!; %50; submit_wave2_reference_gaussian_x3_blend; pin PyAutoFit df6d218f10cd
- 408245_[0-47] — running — ral — 2026-10-14 — wave-2 separated references: realisations 1,3,4,5 x numpy/jax x 6 runs; %48; submit_wave2_reference_gaussian_x3_separated; pin df6d218f10cd
- 408246_[0-19] — running — ral — 2026-10-14 — wave-2 probe: Zeus JAX + NSS n_live_200_mcmc_steps_50, both datasets, realisation 1, seeds 0-4 (timeouts for probe-first cells); %20; submit_wave2_probe
- 408346_[0-7] — open — ral — 2026-10-14 — wave-2 blend reference builds (MAP + build_reference), afterany 408244; %8
- 408347_[0-7] — open — ral — 2026-10-14 — wave-2 separated reference builds, afterany 408245; %8
- 408348_[0-379] — open — ral — 2026-10-14 — scored wave 2 (gaussian_x3@2) blend numpy: 2250 runs, 50 seeds x 5 realisations, %60, afterany 408346:408347; submit_wave2_scored_gaussian_x3_blend_numpy
- 408365_[0-344] — open — ral — 2026-10-14 — scored wave 2 blend jax_cpu: 3500 runs, %60, afterany 408346:408347
- 408366_[0-379] — open — ral — 2026-10-14 — scored wave 2 separated numpy: 2250 runs, %60, afterany 408346:408347
- 408367_[0-389] — open — ral — 2026-10-14 — scored wave 2 separated jax_cpu: 3750 runs, %60, afterany 408346:408347

## Log

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
