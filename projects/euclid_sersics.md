# euclid_sersics — Why does the lens-light Sersic index pile up at the n=5 prior edge

Project: euclid_sersics
Issue: euclid_strong_lens_modeling_pipeline#74

## Now

342696 fitted all 100 dr1_sep1_sersics lenses through vis_lp and vis_pix (100/100 tasks, walls 2:47 to 20:58) and the outputs are pulled to the local clone; that run is what the four Sersic-stage variants reuse rather than re-derive.
The variants array — baseline, wide_n, central_noise and sersic_point, the four run sequentially inside each of 100 array tasks — is being submitted to the cluster now (4 cpu / 14 GB / 18 h, partition ral); its pipeline code is euclid_strong_lens_modeling_pipeline#75 (open, CI green, awaiting the human's merge) and the Mind task is sersic-variants.
Next: pull, scrape each variant with catalogue/scripts/lens_sersic.py --unique_tag sersic_lens_model_<variant>, run the per-variant analysis script, and the human rules on the four n distributions.

## Runs


## Log

- 2026-09-12 — run — 342696_[0-99] finished — wall 20:58: euclid_sersics_two_stage: the core two-stage fit (vis_lp then vis_pix) of the 100-lens dr1_sep1_sersics sample, array 0-99, one lens per task, 8 cpu / 64 GB / 36 h on partition ral, submitted 11:43 BST; it is the run the four Sersic-stage variants reuse rather than re-derive — 100/100 tasks completed both stages (vis_lp and vis_pix); task walls 2:47 to 20:58; outputs pulled to the local clone on 2026-09-12
- 2026-09-11 — run — 342696_[0-99] submitted: euclid_sersics_two_stage: the core two-stage fit (vis_lp then vis_pix) of the 100-lens dr1_sep1_sersics sample, array 0-99, one lens per task, 8 cpu / 64 GB / 36 h on partition ral, submitted 11:43 BST; it is the run the four Sersic-stage variants reuse rather than re-derive
- 2026-09-11 — note — project born ~11:45 BST once the human confirmed the euclid_dr1 sep1 results good: 100 unanimous-success lenses from the euclid inspection tables, remodelled on the sep1 Segmentation.zip data, to explain why the lens-light Sersic index piles up at the prior edge n = 5 (June catalogue: 61 % of 2983 fits above 4.5; 67 of the chosen 100 above 4.5). Local clone /mnt/c/Users/Jammy/Science/euclid_sersics (a site copy of PyAutoLabs/euclid_strong_lens_modeling_pipeline, its own journal at wiki/project/state.md), RAL root /mnt/ral/jnightin/euclid_sersics, sync CLI hpc/sync, sample dataset/dr1_sep1_sersics (100 tiles) with the June-to-sep1 join in sample/lens_map.csv. The plan is the core two-stage run first, then the Sersic stage rerun in four variants — baseline (the June recipe on the new data), wide_n (lens n prior Uniform(0.5, 10)), central_noise (multiplicative Gaussian noise inflation A = 9, sigma = 0.17 arcsec at the vis_lp lens-light centre) and sersic_point (Sersic + 5-Gaussian point MGE, free centre, +4 params) — with the human ruling on the per-variant n distributions afterwards; nothing is pre-registered as a verdict.
- 2026-09-11 — note — ledger opened
