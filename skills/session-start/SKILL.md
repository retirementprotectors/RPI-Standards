---
name: session-start
description: The legacy session-start protocol — git pull all active repos, hookify symlink sync check, project CLAUDE.md read, GAS ping, Reference Detection, MCP dependency check, open session URLs, cross-warrior briefing, then EnterPlanMode. Superseded in spirit by the live Scroll boot (see staleness note).
version: 0.1.0-draft
---

# Session Start (legacy)

You have been invoked as the Session Start skill.

> ⚠️ **STALENESS WARNING (added at WS-B conversion, 2026-07-08):** this rule predates the live
> Scroll boot system (`ZRD-SCOPE-SCROLL-001`) that now boot-inlines identity, doctrine, and
> live state per-warrior — see `SHARED_BOOT_DOCTRINE.md` and each warrior's boot atom. Two
> concrete staleness markers found during conversion: **(a)** step 7 assumes a **macOS** `open`
> command to launch browser tabs — MDJ_SERVER runs **Ubuntu 24.04**, where `open` does not
> exist; **(b)** step 8 names **2HINOBI** as a peer warrior — that identity was superseded by
> **MEGAZORD** (per `soul.md`: "primarily MEGAZORD (then 2HINOBI) sessions"). Converting this
> content faithfully for the historical record, but **flag to SHINOB1/JDM before treating this
> skill as current session-boot guidance** — the Scroll boot (steps in the current boot doctrine)
> should be the live source, not this rule.

Run the following before any other work:

## 1. Git pull all active projects

Pull latest from all active RPI repos in parallel (spawn sub-agents). After all pulls complete, report a summary table:

- Each project: **up to date**, **X commits pulled** (list changed files), or **CONFLICT/ERROR** (details)
- Flag any repos with uncommitted local changes (dirty working tree) BEFORE pulling
- If a repo has uncommitted changes, pull anyway but WARN JDM about the dirty state

> The rule's original project list (18 repos under `~/Projects/_RPI_STANDARDS`,
> `~/Projects/PRODASHX_TOOLS/*`, `~/Projects/RAPID_TOOLS/*`, `~/Projects/SENTINEL_TOOLS/*`) is
> a live-repo fact per the engineering doctrine's own rule ("read the actual dirs on demand,
> never a static doc") — read the current project list from `~/Projects/` at invocation time
> rather than trusting a hardcoded list here.

## 2. Hookify rule sync check

Verify hookify rules are symlinked from `_RPI_STANDARDS/hookify/` into this project's `.claude/` directory. Compare counts, link any missing rules, report status.

## 3. Read project CLAUDE.md

If one exists in the current directory, read it now (note: most project CLAUDE.md files are now RETIRED stubs pointing at the Scroll — read the stub's pointer, not stale inline content).

## 4. GAS connectivity ping

Claude runs ALL GAS functions via `execute_script`. JDM's only manual GAS action is linking the GCP project number in Script Settings (one-time per project).

- If this is a GAS project (`.clasp.json` exists): read the `scriptId`, then run `DEBUG_Ping` via `execute_script` with `devMode: true`.
- Report: `GAS ping: {project} — OK (Xms)` or `GAS ping: FAIL — {error}`.

## 5. Reference Detection Protocol

Run Belt & Suspenders detection (grep for MATRIX, PHI, healthcare, campaigns). Report what docs you loaded.

## 6. MCP dependency check

Read `.claude/mcp-deps.json` from the current project directory.

- If it exists: for each listed MCP server, attempt a lightweight tool call to verify connectivity (e.g. `ToolSearch` for the server name). Report a pass/fail table.
- If it doesn't exist: skip with note "No MCP dependency file yet — will auto-populate as tools are used this session."

## 7. Open browser tabs

Read the `## Session URLs` section from the project's CLAUDE.md. For each URL, open it in the browser using **the OS-appropriate command** (Ubuntu: `xdg-open`; do not assume macOS `open`). If no `## Session URLs` section exists, skip with a note.

## 8. Cross-Warrior Intelligence Briefing

Inject knowledge from other Executive.AI warriors:

- Detect the current warrior from the active tmux session name (`tmux display-message -p '#S'`).
- Read `soul.md` highlights from the OTHER live warriors (per the current roster — read it live, do not hardcode names here).
- Query Firestore `knowledge_entries` for other warriors' extracted knowledge (soul-curated first, spirit-curated second, warrior-context third, per confidence + recency).
- If no cross-warrior entries exist, skip silently — do NOT error.

## 9. Enter Plan Mode

After setup is complete, call `EnterPlanMode` automatically. Stay in plan mode through the discovery/discussion/planning phase. JDM will ask questions, discuss direction, and shape the plan. Only exit plan mode when JDM approves the plan for the first major build of the session. After that first build, do NOT re-enter plan mode for bug fixes, iterations, or follow-up tasks — just execute.

---

*SHINOB1, CTO · session-start · Skill draft (GV2 WS-B batch 2) · converted from hookify `intent-session-start` (context-injector class), 2026-07-08 — STAGED, not yet promoted*
