---
name: warn-unretired-writeback-loop
enabled: true
event: file
action: warn
conditions:
  # Fires on a full-table-replace BigQuery load — the `bq load --replace` shell
  # form AND the `bq(['load', '--replace', ...])` array-exec form this codebase's
  # writeback scripts actually use (see _tmp-p40-writeback-bq.mjs).
  - field: content
    operator: regex_match
    pattern: \bload\b[\s\S]{0,80}--replace\b|--replace\b[\s\S]{0,80}\bload\b
  # ...wrapped in a construct that keeps running unattended: setInterval, a
  # `while(true)` pump, or a node-cron schedule. A one-shot `bq load --replace`
  # (run once, exits) is NOT what burned us — it's the loop that outlives its
  # sweep and nobody remembers to kill.
  - field: content
    operator: regex_match
    pattern: setInterval\s*\(|while\s*\(\s*true\s*\)|while\s+true\b|while:\s*true|cron\.schedule\(
  # Opt-out by convention (mirrors warn-bq-write-without-dedup-key's `dedup`
  # marker): reference either token ANYWHERE in the file — a comment, a var
  # name, a call to a shared liveness helper — and this clears. A loop with
  # NEITHER token is what trips the warn.
  - field: content
    operator: not_contains
    pattern: RETIREMENT_CHECK
  - field: content
    operator: not_contains
    pattern: LIVENESS_CHECK
  # Code only — never tests, dist, node_modules, or docs.
  - field: file_path
    operator: regex_match
    pattern: ^(?!.*(\.(test|spec)\.(ts|js|mjs)|node_modules/|/dist/|docs/)).*\.(mjs|js|ts|sh|py)$
owner: ronin
co_sign: megazord
---

⚠️ **WARN: un-retired full-table-replace writeback loop.**

This file runs a `bq load --replace` (full-table-replace) inside a construct that keeps it running unattended (`setInterval` / `while(true)` / a cron schedule) — with no retirement or liveness check anywhere in the file.

**The invariant (OB1-MWM-META-001, source of the class):** *any background writeback loop that does a full-table-replace must carry an explicit retirement/liveness check. It cannot be left running on the assumption a human will remember to kill it once its originating sweep ends.*

**Why this is a WARN, not a BLOCK:** a 13-hour-old background loop (`_tmp-writeback-bq.mjs`) silently destroyed a real BQ load before anyone noticed it was still running. The loop wasn't wrong when it was written — it became dangerous the moment its sweep ended and nobody killed it. Ratchet to BLOCK is a SHINOB1 call, not this rule's.

**Fix — add an explicit retirement/liveness check**, then reference either token below in the file so the rule clears:
- `RETIREMENT_CHECK` — a hard stop past a kill-date/TTL (e.g. `if (Date.now() > RETIRE_AFTER) { process.exit(1) }`), or a max-iteration cap.
- `LIVENESS_CHECK` — a check that the thing the loop feeds is still needed (a lockfile, a "source sweep still active" flag, a companion ticket reference) before each pass.

**Conscious opt-out** (a scratch/staging-table replace that's genuinely idempotent and never touches the live table): still add the marker — the rule can't tell staging from production, and it costs one comment line.

**Known false-positive class (gotcha #14's family):** this rule greps literal content, not parsed code — a comment or doc-string that quotes the replace flag or the loop constructs it watches for trips it exactly like real code. Describe the pattern in prose instead of quoting the flag verbatim if you need to reference it without triggering the warn.

See: `_RPI_STANDARDS/hookify/hookify.warn-bq-write-without-dedup-key.local.md` for the sibling BQ-write rule this one is modeled on. Class incident + L2/L3 split: `TRK-S-META-004`.
