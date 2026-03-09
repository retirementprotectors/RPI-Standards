# _RPI_STANDARDS Governance Roadmap

> Consolidated from 3 open/partial plans + 5 completed Immune System milestones.
> Last updated: 2026-03-04

---

## Version History

| Version/Milestone | Date | What Shipped |
|-------------------|------|-------------|
| Hookify activation | ~Feb 15-16 | Hookify plugin enabled in settings.json. 4 new rules created (intent-session-start, intent-sendit, quality-gate-deploy-verify, quality-gate-commit-remind). CLAUDE.md updated to reflect hookify as implementation (not shell scripts). Symlinked to 18 projects. |
| OS directory consolidation | ~Feb 16-17 | 6 governance docs created in `reference/os/`: STANDARDS.md (merged from COMPLIANCE_STANDARDS + PHI_POLICY), POSTURE.md (evolved from SECURITY_COMPLIANCE), IMMUNE_SYSTEM.md (renamed from HOOKIFY_SYSTEM), MONITORING.md (merged from PROJECT_AUDIT + WEEKLY_HEALTH_CHECK), OPERATIONS.md (extracted procedures), CLAUDE_CODE_EXECUTION.md. Backward-compatible symlinks from old paths. Global CLAUDE.md updated with OS tree. 7 project CLAUDE.md files updated. 4 hookify rules updated with new paths. |
| Reference pruning | ~Feb 14 | 51 docs deleted from `reference/` (57 -> 6 keepers). 2 new hookify rules created (block-anyone-anonymous-access, block-credentials-in-config). CLAUDE.md gained GAS Gotcha #11 (appsscript.json source of truth), Documentation Maintenance Triggers section. Doc maintenance triggers prevent future drift. |
| Knowledge pipeline closed loop | ~Feb 19 | knowledge-promote.js gained Slack daily digest (DM to JDM U09BBHTN8F2), compliance-history.json trend tracking, adaptive MAX_PROMOTIONS (5-15/day based on backlog), duplicate log line fix. New hookify intent rule: intent-immune-system-check. CLAUDE.md updated with "check the immune system" signal. |
| Knowledge Machine v2 | ~Feb 20 | AI fix: `stripMarkdownFences()` unblocked all Haiku-powered classification. Improved duplicate detection (Jaccard similarity). Temporal data filter. AI-powered section-aware insertion (replaces EOF append). Reference doc routing via `procedureCategory`. Full compliance sweep (`--sweep-only` mode scans all projects against all hookify rules). Launchd schedules moved: knowledge-promote 11:15pm -> 4am, analytics-push 11pm -> 3:30am. |
| Rule growth (ongoing) | Feb 14 - Mar 3 | Hookify rules grew from 4 initial to 21 total: 10 block rules, 6 warn rules, 3 intent rules, 2 quality gates. All symlinked to 18 projects via setup-hookify-symlinks.sh. |
| Shell hooks (2A) | Mar 3 | 3 deterministic PreToolUse hooks shipped: `phi-firewall.sh` (blocks PHI in outbound comms), `enforce.sh` + `rules.json` (5 Tier 1 rules on Write/Edit), `destructive-gate.sh` (blocks dangerous Bash commands). Registered in settings.json. Belt + suspenders: hookify (instruction) + shell hooks (code). |

---

## Stream 1: Data Operating System

**Status: PHASES A-E COMPLETE — Phase F future**
**Source plan:** `radiant-scribbling-goose.md`

The 5-pillar governance framework for data quality, mirroring the Security OS structure. Every manual FIX_ correction becomes a permanent normalizer. Every normalizer becomes a defense layer for M&A imports.

### What's Built (verified 2026-03-04)

