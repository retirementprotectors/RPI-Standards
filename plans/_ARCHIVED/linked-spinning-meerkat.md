# My RPI v3.6.0 — Full UX Enhancement Pass

## Context

My RPI v3.5.1 shipped with core functionality: profile card, job description, module access (now collapsible), documents, onboarding progress, quick links, team view, persistent team selector. JDM provided detailed feedback requesting 5 actionable enhancements. This plan covers ALL of them.

**Bug fix**: Top-right bar still shows email instead of first name — `getUserHierarchy()` didn't return `first_name`/`last_name`. RAPID_CORE already fixed and pushed (adds name fields to return object). Just needs RIIMO redeploy.

---

## Build Items

### 1. Fix First Name in Top-Right Bar
**Status**: RAPID_CORE already pushed. RIIMO needs version + deploy.
- `RAPID_CORE/CORE_Entitlements.gs` — `getUserHierarchy()` now returns `first_name` and `last_name`
- `Index.html` already uses `firstName || fullName` — will work once RAPID_CORE change propagates

### 2. Auto-Create Employee Drive Folder on Onboarding
**Files**: `RIIMO/RIIMO_Pipelines.gs`, `RIIMO/RIIMO_MyRPI.gs`

**What happens**:
- During onboarding System Setup stage (`executeOnboardingSystemSetup_()` in RIIMO_Pipelines.gs), after user is created in `_USER_HIERARCHY`:
  1. Get or create parent folder `Employee Personal Folders` under RAPID_CORE Drive root
  2. Create subfolder named `{FirstName} {LastName}`
  3. Share folder with the new employee (editor access)
  4. Store `drive_folder_url` in `employee_profile` JSON via `updateEmployeeProfile()`
  5. Quick Links section already reads `drive_folder_url` — auto-links with no frontend change

**New helper**: `createEmployeePersonalFolder_(fullName, userEmail)` in RIIMO_Pipelines.gs
- Uses `DriveApp` (already available in GAS)
- Uses `RAPID_CORE.getRootFolder()` + `RAPID_CORE.getOrCreateFolder()` from SETUP_DRIVE.gs
- Shares with employee via `folder.addEditor(email)`

### 3. Profile Photos from Google Workspace
**Files**: `RIIMO/RIIMO_MyRPI.gs`, `RIIMO/MyRPI.html`

**Approach**: Fetch photo URL server-side in `getMyProfileData()`, return it to frontend. Frontend already renders photos when `employee_profile.profile_photo_url` exists.

**Backend** (`RIIMO_MyRPI.gs`):
- New helper `getWorkspacePhotoUrl_(email)` — uses `AdminDirectory.Users.get(email, {fields: 'thumbnailPhotoUrl'})`
- Requires `AdminDirectory` advanced service enabled in RIIMO's GAS project
- Called in `getMyProfileData()` — sets `data.workspacePhotoUrl`
- Falls back gracefully if AdminDirectory not available (returns null, avatar shows initials)

**Frontend** (`MyRPI.html`):
- Profile card avatar already checks `empProfile.profile_photo_url`
- Add fallback: also check `data.workspacePhotoUrl` from Workspace
- Top-right avatar in Index.html: update `updateTopUserBar()` to accept photo URL and render `<img>` instead of initials

**No manual setup**: AdminDirectory gets enabled via `appsscript.json` manifest (`enabledAdvancedServices`). Clasp push handles it automatically.

### 4. Communication Preferences Section
**Files**: `RIIMO/MyRPI.html`, `RIIMO/RIIMO_MyRPI.gs`

**Schema** (stored in `employee_profile.communication_preferences`):
```json
{
  "preferred_contact": "email|phone|text",
  "best_time": "morning|afternoon|evening|anytime",
  "notifications": {
    "email_updates": true,
    "sms_alerts": false,
    "slack_notifications": true
  }
}
```

**Frontend**: New section `_myrpiRenderCommunicationPrefs(data)` — renders after Documents (#4), before Onboarding Progress (#5):
- 3 setting groups using toggle switches and radio-style selectors
- Preferred Contact Method: Email / Phone / Text (radio)
- Best Time to Reach: Morning / Afternoon / Evening / Anytime (radio)
- Notification Channels: Email Updates / SMS Notifications / Slack Notifications (toggles)
- Save button calls `uiUpdateEmployeeProfile()` with merged prefs
- Read-only for non-self profiles (admin can view but not change someone's prefs)

### 5. Google Picker for Document Upload
**Files**: `RIIMO/MyRPI.html`, `RIIMO/Code.gs`

**Replace** the manual URL text input in the Add Document modal with Google Picker:
- Load Google Picker API (`gapi.load('picker')`)
- Backend endpoint `uiGetPickerToken()` returns OAuth token via `ScriptApp.getOAuthToken()`
- Picker opens, user browses their Drive, selects file
- On selection: auto-fills document name (from file name) and URL (from file webViewLink)
- User can edit name before saving
- Fallback: keep manual URL input as secondary option ("Or paste a link")

**API Key**: Reuse existing `GOOGLE_PLACES_API_KEY` (`AIzaSyClhh90EEp2BosmZPJKJwnLAfUh9EYRXdk`) from RAPID_CORE config — same GCP project, works for Picker. Backend returns it via `uiGetPickerToken()`.

---

## Files Modified

| File | Changes |
|------|---------|
| `RAPID_CORE/CORE_Entitlements.gs` | Already pushed — `first_name`/`last_name` in `getUserHierarchy()` |
| `RIIMO/RIIMO_Pipelines.gs` | `createEmployeePersonalFolder_()` helper, hook into System Setup |
| `RIIMO/RIIMO_MyRPI.gs` | `getWorkspacePhotoUrl_()`, photo URL in profile response |
| `RIIMO/Code.gs` | `uiGetPickerToken()` endpoint |
| `RIIMO/MyRPI.html` | Communication Prefs section, Picker in doc modal, photo fallback |
| `RIIMO/Index.html` | Top-right avatar photo support |

---

## Deployment Order

1. **RAPID_CORE** — already pushed, just needs `clasp version` + git commit/push
2. **RIIMO** — add AdminDirectory to `appsscript.json` manifest + push + version + deploy (all changes)
3. **Verify** — test profile photos load, test Picker, test comms prefs save

---

## Items NOT in This Build (Future)

| Item | Why Later |
|------|-----------|
| LC3 integration (MyRPI vs MyLC3 dropdown) | LC3 doesn't exist yet |
| Cross-platform top-right bar (PRODASH/SENTINEL) | Separate platform deploys |
| Auto-onboarding Drive folder for EXISTING users | Needs a one-time migration script — can do after this deploy |
