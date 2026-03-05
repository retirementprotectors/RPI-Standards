# MATRIX Tab Audit — 2026-03-04

> **Status:** Handoff document. JDM needs to make delete/keep decisions on 24 dead tabs.
> **Context:** Full audit of all 79 physical tabs across 3 MATRIX spreadsheets.
> **Previous work:** 4 dead tabs already removed from TABLE_ROUTING in RAPID_CORE (uncommitted, needs deploy).

---

## Summary

| MATRIX | Total Tabs | Active | Dead/Unused | % Dead |
|--------|-----------|--------|-------------|--------|
| **PRODASH** | 23 | 19 | 4 | 17% |
| **SENTINEL** | 16 | 5 | 11 | 69% |
| **RAPID** | 40 | 31 | 9 | 23% |
| **TOTAL** | **79** | **55** | **24** | **30%** |

---

## Already Done (This Session)

Changes made to RAPID_CORE (pushed to GAS, NOT yet committed to git):

1. **Removed from TABLE_ROUTING:** `_DEAL_MASTER`, `_SENTINEL_PIPELINES`
2. **Fixed naming mismatch:** `_SENTINEL_OPPORTUNITIES` → `'Opportunities'` (matches actual sheet name)
3. **Removed deprecated schema:** `_CLIENT_INVESTOR` (from TAB_SCHEMAS, TABLE_NAMES, SETUP_MATRIX.gs)
4. **Removed dead FK reference:** `_DEAL_MASTER` from CORE_Reconcile.gs

### To finish this work:
```bash
cd ~/Projects/RAPID_TOOLS/RAPID_CORE
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "v1.7.1 - Remove dead TABLE_ROUTING entries, fix Opportunities naming"
git add -A && git commit -m "v1.7.1 - Remove dead TABLE_ROUTING entries, fix Opportunities naming"
git push
```
Note: As a library, RAPID_CORE doesn't need `clasp deploy` — consuming projects reference HEAD.

---

## Decisions Needed: 24 Dead Tabs

### PRODASH_MATRIX (4 dead tabs)

| # | Tab | Rows | Why It's Dead | Recommendation | Decision |
|---|-----|------|---------------|----------------|----------|
| 1 | `_ACCOUNT_BANKING` | 1 | Schema defined in CORE_Database.gs but never populated. Zero data rows. No functional writes anywhere. | **DELETE** — if banking accounts are needed later, re-create from schema | ☐ Delete ☐ Keep |
| 2 | `_CAMPAIGN_LOG` | 1 | Header only. Campaign logging was never implemented here. | **DELETE** — _COMMUNICATION_LOG handles this now | ☐ Delete ☐ Keep |
| 3 | `_CAMPAIGN_SEND_LOG` | 1 | Replaced by `_COMMUNICATION_LOG`. MCP-Hub campaign-tools.js writes to _COMMUNICATION_LOG instead. | **DELETE** — superseded | ☐ Delete ☐ Keep |
| 4 | `_MEET_ROOMS` | 1 | Being consolidated into `_SPECIALIST_FOLDERS`. RPI-Command-Center has migration code ready. | **DELETE** after confirming consolidation is complete | ☐ Delete ☐ Keep |

### SENTINEL_MATRIX (11 dead tabs)

**Context:** SENTINEL_MATRIX is 69% dead. These tabs were scaffolded for v2 infrastructure that was never implemented. v1 uses its own per-deal spreadsheets (separate from SENTINEL_MATRIX). v2 only actively uses 3 tabs: `Opportunities`, `_PRODUCER_MASTER`, `_DEAL_VALUATIONS`.

| # | Tab | Rows | Why It's Dead | Recommendation | Decision |
|---|-----|------|---------------|----------------|----------|
| 5 | `_PARTNER_TIERS` | 1 | Zero code references anywhere. Planned partner tier system never built. | **DELETE** | ☐ Delete ☐ Keep |
| 6 | `_PRODUCER_HIERARCHY` | 1 | Zero code references. Planned org hierarchy for producers never built. | **DELETE** | ☐ Delete ☐ Keep |
| 7 | `_PRODUCER_CREDENTIALS` | 1 | Zero code references. Planned credential tracking never built. | **DELETE** | ☐ Delete ☐ Keep |
| 8 | `_COMMISSION_CYCLES` | 1 | Zero code references. Planned commission cycle tracking never built. | **DELETE** | ☐ Delete ☐ Keep |
| 9 | `_COMMISSION_DETAILS` | 1 | Zero code references. Planned commission detail storage never built. | **DELETE** | ☐ Delete ☐ Keep |
| 10 | `_STATEMENT_IMPORTS` | 1 | Zero code references. Planned statement import tracking never built. | **DELETE** | ☐ Delete ☐ Keep |
| 11 | `_RECONCILIATION_LOG` | 1 | Zero code references in SENTINEL context. (RAPID_MATRIX has its own _RECONCILIATION_LOG that IS active.) | **DELETE** | ☐ Delete ☐ Keep |
| 12 | `_SYSTEM_CONFIG` | 1 | Schema defined in v2 init function, but never written to. TODO stubs only. | **KEEP** — v2 will likely need this. Wire it up instead of deleting. | ☐ Delete ☐ Keep |
| 13 | `Tasks` | 1 | Schema defined in v2 init, `logActivity()` has TODO: "Write to Tasks tab" — never implemented. | **KEEP** — v2 task management is planned. Wire it up. | ☐ Delete ☐ Keep |
| 14 | `ActivityLog` | 1 | Schema defined in v2 init, TODO: "Write to ActivityLog" — never implemented. | **KEEP** — v2 audit trail is planned. Wire it up. | ☐ Delete ☐ Keep |
| 15 | `_ERROR_LOG` | 1 | Schema defined in v2 init, TODO: "Write to _ERROR_LOG" — never implemented. | **KEEP** — v2 error logging is planned. Wire it up. | ☐ Delete ☐ Keep |

