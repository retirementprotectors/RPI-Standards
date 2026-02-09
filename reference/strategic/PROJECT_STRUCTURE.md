# RPI Projects Folder Structure

> **Purpose**: Document the structure of `/Users/joshd.millang/Projects` so the same framework can be replicated on another machine.  
> **Last updated**: February 9, 2026

---

## 1. Top-level layout

All work lives under **one** root: `~/Projects/`. Nothing lives in `~/` or random repos elsewhere.

```
~/Projects/
├── _RPI_STANDARDS/     # Standards, rules, reference docs (this repo)
├── PRODASH_TOOLS/      # B2C apps (RPI channel)
├── RAPID_TOOLS/        # Shared services / B2E
└── SENTINEL_TOOLS/     # B2B apps (DAVID channel)
```

**Rule**: New projects go inside the correct *SuperProject* folder (see `new-project/PROJECT_KICKOFF_TEMPLATE.md`).

---

## 2. _RPI_STANDARDS (framework to copy)

This folder is the **single source of truth** for conventions and rules. Copy it first to the other machine.

```
_RPI_STANDARDS/
├── CLAUDE.md                    # Global agent instructions (symlinked to ~/.claude/CLAUDE.md)
├── hookify/                     # Hookify rule files (*.local.md)
│   ├── hookify.block-alert-confirm-prompt.local.md
│   ├── hookify.block-drive-url-external.local.md
│   ├── hookify.block-forui-no-json-serialize.local.md
│   ├── hookify.block-hardcoded-colors.local.md
│   ├── hookify.block-hardcoded-matrix-ids.local.md
│   ├── hookify.block-hardcoded-secrets.local.md
│   ├── hookify.block-let-module-caching.local.md
│   ├── hookify.block-phi-in-logs.local.md
│   ├── hookify.warn-date-return-no-serialize.local.md
│   ├── hookify.warn-missing-structured-response.local.md
│   ├── hookify.warn-modal-no-flexbox.local.md
│   └── hookify.warn-phi-in-error-message.local.md
├── reference/                   # Read-only reference; don’t copy into projects
│   ├── archive/                 # Legacy setup, plans, misc
│   ├── compliance/              # PHI, security, audit
│   ├── integrations/           # GHL, MATRIX
│   ├── maintenance/             # Audits, health checks
│   ├── new-project/             # PROJECT_KICKOFF_TEMPLATE.md
│   ├── playbooks/               # Team playbooks
│   ├── production/              # Launch checklists, rollout
│   └── strategic/               # Vision, roadmap, architecture
└── scripts/
    └── setup-hookify-symlinks.sh   # Run on new machine to link CLAUDE.md + hookify
```

**New-machine setup**: From `_RPI_STANDARDS/`, run:

```bash
./scripts/setup-hookify-symlinks.sh
```

This script:

- Symlinks `~/.claude/CLAUDE.md` → `_RPI_STANDARDS/CLAUDE.md`
- For each project in its list, creates `.claude/` and symlinks every `hookify/*.local.md` into it

The script’s project list is the canonical list of “RPI projects” (see inside the script for the full array).

---

## 3. PRODASH_TOOLS (B2C)

```
PRODASH_TOOLS/
├── PRODASH/                     # Main client portal (GAS + Clasp)
│   ├── .clasp.json, appsscript.json, .gitignore
│   ├── CLAUDE.md
│   ├── Code.gs
│   ├── PRODASH_*.gs             # Modules (Accounts, Clients, Client360, RMD_CENTER, Testing)
│   ├── Docs/                    # 0-SESSION_HANDOFF, 1-AGENT_BRIEFING, 2.x, 3.x scopes
│   ├── ProDash_MATRIX_Fields/   # CSV config (GHL contacts, pipelines, products)
│   ├── Index.html, Scripts.html, Styles.html
│   └── DEBUG_API.gs
└── QUE/
    └── QUE-Medicare/            # Medicare quoting (GAS + Node API)
        ├── .clasp.json, appsscript.json, .gitignore
        ├── CLAUDE.md, Code.gs
        ├── Docs/                # Agent briefing, scope, carrier API, TODO
        ├── lib/                 # blue-button-parser, cost-calculator, mcp-client, quote-engine
        ├── api/server.js
        ├── test/
        └── package.json
```

---

## 4. RAPID_TOOLS (shared services / B2E)

Pattern: **GAS (Google Apps Script)** projects use **Clasp**, a `Docs/` folder with numbered agent docs, and a root `CLAUDE.md`. Node/cloud projects have their own layout.

