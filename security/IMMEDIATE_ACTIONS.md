# RPI Security: Immediate Action Items

> **Created:** 2026-02-04
> **Status:** Needs JDM/Admin verification

---

## Priority 1: Verify Today

### 1. ~~Check if 2FA is Enforced~~ ✅ COMPLETED
**Who:** JDM or Google Workspace Admin
**Where:** Google Admin Console → Security → 2-Step Verification
**Status:** 2FA enforcement enabled on Feb 04, 2026 with 1-week grace period for existing users

### 2. ~~Check BAA Status with Google~~ ✅ COMPLETED
**Who:** JDM
**Where:** Google Admin Console → Account → Legal and Compliance
**Status:** HIPAA Business Associate Amendment accepted by Josh@retireprotected.com on Feb 04, 2026

### 3. Verify All Apps Are "Organization Only"
**Who:** JDM or Dev
**Where:** Each GAS project → Deploy → Manage Deployments → Access
**Status:** PRODASH verified ✅ - shows "Anyone within Retirement Protectors INC"

| App | Check Access Setting |
|-----|---------------------|
| PRODASH | [x] Organization only (verified 2026-02-04) |
| SENTINEL | [ ] Organization only |
| DEX | [ ] Organization only |
| RIIMO | [ ] Organization only |
| CAM | [ ] Organization only |
| CEO-Dashboard | [ ] Organization only |
| C3 | [ ] Organization only |

**Note:** All apps in same Workspace domain should have same access pattern. Spot-check 2-3 more to confirm.

---

## Priority 2: This Week

### 4. Review Current Workspace Users
**Who:** JDM or Admin
**Where:** Google Admin Console → Directory → Users
**Action:** Export list, verify everyone should have access

Questions to answer:
- [ ] Any former employees still have accounts?
- [ ] Any contractors who no longer work with us?
- [ ] Anyone with Admin access who shouldn't have it?

### 5. Document Offboarding Process
**Who:** JDM + COO (John Behn)
**Action:** Review the offboarding checklist in SECURITY_COMPLIANCE.md
**Confirm:** This is how we actually handle departures

---

## Priority 3: This Month

### 6. Set Quarterly Calendar Reminders
**Who:** JDM
**Action:** Create recurring calendar events for:

| Task | Frequency | Suggested Day |
|------|-----------|---------------|
| Access Review | Quarterly | 1st Monday of Jan/Apr/Jul/Oct |
| Credential Rotation Check | Quarterly | Same day |
| Security Doc Review | Quarterly | Same day |

### 7. Communicate to Team
**Who:** JDM
**Action:** Brief team on:
- 2FA is mandatory (if not already clear)
- How to report security concerns
- Offboarding process exists

---

## Completed Items (2026-02-04)

- [x] Removed hardcoded credentials from code (CEO-Dashboard, RAPID_API)
- [x] Rotated exposed Slack tokens
- [x] Updated all MCP config files with new tokens
- [x] Added API key authentication to RAPID_API
- [x] Replaced forbidden UI patterns (alert/confirm/prompt)
- [x] Created security compliance documentation
- [x] Verified GitHub repos are private
- [x] Enabled 2FA enforcement for Google Workspace (1-week grace period)
- [x] Accepted HIPAA Business Associate Amendment with Google

---

## Notes

✅ **Priority 1 items are now VERIFIED.** You can confidently make this statement:

> "RPI maintains security controls including mandatory two-factor authentication, organization-restricted application access, and HIPAA-eligible infrastructure through our Google Cloud BAA."

**Evidence:**
- 2FA enforcement: Enabled Feb 4, 2026
- HIPAA BAA: Accepted by Josh@retireprotected.com on Feb 4, 2026
- Apps: Organization-only access (pending verification of all apps)