| Layer | Current State |
|-------|---------------|
| Normalizers | 16 types in `normalizeData_()`, 90+ fields mapped in `FIELD_NORMALIZERS` including product_name, plan_name, imo_name. Fires on every `insertRow()`/`updateRow()`/`bulkInsert()`. PRODUCT_TYPES bug fixed (MAPD/MedSupp). |
| Dedup | Phase 2 pre-write dedup in `dedupCheck_()` — scores incoming vs existing, auto-merge at 100 |
| Reconciliation | Phase 3 in `CORE_Reconcile.gs` — batch client/account/agent dedup scans |
| Quality Gate | `assessDataQuality()` in CORE_Database.gs — A-F scoring, required fields, canonical value checks, garbage detection, optional contact validation sampling |
| Health Check | `DEBUG_DataHealthCheck()` in IMPORT_BoBEnrich.gs — drift, orphans, blank fields, contact quality |
| Contact Validation | `FIX_ValidateContacts_()` built, 5 columns added to _CLIENT_MASTER. Awaiting first execution (JDM GAS editor). |
| FIX_ functions | 22 families (44 entry points) in `IMPORT_BoBEnrich.gs` — ad-hoc corrections with DryRun pattern |
| DEBUG_ functions | 16 diagnostic tools — distinct values, orphan scan, field quality, numeric scan |
| Validation APIs | 6 functions in `CORE_Validation_API.gs` — phone, email, address, city/state, bank routing, composite score. Built + keyed. |
| Docs | `reference/data/` has 8 files: DATA_STANDARDS (387 lines), DATA_POSTURE (91), DATA_MONITORING (106), DATA_OPERATIONS (192), DATA_SOURCE_REGISTRY, DATA_TEAM_GUIDE, CARRIER_INTEGRATION_MATRIX, CARRIER_INTEGRATION_TEMPLATE |

### Known Gaps (remaining)

- Contact validation never executed — 5,000+ clients have no quality scores yet
- 384 blank client_ids + 39 junk entries across account tabs (manual review needed)
- Drive-based enrichment not designed yet (Phase F)

### Phase A: Promote Corrections into RAPID_CORE Normalizers — COMPLETE

All normalizers already exist and are wired. Verified 2026-03-03.

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| A.1 | `normalizeProductName()` with PRODUCT_NAME_ALIASES map | P1 | **DONE** | Line 1124, 50+ entries (annuity + life corrections). |
| A.2 | `normalizePlanName()` with PLAN_NAME_ALIASES map | P1 | **DONE** | Line 1207, 139+ entries + regex typo fixes (Heathcare→Healthcare, PLATNIUM→PLATINUM) + CMS ID clearing. |
| A.3 | Wire `product_name`, `plan_name` into FIELD_NORMALIZERS + normalizeData_() | P1 | **DONE** | Lines 1146, 1149, 1234-1235 in CORE_Database.gs. |
| A.4 | Wire `imo_name: 'imo'` in FIELD_NORMALIZERS | P2 | **DONE** | Line 1152. normalizeIMOName() at line 374 with IMO_ALIASES. |
| A.5 | Epoch date guard in `normalizeAmount()` | P2 | **DONE** | Lines 764-768. Handles Date objects + epoch date strings. |
| A.6 | Deploy RAPID_CORE | P1 | **DONE** | Already deployed with normalizers live. |

**Files:** `CORE_Normalize.gs`, `CORE_Database.gs` (both in RAPID_CORE)

### Phase B: Write Data OS Documentation — COMPLETE

All 4 docs exist with real content. Verified 2026-03-03.

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| B.1 | `DATA_STANDARDS.md` — Field Registry + Canonical Values + Garbage Patterns | P2 | **DONE** | 387 lines. Full field registry across MATRIX tabs. |
| B.2 | `DATA_POSTURE.md` — Tab-level health metrics + M&A log template | P2 | **DONE** | 91 lines. PRODASH_MATRIX health summary. |
| B.3 | `DATA_MONITORING.md` — Health check design + trigger spec | P3 | **DONE** | 106 lines. DEBUG_DataHealthCheck() design. |
| B.4 | `DATA_OPERATIONS.md` — 4 playbooks | P2 | **DONE** | 192 lines. M&A Ingestion, Drive Enrichment, Periodic Maintenance, Correction→Rule. |

