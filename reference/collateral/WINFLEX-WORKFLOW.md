---
name: Winflex Illustration Workflow
description: Complete workflow for running JH life insurance illustrations in Winflex Web — login, input, save cases, calculate, and download PDFs. Learned during Mineart casework 2026-03-20.
type: reference
---

## Winflex Web — Full Workflow

**URL:** https://www.winflexweb.com/wfw_login.aspx
**Login:** Auto-fills from Chrome (Josh Millang account). Browser session cookies persist.

### Navigation Structure

1. **Dashboard** → Click "Illustrations" shortcut tile
2. **Client Editor** has a left sidebar (saved cases) and tabbed input area:
   - First Insured | Second Insured | Solve For | Disbursements | Assumed Rate | Policy Options | Policy Riders | Optional Pages | Agent Info
3. **"Use Last Case"** loads the most recently used inputs (but resets to defaults, NOT the saved case)
4. **"Load a Saved Case"** loads a previously saved case by name

### Input Tabs — What Goes Where

**First Insured:**
- Insured Name, Sex, Date of Birth (mm/dd/yyyy), Class (dropdown), Permanent Percentage (dropdown), Flat Extra, Age at Death, State (Iowa), Backdate to Save Age (checkbox), Estimated Policy Issue Date, Tax Bracket

**Second Insured:** Same fields for spouse/joint insured

**Solve For:**
- Solve For dropdown: "No Solve" | "Premium" | "Face Amount"
  - **No Solve**: Enter BOTH face amount AND premium manually (clean numbers for presentation)
  - **Premium**: Enter face amount, system solves for premium
  - **Face Amount**: Enter premium, system solves for face. **MUST select "Max DB to Endow/Target" from the Face Amount dropdown** or it won't actually solve — it'll just use whatever face was there before
- Vitality Plus: Yes, Gold (both statuses)
- LifeTrack Billing: Yes
- Total Face Amount + Premium fields
- Target Cash Value: $1,000 at Age 100 (for solve modes)
- Preliminary Funding Account: unchecked

**Assumed Rate:**
- Allocation Option: Custom Allocation and Rate
- Base Capped Rate: 6.71%
- **Premium Allocation: 100% Base Capped Acct, 0% everything else** (must match application)

**Policy Options:**
- DB Option 1 (Level)
- Premium Mode: Annual
- Prevent MEC: Checked
- Charges: Current

### Saving Cases

1. Click **Save** dropdown → **Save As**
2. Dialog shows all saved case names + text field for new name
3. Enter descriptive name: e.g., "Mineart $90K 4.5M"
4. Click Save → confirms "1 client(s) saved to [case name]"
5. **Always save BEFORE calculating** — the illustration results don't save the case

### Calculating

1. Click **Calculate** button (green, top right of input area OR top-left nav)
2. If nav dropdown appears: click "Calculate" (not Composite/Multiplan)
3. Status shows "Submitted" → "Calculating" → Results appear
4. Takes ~15-20 seconds typically

### Getting the PDF Illustration

**This is the critical step — learned the hard way:**

1. After calculation completes, results page shows Summary with a **PDF icon** (red/white) in the Illustration column
2. **Click the PDF icon** → opens PDF in a **new browser tab** as a Chrome PDF viewer
3. The URL is `wfw_imagefetch.aspx?id=pdf0&type=PDF&PBS=...&Group=...`
4. **To download the actual PDF:**
   - Use `curl` with the ASP.NET session cookie:
     ```bash
     curl -s -o ~/Desktop/"filename.pdf" \
       -b "ASP.NET_SessionId=SESSION_ID_HERE" \
       "FULL_WFW_IMAGEFETCH_URL_HERE"
     ```
   - Get the session cookie from Playwright: `page.context().cookies()` → find `ASP.NET_SessionId`
   - Get the PDF URL from the new tab that opened
5. **Verify the PDF:** `file` command may show "0 pages" but `mdls -name kMDItemNumberOfPages` shows the real count. Open with Preview to confirm.
6. **Alternative (Playwright):** Inject a download link:
   ```js
   await page.evaluate((u) => {
     const a = document.createElement('a');
     a.href = u;
     a.download = 'filename.pdf';
     document.body.appendChild(a);
     a.click();
   }, url);
   ```
   This saves to `.playwright-mcp/` folder — copy to Desktop after.

### Mineart Case Specifics (for reference)

**Saved cases in Winflex:**
- "Mineart $90K 4.5M" — $4,500,000 face, $90,000 premium
- "Mineart $60K 3M" — $3,000,000 face, $60,000 premium
- Existing on file: $120K/$6M (ran 03/17/2026)

**Shared inputs across all Mineart cases:**
- Stephen: DOB 09/23/1954, Male, Standard NS, Perm 175%, Gold
- Joyce: DOB 06/16/1955, Female, Preferred NS, Gold
- Issue Date: 12/15/2025 (backdated)
- State: Iowa
- DB Option 1, CVAT, Prevent MEC
- 100% Base Capped allocation, 6.71% rate
- No Estate Preservation Rider
- Product: Protection SIUL 24 (form 22PSIUL)

### Common Gotchas

1. **"Use Last Case" resets to defaults** — DOBs, classes, ratings all go back to default. Must re-enter everything. Use "Load a Saved Case" instead.
2. **Solve For: Face Amount requires "Max DB to Endow/Target"** in the face amount dropdown. If you leave it at a number (e.g., 1,000,000), it won't solve — it'll just calculate premium for that face.
3. **Issue date drives age calculation** — 12/15/2025 backdate makes Stephen 71 and Joyce 70. Default date (04/16/2026) makes Stephen 72.
4. **PDF icon opens in new tab** — can't right-click save from the results page. Must click it, then download from the new tab.
5. **Session cookie is `ASP.NET_SessionId`** — needed for curl downloads.
6. **Save BEFORE calculate** — Winflex doesn't auto-save after calculation.
7. **Alert dialogs after save** sometimes block the Calculate button — use `page.locator('#btnAlertOkay').click({force: true})` or Escape to dismiss.
