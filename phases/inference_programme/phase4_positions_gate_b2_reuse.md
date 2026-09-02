# Inference_programme — phase 15: the legacy MGE PositionsLH evidence behind GATE B part 2

Project: inference_programme
Phase: 15
State: awaiting-ruling
Gates:
Witness: the Stage 2 and Stage 3 legacy runs are health-clean on the current stack (2026.8.17.1) with the one known invalid resume isolated, and the 5/5 vs 2/5 vs 0/4 hit counts behind Gate B part 2 recompute from their committed result rows
Budget: 0:15
Runs: 338525, 340114, 340115, 341892
Ruling:
Lane: local-dev
Review-minutes: 15
Epic: jax-inference-profiling
Filed: 2026-09-02
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-08-27 — GATE B part 2 CALLED (human-approved)

## Question

Programme Phase 4 — *PositionsLH on MGE* — asked whether the positions likelihood is safe to
run under a gradient MAP search on the MGE cell, and at what penalty factor. The 2026-08-31
REWIND left the answer standing but **provisional**: all of Stage 2's and Stage 3's evidence
is MGE and sits in `output/legacy/`, reusable only after a human ruling in a batch packet.

**The gate wording, verbatim from `DECISIONS.md` § 2026-08-27:**

> **Decision (human, 2026-08-27):** **PositionsLH is not intrinsically hostile to gradient MAP
> search on MGE; the pre-registered factor 1e8 was mis-scaled for a fixed-step searcher.** At
> factor 1e5, Prodigy(n=256, prior_box, autoconv) is **5/5 with positions on**, at parity with
> positions-off in likelihood, parameters, steps and wall. **Gate B part 1 extends to
> positions-on at factor ≤ 1e5; factor 1e8 is rejected for gradient search.**

Six caveats ride with the call (full text in that entry): (1) idealised simulator-truth
positions, and for `auto` the threshold-resolution tracer is the truth tracer, not a completed
search's max-likelihood model; (2) one cell, five seeds — Wilson-95 lower bound 0.57, which
**does not** re-establish the ≥ 99 % reliability Gate B pt 1 demonstrated positions-off at
n=256; (3) 1e5 is shown safe, not calibrated — nothing ran between 1e5 and 1e8 and SLaM's own
`factor=3` convention is untested; (4) Nautilus is unaffected either way; (5) no
`penalty_at_best` field, so "the penalty is ≈ 0 at the winner" is inferred from parity, not
measured; (6) a provenance defect — all three positions-on arms hashed to the same `target_id`
`sha256:bf3d096fda76` and every positions-on JSON recorded `threshold 0.3 / factor 1e8`
regardless of what ran — fixed in the same PR, the three arms re-derived to
`bf3d096fda76` / `cd522872a7ed` / `6b93f0e52ecd`.

**The question for this ruling:** does the legacy evidence stand, and does GATE B part 2 move
from PROVISIONAL back to CALLED?

**What the redo standard requires.** Under the MGE reuse rule these runs are reusable *pending
a human ruling in a packet*; they are not to be resubmitted. Every run here is MGE, so nothing
in this phase is quarantined by the rewind's mesh failure modes.

**The `f1e8` question the human will ask, stated cleanly.** R-20260902-01 (2026-09-02) made a
binding rule for **mesh** sources — *"pos_tauto0.2_f1e8 gives a physical solution which is
acceptable […] if a fit uses a mesh and does not have a positions.info file, it should be
assumed its result is unreliable and it cannot be used"* — and R-20260901-01 accepted
340210_9, a Nautilus run at `tauto0.2_f1e8`, as the `mge_pos_fp64` reference. Phase 4 rejects
factor 1e8. **These do not collide, and the reason is the engine, not the factor.**

- R-20260901-01 / R-20260902-01 and the certified `pos_tauto0.2_f1e8` reference rows are all
  **Nautilus**, a nested sampler that proposes by rejection and never has to walk across the
  hinge. Caveat (4) of the Gate B pt 2 call says exactly this, and this phase's own Stage-2
  Nautilus pair measures it: at `t0.3_f1e8` on MGE, logZ moves by at most 0.022 nats across
  5 seeds (see Witness).
