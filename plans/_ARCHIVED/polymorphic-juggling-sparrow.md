# Fix OU Structure: Separate FINRA Compliance from Offboarded Users

## Context

The `/RPI- Archived Users` OU controls FINRA email compliance — Global Relay (Gradient's archiving vendor) archives email for everyone in this OU. Active securities-licensed users (Josh, Nikki, Angelique) belong here.

**The bug:** `runAutoOffboard_()` in `API_Compliance.gs` moves suspended/departed users INTO this same OU, mixing them with active licensed users. Alex and JMDC were just auto-offboarded into the FINRA compliance OU. Additionally, 3 other suspended users (allison@, rpifax@, christa@) are in the wrong OUs entirely.

---

## Step 1: JDM Creates New OU (Manual — 30 seconds)

JDM is already in Admin Console. Create:
- **Name:** `RPI- Offboarded`
- **Path:** `/RPI- Offboarded`
- **Description:** "Suspended/departed employees. NOT archived to Global Relay."

---

## Step 2: Move Suspended Users to Offboarded OU

Using `update_user_ou` MCP tool, move all 5 suspended users:

| User | Current OU | Move To |
|------|-----------|---------|
| alex@retireprotected.com | /RPI- Archived Users | /RPI- Offboarded |
| jmdconsulting@retireprotected.com | /RPI- Archived Users | /RPI- Offboarded |
| allison@retireprotected.com | /RPI- Non-Archived Users | /RPI- Offboarded |
| rpifax@retireprotected.com | /RPI- Non-Archived Users | /RPI- Offboarded |
| christa@retireprotected.com | / (root) | /RPI- Offboarded |

---

## Step 3: Update Auto-Offboard Code

**File:** `RAPID_API/API_Compliance.gs`

- **Line 801:** Change `var ARCHIVED_OU = '/RPI- Archived Users'` → `var ARCHIVED_OU = '/RPI- Offboarded'`
- **Lines 804-808:** Update `knownArchived` list — remove allison/christa/rpifax (they'll be in Offboarded OU now, not a special case) OR keep as safety net
- **Line 894:** Update report text to say "Moved to /RPI- Offboarded" instead of "/RPI- Archived Users"

Also check `weekly-check.js` line ~84-90 for the same `complianceArchivedUsers` list.

---

## Step 4: Deploy RAPID_API

6-step deploy to push the code change live. The GAS trigger runs Mondays 8 AM — next run would use the new OU.

---

## Step 5: Update Documentation

### Files to update:

1. **`_RPI_STANDARDS/CLAUDE.md`** — Update the line "OU `/RPI- Archived Users` = FINRA archiving" to clearly document BOTH OUs and their purposes

2. **`_RPI_STANDARDS/reference/os/POSTURE.md`** — Add OU structure documentation:
   - `/RPI- Archived Users` = FINRA compliance, email archived to Global Relay (active licensed users)
   - `/RPI- Non-Archived Users` = Active employees NOT under securities email archiving
   - `/RPI- Offboarded` = Suspended/departed employees (NOT archived to Global Relay)

3. **`_RPI_STANDARDS/reference/os/OPERATIONS.md`** — Update offboarding checklist line 41 to reference `/RPI- Offboarded` for departed users, distinguish from FINRA archiving OU

4. **`RAPID_API/API_Compliance.gs`** — Update comments to document the distinction

5. **`MCP-Hub/maintenance/weekly-check.js`** — Update complianceArchivedUsers list and comments

---

## Step 6: Update MEMORY.md

Add the OU structure documentation so future sessions understand the distinction.

---

## Verification

1. Run `audit_workspace_users` — confirm all 5 suspended users are in `/RPI- Offboarded`
2. Confirm Josh, Nikki, Angelique remain in `/RPI- Archived Users`
3. Run `DEBUG_Ping` on RAPID_API to verify deploy
4. Grep codebase for any remaining references to the old pattern