**Directory:** `_RPI_STANDARDS/reference/data/` (also has DATA_SOURCE_REGISTRY.md, DATA_TEAM_GUIDE.md, CARRIER_INTEGRATION_*.md)

### Phase C: Build Import Quality Gate — COMPLETE

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| C.1 | `assessDataQuality(records, tabName, options)` in CORE_Database.gs | P1 | **DONE** | Line 2785. Returns score A-F, issues, samples, recommendation. |
| C.2 | Required fields, canonical value checks, garbage detection, client_id validity | P1 | **DONE** | All checks implemented. |
| C.3 | Optional `validateContacts: true` flag via `scoreContactQuality()` | P2 | **DONE** | Line 2882. Samples 10% (max 50), cost-controlled. |
| C.4 | Export + deploy RAPID_CORE | P1 | **DONE** | Live. |

### Phase D: Build Health Check + Contact Validation — COMPLETE

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| D.1 | `DEBUG_DataHealthCheck()` in IMPORT_BoBEnrich.gs | P2 | **DONE** | Line 3422. Aggregates drift, orphans, blank fields, contact quality. |
| D.2 | `FIX_ValidateContacts_()` in IMPORT_BoBEnrich.gs | P2 | **DONE** | Line 3589. Batch validation with DryRun variant. 50/batch, 2-sec delay. |
| D.3 | 5 new fields in TAB_SCHEMAS for _CLIENT_MASTER | P2 | **DONE** | contact_quality_score, phone_valid, email_valid, address_standardized, last_validated_date (line 361). |
| D.4 | Schema flow propagation | P2 | **DONE** | Fields in RAPID_CORE schemas. |

### Phase E: Execute Remaining Data Fixes — MOSTLY COMPLETE

Executed 2026-03-03. Two items blocked on prerequisite fixes.

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| E.1 | Run `DEBUG_OrphanDiagnostic` | P3 | **DONE** | 384 blank client_ids + 39 junk. Life 99.7% healthy. |
| E.2 | Run `FIX_LinkOrphanAccountsV2` | P3 | **DONE** | 0 linkable — V1 already got them all. Remaining orphans need manual review. |
| E.3 | Run `FIX_ImportGHLOpportunities` | P3 | **DONE** | 0 to import — 605 skipped as dupes, 606 already exist. |
| E.4 | Run normalization sweep (all tabs) | P3 | **DONE** | Clients: 27 (ZIP pads + DOB). Life: 2 (dates + amounts). Annuity: 0. BDRIA: 11 (status + dates). Medicare: 3 (MAPD + MedSupp → canonical). Fixed PRODUCT_TYPES bug in RAPID_CORE, deployed. |
| E.5 | Run `FIX_ValidateContacts_()` | P3 | **UNBLOCKED** | Columns added via SETUP_AddValidationColumns. Exceeds execute_script timeout (external APIs). **Run from GAS editor:** RAPID_IMPORT → IMPORT_BoBEnrich.gs → FIX_ValidateContactsDryRun, then FIX_ValidateContacts. |

**Remaining:** E.5 only — JDM runs from GAS editor (too heavy for MCP execute_script).

### Phase F: Drive-Based Enrichment (Future Sprint)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| F.1 | Design enrichment mode for DEX intake pipeline | P4 | Not started | Claude Vision extraction from policy PDFs → structured MATRIX fields |
| F.2 | Match to existing records by policy number, client name, or carrier+product | P4 | Not started | Fill blank fields: effective_date, face_amount, premium, etc. |
| F.3 | Support both RPI existing Drive files and M&A partner files | P4 | Not started | Document design in DATA_OPERATIONS.md only |

**Dependencies (remaining):**
- Phase E can execute now (all functions built, quality gate + validation exist)
- Phase F is future — document only, no code

---

