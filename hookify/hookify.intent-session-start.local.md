---
name: intent-session-start
enabled: false
# GV2 WS-B batch 2: a DRAFT skill exists at _RPI_STANDARDS/skills/session-start/.
# It is NOT WIRED. Skills load only via a manual symlink into ~/.claude/skills/;
# exactly one such symlink exists on the box today (case-drive-checklist).
# Until that symlink exists AND the skill is proven to load, THIS RULE IS THE ONLY
# ENFORCEMENT PATH. Do NOT set enabled:false on the strength of the draft alone --
# that removes enforcement and replaces it with a skill that never loads.
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (session\s+launch|let'?s\s+get\s+started|kick\s+off|new\s+project|get\s+started|SKODEN|skoden)
owner: shinob1
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

**SESSION START PROTOCOL TRIGGERED**

Run the following before any other work:

1. **Git pull all active projects** — Pull latest from all 18 RPI repos in parallel (spawn sub-agents). After all pulls complete, report a summary table:
   - Each project: **up to date**, **X commits pulled** (list changed files), or **CONFLICT/ERROR** (details)
   - Flag any repos with uncommitted local changes (dirty working tree) BEFORE pulling
   - If a repo has uncommitted changes, pull anyway but WARN JDM about the dirty state
   Projects:
   - `~/Projects/_RPI_STANDARDS`
   - `(RETIRED - not on disk; verify before citing)`
   - `~/Projects/archive/QUE-Medicare`
   - `(RETIRED - not on disk; verify before citing)`
   - `~/Projects/archive/CAM`
   - `(RETIRED - not on disk; verify before citing)`
   - `~/Projects/archive/DEX`
   - `~/Projects/archive/Marketing-Hub`
   - `~/Projects/services/MCP-Hub`
   - `~/Projects/archive/RAPID_API`
   - `~/Projects/archive/RAPID_CORE`
   - `~/Projects/archive/RAPID_IMPORT`
   - `~/Projects/archive/RIIMO`
   - `~/Projects/archive/RPI-Command-Center`
   - `~/Projects/archive/PDF_SERVICE`
   - `~/Projects/archive/DAVID-HUB`
   - `~/Projects/archive/sentinel`
   - `~/Projects/archive/sentinel-v2`

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
   - Script: `npx tsx (RETIRED - not on disk; verify before citing).ts [warrior-name]`
   - Present the output block to JDM as part of the session start briefing

9. **Enter Plan Mode** — After setup is complete, call `EnterPlanMode` automatically. Stay in plan mode through the discovery/discussion/planning phase. JDM will ask questions, discuss direction, and shape the plan. Only exit plan mode when JDM approves the plan for the first major build of the session. After that first build, do NOT re-enter plan mode for bug fixes, iterations, or follow-up tasks — just execute.