- Phase 4's "1e8 rejected" is a statement about **fixed-step gradient MAP search** (Prodigy).
  It is transit damage, not a moved optimum.
- The mesh positions rule does not reach MGE at all: MGE sources are not subject to the
  Inversion demagnified-source bias that R-20260901-03 found, which is why the REWIND put MGE
  in `legacy/` and mesh in `legacy_wrong/` in the first place.

So the accepted mesh references may keep `f1e8` while gradient searches on MGE are capped at
`≤ 1e5`; what the ruling must decide is whether that split reads as intended, not whether one
of the two is wrong.

**Stage 1 has no SLURM job.** The threshold/plateau/argmax-switch characterisation
(`phase_04_positions/RESULTS.md` "Findings" 1–4) was run on CPU from
`scripts/misc/searches/positions_transects.py` with `JAX_ENABLE_X64=True`, not on RAL. Its
artefacts are `transects/transect_{a,b,c}.json` + `.png` in the repo, and there is no run dir
and no job log to health-check. It is cited below by artifact alone.

## Witness

Every number below was recomputed from the committed result rows in
`autolens_profiling/results/searches/{nautilus,multi_start_prodigy_autoconv}/imaging/mge/hst/`
on `main`, not copied from the write-up. Hits are Phase 3's coded rule: ≥ 1 lane at
≥ 31784.782.

**Stage 2 — Nautilus is inert on logZ and the mode, but not a strict no-op** (RESULTS.md
223–247; the 2026-08-27 correction). Per seed, positions-off (340114_[0-4]) vs positions-on
`t0.3 f1e8` (340114_[5-9]):

| seed | logZ off | logZ on | Δ logZ | maxL off | maxL on | Δ maxL | wall off | wall on |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 31690.5038 | 31690.4961 | −0.0077 | 31786.6871 | 31786.4604 | −0.2267 | 773.5 s | 764.2 s |
| 1 | 31690.5049 | 31690.4834 | −0.0215 | 31786.7733 | 31786.7609 | −0.0124 | 734.3 s | 735.4 s |
| 2 | 31690.5046 | 31690.4854 | −0.0192 | 31786.5724 | 31786.4868 | −0.0856 | 742.1 s | 720.0 s |
| 3 | 31690.4996 | 31690.4974 | −0.0022 | 31786.6055 | 31786.4711 | −0.1344 | 716.2 s | 768.6 s |
| 4 | 31690.4789 | 31690.4851 | **+0.0062** | 31786.8945 | 31786.7256 | −0.1689 | 758.4 s | 810.4 s |

logZ agrees to **0.022 nats** (recorded 0.02). maxL is lower with positions on in **5/5**
seeds, mean **−0.1256 nats**, paired **t = −3.45** — both recomputed, matching the recorded
−0.126 / −3.45. Wall change **−2.97 % to +7.32 %**, matching the recorded −3.0 to +7.3 %.

**Stage 2 — Prodigy n=256 at `t0.3 f1e8` is 2/5** (RESULTS.md 251–269, the 2026-08-27
correction). maxL per seed (340115_[0-4]): 31764.2992 · **31785.5549** · **31787.3787** ·
31702.4803 · **16727.5248** — two rows clear 31784.782, so **2/5** under the coded rule. The
"1/5" headline used an undeclared 0.04-nat band around the positions-off plateau and is not
the rule of record. Seed 4's 16727.52 is 15,059 nats below the bar.

**Stage 3 — the hypothesis is falsified; stiffness, not tightness** (RESULTS.md 336–372).
Recomputed hit counts and walls:

| arm | job | hits | max logL range | total wall |
|---|---|---|---|---|
| positions off (CP-3) | 338525_[0-4] | **5/5** | 31787.9062 – 31787.9161 | 172.2 – 224.8 s |
| `t0.3 f1e5` | 341892_[5-9] | **5/5** | 31787.9067 – 31787.9133 | 163.1 – 297.4 s |
| `t0.3 f1e8` (Stage 2) | 340115_[0-4] | **2/5** | 16727.52 – 31787.38 | 172.7 – 553.4 s |
| `tauto0.2 f1e8` | 341892_[1-4] | **0/4** | 27913.51 – 31779.30 | 147.5 – 336.4 s |

