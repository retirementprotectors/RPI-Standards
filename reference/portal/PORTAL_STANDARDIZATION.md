# Portal Standardization Spec

> Defines the standard UI/UX structure for all 3 RPI portals: PRODASHX, SENTINEL, RIIMO.

## Color System

### Dark Mode Foundation (ALL portals)
| Variable | Value | Usage |
|----------|-------|-------|
| `--bg-deepest` | `#0a0a0f` | Body/main content background |
| `--bg-dark` | `#111118` | Modal/card containers |
| `--bg-card` | `#1a1a24` | Sidebar, topbar, cards |
| `--bg-card-hover` | `#22222e` | Card hover states |
| `--bg-surface` | `#2a2a36` | Elevated surfaces |
| `--text-primary` | `#f0f0f5` | Headings, primary text |
| `--text-secondary` | `#8888a0` | Body text, descriptions |
| `--text-muted` | `#55556a` | Labels, hints |
| `--border-subtle` | `rgba(255,255,255,0.06)` | Subtle dividers |
| `--border-medium` | `rgba(255,255,255,0.1)` | Visible borders |

### Section Type Colors (ALL portals)
| Type | Color | Variable |
|------|-------|----------|
| Pipelines | `#63b3ed` (blue) | `--pipeline-color` |
| Modules | `#a78bfa` (purple) | `--module-color` |
| Apps | `#f6ad55` (orange) | `--app-color` |
| Admin | `#fc8181` (red) | `--admin-color` |
| RPI Connect | `#68d391` (green) | `--connect-color` |

### Portal Brand Colors
| Portal | `--portal` | `--portal-glow` | `--portal-accent` |
|--------|-----------|-----------------|-------------------|
| PRODASHX | `#3d8a8f` | `rgba(61,138,143,0.15)` | `#5bbfc5` |
| SENTINEL | `#3CB371` | `rgba(60,179,113,0.15)` | `#5dd99a` |
| RIIMO | `#276749` | `rgba(39,103,73,0.15)` | `#48bb78` |

## Sidebar Structure (Left Nav)

### Order (ALL portals)
1. **Logo** (top-left) - click = Dashboard. NO Dashboard item in nav.
2. **Pipelines** - FIRST section, collapsed by default. Blue icons.
3. **Module Sections** - Portal-specific groupings. Purple icons. Collapsed by default.
4. **Apps** - Standalone branded modules (Pipeline Studio, ATLAS, etc.). Own brand identity in every portal. Some legacy apps were external GAS projects.
5. **Admin** - Pinned to bottom. Red icon. Flat button (no collapse). Permission-gated.

### Visual Rules
- All sections default **collapsed** with spinning icon animation on expand
- Section headers: uppercase label, 10px, 700 weight, 1.2px letter-spacing
- Icon buttons: 34x34px, subtle background when collapsed, transparent when expanded
- Spin on expand (360deg), spin-back on collapse (-360deg)
- Dividers between major groups (pipelines | modules | apps)

### Per-Portal Sidebar Content

**PRODASHX:**
- Pipelines: Discovery, Data Foundation, Case Building, Close
- Workspace (module): Clients, Accounts, Comms Hub
- Sales Centers (module): Medicare, Life, Annuity, Advisory
- Service Centers (module): RMD Center, Beni Center
- Apps: QUE-Medicare, CAM, C3

**SENTINEL:**
- Pipelines: Prospecting, Sales Process, Transition
- Deal Management (module): All Deals, Producers
- Analysis (module): Business, MEC, PRP, SPH
- Market Intel (module): Agent Search, Carrier Intel, Cross-Reference
- Apps: DAVID-HUB, CAM, Proposal Maker

**RIIMO:**
- Pipelines: On-Boarding, Off-Boarding, Tech Maintenance, Data Maintenance, Security
- RAPID Tools (module): RAPID Import, Platform Intel
- Tool Suites (module): DAVID Tools, RPI Tools
- Apps: CAM, DEX, C3, CEO Dashboard, Command Center

## Admin Panel (Tabbed)

### Standard Tabs (first 3, ALL portals)
| Tab | Icon | Content |
|-----|------|---------|
| **Team Management** | `group` | Add/edit/deactivate users, assign levels (OWNER/LEADER/USER), divisions, reports-to |
| **Pipeline Config** | `route` | Which pipelines exist, per-user View/Edit/Add-Delete permissions |
| **Module Config** | `extension` | Per-module View/Edit/Add permissions per user |

### Portal-Specific Tabs (4+)
| Portal | Additional Tabs |
|--------|----------------|
| PRODASHX | C3/BOB Matrix, Org Structure |
| SENTINEL | Integrations, Database |
| RIIMO | On-Boarding, Off-Boarding, Job Templates, Task Templates, Error Log |

### Permission Gating
| Level | Sees Admin? | Scope |
|-------|-------------|-------|
| USER | No | N/A |
| LEADER | Yes (scoped) | Only their division's users and pipelines |
| OWNER | Yes (full) | Everything |

## My RPI (Top-Right, Tabbed Panel)

### Location
Top-right of topbar. Avatar + name + role. Click opens tabbed panel. **NEVER in left nav.**

### Standard Tabs (first 4, ALL portals)
| Tab | Icon | Content |
|-----|------|---------|
| **Profile** | `badge` | Avatar, name, email, level, division, reports-to |
| **MyDropZone** | `cloud_download` | Meet link, intake folder, booking page, internal calendar |
| **Meetings** (NEW) | `event` | Meeting type CRUD + availability grid |
| **Permissions** | `lock` | Read-only view of module access (V/E/A matrix) |

### Portal-Specific Tabs (5+)
| Portal | Additional Tabs |
|--------|----------------|
| PRODASHX | My Team, Documents |
| SENTINEL | (none) |
| RIIMO | Onboarding, Job Description |

### Meetings Tab Data Model
Stored in `employee_profile` JSON on `_USER_HIERARCHY`:
```json
{
  "meeting_types": [
    { "id": "uuid", "name": "Discovery Call", "duration_minutes": 30, "location_type": "virtual", "description": "" }
  ],
  "availability": {
    "meeting-type-id": {
      "monday": [{"start": "09:00", "end": "09:30"}],
      "wednesday": [{"start": "09:00", "end": "09:30"}, {"start": "11:00", "end": "11:30"}]
    }
  }
}
```

## Shared CSS Delivery
- Master file: `_RPI_STANDARDS/reference/portal/PortalStandard.html`
- Shared via packages/ui in the toMachina monorepo. Legacy GAS projects copied the file.
- Include via: `<?!= include('PortalStandard') ?>`
- Each portal overrides `--portal`, `--portal-glow`, `--portal-accent` on `:root`

## Module vs App Classification
| Type | Definition | Visual Treatment |
|------|-----------|-----------------|
| **Module** | Native `.gs` file in the portal project | Purple icon, solid background |
| **App** | Separate GAS project with its own backend/frontend | Orange icon, dashed border, `open_in_new` icon, opens new window |
