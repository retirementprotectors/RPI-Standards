> ARCHIVED: Superseded by memoized-stirring-nova.md on 2026-03-08

# Phase 6: Booking Pages (Calendly-Style)

## Context

Operation Virus Kill unified all org data into _USER_HIERARCHY. Calendar booking types (6 types) and meet links are already stored in employee_profile. Team members need a public URL to share with clients/prospects so they can book meetings. RIIMO is org-only, so the public page lives on WordPress (retireprotected.com). The internal piece (copy your booking URL) lives in RIIMO's MyDropZone.

## Architecture Decision

**WordPress** at `retireprotected.com/book/vinnie/` — not a GAS web app.

Why:
- RIIMO and RAPID_API are org-only — clients can't access them
- `retireprotected.com/book/vinnie` is business-card-ready; `script.google.com/macros/s/AKfycb...` is not
- Zero PHI exposure risk — WordPress is isolated from MATRIX
- WordPress MCP tools already available
- No new GAS project to maintain

## Data Flow

```
_USER_HIERARCHY.employee_profile (source of truth)
    ↓ booking_types, meet_link, name, job_title
    ↓
WordPress pages (static HTML, synced on demand)
    ↓
Client visits retireprotected.com/book/vinnie
    ↓ clicks "Discovery Call (60 min)"
    ↓
Google Calendar opens with pre-filled event
    (title, duration, meet link, agent as attendee)
```

Data is baked into each WordPress page as HTML. No live API calls needed. When booking types change (rare), agent clicks "Publish" in MyDropZone to sync.

## Implementation Plan

### Step 1: Seed booking_slug values
- **File:** `RIIMO/RIIMO_MyRPI.gs`
- Add `FIX_SeedBookingSlugs()` — sets `employee_profile.booking_slug` = lowercase first name for each active user with a meet_link
- Execute via execute_script

### Step 2: Create WordPress parent page
- **Tool:** `wordpress_create_post` (or page equivalent via MCP)
- Create parent page with slug `book` at retireprotected.com/book/
- Minimal content: "Schedule a meeting with our team"
- Check if `wordpress_create_post` supports pages — if not, may need to add page support to wordpress-tools.js

### Step 3: Create per-member WordPress booking pages
- **Tool:** WordPress MCP or GAS UrlFetchApp
- For each team member with a booking_slug: create a child page under /book/
- Page content = self-contained HTML + inline CSS + inline JS
- Template renders: name, job_title, booking type cards, Google Calendar link generator
- Mobile-responsive, RPI-branded (inline styles — Elementor CSS won't compile via REST API)
- Google Calendar link format: `https://calendar.google.com/calendar/r/eventedit?text=Discovery+Call+with+Vinnie&dates=START/END&location=MEET_LINK&add=AGENT_EMAIL`
- Calendar link JS: user picks a date/time slot, or just "Book Now" generates a link for tomorrow (MVP)

### Step 4: Update RIIMO MyDropZone — booking URL display
- **File:** `RIIMO/MyRPI.html`
- In `_myrpiRenderMeetRoom()`: add row showing `retireprotected.com/book/{slug}` with Copy + Open buttons
- Only shows if user has `booking_slug` in employee_profile
- Add `booking_slug` field to the meet room edit form

### Step 5: Add "Publish Booking Page" to RIIMO
- **File:** `RIIMO/RIIMO_MyRPI.gs` + `MyRPI.html`
- Backend: `publishBookingPage(callerEmail, targetUserId)` — reads profile, generates HTML template, pushes to WordPress via WP REST API (credentials in Script Properties)
- Frontend: "Publish Booking Page" button in MyDropZone, calls backend on click
- OR: simpler — Claude syncs via MCP when booking types change (no GAS→WP integration needed for MVP)

### Step 6: Deploy + Test
- Deploy RIIMO (booking_slug seed + MyDropZone update)
- Verify WordPress pages load on mobile
- Test Google Calendar links open correctly with pre-filled data
- Test Copy button in MyDropZone

## Booking Page HTML Template (per member)

```
Header: "Book a Meeting with {First Name}"
Subtitle: "{Job Title} at Retirement Protectors"

Cards (one per booking type):
  ┌─────────────────────────┐
  │  Discovery Call          │
  │  60 minutes              │
  │  [Book Now]              │
  └─────────────────────────┘
  ┌─────────────────────────┐
  │  Follow-Up               │
  │  30 minutes              │
  │  [Book Now]              │
  └─────────────────────────┘
  ... etc

Footer: "Powered by Retirement Protectors"
```

"Book Now" → opens Google Calendar with:
- Title: "{Type Name} with {First Name}"
- Duration: from booking_type.duration_minutes
- Location: meet_link
- Attendee: agent email

## Key Files

| File | Change |
|------|--------|
| `RIIMO/RIIMO_MyRPI.gs` | FIX_SeedBookingSlugs(), publishBookingPage() |
| `RIIMO/MyRPI.html` | Booking URL row + copy button + slug edit field |
| WordPress (via MCP) | Parent /book/ page + child pages per member |

## MVP Simplification

For MVP, skip the GAS→WordPress publish integration. Instead:
1. Seed slugs via execute_script
2. Create WordPress pages via MCP (Claude does it once)
3. MyDropZone shows the URL with copy button
4. When booking types change, JDM says "sync booking pages" and Claude updates WordPress via MCP

This avoids WordPress credentials in GAS Script Properties and keeps the sync simple. The automated publish button is a Phase 6.5 enhancement.

## Verification

1. Visit `retireprotected.com/book/vinnie/` on phone — see booking cards
2. Click "Book Now" on Discovery Call — Google Calendar opens with 60-min event, meet link, vinnie@ as attendee
3. In RIIMO MyDropZone — see booking URL, copy it, open it
4. Change a booking type in MyRPI — ask Claude to sync — WordPress page updates
