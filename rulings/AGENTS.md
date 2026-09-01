# Rulings — the ledger of record

`rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md`, one file per verdict per phase.
This folder is canonical: **a verdict recorded only outside the Cortex does
not exist.** A project's own ledger (`DECISIONS.md`, `state.md`,
`RESULTS.md`) is scientific commentary — evidence, reasoning, consequences —
and cites the ruling id; it never holds a verdict the Cortex does not.

Why: on 2026-09-01 one ruling was written in up to three places and one of
them was never written at all.

## The rules

1. **Append-only.** A ruling file, once committed, is never modified or
   deleted. `scripts/ledger_merge.py` classifies an `M`, `D` or `R` entry
   under `rulings/**` as code, which leaves the branch for a human; there is
   no auto-merge path for an edited ruling.
2. **Supersede, never edit.** A wrong ruling gets a new ruling with
   `Supersedes: <old id>` — same project, same phase, later id. The new one
   becomes the phase's `Ruling:`. Chains, not trees: supersede the current
   head, never a ruling that already has a successor.
3. **`cortex.py rule` writes them.** It assigns the id, refuses to touch an
   existing file, updates the phase's `Ruling:` and `State:` in the same
   change. Write one by hand only to migrate history (phase 4), and run
   `cortex.py check` before pushing.
4. **The human's words, verbatim.** `## Ruling` is what they said; `##
   Evidence` is where to look. Paraphrase belongs in the project ledger.

## The id

`R-YYYYMMDD-nn`: the review date and a two-digit per-day sequence, global
across projects (`01`, `02`, … in the order filed that day). The filename is
the id; so is the title line (`# R-20260901-02` or `# R-20260901-02 — <one-line
summary>`). Two branches that both assign `-03` on the same day collide on the
trial-merge check in `ledger_merge.yml`, which is the point of running it
there.

## One file per phase

A ruling names exactly one phase (`Phase: phases/<project>/<slug>.md`). A
verdict spanning several phases — a REWIND — is N files with the same
`## Ruling` body, one per phase, joined by one `Batch:` slot; `cortex.py rule
--also <phase>` fans them out. `Batch:` is also how rulings filed from one
review slot are found together.

The header keys and the chain rules `check` enforces are in
[REFERENCE.md](../REFERENCE.md) "Rulings".
