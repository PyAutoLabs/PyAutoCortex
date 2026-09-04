# Euclid — phase 7: how robust are magnification estimates? model-match vs mismatch across the 10 Euclid lenses

Project: euclid
Phase: 7
State: planned
Gates:
Witness: all five model rungs run on all 10 simulated lenses (or a documented, justified reduction), source-mismatch and lens-light-leakage effects quantified separately, and a written Delaunay magnification verdict
Budget: 24:00
Runs:
Ruling:
Review-minutes: 20
Epic: euclid-dr1-prep
Filed: 2026-08-28
Migrated-from: PyAutoMind/draft/research/euclid/magnification_robustness.md

## Question

Ready when: euclid 5 accepted. Runs in parallel with euclid 6.

There are known systematics in magnification estimation: when the lens light and source model
match the simulated data (Sersics fitted to Sersics) it is fine; when there is mismatch (an MGE
is used) it breaks — for two distinct reasons. An MGE *source* is source-model mismatch; an MGE
*lens light* lets lens light "leak" into the source model and corrupt the magnification. The
Delaunay source magnification has never been validated and could carry a bug (pixel areas).

The comparison matrix, fitted against the recorded true magnification of the 10 phase-5
simulations (Sersic lens light + Sersic source):

1. **Matched** — Sersic lens light, Sersic source. The control. If it is not fine, nothing
   below is interpretable.
2. **MGE source, Sersic lens light** — isolates *source*-model mismatch.
3. **MGE lens light, Sersic source** — isolates the **lens-light leakage** channel. A
   different failure mode from (2); the two must be separated, not lumped as "MGE breaks it".
4. **MGE both** — to see whether the effects add.
5. **Delaunay source** (with Sersic and MGE lens light) — never validated. The novel leg.

Definitions matter: there is more than one magnification in play (the point/Hessian value and
the area-based ratio `A_img / A_src`). State which is compared at each rung and make sure the
phase-5 truth is the same quantity; a disagreement between the two is itself a finding.

Prior art to consult before designing the runs — do not duplicate it: the cluster epic's
`mesh_magnification_correctness` prompt already covers simulate-and-recover magnification
across every mesh variant, and its audit found `areas_for_magnification` exists for only two
mesh geometries and has no direct test. This phase is the Euclid-data instance of that
question. The user's own earlier magnification research is the origin of the "matched is fine,
mismatched breaks" intuition — surface it rather than rediscovering it.

## Witness

Acceptance, verbatim from the Mind prompt:

- All five rungs run on all 10 lenses (or a documented, justified reduction).
- Source-mismatch and lens-light-leakage effects quantified separately.
- A written robustness verdict, including a usable statement of when Euclid DR1
  magnifications can be trusted and when they cannot.
- Feeds phase 7's magnification products.

("Phase 7" there is the Mind's numbering — the catalogue phase, now Mind `Phase: 9`.)

## Where to look

- `euclid_dr1_prelim` (project row): the phase-5 simulations and their recorded true magnifications
- Mind `draft/bug/autoarray/delaunay_area_magnification_audit.md` — the source-code half (6c),
  which this phase hands its Delaunay leg to whatever it shows
- Mind `draft/test/workspaces/mesh_magnification_correctness.md` — the cluster epic's
  simulate-and-recover work; read it, do not duplicate it

## Runs

## Ruling

(none)
