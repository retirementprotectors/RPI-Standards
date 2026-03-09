# RPI Connect — Enhancement Plan

## Context

Phase 3 (Dynamic Sidebars) and Phase 8 MVP (Messenger drawer) are deployed and working across all 3 portals. JDM feedback:

1. **Rename** "Messenger" → "RPI Connect" — it's more than messaging
2. **FAB trigger** — floating action button instead of pinned to sidebar bottom. Draggable.
3. **Shield styling** — gradient background washes out the shield leaves. Needs to be bigger/cleaner.
4. **Header cramped** — messenger header needs more vertical padding
5. **Meet integration** — "Start Meet" per channel AND per DM. Quick 1-click calls.
6. **Favorites bar** — top 5 team members for instant chat/meet (PRODASHX already has this as `teamQuickComms` in the header — kill it there, move into RPI Connect)
7. **Calendar tab** — show today's agenda / upcoming meetings
8. **Threads tab** — currently placeholder, needs real implementation

---

## Existing Code to Reuse

| What | Where | Reuse How |
|------|-------|-----------|
| Team quick comms (avatars + Meet) | `PRODASHX/Scripts.html:189-243, 14244-14340` | Move favorites concept into RPI Connect |
| `uiCreateQuickMeeting(email)` | `PRODASHX/PRODASH_Communications.gs:254-300` | Reuse for Meet-per-DM. Port to RIIMO/SENTINEL. |
| `uiGetTeamMembers()` | `PRODASHX/PRODASH_Communications.gs` | Backend for favorites bar |
| Meet MCP tools | `rpi-workspace-mcp/src/meet-tools.js` | `meet_create_meeting`, `meet_list_upcoming` |
| Calendar MCP tools | `google-calendar` MCP | `list-events`, `get-freebusy`, `create-event` |
| Huddle bar mockup | `PRODASHX/Docs/RPI_MESSENGER_MOCKUP.html:285-362` | Design pattern for active Meet indicator |
| ~~CEO-Dashboard Meet~~ | N/A — irrelevant, ignore | N/A |

---

## Build Plan

### Wave 1: RPI Connect Core Redesign (all 3 portals)

**1a. FAB Trigger (replace sidebar-pinned shield)**
- Remove `.rpi-shield-trigger` from inside `<aside>` on all 3 portals
- Add floating `<div class="rpi-connect-fab">` to body, positioned `bottom: 24px; right: 24px`
- 56px circle, RPI shield SVG (inline, not img — no gradient wash)
- Draggable via mousedown/touchstart (save position to localStorage)
- Notification badge for unread count
- Pulse animation when active Meet exists

**1b. Rename + Header Fix**
- "Messenger" → "RPI Connect" in drawer header
- Increase header padding: `14px 16px 10px` → `16px 16px 14px`
- Shield icon in header stays

**1c. Shield SVG Fix**
- Replace `<img src="...RPI-3.svg">` with inline SVG
- No gradient background on FAB — use solid dark circle with subtle border glow
- Shield renders at native quality, no filter/brightness hacks

### Wave 2: Tabs Redesign

Current: `Channels | Chat | Threads`
Phase I: `Channels | Chat | Meet`
Phase II (future): Add `Schedule` tab with internal meeting templates framework

**2a. Channels tab** — keep as-is (working)

**2b. Chat tab** — keep as-is (DM spaces)

**2c. Meet tab (NEW)**
- **Favorites bar** at top: 5 team member avatars (from `_USER_HIERARCHY`)
  - Click avatar → instant Meet (calls `uiCreateQuickMeeting`)
  - Long-press → choose: Meet / Chat / View Profile
  - Configurable: gear icon opens picker (same as current `openTeamEditor()` pattern)
  - Stored in localStorage per-user
- **Active Meets** section: list any calendar events happening NOW with Meet links
  - Green pulse indicator
  - "Join" button
  - Participant avatars