```
RAPID_TOOLS/
├── C3/                          # Content Block Manager (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md, Code.js
│   ├── docs/                    # Agent briefing, scope, guides (HTML/PDF)
│   └── *.xlsx                   # Content library, GHL spec, etc.
│
├── CAM/                         # Commission Accounting (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md
│   └── (similar GAS + docs pattern)
│
├── CEO-Dashboard/               # Executive visibility (GAS + docs)
│   └── (GAS + markdown/docs)
│
├── DEX/                         # Document/forms pipeline (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md, Code.gs
│   ├── DEX_*.gs                 # ClientData, Config, DocuSign, FormLibrary, KitBuilder, etc.
│   └── Docs/                    # 0-SESSION_HANDOFF, 1-AGENT_BRIEFING, 2.x, 3.x scopes
│
├── MCP-Hub/                     # Node.js MCP / meeting intelligence
│   ├── CLAUDE.md, README.md, mcp.json, .env.example
│   ├── docs/                    # Setup, handoffs, integration guides
│   ├── commission-intelligence/ # JSON config
│   ├── document-processor/      # Node (watcher, etc.)
│   ├── healthcare-mcps/         # Node API (QUE server, Medicare, FHIR, etc.)
│   └── rpi-meeting-processor/   # Node (meeting processor)
│
├── PDF_SERVICE/                 # Cloud PDF service (Node, Vercel/GCP)
│   ├── CLAUDE.md, README.md
│   ├── index.js, package.json
│   ├── Dockerfile, cloudbuild.yaml, vercel.json
│   └── (build output: dist, etc.)
│
├── RAPID_API/                   # REST API (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md, Code.gs
│   ├── API_*.gs                 # Account, Activity, Agent, Client, GHL_Sync, etc.
│   ├── Docs/                    # Session handoff, briefing, scopes
│   ├── RAPID_API_UI.html
│   └── push.sh, SETUP_*.gs, TEST_*.gs
│
├── RAPID_CORE/                  # Core GAS library (shared by other GAS projects)
│   ├── .clasp.json, appsscript.json, CLAUDE.md, Code.gs
│   ├── CORE_*.gs                # Api, Carriers, Compliance, Config, Database, Drive, etc.
│   ├── SETUP_DRIVE.gs, SETUP_MATRIX.gs
│   └── Docs/                    # Handoff, briefing, scopes, setup, deployment
│
├── RAPID_IMPORT/                # Data ingestion (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md
│   └── Docs/ + *.gs
│
├── RIIMO/                       # Operations UI (GAS, to be built out)
│   └── (minimal GAS + CLAUDE.md)
│
├── RPI-Command-Center/          # Cross-suite communications (GAS)
│   └── (GAS + docs)
│
└── TOMIS/                       # (GAS project; in setup script project list)
```

---

## 5. SENTINEL_TOOLS (B2B / DAVID)

```
SENTINEL_TOOLS/
├── DAVID-HUB/                   # BD qualification + calculators (GAS)
│   ├── .clasp.json, appsscript.json, CLAUDE.md
│   └── *.gs, *.html
│
├── sentinel/                    # Main M&A / Sentinel platform (GAS)
│   ├── .clasp.json, .claspignore, appsscript.json, CLAUDE.md
│   ├── Code.gs
│   ├── SENTINEL_*.gs            # AgencySetup, Annuity, Core, CRMUpload, Database, etc.
│   ├── MATRIX_Setup.gs
│   ├── Docs/
│   │   ├── 0-SESSION_HANDOFF, 1-AGENT_BRIEFING, 2.x, 3.x, 4-AGENT_SCOPE_BOB_ANALYSIS
│   │   ├── Archive/            # Backups, handoffs
│   │   ├── Reference/          # Architecture, Clasp setup, quick start
│   │   ├── Revenue/            # Revenue docs (Annuity, Life, MAPD, MedSup, etc.)
│   │   └── *.md                # Design, spec, testing, NDA, etc.
│   ├── outputs/                # Generated HTML/text reports
│   ├── setup-*.sh               # Clasp, RAPID_CORE, new project
│   ├── *.xlsx, *.json, *.csv   # Grids, config, data
│   └── Index.html, pdf-style.css, EXECUTIVE_SUMMARY*.html
│
└── sentinel-v2/                # Sentinel v2 (GAS)
    ├── CLAUDE.md
    └── *.gs, Docs/
```

---

## 6. Conventions (how projects are structured)

### 6.1 Google Apps Script (GAS) projects

