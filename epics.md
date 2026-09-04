# Epics — the Cortex half

Long-running multi-phase programmes whose **science** phases live here. An
epic is split by slug across the two dashboards: the Mind holds the
development phases (prompts, issues, PRs), the Cortex holds the run-and-ruling
phases (`phases/<project>/`), and each half's card links the other. A Cortex
phase declares its membership in its own header: `Epic: <slug>` (this file's
slug) plus its `Phase: <n>`, the same join key the Mind's prompts use.

Schema per entry — the Mind's, plus one field:

```markdown
## <slug>
- title: <the programme in one line>
- ledger: <the file that holds this half's phase/gate state — a phase directory or a project ledger>
- mind-half: <slug>          # the Mind's epics.md entry for the development half; `none` if the epic moved whole
- status: <coarse, durable state — never per-phase detail>   # optional
- notes: <free text>
```

`- mind-half:` names the Mind entry by slug, or `none` when the epic moved
whole. The Mind carried a reciprocal `- cortex-half:` key until 2026-09-03,
when mind-post-cortex phase 2 removed it — nothing read it, and the pointer
now lives in the Mind entry's own `notes:` as a "Science half:" clause. This
file's `- mind-half:` stays the machine-readable half of the join.
The four split epics below moved their science
halves here in phase 4 of the birth epic (2026-09-01): `euclid-dr1-prep`
phases 4, 5, 6a and 6b (renumbered here as Cortex phases 4–7);
`jax-inference-profiling` whole; the science halves of `graphical-ep` phases
3 and 4; and `cluster-strong-lensing` phase 11.

This file is ledger: it auto-merges (`scripts/ledger_merge.py`).

---

## euclid-dr1-prep
- title: prepare the Euclid DR1 modelling pipeline, then prove it on real DR1 lenses
- ledger: phases/euclid/
- mind-half: PyAutoMind/epics.md#euclid-dr1-prep
- status: science half opens at phase 4, gated on the 3a PR and the 3b issue; 5–7 planned behind it
- notes: The Mind keeps the development phases (0–3, 8, 9) and renumbered them in
  phase 4 of the birth epic so the old 3a/3b/6a/6b/6c collisions are gone. Here,
  phase 4 is the 10-lens DR1 prelim science run, 5 the resimulator, 6 Sersic-index
  recovery (was 6a) and 7 magnification robustness (was 6b); 6c stays in the Mind as
  its `Phase: 8` because it is a source-code audit, not a run. Phase 4 gates 5, and 5
  gates 6 and 7 — as intra-Cortex sequencing (decision 54) those waits are `Ready
  when:` lines in each phase's `## Question`, not `Gates:` refs.

## gradient-slam-baseline
- title: would a gradient search dropped into a SLaM mass[1] search beat Nautilus?
- ledger: autolens_profiling/results/notes/gradient_slam/LEDGER.md
- mind-half: draft/feature/autolens_profiling/gradient_slam_mass_pix_target.md (dev leg, phase 1 gate)
- status: BORN 2026-09-04 from the retired jax-inference-profiling; phase 1 gated on the dev leg

## graphical-ep
- title: expectation propagation as the scalable alternative to graphical joint fits
- ledger: PyAutoMind/draft/research/graphical_ep/ep_campaign.md
- mind-half: PyAutoMind/epics.md#graphical-ep
- status: both science phases planned; the projects are dormant and the campaign's
  development phases run first
- notes: Two science phases, one per project — `slope_hierarchy/n25_scale_up` (the
  optional N=25–50 scale-up of a project that answered all four of its goals at N=5)
  and `ic50_workspace/ep_scale_up` (EP end to end on the real IC50 model, with the
  derived-variable handling used exactly as it exists). Both wait on the campaign's
  Mind phase 2 being issued — `Ready when:` lines, not `Gates:` refs, until that
  prompt has an issue to point at. A planned phase on a dormant project is legal.

## cluster-strong-lensing
- title: the Source & Cluster arc — cluster mass modelling and pixelized source inference
- ledger: PyAutoMind/draft/feature/autolens/source_cluster_arc.md
- mind-half: PyAutoMind/epics.md#cluster-strong-lensing
- status: one science phase (arc phase 11), planned behind the arc's phase 10
- notes: Only the arc's line 11 — the feasibility study for joint gradient-based
  inference of cluster mass plus pixelized sources — is a run-and-ruling phase; the
  rest of the twelve are development. It is filed under `phases/inference_programme/`
  because that is the project whose RAL tree and profiling harness its runs would use.
  The arc's `Phase: 10` collision with `cluster_regime_narrative.md` is noted in the
  Mind's arc ledger, not fixed here.
