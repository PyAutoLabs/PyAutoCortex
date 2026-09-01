# Batch reviews — what the human ruled, verbatim

One markdown file per slot: `<YYYY-MM-DD>-<slot>.md` — the review the human
submitted from the packet page (its "submit" step produces exactly this file,
committed via the page's GitHub button or pasted to the orchestrator), or the
same content dictated in-chat and transcribed. The batch record's `review:`
field points here.

The orchestrator parses this file at close-out: every ruling it files
(`cortex.py rule <phase> <verb> --batch <slot>`) and every follow-up issue it
opens traces back to a line here — not to a memory of a conversation.
Follow-ups are enacted in the **next** slot; a review never executes its own
follow-ups.

## Schema — the one review grammar

```markdown
# Batch review 2026-09-01-pm

- packet: batches/packets/2026-09-01-pm.html
- reviewed-at: 2026-09-01T17:10Z
- review-minutes-actual: 18

## <member slug> — <HEALTH>
- decision: accept | rerun | drop | leave-to-finish | (none)
- ruled: yes | no

The human's words, verbatim, or (no note). For rerun this paragraph becomes
the rerun phase's seed; for drop it is the ruling body.
```

`<HEALTH>` ∈ `HEALTHY | SUSPECT | FAILED | RUNNING`. The four verbs are the
**whole** vocabulary — the Mind's `merge | tweak | reject | defer` belongs to
the dev surface and never appears here. Members the human left untouched are
listed with `- decision: (none)` and `- ruled: no` by the orchestrator, never
silently dropped. `cortex.py check` verifies every section names a member of
the slot's batch record and uses the grammar.

Like every file in `batches/`, this is ledger-side: it auto-merges, because a
review that cannot land unattended cannot close a board unattended.