## Stream 2: Immune System Evolution

**Status: PARTIAL — 2A shipped (shell hooks), 2B-2E outstanding**
**Source plans:** `peaceful-forging-kurzweil.md` (Hooks as Layer 0) + `quizzical-pondering-chipmunk.md` (Comprehensive Immune System)

These two plans overlap heavily. Both describe the Immune System / hooks architecture. The key distinction: `peaceful-forging-kurzweil` originally proposed shell-based hooks (`enforce.sh`, `intent-router.sh`, etc.) as Layer 0. The actual implementation chose **hookify** (Python plugin with `.local.md` YAML rules) instead. `quizzical-pondering-chipmunk` was the refined, comprehensive plan that acknowledged hookify as the implementation and expanded the scope.

### What's Built (SHIPPED)

| Component | Status | Details |
|-----------|--------|---------|
| **Hookify plugin** | LIVE | Python enforcement engine at `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/`. 4 hook handlers (PreToolUse, PostToolUse, UserPromptSubmit, Stop). Rule engine with regex matching, block/warn, LRU cache (314 lines). |
| **21 hookify rules** | LIVE | 10 block rules (Tier 1), 6 warn rules (Tier 2), 3 intent rules (prompt event), 2 quality gates (bash event). All `.local.md` files with YAML frontmatter in `_RPI_STANDARDS/hookify/`. |
| **Rule propagation** | LIVE | `setup-hookify-symlinks.sh` symlinks all rules to 18 projects. One source, 18 destinations. |
| **knowledge-promote.js** | LIVE | 1091 lines. Daily 4am run. AI-powered classification (Haiku), section-aware insertion, temporal data filter, Jaccard duplicate detection, reference doc routing, compliance sweep. |
| **Compliance sweep** | LIVE | `--sweep-only` mode loads all 21 hookify rules and scans all projects. Reports to `~/.claude/compliance-sweep.md`. |
| **compliance-history.json** | LIVE | Trend tracking. Last 30 runs with per-rule violation counts. Delta calculation between runs. |
| **Slack daily digest** | LIVE | Posts to JDM DM (U09BBHTN8F2) via Slack Bot Token. Promotions, deletions, holding count, violations, top rules, pipeline stats. |
| **5 launchd agents** | LIVE | document-watcher (always-on), analytics-push (daily 3:30am), mcp-analytics (Mon 8am), claude-cleanup (Sun 3am), knowledge-promote (daily 4am). |
| **Closed loop** | LIVE | Sessions -> violations -> knowledge-promote reads violations -> compliance report updated -> CLAUDE.md adjusted -> next session smarter. |
| **6 OS reference docs** | LIVE | `reference/os/`: STANDARDS.md, POSTURE.md, IMMUNE_SYSTEM.md, MONITORING.md, OPERATIONS.md, CLAUDE_CODE_EXECUTION.md |
| **_ARCHIVED directory** | LIVE | Completed plans archived with original filenames preserved. |
| **6-layer hierarchy** | DOCUMENTED | Layer 0 (Hooks) > Layer 1 (CLAUDE.md) > Layer 2 (MEMORY.md) > Layer 3 (Knowledge Pipeline) > Layer 4 (_RPI_STANDARDS) > Layer 5 (Project CLAUDE.md) > Layer 6 (Project Code) |

### What's Next (OUTSTANDING)

#### 2A: Shell-Level Enforcement (Upgrade Hookify -> Code-Level Hooks) — COMPLETE

