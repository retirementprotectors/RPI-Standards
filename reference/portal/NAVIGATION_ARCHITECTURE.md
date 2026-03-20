# Navigation Architecture

> How sidebar navigation, admin routing, and My RPI work across all 3 portals.

## Section Types

| Type | Data Attr | Icon Color | Behavior |
|------|-----------|------------|----------|
| Pipeline | `data-type="pipeline"` | `--pipeline-color` (#63b3ed) | Collapsible, spinning icon, items are pipeline stages |
| Module | `data-type="module"` | `--module-color` (#a78bfa) | Collapsible, spinning icon, items are native views |
| App | `data-type="app"` | `--app-color` (#f6ad55) | Collapsible, items open new window (dashed border) |
| Admin | `.admin-section` | `--admin-color` (#fc8181) | Pinned bottom, flat button, no collapse |

## Collapse Behavior

### Default State
All sections start **collapsed**. Only the icon button is visible.

### Expand/Collapse
1. Click section header
2. Icon spins (360deg on expand, -360deg on collapse)
3. Title text fades in/out
4. Chevron shows/hides
5. Items slide down/up (max-height transition)

### JavaScript Pattern
```javascript
// Shared function (in PortalStandard.html)
function toggleSidebarSection(header) {
  var items = header.nextElementSibling;
  var iconBtn = header.querySelector('.section-icon-btn');
  var isCollapsed = header.classList.contains('collapsed');
  if (iconBtn) {
    iconBtn.classList.remove('spinning', 'spinning-back');
    void iconBtn.offsetWidth; // force reflow
    iconBtn.classList.add(isCollapsed ? 'spinning' : 'spinning-back');
    setTimeout(function() { iconBtn.classList.remove('spinning', 'spinning-back'); }, 500);
  }
  header.classList.toggle('collapsed');
  items.classList.toggle('collapsed');
}
```

### HTML Pattern
```html
<div class="sidebar-section" data-type="pipeline">
  <div class="sidebar-section-header collapsed" onclick="toggleSidebarSection(this)">
    <div class="section-icon-btn"><span class="material-icons-outlined">route</span></div>
    <span class="section-title-text">Pipelines</span>
    <span class="material-icons-outlined chevron">expand_more</span>
  </div>
  <div class="sidebar-section-items collapsed">
    <div class="nav-item pipeline-item">
      <span class="material-icons-outlined">explore</span>Discovery
    </div>
    <!-- more items -->
  </div>
</div>
```

## Routing

### Sidebar Item Click
Each portal defines its own click handler that:
1. Sets `.active` class on the clicked nav-item
2. Removes `.active` from all other nav-items
3. Loads the corresponding view into `.main-content`

### App Items
App nav-items are React modules rendered within the portal. Some legacy apps may still open external URLs.

### Logo Click
Calls `showDashboard()` (or equivalent) to load the dashboard view.

### Admin Click
Permission-checked. If authorized, loads admin panel with tabbed UI.

## Icon Conventions

| Section | Icon | Material Icons Outlined Name |
|---------|------|------------------------------|
| Pipelines | route | `route` |
| Workspace | workspaces | `workspaces` |
| Sales Centers | storefront | `storefront` |
| Service Centers | support_agent | `support_agent` |
| Deal Management | business_center | `business_center` |
| Analysis | analytics | `analytics` |
| Market Intel | insights | `insights` |
| RAPID Tools | build_circle | `build_circle` |
| Tool Suites | category | `category` |
| Apps | apps | `apps` |
| Admin | admin_panel_settings | `admin_panel_settings` |

## Admin Tab Routing

### Standard Tabs (shared backend pattern)
Each portal has a `*_OrgAdmin.gs` file wrapping RAPID_CORE:
- `uiGetAllUsersForUI()` - Team Management
- `uiSaveUserForUI(userData)` - Team Management save
- `uiDeleteUserForUI(userId)` - Team Management delete
- `uiGetPipelineConfigForUI()` - Pipeline Config
- `uiSavePipelineConfigForUI(config)` - Pipeline Config save
- `uiGetModuleConfigForUI()` - Module Config
- `uiSaveModuleConfigForUI(config)` - Module Config save

All return `{ success: true/false, data/error }` via `JSON.parse(JSON.stringify())`.

### Tab Switching (frontend)
```javascript
function switchAdminTab(tabId) {
  // Hide all admin content sections
  document.querySelectorAll('.admin-content-section').forEach(function(s) { s.style.display = 'none'; });
  // Show selected
  document.getElementById('admin-' + tabId).style.display = 'block';
  // Update tab active state
  document.querySelectorAll('.admin-tab').forEach(function(t) { t.classList.remove('active'); });
  event.target.closest('.admin-tab').classList.add('active');
}
```

## My RPI Tab Routing

Same pattern as admin tabs. `*_MyRPI.gs` (or functions in the portal's main `.gs`) provide:
- `uiGetMyProfileForUI()` - Profile tab
- `uiGetMyDropZoneForUI()` - MyDropZone tab
- `uiGetMyMeetingTypesForUI()` - Meetings tab
- `uiSaveMeetingTypesForUI(types)` - Meetings save
- `uiSaveAvailabilityForUI(availability)` - Meetings availability save
- `uiGetMyPermissionsForUI()` - Permissions tab (read-only)

## OrgAdmin Backend Pattern

Standard wrapper file (`*_OrgAdmin.gs`):
```javascript
// Thin wrapper around RAPID_CORE, filtered to this portal's platform
function uiGetAllUsersForUI() {
  var users = RAPID_CORE.getUsersByPlatform('PORTAL_NAME');
  return JSON.parse(JSON.stringify({ success: true, data: users }));
}

function uiSaveUserForUI(userData) {
  var result = RAPID_CORE.saveUser(userData);
  return JSON.parse(JSON.stringify(result));
}
```
