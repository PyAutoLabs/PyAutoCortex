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

`- mind-half:` names the Mind entry by slug; the Mind's entries gain the
reciprocal `- cortex-half:` in phase 4 of the birth epic, when the split epics
(`euclid-dr1-prep` phases 4, 5, 6a, 6b; `jax-inference-profiling` whole;
`graphical-ep` phases 3/4 science halves; `cluster-strong-lensing` phase 11)
move here. Until then this file holds no entries.

This file is ledger: it auto-merges (`scripts/ledger_merge.py`).
