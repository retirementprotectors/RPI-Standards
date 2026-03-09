# Humana FHIR Patient Access API — Implementation Plan

## Context

Humana approved RPI's FHIR API application. Credentials are live. The MCP code (`humana-fhir-tools.js`) already has 24 tools wired in, but the **auth URLs are wrong** and **refresh token support is missing**. This plan fixes the code to match Humana's actual endpoints and adds the missing pieces.

This is a **Patient Access FHIR API** — member-mediated OAuth (Authorization Code flow). Members log in at Humana, authorize data sharing, and we pull their health data (Coverage, EOBs, Medications, Conditions, etc.).

---

## Changes (2 files + 1 comment update)

### File 1: `rpi-healthcare-mcp/src/humana-fhir-tools.js` (primary)

**1. Fix `HUMANA_CONFIG` — add Patient Access auth URLs (lines 18-28)**
| Field | Sandbox | Production |
|-------|---------|------------|
| `patientAuthUrl` | `https://sandbox-fhir.humana.com/auth/authorize` | `https://fhir.humana.com/auth/authorize` |
| `patientTokenUrl` | `https://sandbox-fhir.humana.com/auth/token` | `https://fhir.humana.com/auth/token` |
| `patientAud` | `https://sandbox-fhir.humana.com/api` | `https://fhir.humana.com/api` |

Existing `tokenUrl` (for client_credentials Agent/Plan APIs) stays as-is.

**2. Fix `humana_get_patient_auth_url` (line 331)**
- Add `environment` param to tool definition (default: `production`)
- Use `config.patientAuthUrl` instead of hardcoded sandbox URL
- Use `config.patientAud` instead of hardcoded sandbox aud

**3. Fix `humana_exchange_patient_code` (line 356)**
- Use `config.patientTokenUrl` instead of hardcoded `/oauth2/token` URLs
- Add `patient` field to response (Humana returns patient ID in token response)
- Default environment to `production`

**4. Add `humana_refresh_patient_token` — NEW tool**
- POST to `config.patientTokenUrl` with `grant_type=refresh_token`
- Returns new access_token + refresh_token (tokens may rotate)
- HEM tier: T3

**5. Update FHIR resource enum (line 190)**
- Add: `Goal`, `DocumentReference`, `List` (per Humana's actual supported resources)
- Remove: `DiagnosticReport` (not in Humana's list)
- Update `HUMANA_CONFIG.apis.patientAccess.resources` to match

**6. Update `humana_get_api_status` (line 404)**
- Environment-aware status (`PRODUCTION_APPROVED` vs `SANDBOX_ACTIVE`)
- Add per-API approval status (Patient Access = approved, others = pending)
- Tool count: 24 → 25

### File 2: `analytics/hem-config.json`
- Add `"humana_refresh_patient_token": "T3"`

### File 3: `rpi-healthcare-mcp/src/index.js` (comment only)
- Update tool count comment: 24 → 25 Humana tools, 78 → 79 total

---

## Callback Strategy: Playwright (zero infrastructure)

No new callback handler needed. The MCP workflow:
1. `humana_get_patient_auth_url` → generates auth URL
2. Open in Playwright → member logs in at Humana, authorizes
3. Playwright reads redirect URL → extracts `?code=XXX` from URL bar
4. `humana_exchange_patient_code` → exchanges code for tokens
5. `humana_fetch_patient_data` → pulls FHIR resources
6. `humana_refresh_patient_token` → renews when token expires

The registered redirect URI (`https://prodash.com/callback`) will 404 for now — that's fine. Playwright captures the code from the URL bar before the page loads.

---

## Non-Patient APIs (Agent, Plan Info, Eligibility, etc.)

**Leave as-is.** The 18 non-Patient-Access tools are structurally correct and will work when those API scopes are approved. No removal, no changes.

---

## Test Strategy

| Phase | Test | Needs Member? |
|-------|------|---------------|
| 1 | `humana_get_api_status(environment: 'production')` — verify URLs + tool count | No |
| 2 | `humana_get_patient_auth_url(redirectUri, state, environment: 'production')` — verify correct auth URL generated | No |
| 3 | Full OAuth flow via Playwright — generate URL, member authorizes, capture code, exchange for tokens, fetch Patient resource | Yes |
| 4 | `humana_refresh_patient_token` — refresh the token from Phase 3 | No (uses Phase 3 token) |

---

## After Implementation

1. Commit + push MCP-Hub
2. JDM runs `/export`, restarts Claude Code for MCP to pick up changes
3. Run test phases 1-2 immediately (no member needed)
4. Phase 3-4 when a Humana member is available for testing