- **Start Meet** button: create ad-hoc Meet (no calendar event, just a link)

**2d. Schedule tab — PHASE II (deferred)**
- NOT just "today's agenda" — needs proper internal meeting framework
- Internal meeting templates: TouchBase, Project Work, PRP (Performance/Review/Plan), Quarterly Review
- Recurring vs one-time meeting types
- Internal meetings vs Client-facing structures (different templates)
- Wire to INTERNAL Meetings Page by person to schedule using existing calendar framework
- This is a separate phase — too much scope for this build

### Wave 3: Per-Channel/DM Meet Actions

- Add "Start Meet" icon button next to each channel name in the list
- Add "Start Meet" icon button next to each DM
- When Meet is active in a channel, show green indicator + "Join" link
- Compose area gets a "Start Meet" button (like mockup's huddle button)

### Wave 4: Remove PRODASHX Header Team Comms

- Remove `#teamQuickComms` div from PRODASHX Index.html header
- Remove `loadTeamQuickComms()` call from init
- Remove `renderFilteredTeamAvatars()`, `showTeamQuickActions()`, `openTeamEditor()` from Scripts.html
- The favorites bar in RPI Connect replaces this entirely

---

## Files to Modify

### Modified (per portal)
| File | Changes |
|------|---------|
| `RPI_Messenger.html` → rename to `RPI_Connect.html` | Full rewrite: FAB, new tabs, Meet tab, Schedule tab, favorites bar |
| `*_Messenger.gs` | Add: `uiGetTodayEvents()`, `uiCreateQuickMeeting()` (port from PRODASHX), `uiGetTeamFavorites()` |
| `Index.html` (all 3) | Remove shield trigger from sidebar, add FAB to body, update include name |
| `PRODASHX/Index.html` | Remove `#teamQuickComms` from header |
| `PRODASHX/Scripts.html` | Remove team quick comms JS functions |
| `appsscript.json` (all 3) | Add Calendar scope (for Meet link creation): `https://www.googleapis.com/auth/calendar` |

### New (0 new files — all modifications to existing)

---

## Backend Functions Needed (per-platform .gs)

```
uiGetChatSpaces()           — EXISTING
uiGetChatMessages(space)    — EXISTING
uiSendChatMessage(space, t) — EXISTING
uiReplyToThread(s, t, txt)  — EXISTING
uiGetChatMembers(space)     — EXISTING
uiCreateQuickMeeting(email) — PORT from PRODASH_Communications.gs
uiGetTeamFavorites()        — NEW (reads _USER_HIERARCHY, returns top team members)
```

---

## Verification

- [ ] FAB visible on all 3 portals (floating, bottom-right)
- [ ] FAB draggable, position persists across page loads
- [ ] Clicking FAB opens RPI Connect drawer
- [ ] "RPI Connect" header (not "Messenger")
- [ ] Shield SVG renders clean (no gradient wash)
- [ ] Channels tab loads spaces + messages (existing functionality)
- [ ] Chat tab shows DMs (existing)
- [ ] Meet tab shows favorites bar with 5 team avatars
- [ ] Click favorite → instant Google Meet link created + opened
- [ ] Favorites configurable via gear icon
- [ ] Threads tab placeholder says "Phase II" (deferred)
- [ ] Schedule tab NOT present (Phase II scope)
- [ ] Per-channel "Start Meet" button works
- [ ] PRODASHX header team comms removed (no duplicate)
- [ ] No alert/confirm/prompt
- [ ] All ForUI functions use JSON.parse(JSON.stringify())

---

## Estimated Scope
- `RPI_Connect.html`: ~600 LOC (rewrite of current ~380 LOC messenger)
- Backend .gs additions: ~80 LOC per platform (3 new functions)
- Index.html changes: ~-20 LOC net (remove sidebar trigger, add FAB, update include)
- PRODASHX cleanup: ~-150 LOC (remove team quick comms)
- **Net: ~700 LOC added, ~170 LOC removed**
