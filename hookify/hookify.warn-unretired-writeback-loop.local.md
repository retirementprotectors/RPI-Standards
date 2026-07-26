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

**WHO ACTUALLY READS THIS (read before you act on anything below).** This is an `event: file` (PreToolUse) rule, so a match returns a `systemMessage` — it lands in the **violation log and on the human's pane, and never enters the writing agent's context.** The agent that writes an offending loop will not see one word of this text. (The `event: prompt` carve-out where a warn IS injected as model instructions — `OB1-INTENT-INJECT-001` — is prompt-event only and does not apply here.) **The layer that actually corrects the author is the L3 CI twin** (`.github/workflows/writeback-retirement-gate.yml` in `toMachina`, PR #2596), via a red check on the PR. Treat this rule as a signal to the human and the log; treat L3 as the teaching layer. Do not "improve" this body into agent-directed instructions — that was its original defect (caught by MEGAZORD in the `co_sign` audit, 2026-07-26, re-proved live in-harness).

**Why this is a WARN, not a BLOCK:** a 13-hour-old background loop (`_tmp-writeback-bq.mjs`) silently destroyed a real BQ load before anyone noticed it was still running. The loop wasn't wrong when it was written — it became dangerous the moment its sweep ended and nobody killed it. A literal-grep detector with a known false-positive class (below) that BLOCKS gets muted within a day — and then the gap is open *and* everyone believes it's covered (gotcha #33), which is worse than no rule.

**Ratchet criterion — the named trigger, so this is a plan and not a comment.** Ratchet to BLOCK when **the violation log shows this warn firing repeatedly on the same file with no retirement/liveness marker appearing in that file afterward.** That is the evidence the warn is not changing behaviour and only a block will. The call itself is SHINOB1's; this line exists so someone can actually make it. (Criterion set by MEGAZORD, `co_sign` audit 2026-07-26.)

**Fix — add an explicit retirement/liveness check**, then reference either token below in the file so the rule clears:
- `RETIREMENT_CHECK` — a hard stop past a kill-date/TTL (e.g. `if (Date.now() > RETIRE_AFTER) { process.exit(1) }`), or a max-iteration cap.
- `LIVENESS_CHECK` — a check that the thing the loop feeds is still needed (a lockfile, a "source sweep still active" flag, a companion ticket reference) before each pass.

**Conscious opt-out** (a scratch/staging-table replace that's genuinely idempotent and never touches the live table): still add the marker — the rule can't tell staging from production, and it costs one comment line.

**KNOWN LIMITATION 1 — the marker is FILE-scoped; the invariant is LOOP-scoped.** `not_contains` scans the whole file, so **one retired loop immunizes every other loop in the same file.** MEASURED on the live engine (MEGAZORD, `co_sign` audit 2026-07-26; independently reproduced by HIKARI before merge, positive control first): naked unretired loop → WARN fires; single retired loop → silent (correct); **two loops in one file where A carries `RETIREMENT_CHECK` and B is a naked full-table-replace forever → SILENT.** This needs no bad actor and no forgotten comment — a file grows a second loop months later and the rule goes quiet on it permanently, failing GREEN in the safe-looking direction. **Not fixed, excluded with cause:** file-granularity is what the hookify engine gives a content rule; loop-granular detection needs parsed code, which is out of scope for a v1 rule. **The identical hole exists in the L3 twin** (its marker check also spans the file's added lines). Mitigation until then: one writeback loop per file.

**KNOWN LIMITATION 2 — the marker is honor-system.** A bare `RETIREMENT_CHECK` comment with no actual check clears the rule. Inherited deliberately from the sibling `dedup` marker convention — consistency across the ruleset beats tightening one rule in isolation.

**KNOWN LIMITATION 3 — false-positive class (gotcha #14's family):** this rule greps literal content, not parsed code — a comment or doc-string that quotes the replace flag or the loop constructs it watches for trips it exactly like real code. Describe the pattern in prose instead of quoting the flag verbatim if you need to reference it without triggering the warn.

See: `_RPI_STANDARDS/hookify/hookify.warn-bq-write-without-dedup-key.local.md` for the sibling BQ-write rule this one is modeled on. Class incident + L2/L3 split: `TRK-S-META-004`.