Deterministic shell hooks for the most critical rules — the AI cannot ignore a hook that blocks the tool call at the code level. Hookify is ~90% reliable (instruction-based). Shell hooks are 100%.

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2A.1 | Build `enforce.sh` — PreToolUse engine for Write/Edit | P2 | **DONE** | 5 rules: hardcoded-secrets, anyone-anonymous, alert-confirm-prompt, phi-in-logs, credentials-in-config. Reads rules.json companion. <500ms. |
| 2A.2 | Build `rules.json` — Tier 1 rule definitions (5 rules in JSON) | P2 | **DONE** | Companion config for enforce.sh. Documents patterns, exceptions, messages. |
| 2A.3 | Build `phi-firewall.sh` — PreToolUse on outbound comms MCP tools | P1 | **DONE** | Scans for SSN (dashed + keyword), MBI (11-char format + keyword), DOB (keyword + date). Covers Slack, Gmail, SMS, Google Chat, campaigns. |
| 2A.4 | Build `destructive-gate.sh` — PreToolUse on Bash | P2 | **DONE** | Blocks: rm -rf (broad targets), git push --force, git reset --hard, git checkout -- ., git clean -f, git branch -D, DROP TABLE, chmod 777. Each with safe alternative. |
| 2A.5 | Register shell hooks in `settings.json` alongside hookify | P2 | **DONE** | 3 PreToolUse entries: enforce.sh (Write/Edit), destructive-gate.sh (Bash), phi-firewall.sh (outbound comms regex). Live immediately — no restart needed. |

**Files:** `~/.claude/hooks/enforce.sh`, `~/.claude/hooks/rules.json`, `~/.claude/hooks/phi-firewall.sh`, `~/.claude/hooks/destructive-gate.sh`, `~/.claude/settings.json`
**Shipped:** 2026-03-03

#### 2B: Intent Router Enhancement

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2B.1 | Build `intent-router.sh` (or upgrade intent hookify rules) | P3 | Not started | Config-driven from `intent-triggers.json`. 19 trigger categories: memory, deploy, maintenance, audit, project, outbound, status, onboard, catchup, emergency, cleanup, testing, revert, report, domain-specific (CAM/C3/QUE/DAVID), architecture, meta. |
| 2B.2 | Tier 0 Full Workflow Scripts | P3 | Not started | "session launch" -> SOAP analysis + Google Doc. "post-deployment" -> debrief + delegation guide + testing guide. |
| 2B.3 | Self-extending trigger library | P4 | Not started | "make that a trigger" / "add a trigger" -> ask JDM: what phrase + what protocol, write to intent-triggers.json. |

#### 2C: Quality Gates (PostToolUse)

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2C.1 | Build `quality-gate.sh` — PostToolUse on Bash/Write/Edit | P3 | Not started | After `clasp deploy` -> verify version in stdout. After `git commit` in GAS project -> warn about commit+deploy together. |
| 2C.2 | Deploy verifier auto-check | P2 | Partially covered | `quality-gate-deploy-verify` hookify rule warns but doesn't auto-verify the output. Shell hook could parse stdout. |

#### 2D: Session Lifecycle

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2D.1 | Build `session-end.sh` — Stop hook | P3 | Not started | Diff MEMORY.md since session start. Detect [LOCKED] entries for immediate promotion. Log session stats to `session-stats.jsonl`. |
| 2D.2 | Compact context reinject | P4 | Not started | After context compaction, reinject critical rules so long sessions don't lose enforcement. |
| 2D.3 | Session duration tracking | P4 | Not started | enforce.sh writes `.session-start` timestamp on first invocation. session-end.sh reads for duration calc. |

#### 2E: Violation Analytics

| # | Item | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 2E.1 | Real-time violation logging | P3 | Not started | `enforce.sh` writes ALL matches to `~/.claude/hooks/violation-log.jsonl`. Currently hookify logs but no central violation-log exists. |
| 2E.2 | "Hot Rules" analysis | P3 | Not started | knowledge-promote.js reads violation-log.jsonl. Tier 2 rules with >10 violations/week -> graduation candidates for Tier 1. |
| 2E.3 | "Hot Projects" analysis | P3 | Not started | Projects with >20 violations/week -> audit targets. Surfaces in Slack daily digest. |
| 2E.4 | Auto-quarantine (future) | P4 | Not started | V2: auto-promote frequently violated Tier 2 rules to Tier 1. Requires confidence threshold. |

