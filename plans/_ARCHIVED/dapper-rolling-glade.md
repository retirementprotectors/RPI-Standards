# Plan: Fix Multi-Doc Mail Approval Workflow

## Context

The document watcher's multi-doc split is working — it correctly splits a multi-page scan into individual labeled PDFs, uploads them to Drive, and creates approval batches. But the downstream workflow has 5 gaps:

1. **Slack "Review in RAPID_IMPORT" link is broken** — generic URL with no batch_id
2. **Single-doc MAIL notifications route to #ai-data-approvals** — should go to #service-general (actionable tasks, not notifications)
3. **Pending batches don't appear on RAPID_IMPORT home page** — no way to find them
4. **Document Type / Pipeline classification needs work** — taxonomy data issue
5. **No clear path from REVIEWING → Approved → Write** — the approval UI exists but isn't reachable

## Changes

### 1. Fix Slack per-doc links + channel routing (watcher.js)

**File:** `MCP-Hub/document-processor/src/watcher.js`

**A. Per-doc clickable "Review" links** (in `sendMultiDocScanNotification()`, ~line 303):
- Replace `_Batch:_ ${doc.batchId}` metadata text with a clickable Slack link: `<${CONFIG.rapidImportUrl}?page=approval&batch_id=${doc.batchId}|📋 Review>`
- Each document card gets its own direct link to APPROVAL_UI

**B. Footer "Review All" link** (~line 316):
- Change generic `approvalUrl` to: `<${CONFIG.rapidImportUrl}?page=training|Review All in RAPID_IMPORT>`
- Links to Training Dashboard which lists all pending batches

**C. Pass `routed_channel` for MAIL items** (in `createApprovalViaApi()` calls, ~lines 1711 and 3873):
- When `item.source === 'MAIL'`, add `routed_channel: CONFIG.slackServiceChannel` to the context payload
- GAS already supports `context.routed_channel` at line 2691 of IMPORT_Approval.gs — it will use #service-general instead of falling back to #ai-data-approvals
- This fixes BOTH single-doc and multi-doc MAIL notifications

**D. Multi-doc Slack sends per-batch notifications to #service-general** (~line 1711):
- Each per-doc `createApprovalViaApi()` call already triggers `sendApprovalNotification_()` on the GAS side
- With `routed_channel` set, each batch gets its own "Mail Review Needed" card in #service-general with a working "Review Now" link
- The multi-doc summary in #service-general provides the overview, individual batch cards provide the action items

### 2. Add pending batch list to RAPID_IMPORT home page

**File:** `RAPID_IMPORT/IMPORT_Approval.gs`

**Enhance `getApprovalQueueDepthForUI()`** (~line 4705):
- Inside the existing loop that counts pending items, accumulate batch metadata: `{ batch_id, entity_name, source_type, created_at, field_count }`
- Return a `pendingBatchList` array (newest first, capped at 10) alongside existing counts

**File:** `RAPID_IMPORT/Code.gs`

**Add pending batch list to home page HTML:**
- Add a `<div id="pending-batch-list">` container in the Approval Queue card area
- In the `getApprovalQueueDepthForUI` success handler, render clickable batch items: client name + field count + source → links to `?page=approval&batch_id=UUID`
- Compact vertical list, CSS variables for colors, hover highlight
- "More batches..." overflow link → Training Dashboard

### 3. Verify/fix taxonomy for MAIL document types

**No code changes** — data verification only:
- Check `_DOCUMENT_TAXONOMY` in RAPID_MATRIX for rows with `source = MAIL`
- If missing: run `SETUP_DocumentTaxonomy` + `SETUP_TaxonomyPhase2` to seed
- Check `_TAXONOMY_SUGGESTIONS` for accumulated misses from MAIL processing
- Promote valid suggestions via `FIX_PromoteSuggestions()`

### Execution Order

1. **Fix 1** — watcher.js Slack links + channel routing → restart watcher
2. **Fix 3** — taxonomy data check (quick verification via execute_script)
3. **Fix 2** — home page + approval depth → clasp push + deploy
4. **Test** — drop a multi-page PDF in Incoming, verify:
   - Slack notification goes to #service-general (not #ai-data-approvals)
   - Per-doc "Review" links work in Slack
   - Batches appear on RAPID_IMPORT home page
   - Clicking through to APPROVAL_UI works
   - Push/Edit/Kill → DONE → writes to MATRIX

### Files Modified

| File | Changes |
|------|---------|
| `MCP-Hub/document-processor/src/watcher.js` | Per-doc Slack links, footer link, routed_channel for MAIL |
| `RAPID_IMPORT/IMPORT_Approval.gs` | Enhance getApprovalQueueDepthForUI with batch list |
| `RAPID_IMPORT/Code.gs` | Home page pending batch list UI |

### Verification

1. Drop a multi-page scanned PDF into MAIL_INTAKE/Incoming
2. Wait for watcher to process (60s poll + extraction time)
3. Confirm #service-general gets multi-doc summary WITH per-doc "Review" links
4. Confirm #service-general gets individual "Mail Review Needed" cards (not #ai-data-approvals)
5. Click "Review" link → lands on APPROVAL_UI with correct batch
6. Push/Edit/Kill fields → DONE → verify MATRIX writes
7. Check RAPID_IMPORT home page shows pending batches with clickable links
