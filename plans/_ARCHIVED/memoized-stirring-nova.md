> ARCHIVED: Consolidated into riimo-platform-roadmap.md (Stream 7: Booking Engine Phase 6+7) on 2026-03-08

# Phase 7: The Calendly-Killer + Phase 6 Cleanup

## Context

Phase 6 delivered 19 booking pages on WordPress (12 individual + 7 team) with auto-sync, Google profile photos, schema-driven titles, and tiered directory. The "Book Now" buttons currently link to Google Calendar pre-fill URLs — functional but dumb. No availability checking, no contact collection, no automated confirmations.

JDM wants the full Calendly replacement: availability view, meeting mode selection (Call/Meet/F2F), contact form, auto-booking, and automated comms. This plan covers the remaining Phase 6 cleanup AND the Phase 7 booking engine.

---

## Phase 6 Cleanup (30 min, do first)

| Item | Status | Action |
|------|--------|--------|
| Daily sync trigger | JDM ran it — DONE | Verify it's active |
| WP credentials in Script Props | Done via execute_script | Already stored |
| Phase 6.5: Instant sync on save | NOT BUILT | Hook `syncBookingPage()` into `saveUser()` and `updateMeetRoom()` in RIIMO_OrgAdmin.gs and RIIMO_MyRPI.gs |
| Headshot cropping (Vince/Shane/Archer) | DONE (v3.17.1) | Already deployed with per-person object-position |
| On-boarding/Off-boarding pipeline steps | NOT BUILT | Add booking page creation/deletion to pipeline stage configs in `_PIPELINE_CONFIG` |

---

## Phase 7: Booking Engine Architecture

### Architecture Decision: RAPID_API iframe + WordPress shell

**Why this approach:**
- RAPID_API is already public (`ANYONE_ANONYMOUS`) — the only RPI GAS app with public access
- RAPID_API has RAPID_CORE library → direct access to `_USER_HIERARCHY`, `CalendarApp`, `MailApp`
- WordPress pages already exist → embed the booking form as an iframe
- No new GAS project needed — extends RAPID_API with a `?page=booking` HTML route
- CalendarApp gives native Google Calendar read/write (no MCP needed from GAS)

**Data flow:**
```
Client visits retireprotected.com/book/vince/
    ↓
WordPress page loads iframe: RAPID_API?page=booking&agent=vince
    ↓
GAS serves booking HTML (date picker, contact form)
    ↓
Client selects meeting type → JS calls google.script.run.getAvailableSlots()
    ↓
GAS checks CalendarApp.getEvents() for agent's calendar
    ↓
Returns available time slots → client picks one
    ↓
Client fills: name, email, phone, guests, reason, mode (Call/Meet/F2F)
    ↓
JS calls google.script.run.createBooking()
    ↓
GAS creates CalendarApp event + logs to _BOOKING_LOG + sends confirmations
    ↓
Client sees confirmation with Meet link + calendar invite
```

### Key Files to Modify

| File | Changes |
|------|---------|
| `RAPID_API/Code.gs` | Add `?page=booking` route in `doGet()` |
| `RAPID_API/BOOKING_UI.html` | NEW — booking form frontend (date picker, contact form, confirmation) |
| `RAPID_API/API_Booking.gs` | NEW — backend: `getAvailableSlots()`, `createBooking()`, `sendConfirmation()` |
| `RAPID_CORE/CORE_Database.gs` | Add `_BOOKING_LOG` tab schema to TABLE_ROUTING |
| `RIIMO/RIIMO_MyRPI.gs` | Extend `employee_profile` schema with `availability` config |
| `RIIMO/MyRPI.html` | Add availability editor (business hours, blocked dates, F2F toggle) |

### Schema Extensions

**`employee_profile.availability` (new field):**
```javascript
{
  timezone: "America/Chicago",
  business_hours: {
    mon: { start: "09:00", end: "17:00" },
    tue: { start: "09:00", end: "17:00" },
    wed: { start: "09:00", end: "17:00" },
    thu: { start: "09:00", end: "17:00" },
    fri: { start: "09:00", end: "12:00" },
    sat: null,  // unavailable
    sun: null
  },
  buffer_minutes: 15,        // gap between meetings
  max_advance_days: 90,      // how far ahead clients can book
  allow_f2f: false,          // F2F meetings enabled (internal toggle)
  f2f_location: ""           // office address when F2F enabled
}
```

**`employee_profile.calendar_booking_types` extension:**
```javascript
{
  name: "Discovery Call",
  duration_minutes: 60,
  category: "standard",
  modes: ["meet", "call"],   // NEW: available modes (meet/call/f2f)
  auto_confirm: true         // NEW: auto-create event or require approval
}
```

