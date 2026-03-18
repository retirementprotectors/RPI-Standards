# Sprint 10 Post-Merge Audit — Findings & Remediation

> Audited all 5 builders against SPRINT10_PLAN.md (1,192 lines)
> Backend code + Frontend UI checked task-by-task

---

## AUDIT SUMMARY

| Builder | Tasks | Pass | Fail | Partial | Verdict |
|---------|-------|------|------|---------|---------|
| B1 Smart Search | 3 | 3 | 0 | 0 | CLEAN |
| B2 Access Center | 12 | 9 | 1 | 2 | NEEDS FIXES |
| B3 Audit Trail | 5 | 5 | 0 | 0 | CLEAN |
| B4 AI3 Report | 4 | 4 | 0 | 0 | CLEAN |
| B5 Sidebar + FAB | 3 | 3 | 0 | 0 | CLEAN |

**27 tasks total. 24 PASS. 1 FAIL. 2 need JDM decision.**

---

## BUILDER 1: Smart Search — CLEAN

| Task | Status | Notes |
|------|--------|-------|
| SS-1: Search API | PASS | 7 parallel Firestore queries (4 client + 3 account), dedup, correct response shape |
| SS-2: SmartSearch Component | PASS | 300ms debounce, keyboard nav, grouped results, `/` shortcut, blur handling, loading/empty states |
| SS-3: TopBar wiring | PASS | Old dead input replaced, SmartSearch imported correctly |

No hookify violations. All CSS variables. Structured responses.

---

## BUILDER 2: Access Center — 3 GAPS

| Task | Status | Notes |
|------|--------|-------|
| AX-1: Carrier/Product Type | PASS | Both columns present in PortalAccessTable |
| AX-2: Status values | PASS | All 4 states (active/pending/expired/not_started) |
| AX-3: Auth tracking | PASS | auth_status cycling (none→sent→on_file) works |
| AX-4: Remove portal URL text | PASS | URL not displayed, only "Open" button |
| AX-5: Dynamic from accounts | PASS | Auto-generate reads client's accounts, no more seed data |
| AX-6: Medicare.gov | PASS | Auto-generated |
| AX-7: SSA.gov | PASS | Auto-generated as "Social Security / SSA.gov" |
| AX-8: IRS.gov | PASS | Auto-generated |
| AX-9: Auth on APIs | PASS | Authorization column with cycling on ApiAccessTable |
| **AX-10: MasterCard API** | **FAIL** | **Not included in auto-generate. Plan specifies it but builder didn't implement.** |
| **AX-11: Carrier Connect** | **UNCLEAR** | **Plan mentions it but has no detailed spec in Builder 2 section. Needs JDM decision: is this Sprint 10 or deferred?** |
| AX-12: Backend CRUD | PASS | 6 endpoints (list, get, create, update, delete, auto-generate) all working |

---

## BUILDER 3: Audit Trail — CLEAN

| Task | Status | Notes |
|------|--------|-------|
| AT-1: Audit middleware | PASS | res.json override, fire-and-forget, PHI-safe (field names only) |
| AT-2: Activities endpoint | PASS | GET / (global), GET /client/:id (scoped), POST / (manual) |
| AT-3: Wire middleware | PASS | Applied globally after auth, before routes |
| AT-4: Register routes | PASS | All 4 Sprint 10 routes registered (search, access, activities, ai3) |
| AT-5: Firestore rules | PASS | activities collection rule added, subcollections covered by wildcard |

---

## BUILDER 4: AI3 Report — CLEAN

| Task | Status | Notes |
|------|--------|-------|
| AI3-1: Data aggregation | PASS | Parallel fetch: client + accounts + access_items + activities + connected_contacts |
| AI3-2: AI3Report component | PASS | All 7 sections (Header, Personal, Estate, Accounts, Insurance, Access, Activity) |
| AI3-3: PDF generation | PASS | html2canvas + jsPDF, multi-page support, correct filename format |
| AI3-4: Wire handleAI3 | PASS | Full async flow: fetch → render hidden → capture → download. No PHI in errors |

---

## BUILDER 5: Sidebar + FAB — CLEAN

| Task | Status | Notes |
|------|--------|-------|
| SC-1: Sidebar collapse | PASS | Toggle button, localStorage persistence, icon-only at 60px |
| SC-2: Auto-collapse | PASS | useEffect watches panelOpen, restores user pref when panels close |
| SC-3: IntakeFAB | PASS | 3 actions (Quick Client, Upload Doc, Paste Data), animations, click-outside close, Escape key |

---

## REMEDIATION PLAN

### Fix 1: Add MasterCard API to auto-generate (AX-10)
**File**: `services/api/src/routes/access.ts`
**Change**: Add MasterCard to the standard APIs array in the auto-generate endpoint (alongside Medicare.gov, SSA.gov, IRS.gov)
**Spec**: `{ service_name: 'MasterCard', subheading: 'Financial and Insurance', type: 'api', category: 'financial' }`

### Fix 2: Add Carrier Connect dynamic entries (AX-11) — JDM APPROVED: ADD NOW
**File**: `services/api/src/routes/access.ts`
**Change**: In the auto-generate endpoint, after creating standard API entries, query the client's accounts for Medicare-type accounts. For each unique carrier found, create a "Carrier Connect {carrier}" portal entry:
```
{ service_name: 'Carrier Connect {carrier}', subheading: 'MAPD — Blue Button Data', type: 'portal', category: 'medicare', carrier: '{carrier}' }
```
Deduplicate by carrier name (only one entry per unique Medicare carrier).

### Cross-Builder Checks — ALL PASS
- File ownership matrix: No violations
- Hookify compliance: No hardcoded colors, no alert/confirm/prompt
- PHI safety: Audit logs field names only, AI3 errors sanitized
- TypeScript: No `any` types, all interfaces defined
- Structured responses: All API routes return `{ success, data/error }`

---

## VERIFICATION

After remediation:
1. `npm run type-check` — must pass 13/13
2. Test Smart Search: type "smith" in TopBar → see grouped client + account results
3. Test Access Center: visit /service-centers/access → select client → click Auto-Generate → see dynamic entries
4. Test Audit Trail: edit a client field → check Activity tab → see auto-logged entry
5. Test AI3: click AI3 button on Client360 → PDF downloads with all 7 sections
6. Test Sidebar: click Communications → sidebar auto-collapses → click X → sidebar restores
7. Test FAB: lightning bolt bottom-right → 3 options expand → Quick Client navigates to /intake
