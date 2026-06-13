---
name: warn-bulk-delete-without-count-dryrun
enabled: true
event: bash
action: warn
# 2026-06-13 (SHINOB1): born from the chat_mirrored sweep — a cleanup job filtered
# on a DUAL-PURPOSE flag (chat_mirrored was both a test marker AND a runtime
# bookkeeping field) and swept 37 real production messages. PITR recovered them
# (net zero loss) ONLY because PITR was on. The class: bulk DELETE by a flag the
# system writes for its own bookkeeping, with no dry-run COUNT first.
#
# Sibling to block-seed-without-snapshot (which covers seed-/migrate-/backfill-
# WRITES) — this covers the DELETE/cleanup/purge side, which that rule does NOT.
# WARN not block: legitimate cleanups exist; the goal is to force the COUNT-first
# habit, not to stop deletes. Uses not_contains (ANDed) — the runtime dropped
# `exclude:` semantics. Fires only when a delete/cleanup script runs with NEITHER
# a --dry-run NOR a --count/--dry-count safety flag.
conditions:
  - field: command
    operator: regex_match
    pattern: (?:tsx|node|python3?).*(?:delete-|cleanup-|purge-|sweep-|prune-|wipe-)
  - field: command
    operator: not_contains
    pattern: --dry-run
  - field: command
    operator: not_contains
    pattern: --count
  - field: command
    operator: not_contains
    pattern: --dry-count
owner: shinob1
---

⚠️ **BULK DELETE WITHOUT A DRY-RUN COUNT**

You are running a delete/cleanup/purge script with no `--dry-run` and no `--count`. Before any bulk delete (HIPAA §164.308(a)(7) — contingency/data-integrity):

**1. Dry-run a COUNT first.** Run the EXACT filter as a COUNT and compare to the expected number. An unexpected count is the primary early-warning signal — if it doesn't match, **STOP** and explain the discrepancy before proceeding.

**2. NEVER delete by a flag the system writes for its own bookkeeping.** Dual-purpose flags (a field used as both a test marker AND a runtime field) WILL sweep real production records the runtime legitimately stamped. This is exactly what swept 37 real messages via `chat_mirrored` on 2026-06-13.
   - ✅ Delete only by a marker set **exclusively at record creation** for test data: an ID prefix (`e2e-test-`) or a field set only then (`is_test: true`).
   - ❌ A runtime/bookkeeping flag (`chat_mirrored`, `processed`, `synced`, `delivered`, …) is NEVER a safe delete filter.

**3. Confirm PITR is ON** for any collection holding conversation history, PII, or PHI. PITR turned a permanent 37-record loss into a 2-minute recovery. If PITR is not confirmed active, the delete does not proceed.

**The compliant pattern:**
```bash
npx tsx scripts/cleanup-foo.ts --count          # 1. count what the filter matches
npx tsx scripts/cleanup-foo.ts --dry-run        # 2. preview the exact records
npx tsx scripts/cleanup-foo.ts                  # 3. only after both check out
```

Reference: `reference/os/OPERATIONS.md` → "Bulk-Delete Procedure" · `reference/os/COMPLIANCE.md` → breach runbook (data-loss prevention) · [[feedback_never_delete_by_system_bookkeeping_flag]]
