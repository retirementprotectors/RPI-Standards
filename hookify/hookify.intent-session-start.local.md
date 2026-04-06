---
name: intent-session-start
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (session\s+launch|let'?s\s+get\s+started|kick\s+off|new\s+project|get\s+started|SKODEN|skoden)
---

**SESSION START PROTOCOL TRIGGERED**

Run the following before any other work:

1. **Git pull all active projects** — Pull latest from all 18 RPI repos in parallel (spawn sub-agents). After all pulls complete, report a summary table:
   - Each project: **up to date**, **X commits pulled** (list changed files), or **CONFLICT/ERROR** (details)
   - Flag any repos with uncommitted local changes (dirty working tree) BEFORE pulling
   - If a repo has uncommitted changes, pull anyway but WARN JDM about the dirty state
   Projects:
   - `~/Projects/_RPI_STANDARDS`
   - `~/Projects/PRODASHX_TOOLS/PRODASHX`
   - `~/Projects/PRODASHX_TOOLS/QUE/QUE-Medicare`
   - `~/Projects/RAPID_TOOLS/C3`
   - `~/Projects/RAPID_TOOLS/CAM`
   - `~/Projects/RAPID_TOOLS/CEO-Dashboard`
   - `~/Projects/RAPID_TOOLS/DEX`
   - `~/Projects/RAPID_TOOLS/Marketing-Hub`
   - `~/Projects/RAPID_TOOLS/MCP-Hub`
   - `~/Projects/RAPID_TOOLS/RAPID_API`
   - `~/Projects/RAPID_TOOLS/RAPID_CORE`
   - `~/Projects/RAPID_TOOLS/RAPID_IMPORT`
   - `~/Projects/RAPID_TOOLS/RIIMO`
   - `~/Projects/RAPID_TOOLS/RPI-Command-Center`
   - `~/Projects/RAPID_TOOLS/PDF_SERVICE`
   - `~/Projects/SENTINEL_TOOLS/DAVID-HUB`
   - `~/Projects/SENTINEL_TOOLS/sentinel`
   - `~/Projects/SENTINEL_TOOLS/sentinel-v2`

2. **Hookify rule sync check** — Verify hookify rules are symlinked from `_RPI_STANDARDS/hookify/` into this project's `.claude/` directory. Compare counts, link any missing rules, report status.

3. **Read project CLAUDE.md** — If one exists in the current directory, read it now.

4. **GAS connectivity ping** — I (Claude) run ALL GAS functions via `execute_script`. JDM's only manual GAS action: linking the GCP project number in Script Settings (one-time per project). Everything else — I execute directly.
   - If this is a GAS project (`.clasp.json` exists): read the `scriptId`, then run `DEBUG_Ping` via `execute_script` with `devMode: true`
   - Report: `GAS ping: {project} — OK (Xms)` or `GAS ping: FAIL — {error}`
   - The act of running execute_script at session start establishes the pattern: Claude runs functions, not JDM

5. **Reference Detection Protocol** — Run Belt & Suspenders detection (grep for MATRIX, PHI, healthcare, campaigns). Report what docs you loaded.

6. **MCP dependency check** — Read `.claude/mcp-deps.json` from the current project directory.
   - If file exists: for each listed MCP server, attempt a lightweight tool call to verify connectivity (e.g., `ToolSearch` for the server name). Report a table:
     ```
     | MCP Server     | Status |
     |----------------|--------|
     | rpi-workspace   | pass   |
     | slack           | pass   |
     | gmail           | FAIL   |
     ```
   - If no `mcp-deps.json` exists: skip with note "No MCP dependency file yet — will auto-populate as tools are used this session"

7. **Open browser tabs** — Read the `## Session URLs` section from the project's CLAUDE.md.
   - For each URL listed, run `open "{url}"` via Bash (opens in Chrome with JDM's existing Google auth)
   - Do NOT use Playwright for this — use macOS `open` command (uses existing browser session)
   - If no `## Session URLs` section exists, skip with note "No Session URLs configured"

8. **Cross-Warrior Intelligence Briefing** — Inject knowledge from other Executive.AI warriors:
   - Detect the current warrior from the active tmux session name (`tmux display-message -p '#S'`)
   - Read soul.md highlights from OTHER warriors in `~/Projects/dojo-warriors/`:
     - For each other tmux warrior (SHINOB1, 2HINOBI, MUSASHI — excluding yourself), read their `soul.md`
     - Extract key highlights: Architecture Decisions, Operational Rules, Creative Philosophy, Lasting Decisions
     - Format as: `### From {WARRIOR} ({Role}) — Soul Highlights` with bullet points
   - Query Firestore `knowledge_entries` for other warriors' extracted knowledge:
     - Tags containing `soul-curated` + warrior name (confidence ≥ 0.9) — show FIRST
     - Tags containing `spirit-curated` + warrior name (confidence ≥ 0.85) — show second
     - Tags containing `warrior-context` + warrior name (confidence ≥ 0.7, last 7 days) — show third
     - Format as: `### Recent Warrior Knowledge (7 days)` with `[TYPE] content (confidence, tier)` bullets
   - Soul-curated entries always appear FIRST in the output
   - If no cross-warrior entries exist (no soul.md files, no Firestore entries), skip silently — do NOT error
   - Script: `npx tsx ~/Projects/toMachina/services/learning-loop/cross-warrior-briefing.ts [warrior-name]`
   - Present the output block to JDM as part of the session start briefing

9. **Enter Plan Mode** — After setup is complete, call `EnterPlanMode` automatically. Stay in plan mode through the discovery/discussion/planning phase. JDM will ask questions, discuss direction, and shape the plan. Only exit plan mode when JDM approves the plan for the first major build of the session. After that first build, do NOT re-enter plan mode for bug fixes, iterations, or follow-up tasks — just execute.
