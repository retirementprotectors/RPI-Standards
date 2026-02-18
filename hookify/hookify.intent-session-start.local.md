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
3. **Reference Detection Protocol** — Run Belt & Suspenders detection (grep for MATRIX, PHI, healthcare, campaigns). Report what docs you loaded.
4. **Survey the ecosystem** — Check sibling projects and available MCP tools.

Then proceed with the task.
