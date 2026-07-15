---
name: registry-check
description: Mandatory pre-flight before creating ANY folder, MCP, service account, OAuth scope, Workspace account/OU, Drive structure, Firestore collection, GitHub repo, Cloud Run service, secret, cron job, systemd unit, or webhook — check the authoritative registry first, verify the asset does not already exist, and register on creation.
version: 0.1.0-draft
---

# Registry Check — Don't Create Without It

You have been invoked as the Registry Check skill. Before creating ANY folder, file, MCP, service account, OAuth scope/client/token, Workspace account or OU, Drive structure, Shared Drive, Firestore collection, GitHub repo, Cloud Run service, secret, environment variable, cron job, systemd unit, launchd agent, trigger, webhook, alias, or DWD grant — CHECK THE REGISTRY FIRST.

This discipline is universal across every warrior on the platform: SHINOB1, MEGAZORD, MUSASHI, VOLTRON, RAIDEN, RONIN, TAIKO.

## Registries to Check (by domain)

| Domain | Registry | Owner Warrior |
|---|---|---|
| Data sources, atomic tools, super tools, wires | **ATLAS** (Firestore: `source_registry`, `tool_registry`, `atlas_audit`, `import_runs`) | MEGAZORD |
| Client-ops capabilities, product-domain wires | **QUE** | VOLTRON |
| Creative tools (Canva, WordPress, Veo, C3, PDF, Drive, frontend-design) | **CMO Registry** (`packages/core/src/cmo/`) | MUSASHI |
| Comms infrastructure (Twilio, SendGrid, Meet, Chat, RPI Connect) | **Pipes** | TAIKO |
| MCP servers + their exposed tools | **MCP-Hub** (`services/MCP-Hub/`) | SHINOB1 |
| AUTH / IAM / OAuth / DWD / SAs | `iam_registry` in ATLAS (when established) | MEGAZORD + SHINOB1 |
| Storage / Drive folder taxonomy | `storage_registry` in ATLAS (when established) | MEGAZORD + SHINOB1 |
| Secrets / API keys / tokens | `secrets_registry` in ATLAS (when established) | MEGAZORD + SHINOB1 |

## Steps

1. **Identify which registry is authoritative** for the asset you're about to create. If multiple registries could be authoritative, default to the warrior owner's registry; if cross-domain, escalate to JDM in the warrior's bilateral channel before creating.
2. **Read the relevant registry** — do not assume. ATLAS via `execute_script` against the registry script ID (see the `/atlas-consult` skill). CMO Registry via reading `packages/core/src/cmo/`. Pipes via TAIKO's bilateral. MCP-Hub via `claude mcp list` and `services/MCP-Hub/` directory listing.
3. **Verify the asset does NOT already exist** in any form — folder by another name, MCP exposing the tool you want, SA already scoped to the subject you need, etc.
4. **If it exists** — use what exists. Do not duplicate.
5. **If it does NOT exist** — document the WHY in the warrior's bilateral channel BEFORE creation. State which registry was checked, what was searched, and why the new asset is needed.
6. **Then create** — and immediately register the new asset in the appropriate registry. Creation without registration is doctrinally identical to creation without prior check.

## Legitimate Bypass

If creation IS the right answer after checking the registry, state explicitly:

- "I checked [REGISTRY NAME] and confirmed [ASSET] does not exist"
- "Creating [ASSET] in [TARGET LOCATION] for [DOCUMENTED REASON]"
- "Will register in [REGISTRY] immediately upon creation"

## Why This Skill Exists

On 2026-05-10, JDM flagged that every CXO and code warrior on the platform had, across many sessions, independently created folders, MCPs, SAs, OAuth scopes, configurations, and documents without first checking what already exists in the appropriate registry — duplicate work, fragmented architecture, scopes nobody could find, configurations that drifted apart between machines. When SHINOB1 proposed putting new IAM/Storage/Secrets registries in `_RPI_STANDARDS` documentation rather than ATLAS, JDM corrected: *"wasn't this the ENTIRE POINT of ATLAS to begin with?"*

**This discipline predates and outranks every other operational doctrine.** If choosing between "ship fast" and "check registry first" — check registry first wins, every time.

---
*Doctrinal companion:* this discipline is reflected as `## CORE DOCTRINE — DON'T CREATE WITHOUT REGISTRY CHECK` in each warrior's `soul.md` and contextualized in `spirit.md`. This skill is the enforcement-by-invocation layer; the soul/spirit entries are the identity layer. Both are required.

---

*SHINOB1, CTO · registry-check · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-no-create-without-registry-check` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
