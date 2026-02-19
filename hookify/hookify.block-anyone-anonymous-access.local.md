---
name: block-anyone-anonymous-access
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: appsscript\.json$
  - field: content
    operator: regex_match
    pattern: "access"\s*:\s*"(ANYONE_ANONYMOUS|ANYONE)"
---

**BLOCKED: Public Web App Access Detected in appsscript.json**

You are setting web app access to `ANYONE` or `ANYONE_ANONYMOUS` in `appsscript.json`.

**Why this is blocked:**
- All RPI internal apps MUST be restricted to organization-only access
- `appsscript.json` is the source of truth — `clasp push` deploys this setting
- Setting DOMAIN in the GAS editor UI is NOT enough if the source file disagrees
- Public access means anyone on the internet can access the app without authentication

**Fix:**
Change the access setting in `appsscript.json`:
```json
{
  "webapp": {
    "access": "DOMAIN",
    "executeAs": "USER_DEPLOYING"
  }
}
```

**Exception:** RAPID_API uses `ANYONE_ANONYMOUS` intentionally for SPARK webhook reception. If this is an approved exception, document the rationale in `POSTURE.md`.

See: `_RPI_STANDARDS/reference/os/POSTURE.md`
