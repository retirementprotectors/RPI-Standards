---
name: block-direct-firestore-write
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: db\.collection\(|\.collection\(.*\)\.doc\(|getFirestore\(\)\.collection\(
  # FIX 2026-06-01 (shinob1, JDM-authorized "you can handle it"; megazord notified): the
  # `exclude:` clause below was DEAD config — the hookify engine never parses `exclude:`
  # (same class that bricked block-warrior-boot-without-workflow, 2026-05-19). So this rule
  # silently false-blocked legit Firestore reads/writes in services/api/src/ etc. The
  # authorized-path exemptions are now baked into a file_path negative-lookahead so they
  # ACTUALLY apply: block fires only when content matches AND path is NOT authorized.
  # MEGAZORD's policy is unchanged — this only restores the exemptions to working order.
  # Surfaced by RONIN-Asset (tm2 Index couldn't wire live A1/A2 substrate reads). Verified 6/6.
  # FIX 2026-06-09 (shinob1, JDM-authorized "GO FIRESTORE"; megazord notified): added
  # `docs/.*\.html` to the exemption. The content regex above matches ANY Firestore
  # collection/doc access — including read-only reads — so APPA standalone-HTML tools
  # (docs/*.html, the JDM-blessed Firebase-web-SDK prototype lane) were false-blocked
  # even on pure reads. Precedent: docs/partners/midwest-medigap/dashboard.html +
  # docs/que/medicare-medsupp-quote-v1.html. Direct Firestore stays gated in apps/ +
  # packages/ (must use the API proxy); only services/* and docs/*.html are exempt.
  # JDM 2026-06-09: "Hard to write when you're just reading, and we have HARD GATES for
  # write-shape on Client/Account data now." Surfaced by VOLTRON-MSG.
  - field: file_path
    operator: regex_match
    # FIX 2026-06-27 (ronin, TRK-14785): added mdj-agent/src/ — the mdj-agent is a
    # standalone server-side service (firebase-admin already initialized in agent/firebase.ts,
    # db used throughout). Same class as services/api/src/. Surfaced by TRK-14785 audit-first wiring.
    # FIX 2026-07-07 (ronin-approval-signer, MEGAZORD-APPROVAL-SIGNER-001, MEGAZORD parent-owner):
    # added services/approval-signer/ -- a NEW standalone Cloud Run deployable, own dedicated SA
    # (approval-hub-signer@...), that writes action_approvals/{id} directly (the money-movement
    # release path). Same class as services/api/src/ + mdj-agent/src/: a server-side service with
    # its own firebase-admin init, not portal/package code that must go through the API proxy.
    pattern: ^(?!.*(services/api/src/|services/bridge/src/|services/intake/|services/bigquery-stream/|services/learning-loop/|mdj-agent/src/|services/approval-signer/|docs/.*\.html|inbox/.*\.html|\.(test|spec)\.(ts|js)|\.(md|txt)$)).*
owner: megazord
---

**BLOCKED: Direct Firestore Write Outside API**

You are writing directly to Firestore outside the authorized write paths.

**Why this is blocked:**
- All data modifications must go through the API write gate
- Direct writes bypass validation, audit logging, and the bridge dual-write layer
- This creates data integrity risks and breaks the single-source-of-truth pattern

**Authorized write paths:**
- `services/api/src/` — Cloud Run REST API (primary write gate)
- `services/bridge/src/` — Dual-write bridge (Firestore + Sheets)
- `services/intake/` — Intake Cloud Functions
- `services/bigquery-stream/` — BigQuery streaming Cloud Functions
- `mdj-agent/src/` — MDJ Agent server-side service (firebase-admin, server runtime)

**Fix:**
- Move your Firestore write logic into the appropriate service
- For new API endpoints: add a route in `services/api/src/routes/`
- For data ingestion: use the intake Cloud Functions
- For read-only access in portal code: use the API client (`/api/[...path]` proxy)

See: `~/Projects/toMachina/CLAUDE.md` -> API Proxy Architecture
