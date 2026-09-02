# Inference_programme — phase 13: the legacy MGE NSS-vs-Nautilus evidence behind GATE A

Project: inference_programme
Phase: 13
State: accepted
Gates:
Witness: the Phase 2 scan's twelve legacy runs are health-clean on the current stack (2026.8.17.1), and every number GATE A was called on recomputes from their committed result rows
Budget: 10:00
Runs: 338491, 338492, 338493, 338870, 338871, 338872, 338873, 339067, 339068, 339069, 339070, 339071
Ruling: R-20260902-08
Lane: local-dev
Review-minutes: 12
Epic: jax-inference-profiling
Filed: 2026-09-02
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-08-24 — Phase 2 scan COMPLETE: H2.1 closed, NSS operating point recorded, GATE A CALLED

## Question

Programme Phase 2 — *Global MGE: Nautilus vs mainline BlackJAX NSS* — asked whether the
fork-era `af.NSS` logZ bias is a code defect or an inner-kernel tuning problem, and whether a
tuned mainline NSS beats Nautilus on wall or sample economy. The 2026-08-31 REWIND left its
answer standing but **provisional**: the MGE evidence sits in `output/legacy/`, reusable only
after a human ruling in a batch packet, and the Delaunay leg sits in `output/legacy_wrong/`.

**The gate wording, verbatim from `DECISIONS.md` § 2026-08-24:**

> **GATE A CALLED (human, 2026-08-24):** Nautilus remains the nested baseline on every model
> family; af.NSS stays mainlined as a correct, tuned alternative, not default. Phase 5's NSS
> arm is dropped. Sample economy sealed it beyond wall: Kish ESS 4,121 vs 1,315 per run on MGE
> (14× wall for equal ESS; ~15 vs ~940 likelihood evals per effective sample, reject-inclusive)
> […] Only re-opening condition (unmeasured): a GPU-only deployment where Nautilus's host-side
> proposal is the bottleneck; W6 (n_batch scan) queued to bound it.

**The question for this ruling:** does the legacy evidence stand, and does GATE A move from
PROVISIONAL back to CALLED?

**What the redo standard requires.** Under the MGE reuse rule the ten MGE runs below are
reusable *pending a human ruling in a packet* — they are not to be resubmitted, they are to be
ruled on. They are not implicated in the rewind's failure modes: the rewind quarantined mesh /
pixelization results for the λ⁴ non-PD overflow flood, the `|e| = 1.41421` box-corner
population and the demagnified-source basin (R-20260901-03), and MGE-source rows are
explicitly unaffected. All twelve runs carry the current stack stamp `2026.8.17.1`.

**One leg of the call is *not* reusable, and the ruling has to face it.** The "18.4× on
Delaunay" half of the cost finding rests on two mesh runs — 339069 (NSS mainline on
`imaging/delaunay/hst`) and 339071 (the Nautilus Delaunay re-baseline it is divided by). Both
are in `output/legacy_wrong/`, and 339071 is the very run R-20260901-03 **dropped** as a
demagnified-source solution. Under R-20260901-03 and R-20260902-01 (a mesh run without a
`positions.info` file is unreliable and cannot be used) neither is citable. They are listed
below as `legacy_wrong` so the human can see exactly which sentence of the Gate A call loses
its evidence. The MGE half — 5.0× on wall, 14× for equal ESS, ~60× per likelihood eval — is
untouched by that, and is the half that "sealed it".

Also unaffected but worth stating: the pixelization re-baseline 339795, named in the Phase 2
"Next" list, was still queued when the gate was called and did not enter it.

## Witness

Every claim below was recomputed from the committed result rows in
`autolens_profiling/results/searches/**` on `main` (version `2026.8.17.1` on all twelve),
not copied from the write-up. All walls are the run's own `Total wall` as printed by its job log.

**H2.1 closed — the logZ bias is inner-kernel under-mixing** (RESULTS.md lines 122–134,
182–188). Bias vs the Nautilus MGE bar `logZ = 31690.4965` (339070):

| arm | job | logZ | bias | max logL | sampler wall |
|---|---|---:|---:|---:|---:|
| inner 5 (anchor) | 338491 | 31698.8529 | +8.36 | 31786.6158 | 839.6 s |
| inner 30 (=2d) | 338492 | 31691.2031 | +0.71 | 31785.8257 | 4,218.6 s |
| inner 45 (=3d) | 338493 | 31690.0385 | −0.46 | 31786.3488 | 6,341.3 s |

