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

1. **Hookify rule sync check** — Verify hookify rules are symlinked from `_RPI_STANDARDS/hookify/` into this project's `.claude/` directory. Compare counts, link any missing rules, report status.
2. **Read project CLAUDE.md** — If one exists in the current directory, read it now.
3. **GAS connectivity check** — If this is a GAS project, verify `execute_script` works by running a lightweight function (e.g., `DEBUG_Ping` or similar). Do NOT ask JDM to check clasp auth — use the MCP tool yourself. Clasp is only needed for deploy operations.
4. **Reference Detection Protocol** — Run Belt & Suspenders detection (grep for MATRIX, PHI, healthcare, campaigns). Report what docs you loaded.
5. **Survey the ecosystem** — Check sibling projects and available MCP tools.

NEVER ask JDM to run GAS functions. Use `execute_script` via rpi-workspace MCP.
Then proceed with the task.