The tighter arm (`auto` resolves to 0.200000 — see `output.341892_1.out`) fails hardest; the
same 0.3″ threshold with the factor loosened to 1e5 recovers the positions-off answer 5/5, at
the same wall band. That is the whole mechanism claim, and it holds at run level.

**The `f1e5` winner reproduces positions-off** (RESULTS.md 374–382): the five `t0.3 f1e5` max
logL values sit inside the positions-off band to 3 d.p., which is the parity the "penalty ≈ 0
at the recovered model" inference rests on. Caveat (5) stands: schema v2 has no
`penalty_at_best`, so this is inferred, not measured.

**`341892_0` is INVALID and excluded — reproduced here from the artefacts, not taken on
trust.** Its log carries `Resuming MultiStartGradient search (previous samples found).`, its
total wall is **68.24 s** against 147–336 s for its siblings, and its row records
`max_log_likelihood = 31775.78` — which under the coded rule would be a miss anyway, but the
run never sampled. It never prints `Fit Already Completed`, which is why a single-string
resume check would have passed it. Arm A is therefore **n = 4 fresh seeds**, exactly as
RESULTS.md line 333 says.

**What this phase did NOT re-verify.** Everything read out of the per-lane arrays: the
constrained lane-step rates (15–18 % off → 38–43 % f1e5 → 44–53 % f1e8 → 41–56 % tauto), the
median Prodigy step scale `d` (0.14–0.16 vs 0.21–0.22, read from the job logs' final step
lines), the out-of-unit-disk `ell_comps` fractions (216/1280 = 16.9 % off, 280/1280 = 21.9 %
f1e5, 368/1280 = 28.7 % f1e8, 315/1024 = 30.8 % tauto at best points; 25.9 % off vs 52.7 % on
at final points), the `alive` counts (241–251 of 256), and Stage 1's transect numbers. Those
are the "fraction of posterior samples with an active penalty" family of claims and they are
checkable from the run dirs and `transects/*.json` below.

**Health evidence, checked from artefacts** — `.completed` present in each run's identifier
dir; the SLURM `.err`; the `.out` tail; the row's version stamp; wall against the 0:15 budget.
Every one of the 25 `.err` files is 222 bytes / 2 lines / 2 distinct lines, holding only the
`mask_2d_util.py:564` mask-padding `UserWarning` — no `Traceback` anywhere. Every `.out` ends
`Finished.` followed by the job's closing `date`.

| job | arm | `.completed` | `.err` | `.out` ends | version | longest wall vs 0:15 | resume marker |
|---|---|---|---|---|---|---|---|
| 340114_[0-4] | nautilus, positions off, seeds 0–4 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:13 | none |
| 340114_[5-9] | nautilus, `t0.3 f1e8`, seeds 0–4 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:14 | none |
| 340115_[0-4] | prodigy n256, `t0.3 f1e8` | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:10 | none |
| 341892_[0-4] | prodigy n256, `tauto0.2 f1e8` | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:06 | **task 0 only** |
| 341892_[5-9] | prodigy n256, `t0.3 f1e5` | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:05 | none |
| 338525_[0-4] | prodigy n256, positions off (the comparator) | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:04 | none |

`338525` is also phase 14's tier — it is listed here because the Stage-3 parity claim is a
comparison *against* it, and a ruling on this phase's evidence has to include the row it is
compared to. `log_evidence` is `NaN` on every Prodigy row (MAP-only, caveat (6) of Gate B pt 1).

## Where to look

- `inference_programme` (project row), Stage 2 Nautilus:
  `output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64_seed{0-4}` (off) and
  `output/legacy/searches/nautilus/imaging/mge/hst/pos_t0.3_f1e8/hpc_a100_fp64_seed{0-4}_pos_t0.3_f1e8` (on)
- Stage 2 Prodigy:
  `output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_t0.3_f1e8/hpc_a100_fp64_n256_seed{0-4}_pos_t0.3_f1e8`
- Stage 3 Prodigy:
  `output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_{t0.3_f1e5,tauto0.2_f1e8}/hpc_a100_fp64_n256_seed{0-4}_pos_{t0.3_f1e5,tauto0.2_f1e8}`