**`_BOOKING_LOG` tab (new in RAPID_MATRIX):**
| Column | Type | Description |
|--------|------|-------------|
| booking_id | string | UUID |
| agent_email | string | Team member's email |
| client_name | string | Booker's name |
| client_email | string | Booker's email |
| client_phone | string | Booker's phone |
| guests | string | CC/additional attendees (comma-separated emails) |
| booking_type | string | Meeting type name |
| meeting_mode | string | "meet" / "call" / "f2f" |
| scheduled_start | string | ISO datetime |
| scheduled_end | string | ISO datetime |
| duration_minutes | number | Meeting duration |
| reason | string | Client's stated reason |
| status | string | confirmed / cancelled / rescheduled |
| calendar_event_id | string | Google Calendar event ID |
| meet_link | string | Google Meet URL (auto-generated) |
| confirmation_sent | boolean | Email + SMS sent |
| created_at | string | ISO datetime |

### Frontend Design (BOOKING_UI.html)

**Step 1: Meeting Type Selection**
- Cards for each booking type (same design as current pages)
- Mode selector under each: Call | Google Meet | In-Person (F2F greyed out unless agent allows it)

**Step 2: Date/Time Selection**
- Calendar grid (current month + next)
- Available days highlighted (based on business_hours + actual calendar)
- Click day → shows time slots in 30-min increments
- Unavailable slots greyed out (existing events + buffer)

**Step 3: Contact Info**
- Name (required)
- Email (required)
- Phone (required)
- Additional guests (optional, email field)
- Reason for meeting (optional text)

**Step 4: Confirmation**
- Summary: date, time, type, mode, meet link
- "Add to Calendar" button (downloads .ics)
- "A confirmation has been sent to your email and phone"

### Backend Functions (API_Booking.gs)

```
getBookingConfig(agentSlug)
  → Returns: agent name, photo, job_title, booking_types, availability, timezone

getAvailableSlots(agentEmail, date, bookingTypeIdx)
  → Checks CalendarApp for existing events
  → Applies business_hours + buffer
  → Returns array of { start, end } available slots

createBooking(agentEmail, slot, clientInfo, bookingType, mode)
  → Creates CalendarApp event (with or without Meet link based on mode)
  → Writes to _BOOKING_LOG
  → Sends confirmation email via RAPID_COMMS (SendGrid template)
  → Sends confirmation SMS via RAPID_COMMS (Twilio)
  → Sends Slack DM to agent
  → Returns { success, booking_id, meet_link, calendar_link }
```

### Communications (Automated)

**To Client (on booking):**
- Email: Confirmation with meeting details, Meet link, reschedule link
- SMS: "Your [type] with [agent] is confirmed for [date] at [time]. Meet link: [url]"

**To Team Member (on booking):**
- Slack DM: ":calendar: New [type] booked by [client_name] for [date] at [time]. Mode: [meet/call/f2f]. Reason: [reason]"
- Google Calendar event auto-appears (they're an attendee)

**Reminders (24hr before):**
- Email to client: "Reminder: Your meeting with [agent] is tomorrow at [time]"
- SMS to client: Same
- (Agent gets Google Calendar reminder natively)

---

## Implementation Phases

### Phase 7a: Core Booking Engine (Session 1)
1. Create `_BOOKING_LOG` tab schema in RAPID_CORE
2. Add `?page=booking` route to RAPID_API doGet()
3. Build `API_Booking.gs` — getBookingConfig, getAvailableSlots, createBooking
4. Build `BOOKING_UI.html` — meeting type cards, date picker, contact form, confirmation
5. Update WordPress booking pages: replace Google Calendar links with iframe embed
6. Test end-to-end: book a meeting → calendar event created → confirmations sent

### Phase 7b: Availability Management (Session 2)
1. Add `availability` schema to employee_profile
2. Build RIIMO MyRPI availability editor section:
   - Editable by the user themselves (own profile)
   - Editable by LEADER+ via the profile switcher (viewing a direct report's profile)
   - Business hours per day (start/end time dropdowns)
   - Blocked dates (date picker for vacations/PTO)
   - F2F toggle + location field (leadership-controlled)
   - Meeting mode preferences per booking type (Call/Meet/F2F checkboxes)
3. Seed default availability for all 12 team members
4. Wire availability into getAvailableSlots() (real calendar + business hours)
5. Add mode selector to booking form (Call/Meet/F2F with gating)

### Phase 7c: Communications + Polish (Session 3)
1. SendGrid email templates for booking confirmation + reminder
2. Twilio SMS confirmation + reminder
3. 24-hour reminder trigger (GAS time-driven)
4. Reschedule/cancel flow (link in confirmation email → updates event + log)
5. On-boarding/off-boarding pipeline integration (auto-create/delete booking pages)

---

## Verification

1. Visit `retireprotected.com/book/vince/` → see iframe booking form
2. Select "Discovery Call" → see available dates/times
3. Pick a slot → fill name/email/phone → submit
4. Check: Google Calendar event created on Vince's calendar with Meet link
5. Check: Confirmation email received by client
6. Check: Confirmation SMS received by client
7. Check: Slack DM sent to Vince
8. Check: `_BOOKING_LOG` has the record
9. Check: RIIMO MyRPI shows booking URL with QR code (already done)
