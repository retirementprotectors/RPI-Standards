# PRODASH v3.11.1 — Post-Deploy Fixes

## Context

v3.11 deployed with several issues found during JDM testing. Prioritized by severity.

---

## PRIORITY 1: Dead Screen on New Tab (PRODUCTION BLOCKER)

**Problem:** "View Full Detail" opens new tab to `userCodeAppPanel?view=account-detail&id=...` — this is the GAS **iframe URL**, not the `/exec` deployment URL. Query params on the iframe URL don't flow through `doGet(e)`, so `deepView`/`deepId`/`deepType` are all empty = dead dashboard.

Same bug exists in `openClient360InNewTab()`.

**Root cause:** `window.location.href.split('?')[0]` inside a GAS web app gives the iframe URL, not the exec URL.

**Fix:**
1. **Code.gs line ~17:** Add `template.execUrl = ScriptApp.getService().getUrl();`
2. **Index.html template vars (~line 4449):** Add `let execUrl = '<?= execUrl ?>';`
3. **Scripts.html — C360 View Full Detail (~line 3448):** Replace `baseUrl` with `execUrl`
4. **Scripts.html — openClient360InNewTab (~line 1688):** Replace `baseUrl` with `execUrl`, delete `var baseUrl` line

---

## PRIORITY 2: Client Global Search Broken

**Problem:** Searching "ojeda" in Clients mode returns "No results". Accounts mode works fine.

**Root cause:** The refactored `executeGlobalSearch` function has the client search in an `else` branch. Need to verify the `uiSearchClients` call is executing properly and the response shape matches what the renderer expects (`response.data.clients`). May be a variable shadowing issue — `var response` is declared in the outer scope of the accounts branch and the client `var response` in the else may conflict.

**Fix:** Use separate variable names or restructure to avoid scoping issues. Also verify `uiSearchClients` works via execute_script test.

---

## PRIORITY 3: MyRPI Layout — Mirror RIIMO Format

**Problem:** Current PRODASH MyRPI is "kinda whack" — doesn't match RIIMO's polished layout.

**Fix:** Read RIIMO `MyRPI.html` fully and port the exact layout structure, including:
- Left column (profile card + job description) / Right column (module access + documents)
- Card styling matching RIIMO's dark sidebar theme adapted for PRODASH light theme
- Proper section headers with icons
- Job template description section (currently missing)

---

## PRIORITY 4: Quick Intake Custom Fields

**Problem:** When adding a custom field or entering beneficiary data:
- "Add Field" asks for a value in a text input — should just SELECT the field name, then show the appropriate input type (dropdown, text, etc.)
- Primary/Contingent beneficiary fields should have structured sub-fields (name, relationship, percentage, etc.) not just a text box

**Fix:** Redesign `addCustomFieldRow()` to be a two-step flow:
1. Select field name from dropdown
2. Render the appropriate input widget for that field type (text, dropdown with options, date picker, etc.)

For beneficiary fields — render structured sub-fields: Name, Relationship (dropdown), Percentage, DOB, SSN (masked).

---

## PRIORITY 5: Quick Intake — Paste Screenshots

**Problem:** JDM wants to paste screenshots/images into Quick Intake (not just PDF + text).

**Fix:** Add image paste support:
- Listen for `paste` event on the Quick Intake panel
- Accept image types from clipboard (`image/png`, `image/jpeg`)
- Convert to base64, set `inputType = 'image'`
- Show thumbnail preview in drop zone area
- Server-side: handle image extraction via OCR/vision (may need Gemini vision API)

---

## PRIORITY 6: Teammate Chat/Meet — Embedded Experience

**Problem:** JDM doesn't want to GO TO Chat or CREATE a Meet. Wants inline/embedded.

**Reality check:** Google Chat and Google Meet don't offer embeddable iframe widgets for third-party web apps. The options are:
- **Chat:** Use Google Chat API to send a message inline (we have this via rpi-workspace MCP). Could open a small compose panel within PRODASH.
- **Meet:** Can create a meeting and show the join link inline, or open Meet in a small popup window rather than navigating away.

**Fix:**
- **Chat:** Replace external link with inline compose box — type message, send via `rpi-workspace.send_message` to the user's Chat DM
- **Meet:** Keep creating the meeting but open it in a popup window (`window.open` with dimensions) instead of `_blank`

---

## Files Modified

| File | Change |
|------|--------|
| `Code.gs` | Add `template.execUrl` |
| `Index.html` | Add `execUrl` template var |
| `Scripts.html` | Fix new-tab URLs, fix client search, redesign custom fields, add image paste, improve Chat/Meet UX |
| `Styles.html` | MyRPI layout improvements |

## Verification

1. C360 → "View Full Detail" → new tab loads account detail (NOT dead screen)
2. Global search Clients → "ojeda" → returns matching clients
3. MyRPI panel matches RIIMO layout
4. Quick Intake → Add Field → select field → shows right input type
5. Quick Intake → Ctrl+V screenshot → image appears in panel
6. Teammate Chat → inline compose, not external redirect
7. Teammate Meet → popup window, not full navigation