### RAPID_MATRIX (9 dead tabs)

| # | Tab | Rows | Why It's Dead | Recommendation | Decision |
|---|-----|------|---------------|----------------|----------|
| 16 | `_SOURCE_TASKS` | 2 | Zero functional code references. Part of a planned source management system (_SOURCE_*) that was only partially built. _SOURCE_REGISTRY (55 rows) is active, but _TASKS/_HISTORY/_METRICS are not. | **DELETE** | ☐ Delete ☐ Keep |
| 17 | `_SOURCE_HISTORY` | 1 | Same as above — planned but never implemented. | **DELETE** | ☐ Delete ☐ Keep |
| 18 | `_SOURCE_METRICS` | 1 | Same as above — planned but never implemented. | **DELETE** | ☐ Delete ☐ Keep |
| 19 | `_EMAIL_INBOX_CONFIG` | 3 | Zero code references. Was likely for email inbox monitoring config that was never built. | **DELETE** | ☐ Delete ☐ Keep |
| 20 | `_IMO_LIBRARY` | 3 | Exists in RAPID_MATRIX but only SENTINEL v1 uses `_IMO_LIBRARY` (in per-deal sheets, not here). This copy is orphaned. | **DELETE** from RAPID_MATRIX (SENTINEL v1 has its own) | ☐ Delete ☐ Keep |
| 21 | `_SOCIAL_QUEUE` | 1 | Marketing-Hub schema defined but never populated. Social posting feature not built. | **DELETE** — or **KEEP** if Marketing-Hub social posting is planned soon | ☐ Delete ☐ Keep |
| 22 | `_JOB_TEMPLATES` | 1 | RIIMO has stubs but uses in-memory job definitions instead of this sheet. | **DELETE** | ☐ Delete ☐ Keep |
| 23 | `_IMPORT_MAPPINGS` | 3 | Setup-only, never read by any functional code. | **DELETE** | ☐ Delete ☐ Keep |
| 24 | `_SYSTEM_CONFIG` | 2 | Zero functional code references in RAPID context. SENTINEL has its own. | **DELETE** | ☐ Delete ☐ Keep |

---

## Key Decisions Made (This Session)

| Decision | Details |
|----------|---------|
| **SENTINEL v1 stays alive** | 16 active v1 tabs (IMO cluster, MedSupp, policies, analytics) are NOT in SENTINEL_MATRIX — they live in per-deal spreadsheets. MCP-Hub only covers 3 of 16 v1 capabilities. Don't touch v1 until v2 catches up. |
| **TABLE_ROUTING is NOT supposed to have all tabs** | It only routes cross-platform lookups. Project-internal tabs (CEO-Dashboard, SENTINEL v1 per-deal, RIIMO-only) don't need routing. |
| **_CLIENT_INVESTOR is deprecated** | Removed from schema. Was never used. |

---

## Context for Next Session

### What MCP-Hub covers vs what SENTINEL v1 covers

MCP-Hub is a **read-only rate lookup tool**. It handles:
- Commission rate lookups (MedSupp, MAPD, Life, Annuity)
- Agent comp configuration
- Carrier comparison

MCP-Hub does NOT handle (still in SENTINEL v1 only):
- IMO entity management (_IMO_CONFIG, _IMO_LIBRARY)
- IMO scenario modeling (_IMO_ANALYSIS_SCENARIOS, _IMO_COMPARISON)
- Policy data storage (_MEDSUP_POLICIES, _ANNUITY_POLICIES)
- Valuation engine (_MEDSUP_ANALYTICS, _ANNUITY_ANALYTICS)
- State-level rate overrides (_MAPD_STATE_RATES, _PDP_OVERRIDE_GRID)
- Export/sync audit trails (_EXPORT_LOG, _SYNC_LOG)

### Cleanup execution plan

Once JDM marks decisions above:

1. **Delete tabs from actual spreadsheets** — Use GAS `deleteSheet()` or manual deletion
2. **Remove from setup/schema code** — Clean RIIMO_MATRIX_Setup.gs, SENTINEL_Database.gs initializeSentinelMatrix()
3. **Remove from TABLE_ROUTING** — If any deleted tabs are routed (most aren't)
4. **Commit + deploy** affected projects
5. **Verify** nothing breaks (the whole point of "zero code refs" = safe to delete)

### Files modified (uncommitted)

| File | Changes |
|------|---------|
| `RAPID_CORE/CORE_Database.gs` | Removed _DEAL_MASTER, _SENTINEL_PIPELINES, _CLIENT_INVESTOR from TABLE_ROUTING + TAB_SCHEMAS. Fixed Opportunities naming. |
| `RAPID_CORE/CORE_Reconcile.gs` | Removed _DEAL_MASTER from _AGENT_MASTER.referencedBy |
| `RAPID_CORE/SETUP_MATRIX.gs` | Removed createClientInvestorTab() function |
| `RAPID_CORE/CORE_DevTools.gs` | Added DEBUG_ListAllMatrixTabs() utility function |

---

## How to Use This Document

1. JDM: Check the boxes above (Delete or Keep) for each of the 24 tabs
2. Hand back to Claude Code with: "Execute the MATRIX cleanup per the audit doc"
3. Claude will delete the marked tabs, clean up code, commit, and deploy

---

*Generated 2026-03-04 by Claude Code during MATRIX tab audit session.*
