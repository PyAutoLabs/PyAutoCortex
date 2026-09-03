# Batch reviews — what the human ruled, verbatim

One markdown file per **sitting**: `<YYYY-MM-DD>-<slot>.md` for the first,
`<YYYY-MM-DD>-<slot>-r<N>.md` (N ≥ 2, one per later sitting) for a rolling
slot the human comes back to — the review they submitted from the packet page
(its "submit" step produces exactly this file, committed via the page's GitHub
button or pasted to the orchestrator), or the same content dictated in-chat
and transcribed. The files are append-only in the sense that matters: a later
one never edits an earlier one, it rules on what the earlier one left open.
The batch record carries one `- review:` line per file.

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

### Follow-ups accepted
- <the human's accepted follow-ups, one per line>

## <member slug> — <HEALTH>
- decision: accept | rerun | drop | leave-to-finish | (none)
- ruled: yes | no

The human's words, verbatim, or (no note). For rerun this paragraph becomes
the rerun phase's seed; for drop it is the ruling body.
```

A later sitting is the same grammar in a numbered file: its title is either its
own stem (`# Batch review 2026-09-01-pm-r2`) or the slot's (`# Batch review
2026-09-01-pm`), it lists only the members ruled at that sitting, and `check`
resolves it against `batches/<slot>.md` like the first. `-r1` is not a name —
the first review is `<slot>.md`.

`Follow-ups accepted` is optional and is an `###`, not a `##`: `check` requires
every `##` in a review file to name a member of the slot's batch record, so a
non-member section has to sit a level down.

`<HEALTH>` ∈ `HEALTHY | SUSPECT | FAILED | RUNNING`. The four verbs are the
**whole** vocabulary — the Mind's `merge | tweak | reject | defer` belongs to
the dev surface and never appears here. Members the human left untouched are
listed with `- decision: (none)` and `- ruled: no` by the orchestrator, never
silently dropped. `cortex.py check` verifies every section names a member of
the slot's batch record and uses the grammar.

Like every file in `batches/`, this is ledger-side: it auto-merges, because a
review that cannot land unattended cannot close a board unattended.
