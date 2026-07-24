---
name: block-bridge-join-bypass
event: pre-write, pre-edit
check: check_bridge_join_invariant.sh
severity: BLOCK
scope: MZD-DATA-601
introduced: 2026-07-23
owner: shinob1
---

# block-bridge-join-bypass

Blocks `Write` / `Edit` tool calls whose **new** content references a MWM signal table
(`medicare_signals` / `retirement_signals`), reads `master_record_id`, and does **not**
bridge through `call_transcripts` (nor carry an explicit `bridge-join-exempt` marker).

This is the **L2 write-time** half of the MWM DATA bridge-join invariant. The **L3
merge-time** half is the toMachina CI check `bridge-join-invariant-gate.yml`
(MZD-DATA-602). L1 is the prose in the relaunch disco + the signal-feed contract.

## The invariant

Contract `docs/warriors/megazord/contracts/mwm-signal-feed.contract.md` §3–§4:

> A call-derived signal row's own `master_record_id` is **often NULL**. To get the person
> key you must **JOIN signals → `call_transcripts` USING (recording_id)** and take
> `t.master_record_id`. A signal-table-only count undercounts people (347/2138 vs the
> correct board-bridged 366/2504). *Always bridge through `call_transcripts`.*

Since 2026-07-14 this invariant has been **L1-only** — declared in prose, enforced by
nothing. The 2026-07-23 DIPSET completion audit named that as one of three governance
gaps that let DATA drift half-built for nine days. This rule closes the write-time half.

## Why

The one invariant that keeps every MWM signal attributable to the **right person** was
guarded by documentation alone. A new query that reads a signal row's own
`master_record_id` (frequently NULL) instead of bridging silently mis-attributes or drops
people — and nothing caught it at write time. A grep-time gate on new DATA code makes the
bypass visible the moment it is typed.

## Effect

When the rule fires and blocks:
- The Write/Edit is rejected before it executes.
- The message shows the correct bridge-join pattern and the escape hatch.
- A violation is logged to `~/.claude/hooks/violation-log.jsonl`.

## Allow path (escape hatch — "never silent omission")

Exactly one documented direct-read is legitimate: the **CRM-notes source**
(`run_tag='crm-notes-*'`, `recording_id=NULL`, contract §7) has no call to bridge through,
so it reads `master_record_id` natively. That path — and any other genuinely
bridge-less-by-design read — **declares** itself with a marker on the read:

```
// bridge-join-exempt: crm-notes source has recording_id=NULL, master_record_id native
```

The exception is stated, not hidden — the same doctrine the disco-compliance gate enforces.

## Scope (blast radius, on purpose)

- **Code files only** — `.ts .tsx .js .jsx .mjs .cjs .sql .py`. Prose (`.md`/`.html`/`docs`)
  is skipped; the contract and disco docs mention these tokens legitimately.
- **New content only** — the check reads the Write `content` / Edit `new_string`, never a
  whole pre-existing file. Pre-existing consumers are grandfathered (validated live
  2026-07-23: `_tmp-board-assembler.mjs` reads pre-resolved NDJSON + `enriched_clients`
  and `gt-qa-gate.mjs` already joins on `recording_id` — neither is the anti-pattern).
- **Fail-open** on any tooling gap (missing `jq`, unreadable input) — never brick a write.

## Belt + suspenders

Companion L3 CI check `bridge-join-invariant-gate.yml` (MZD-DATA-602) evaluates the same
invariant over a PR's **added diff lines** at merge time — the unbypassable suspenders to
this per-worktree-fragile hookify rule, exactly as `phi-cases-gate.yml` backs
`block-case-roadmap-in-repo`.

## Scope id

`MZD-DATA-601` — MWM DATA relaunch (`ob1-mwm-data-relaunch-v1.0.html`), governance L2/L3.