**Operating point n200 / nd100 / inner30** (RESULTS.md lines 155–170): nd20 (338871) 6,138.4 s
→ nd100 (338870) 3,528.2 s = 1.74× at ~constant eval count; n500 (338872) 9,966.2 s; n1000
(338873) 20,265.9 s.

**5/5 seeds, +1.0 ± 0.4 nats vs Nautilus** (RESULTS.md lines 174–188). logZ at the operating
point: seed 42 (338870) 31691.3524 · 43 (339067_0) 31690.9828 · 44 (339067_1) 31691.6948 ·
45 (339067_2) 31691.5347 · 46 (339067_3) 31692.0366. Mean 31691.5202, sample std 0.3919,
range [31690.9828, 31692.0366] → **+1.02 ± 0.39 nats** above 31690.4965. Max logL 31786.2299–
31786.3391, i.e. within 0.55 nats of the truth bar 31786.782 every time; sampler walls
3,429.6–3,528.2 s, spread 2.9 %.

**dlogz −10 is nearly free** (RESULTS.md 190–196): 339068 gives max logL 31787.3269 — the
highest NSS max logL on record — at 3,688.0 s (+4.5 % on the nd100 wall).

**Wall ratio 5.0× on MGE**: 3,528.2 s (338870) ÷ 706.5 s (339070 sampler wall) = **4.99×**.
**Wall ratio 18.4× on Delaunay**: 34,725.8 s (339069) ÷ 1,891.3 s (339071) = **18.36×** —
**this one is computed from two `legacy_wrong` runs and is the leg at risk.**

**Sample economy** (RESULTS.md 249–276) is the leg the human said sealed the gate: Kish ESS
4,121 (Nautilus, 62,208 reject-inclusive evals, ~15 evals/ESS) vs 1,315 (NSS operating point,
1,236,644 evals, ~940 evals/ESS). The ESS figures are derived in the write-up from each run's
stored `samples.csv`; this phase verified the eval counts and walls in the result rows but did
**not** re-derive the Kish ESS from the CSVs.

**Health evidence, checked from artefacts** — `.completed` present in each run's identifier
dir; the SLURM `.err` file; the `.out` tail; the row's version stamp; wall against the 10:00
budget. Every `.err` here is 222 bytes / 2 lines / 2 distinct lines and holds only the
`mask_2d_util.py:564` mask-padding `UserWarning` — no `Traceback` anywhere. Every `.out` ends
`Finished.` followed by the job's closing `date`. No `Fit Already Completed` and no
`Resuming …` marker on any of the twelve.

| job | cell / arm | `.completed` | `.err` | `.out` ends | version | wall vs 10:00 |
|---|---|---|---|---|---|---|
| 338491 | nss mge, inner 5 anchor | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:15 |
| 338492 | nss mge, inner 30 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 1:11 |
| 338493 | nss mge, inner 45 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 1:47 |
| 338870 | nss mge, inner30 nd100 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 1:00 |
| 338871 | nss mge, inner30 nd20 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 1:43 |
| 338872 | nss mge, inner30 n500 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 2:47 |
| 338873 | nss mge, inner30 n1000 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 5:39 |
| 339067_[0-3] | nss mge, seeds 43–46 | yes (4/4) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:59 |
| 339068 | nss mge, dlogz −10 | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 1:03 |
| 339070 | nautilus mge re-baseline | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:13 |
| 339069 | nss **delaunay** (legacy_wrong) | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 9:40 |
| 339071 | nautilus **delaunay** (legacy_wrong) | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:33 |

339070 is already ruled — R-20260901-02 accepted it as the `mge_fp64` InferenceRefs_v1
baseline — and is listed here because it is the denominator of the 5.0× ratio, not for a
second ruling. 339071 is already ruled too: R-20260901-03 **dropped** it.

## Where to look

- `inference_programme` (project row), the ten reusable MGE runs:
  `output/legacy/searches/nss/imaging/mge/hst/{hpc_a100_fp64,hpc_a100_fp64_inner30,hpc_a100_fp64_inner45,hpc_a100_fp64_inner30_nd100,hpc_a100_fp64_inner30_nd20,hpc_a100_fp64_inner30_n500,hpc_a100_fp64_inner30_n1000,hpc_a100_fp64_inner30_nd100_seed{43-46},hpc_a100_fp64_inner30_nd100_dlogz10}/`
  and `output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8`
- The two quarantined mesh runs (failure-mode documentation only):
  `output/legacy_wrong/searches/nss/imaging/delaunay/hst/hpc_a100_fp64_mainline/458f07dbe90f54a13492930e923e20a5`
  and `output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/b29ffe390c18e070b3eaba60270cb502`