**Dependencies:**
- 2A depends on nothing (can start immediately)
- 2B depends on nothing (parallel with 2A)
- 2C depends on 2A (shell hook infrastructure)
- 2D depends on 2A (shell hook infrastructure)
- 2E depends on 2A.1 (violation logging requires enforce.sh)

---

## Recommended Execution Order

### ~~Phase 1: Critical Enforcement (P1-P2)~~ — COMPLETE (2026-03-03)

```
✅ Stream 2A: Shell hooks (phi-firewall.sh, enforce.sh, rules.json, destructive-gate.sh)
✅ Stream 1 Phase A: RAPID_CORE normalizers (already existed)
✅ Stream 1 Phases B-D: Data OS docs + quality gate + health check (already existed)
```

### ~~Phase 2: Execute Data Fixes (P3)~~ — MOSTLY COMPLETE (2026-03-04)

```
✅ E.1: DEBUG_OrphanDiagnostic — 384 blank + 39 junk. Life 99.7% healthy.
✅ E.2: FIX_LinkOrphanAccountsV2 — 0 linkable (V1 already got them all)
✅ E.3: FIX_ImportGHLOpportunities — 0 to import (605 dupes, 606 existing)
✅ E.4: Normalization sweep — all 5 tabs: 43 records fixed. PRODUCT_TYPES bug fixed in RAPID_CORE.
⏳ E.5: FIX_ValidateContacts_ — UNBLOCKED (columns added), needs GAS editor run
```

**JDM action (one-time):** RAPID_IMPORT → IMPORT_BoBEnrich.gs → `FIX_ValidateContactsDryRun`

### Phase 3: Quality of Life (P3)

Improvements that make the system smarter over time.

```
Stream 2B: Intent router enhancement
  — Config-driven trigger library, full workflow scripts.

Stream 2C: Quality gate shell hooks (PostToolUse)
  — Auto-verify deploy versions, commit+deploy enforcement.

Stream 2D: Session lifecycle hooks
  — session-end capture, session stats, context preservation.

Stream 2E: Violation analytics
  — Real-time logging, Hot Rules/Projects, trend analysis.
```

### Phase 4: Future Vision (P4)

Document now, build when ready.

```
Stream 2B.3: Self-extending trigger library
Stream 2D.2-2D.3: Compact reinject + session duration tracking
Stream 2E.4: Auto-quarantine for rule graduation
Stream 1 Phase F: Drive-based enrichment (DEX pipeline)
```

---

## Source Plans (Archived Reference)

| Plan File | Stream | Status |
|-----------|--------|--------|
| `radiant-scribbling-goose.md` | Stream 1: Data Operating System | Phases A-E COMPLETE, Phase F future |
| `peaceful-forging-kurzweil.md` | Stream 2: Immune System Evolution (merged) | 2A COMPLETE (shell hooks shipped 2026-03-03), 2B-2E outstanding |
| `quizzical-pondering-chipmunk.md` | Stream 2: Immune System Evolution (merged) | 2A COMPLETE, 2B-2E outstanding |
| `_ARCHIVED/mighty-fluttering-ripple.md` | Stream 2 (version history) | COMPLETE — hookify activation, 4 rules, 18 projects |
| `_ARCHIVED/wondrous-wiggling-music.md` | Stream 2 (version history) | COMPLETE — OS directory, 6 docs, symlinks |
| `_ARCHIVED/peppy-discovering-naur.md` | Stream 2 (version history) | COMPLETE — knowledge pipeline, Slack digest, compliance-history.json |
| `_ARCHIVED/crystalline-toasting-gadget.md` | Stream 2 (version history) | COMPLETE — reference pruning, 51 docs deleted, 2 new block rules |
| `_ARCHIVED/bright-jumping-rabbit.md` | Stream 2 (version history) | COMPLETE — Knowledge Machine v2, AI fix, compliance sweep |