- **Clasp**: Each has `.clasp.json`, `appsscript.json`, often `.claspignore` / `.gitignore`.
- **Root**: `Code.gs` (or `Code.js`) as entry; feature modules as `PREFIX_ModuleName.gs` (e.g. `SENTINEL_Medicare.gs`, `CORE_Database.gs`).
- **CLAUDE.md**: At project root for agent context.
- **Docs/** (or **docs/**):
  - `0-SESSION_HANDOFF.md`
  - `1-AGENT_BRIEFING.md`
  - `2.1-AGENT_SCOPE_GENERAL.md`, `2.2-AGENT_SCOPE_OPS.md`
  - `3.x-AGENT_SCOPE_SPC*_*.md` for specific scopes (UI, database, Medicare, etc.)
- **Web apps**: `Index.html`, often `Scripts.html`, `Styles.html`.

### 6.2 Hookify and .claude

- **Master rules**: Live in `_RPI_STANDARDS/hookify/*.local.md`.
- **Per project**: No copies; each project gets a `.claude/` directory with **symlinks** to those files, created by `setup-hookify-symlinks.sh`.
- **Global agent**: `~/.claude/CLAUDE.md` is a symlink to `_RPI_STANDARDS/CLAUDE.md`.

### 6.3 Node / cloud projects

- **MCP-Hub**: Multiple sub-apps (healthcare-mcps, document-processor, rpi-meeting-processor); each can have its own `package.json`, `src/`, `docs/`.
- **PDF_SERVICE**: Single service with `index.js`, Docker/Vercel config.
- **QUE-Medicare**: GAS front-end + `api/server.js` and `lib/` for quote/carrier logic.

---

## 7. Replicating on another machine

1. **Clone or copy `_RPI_STANDARDS`** into `~/Projects/_RPI_STANDARDS/`.
2. **Create the three SuperProject folders** (empty is fine):
   - `~/Projects/PRODASH_TOOLS/`
   - `~/Projects/RAPID_TOOLS/`
   - `~/Projects/SENTINEL_TOOLS/`
3. **Run the setup script** (from `_RPI_STANDARDS`):
   ```bash
   chmod +x scripts/setup-hookify-symlinks.sh
   ./scripts/setup-hookify-symlinks.sh
   ```
   This sets global CLAUDE.md and prepares `.claude/` for every project that exists; missing projects are skipped with a warning.
4. **Clone or copy each app** into the correct SuperProject (see sections 3–5). Match paths to the script’s project list so hookify symlinks line up.
5. **New projects**: Create them under the right SuperProject and either add their path to `setup-hookify-symlinks.sh` and re-run it, or manually create `.claude/` and symlink each `_RPI_STANDARDS/hookify/*.local.md` into it.

---

## 8. Canonical project list (from setup script)

Use this to ensure the other machine has the same “universe” of projects (and to add new ones to the script):

| SuperProject   | Project path (relative to `~/Projects/`) |
|----------------|------------------------------------------|
| PRODASH_TOOLS  | PRODASH_TOOLS/PRODASH                    |
| PRODASH_TOOLS  | PRODASH_TOOLS/QUE/QUE-Medicare           |
| RAPID_TOOLS    | RAPID_TOOLS/C3                           |
| RAPID_TOOLS    | RAPID_TOOLS/CAM                          |
| RAPID_TOOLS    | RAPID_TOOLS/CEO-Dashboard                |
| RAPID_TOOLS    | RAPID_TOOLS/DEX                          |
| RAPID_TOOLS    | RAPID_TOOLS/MCP-Hub                      |
| RAPID_TOOLS    | RAPID_TOOLS/RAPID_API                    |
| RAPID_TOOLS    | RAPID_TOOLS/RAPID_CORE                   |
| RAPID_TOOLS    | RAPID_TOOLS/RAPID_IMPORT                 |
| RAPID_TOOLS    | RAPID_TOOLS/RIIMO                        |
| RAPID_TOOLS    | RAPID_TOOLS/RPI-Command-Center           |
| RAPID_TOOLS    | RAPID_TOOLS/TOMIS                        |
| SENTINEL_TOOLS | SENTINEL_TOOLS/DAVID-HUB                 |
| SENTINEL_TOOLS | SENTINEL_TOOLS/sentinel                  |
| SENTINEL_TOOLS | SENTINEL_TOOLS/sentinel-v2               |
| (standards)    | _RPI_STANDARDS                           |

---

## 9. Quick reference: where things live

| What you need           | Where it lives                                      |
|-------------------------|-----------------------------------------------------|
| Global agent rules      | `_RPI_STANDARDS/CLAUDE.md` (symlinked in ~/.claude) |
| Hookify rules           | `_RPI_STANDARDS/hookify/*.local.md`                 |
| New-project process     | `_RPI_STANDARDS/reference/new-project/PROJECT_KICKOFF_TEMPLATE.md` |
| Compliance / PHI        | `_RPI_STANDARDS/reference/compliance/`              |
| Integrations (GHL, etc.) | `_RPI_STANDARDS/reference/integrations/`           |
| Strategy / architecture| `_RPI_STANDARDS/reference/strategic/`              |
| New machine setup       | `_RPI_STANDARDS/scripts/setup-hookify-symlinks.sh` |

---

*End of PROJECT_STRUCTURE.md*