- `logs/output/output.<job>[_<task>].out` and `logs/error/error.<job>[_<task>].err` on the
  mirror for all twelve jobs — each `.out` names the result row it wrote (`Results JSON saved
  to:`), which is how the job → config-dir map above was established rather than assumed
- `autolens_profiling/results/notes/inference/phase_02_nss_mainline/RESULTS.md`
- `autolens_profiling/results/notes/inference/DECISIONS.md` § 2026-08-24 (Gate A) and
  § 2026-08-31 (the REWIND that made it provisional)
- Committed result rows on `main`:
  `autolens_profiling/results/searches/nss/imaging/mge/hst/hpc_hpc_a100_fp64*.json`,
  `autolens_profiling/results/searches/nautilus/imaging/mge/hst/hpc_hpc_a100_fp64.json`,
  `autolens_profiling/results/searches/{nss,nautilus}/imaging/delaunay/hst/hpc_hpc_a100_fp64*.json`
- Rulings already standing on two of these runs: R-20260901-02 (339070, accept),
  R-20260901-03 (339071, drop)

## Runs

- 338491: legacy — gpu — submitted 2026-08-23 — wall 0:15 — NSS anchor at fork knobs (inner 5); node start 16:16 BST
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64/b51405821b58b0c5b0d03cb2790446fa
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64/b51405821b58b0c5b0d03cb2790446fa
- 338492: legacy — gpu — submitted 2026-08-23 — wall 1:11 — wave 1, inner 30 (=2d)
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30/a3d0599d72a83731a0b3a88feb3f959e
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30/a3d0599d72a83731a0b3a88feb3f959e
- 338493: legacy — gpu — submitted 2026-08-23 — wall 1:47 — wave 1, inner 45 (=3d)
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner45/0f93cae07b4b2e67f52cfd285c5e87a3
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner45/0f93cae07b4b2e67f52cfd285c5e87a3
- 338870: legacy — gpu — submitted 2026-08-23 — wall 1:00 — wave 2, nd100: the operating point
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100/7d818ae1c5d5e96eb2e940229b411b4e
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100/7d818ae1c5d5e96eb2e940229b411b4e
- 338871: legacy — gpu — submitted 2026-08-23 — wall 1:43 — wave 2, nd20
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd20/f34e1b347cfb871be4f7d3ca0e4e7e50
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd20/f34e1b347cfb871be4f7d3ca0e4e7e50
- 338872: legacy — gpu — submitted 2026-08-23 — wall 2:47 — wave 2, n_live 500 / nd125
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_n500/f918b17003b3a4c547dc99c761dcb3aa
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_n500/f918b17003b3a4c547dc99c761dcb3aa
- 338873: legacy — gpu — submitted 2026-08-23 — wall 5:39 — wave 2, n_live 1000 / nd250
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_n1000/583b9edbb652eddd72d75e659726243b
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_n1000/583b9edbb652eddd72d75e659726243b
- 339067_[0-3]: legacy — gpu — submitted 2026-08-23 — wall 0:59 — seeds 43-46 at the operating point (longest task)
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100_seed{43,44,45,46}
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100_seed{43,44,45,46}
- 339068: legacy — gpu — submitted 2026-08-24 — wall 1:03 — termination row, dlogz -10
    where: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100_dlogz10/49ffc0b1a0f54213efc58055c0da5907
    pulled_to: output/legacy/searches/nss/imaging/mge/hst/hpc_a100_fp64_inner30_nd100_dlogz10/49ffc0b1a0f54213efc58055c0da5907
- 339070: legacy — gpu — submitted 2026-08-24 — wall 0:13 — Nautilus MGE re-baseline; the denominator of the 5.0x ratio, already accepted
    where: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8
    ruled: R-20260901-02
- 339069: legacy_wrong — gpu — submitted 2026-08-24 — wall 9:40 — NSS mainline on imaging/delaunay/hst; the 18.4x numerator, quarantined mesh
    where: output/legacy_wrong/searches/nss/imaging/delaunay/hst/hpc_a100_fp64_mainline/458f07dbe90f54a13492930e923e20a5
- 339071: legacy_wrong — gpu — submitted 2026-08-24 — wall 0:33 — Nautilus Delaunay re-baseline; the 18.4x denominator, dropped as a demagnified-source solution
    where: output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/b29ffe390c18e070b3eaba60270cb502
    ruled: R-20260901-03

## Ruling

R-20260902-08 — accept
