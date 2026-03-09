# Unit-Based Auto-Assignment + RAPID Tools Defaults in RIIMO

## Context

Phases 1-5 of the Delegated Admin System are deployed. `_USER_HIERARCHY` is the single source of truth. RIIMO has a working Permissions UI with per-module VIEW/EDIT/ADD toggle chips. But:

1. **The unit dropdown in RIIMO user edit form doesn't populate with MEDICARE/RETIREMENT/LEGACY** — it reads from `_COMPANY_STRUCTURE` (entity_ids) instead of `UNIT_MODULE_DEFAULTS` (functional unit keys)
2. **Changing a user's unit doesn't auto-compute their default module permissions** — Leaders must manually toggle every chip
3. **RAPID Tools (C3, RAPID_IMPORT, DEX) have no default assignment logic** — they're toggle-able but never auto-granted to Leaders
4. **CAM is listed in the same group** but should be restricted to RIIMO admin access (EXECUTIVE+)

**JDM's direction:** "Default C3, RAPID Import, DEX for Leaders in both platforms. CAM stays in RIIMO. Leaders can then delegate/assign users as they need to within their teams."

---

## What Changes

### 1. RAPID_CORE/CORE_Entitlements.gs

**Add `LEADER_DEFAULT_RAPID_TOOLS` constant:**
```
['C3', 'RAPID_IMPORT', 'DEX']
```
These get auto-granted to Leaders+ with full access (VIEW/EDIT/ADD).

**Update `computeModulePermissions()`** to include RAPID Tools:
- Leaders+ automatically get C3, RAPID_IMPORT, DEX with `['VIEW', 'EDIT', 'ADD']`
- CAM only included for EXECUTIVE+ (matches its `minUserLevel: 'EXECUTIVE'`)
- MCP_HUB stays individually assignable (not auto-granted)

The function signature stays the same. It already handles PRODASH modules + optional SENTINEL. Now it also adds RAPID Tools for Leaders+.

### 2. RIIMO/Index.html (~line 4250)

**Replace unit dropdown population logic:**

Currently `onUserDivisionChange()` populates units from `orgStructureData.divisions[x].units` (entity_ids from `_COMPANY_STRUCTURE`).

Change to: Populate with options from `UNIT_MODULE_DEFAULTS` (MEDICARE/RETIREMENT/LEGACY). These are functional categories, not org structure entities. The `unit_id` stored in `_USER_HIERARCHY` is already these keys (set by `SETUP_AssignUnits`).

Options: `MEDICARE | Retirement | Legacy` (plus empty "Select unit...")

**Add `onUnitChange()` handler (~after line 4548):**

When unit dropdown changes AND the entitlements panel is open:
1. Get current role template (derive from `user_level` dropdown: LEADER→admin, USER→sales/service based on division)
2. Call server: `uiComputeDefaultPermissions(roleTemplateKey, unitId)`
3. Receive default `module_permissions` object
4. Update ALL toggle chips in the entitlements panel to match defaults
5. Show toast: "Default permissions applied for [Unit] [Role]. You can override individual modules."

This gives Leaders a one-click default that they can then customize per user.

**Decouple unit from division change (~line 4524-4548):**

The unit dropdown should NOT reset when division changes. Unit (functional specialty) is independent of division (organizational hierarchy). A person can be in Sales division + Medicare unit, or Service division + Medicare unit.

### 3. RIIMO/Code.gs

**Add `uiComputeDefaultPermissions(roleTemplateKey, unitId)` endpoint:**
```javascript
function uiComputeDefaultPermissions(roleTemplateKey, unitId) {
  try {
    var perms = RAPID_CORE.computeModulePermissions(roleTemplateKey, unitId);
    return JSON.parse(JSON.stringify({ success: true, data: perms }));
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

**Add `uiGetUnitModuleDefaults()` endpoint:**
```javascript
function uiGetUnitModuleDefaults() {
  try {
    var data = RAPID_CORE.getUnitModuleDefaults();
    return JSON.parse(JSON.stringify({ success: true, data: data }));
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### 4. RIIMO/RIIMO_OrgAdmin.gs — `saveUser()` (~line 328)

**Auto-compute module_permissions on user save when unit_id changes:**

When saving a user with a `unit_id` and the user doesn't already have `module_permissions` (new user), OR if `unit_id` changed from what's stored, auto-compute defaults using `computeModulePermissions()` and write them to `module_permissions` column.

This ensures new users created through the RIIMO form automatically get the right defaults without requiring the Leader to also manually save permissions.

### 5. PRODASHX/PRODASH_Migration.gs — `FIX_RecomputeAllPermissions()`

**One-time function** to recompute all existing users' module_permissions to include the new RAPID Tools defaults for Leaders. Without this, existing Leaders won't get C3/RAPID_IMPORT/DEX until their permissions are manually re-saved.

---

## Files to Modify

| File | Change |
|------|--------|
| `RAPID_CORE/CORE_Entitlements.gs` | Add `LEADER_DEFAULT_RAPID_TOOLS`, update `computeModulePermissions()` |
| `RAPID_CORE/Code.gs` | Export new constant |
| `RIIMO/Code.gs` | Add `uiComputeDefaultPermissions()`, `uiGetUnitModuleDefaults()` |
| `RIIMO/Index.html` | Fix unit dropdown, add `onUnitChange()`, wire auto-compute to entitlements chips |
| `RIIMO/RIIMO_OrgAdmin.gs` | Auto-compute module_permissions on new user save |
| `PRODASHX/PRODASH_Migration.gs` | Add `FIX_RecomputeAllPermissions()` one-time function |

---

## Verification

1. **RAPID_CORE**: Run `computeModulePermissions('admin', 'MEDICARE')` — should return PRODASH base modules + QUE_MEDICARE + QUE_MEDSUP + C3/RAPID_IMPORT/DEX (Leader+ level)
2. **RIIMO UI**: Open user edit panel. Unit dropdown shows MEDICARE/RETIREMENT/LEGACY. Change unit to RETIREMENT → entitlements auto-populate with QUE_ANNUITY, QUE_LIFE, RMD_CENTER + RAPID Tools
3. **Leader override**: After auto-populate, toggle off a module → save → verify it stays off (not overwritten by defaults)
4. **Existing users**: Run `FIX_RecomputeAllPermissions()` → verify Leaders now have C3/RAPID_IMPORT/DEX in their module_permissions
5. **PRODASHX/SENTINEL**: No changes needed — they already read from `_USER_HIERARCHY` module_permissions

---

## Deploy Order

1. RAPID_CORE → `clasp push` + version (library, no deploy needed)
2. RIIMO → `clasp push` + version + deploy
3. Run `FIX_RecomputeAllPermissions()` in PRODASHX to backfill existing users
4. Verify in RIIMO UI