- The positions-off comparator:
  `output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}/hpc_a100_fp64_n256_seed{0-4}`
- `logs/output/output.<job>_<task>.out` and `logs/error/error.<job>_<task>.err` on the mirror
  for all 25 — each `.out` names the result row it wrote (`Results JSON saved to:`), which is
  how the job → config-dir map above was established rather than assumed;
  `output.341892_1.out` carries the resolved `threshold=0.200000  factor=1e+08` line and
  `output.341892_0.out` the `Resuming MultiStartGradient search` line
- `autolens_profiling/results/notes/inference/phase_04_positions/RESULTS.md` (Stages 1, 2, 3)
- Stage 1, which has no run dir: `autolens_profiling/.../transects/transect_{a,b,c}.json` and
  the matching `.png`, reproduced with
  `JAX_ENABLE_X64=True python scripts/misc/searches/positions_transects.py`
- `autolens_profiling/results/notes/inference/DECISIONS.md` § 2026-08-27 (both the W2 Stage-2
  correction and the Gate B pt 2 call) and § 2026-08-31 (the REWIND)
- Committed result rows on `main`:
  `.../nautilus/imaging/mge/hst/hpc_hpc_a100_fp64_seed{0-4}[_pos_t0.3_f1e8].json` and
  `.../multi_start_prodigy_autoconv/imaging/mge/hst/hpc_hpc_a100_fp64_n256_seed{0-4}[_pos_{t0.3_f1e8,t0.3_f1e5,tauto0.2_f1e8}].json`
- The rulings that frame the `f1e8` question: R-20260901-01 (340210_9 accepted at
  `tauto0.2_f1e8`, Nautilus), R-20260901-03 (the mesh demagnified-source drop) and
  R-20260902-01 (the mesh positions rule)

## Runs

- 340114_[0-4]: legacy — gpu — submitted 2026-08-25 — wall 0:13 — Stage 2 Nautilus, positions OFF, seeds 0-4 (longest task 773.5 s)
    where: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64_seed{0-4}
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64_seed{0-4}
- 340114_[5-9]: legacy — gpu — submitted 2026-08-25 — wall 0:14 — Stage 2 Nautilus, positions ON t0.3 f1e8, seeds 0-4 (longest task 810.4 s)
    where: output/legacy/searches/nautilus/imaging/mge/hst/pos_t0.3_f1e8/hpc_a100_fp64_seed{0-4}_pos_t0.3_f1e8
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/pos_t0.3_f1e8/hpc_a100_fp64_seed{0-4}_pos_t0.3_f1e8
- 340115_[0-4]: legacy — gpu — submitted 2026-08-25 — wall 0:10 — Stage 2 Prodigy n256, positions ON t0.3 f1e8: the 2/5 arm (longest task 553.4 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_t0.3_f1e8/hpc_a100_fp64_n256_seed{0-4}_pos_t0.3_f1e8
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_t0.3_f1e8/hpc_a100_fp64_n256_seed{0-4}_pos_t0.3_f1e8
- 341892_[0-4]: legacy — gpu — submitted 2026-08-27 — wall 0:06 — Stage 3 arm A, tauto0.2 f1e8: 0/4, task 0 INVALID (silent resume, 68 s) (longest valid task 336.4 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_tauto0.2_f1e8/hpc_a100_fp64_n256_seed{0-4}_pos_tauto0.2_f1e8
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_tauto0.2_f1e8/hpc_a100_fp64_n256_seed{0-4}_pos_tauto0.2_f1e8
- 341892_[5-9]: legacy — gpu — submitted 2026-08-27 — wall 0:05 — Stage 3 arm B, t0.3 f1e5: the 5/5 arm the call rests on (longest task 297.4 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_t0.3_f1e5/hpc_a100_fp64_n256_seed{0-4}_pos_t0.3_f1e5
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}_pos_t0.3_f1e5/hpc_a100_fp64_n256_seed{0-4}_pos_t0.3_f1e5
- 338525_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:04 — the CP-3 positions-OFF n256 comparator the Stage 3 table is scored against; also phase 14's tier
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}/hpc_a100_fp64_n256_seed{0-4}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}/hpc_a100_fp64_n256_seed{0-4}

## Ruling

(none)
