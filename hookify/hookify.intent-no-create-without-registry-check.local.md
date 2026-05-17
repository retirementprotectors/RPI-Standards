---
name: intent-no-create-without-registry-check
enabled: true
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (create\s+(a\s+|the\s+|new\s+)?(folder|directory|sub-?folder|drive\s+folder|shared\s+drive|workspace|google\s+account|firestore\s+collection|cloud\s+run\s+service|github\s+repo|repository|secret|env\s+var|environment\s+variable|cron\s+job|systemd\s+(unit|service)|launchd\s+agent|trigger|mcp(\s+server)?|service\s+account|sa\s+key|oauth\s+(scope|client|token)|api\s+key|workspace\s+ou|domain[- ]wide\s+delegation|dwd|webhook|alias|ou)|mkdir\s+|gh\s+repo\s+create|claude\s+mcp\s+add|gcloud\s+iam\s+service-accounts\s+create|gcloud\s+secrets\s+create|firebase\s+projects:create|gcloud\s+run\s+deploy|drive\.files\.create|spawn\s+(a\s+)?new\s+(mcp|service|wire))
---

## DON'T CREATE WITHOUT REGISTRY CHECK — Mandatory Pre-Flight

**Before creating ANY folder, file, MCP, service account, OAuth scope/client/token, Workspace account or OU, Drive structure, Shared Drive, Firestore collection, GitHub repo, Cloud Run service, secret, environment variable, cron job, systemd unit, launchd agent, trigger, webhook, alias, or DWD grant — CHECK THE REGISTRY FIRST.**

This rule blocks the prompt if a creation intent is detected without prior evidence of a registry consultation. The discipline is universal across every warrior on the platform: SHINOB1, MEGAZORD, MUSASHI, VOLTRON, RAIDEN, RONIN, TAIKO.

### Registries to Check (by domain)

| Domain | Registry | Owner Warrior |
|---|---|---|
| Data sources, atomic tools, super tools, wires | **ATLAS** (Firestore: `source_registry`, `tool_registry`, `atlas_audit`, `import_runs`) | MEGAZORD |
| Client-ops capabilities, product-domain wires | **QUE** | VOLTRON |
| Creative tools (Canva, WordPress, Veo, C3, PDF, Drive, frontend-design) | **CMO Registry** (`packages/core/src/cmo/`) | MUSASHI |
| Comms infrastructure (Twilio, SendGrid, Meet, Chat, RPI Connect) | **Pipes** | TAIKO |
| MCP servers + their exposed tools | **MCP-Hub** (`services/MCP-Hub/`) | SHINOB1 |
| AUTH / IAM / OAuth / DWD / SAs | **`iam_registry` in ATLAS** (when established — currently in audit phase) | MEGAZORD + SHINOB1 |
| Storage / Drive folder taxonomy | **`storage_registry` in ATLAS** (when established) | MEGAZORD + SHINOB1 |
| Secrets / API keys / tokens | **`secrets_registry` in ATLAS** (when established) | MEGAZORD + SHINOB1 |

### What You MUST Do Before Creating

1. **Identify which registry is authoritative** for the asset you're about to create. If multiple registries could be authoritative, default to the warrior owner's registry; if cross-domain, escalate to JDM in the warrior's bilateral channel before creating.
2. **Read the relevant registry** — do not assume. ATLAS via `execute_script` against the registry script ID. CMO Registry via reading `packages/core/src/cmo/`. Pipes via TAIKO's bilateral. MCP-Hub via `claude mcp list` and `services/MCP-Hub/` directory listing.
3. **Verify the asset does NOT already exist** in any form — folder by another name, MCP exposing the tool you want, SA already scoped to the subject you need, etc.
4. **If it exists** — use what exists. Do not duplicate.
5. **If it does NOT exist** — document the WHY in the warrior's bilateral channel BEFORE creation. State which registry was checked, what was searched, and why the new asset is needed.
6. **Then create** — and immediately register the new asset in the appropriate registry. Creation without registration is doctrinally identical to creation without prior check.

### What This Rule Blocks

This rule fires on prompts containing creation intent across these surfaces:

- Filesystem: `mkdir`, folder creation in any IDE, sub-folder creation in Drive
- Google Workspace: new accounts, OUs, aliases, DWD grants
- Cloud infrastructure: `gcloud iam service-accounts create`, `gcloud secrets create`, `gcloud run deploy` (for net-new services), `firebase projects:create`
- Drive API: `drive.files.create` for folders/Shared Drives
- MCP layer: `claude mcp add` for new MCP servers
- GitHub: `gh repo create`
- Process layer: cron jobs, systemd units, launchd agents, triggers, webhooks
- Architectural: new wires, new super tools, new atomic tools without registry inclusion

### How to Bypass (Legitimately)

If creation IS the right answer after checking the registry, the prompt should explicitly include:

- "I checked [REGISTRY NAME] and confirmed [ASSET] does not exist"
- "Creating [ASSET] in [TARGET LOCATION] for [DOCUMENTED REASON]"
- "Will register in [REGISTRY] immediately upon creation"

This pattern bypasses the block because the registry check is documented in the prompt itself.

### Why This Rule Exists

On 2026-05-10 06:45, JDM stated:

> "We need to get REAL FUCKING SERIOUS about Authorization Levels and OAuths and SAs and everything else for Storage and Reference RIGHT NOW. We're CONSTANTLY fucking up our own shit, can't find the scopes, redoing shit that we already had, generally just being fucking embarrassing. We will get COOKED if we introduce new Google Accounts and all the other shit for MWM, and don't have our own house in order. MASSIVE SHIT SHOW!"

In the same session, when SHINOB1 proposed a sprint structure that put the new IAM/Storage/Secrets registries in `_RPI_STANDARDS` documentation rather than ATLAS, JDM corrected:

> "wasn't this the ENTIRE POINT of ATLAS to begin with?"

The pattern of failure being prevented: every CXO and code warrior on the platform has, across many sessions, independently created folders, MCPs, SAs, OAuth scopes, configurations, and documents *without first checking what already exists in the appropriate registry*. The cumulative result is duplicate work, fragmented architecture, scopes that nobody can find when they're needed, configurations that drift apart between machines, and an embarrassing inability to introduce a new partner cleanly because the existing posture was never mapped.

The root cause is human: each session feels urgent, each individual creation feels small, and the cumulative effect is catastrophic.

The correction is also human: *the discipline is on every warrior to check the registry before any creation event.* No exceptions. No "quick fixes." No "just for now" sub-folders. The check is fast — the cost of skipping it is hours-to-days of duplicate work plus architectural debt that compounds session over session.

This rule predates and outranks every other operational doctrine. If a warrior is choosing between "ship fast" and "check registry first," **check registry first wins, every time.**

---

*Doctrinal companion:* This rule is reflected as `## CORE DOCTRINE — DON'T CREATE WITHOUT REGISTRY CHECK` in each warrior's `soul.md` (operational identity, loaded first) and contextualized in each warrior's `spirit.md` (origin context). The hookify rule is the enforcement layer; the soul/spirit entries are the identity layer. Both are required.
