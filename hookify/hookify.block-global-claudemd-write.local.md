---
name: block-global-claudemd-write
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (/home/jdm/\.claude/CLAUDE\.md|_RPI_STANDARDS/CLAUDE\.md)$
owner: shinob1
status: ARMED_2026-07-08_0.3-complete
---

**BLOCKED: Direct write to the global `CLAUDE.md` — it is a RETIRED STUB, not a doctrine file.**

The 1,342-line global `CLAUDE.md` was migrated into the Scroll shared streams
(`docs/warriors/shared/*.md`, boot-inlined) per Phase 0 (OB1-CLAUDEMD-SCROLL-MIGRATE).
The file at `~/.claude/CLAUDE.md` (and its `_RPI_STANDARDS/CLAUDE.md` mirror) is now a
short **pointer to the Scroll SSOT**. This rule exists because the file drifted BACK to
1,342 lines once before — the durable guard that was never built (that's why it re-grew).

**Doctrine does NOT live here anymore. Put it in the right Scroll stream:**

| Content you want to add | Right home (docs/warriors/shared/) |
|---|---|
| PHI / workspace governance | `phi-governance.md` |
| JDM identity · RPI business · team roster | `rpi-business.md` |
| Warrior roster · Dojo | `dojo-roster.md` |
| MCP inventory | `mcp-inventory.md` (or read-live `claude mcp list`) |
| Platform vocabulary | `platform-taxonomy.md` |
| Session protocol · thinking levels · role | `warrior-ops.md` |
| Golden rules · operating rules | `operating-rules.md` |
| Engineering standards · deploy · trunk | `toMachina-engineering-doctrine.md` |
| Signals · verbosity · hub format | `comms-glossary.md` |
| Terminology | `terminology.md` |
| ATLAS / OS narrative | `os-narrative.md` |

The Scroll streams are boot-inlined — a warrior gets them crutch-free. Re-growing the
global file re-creates the exact SSOT-violation Phase 0 killed.

**READ-block is NOT possible** (hookify has no read event) — this guard is WRITE-only, by
design and stated honestly. The boot-proof gate (RAIDEN, 0.4 companion) covers the
"boot loaded a re-grown file" case that a write-block alone can't.

**Legit stub edit (rare governance):** include the token `# claudemd-stub-update: <reason>`
in the prompt to bypass this block.

**Arming:** `enabled: false` until Phase 0 step 0.3 retires the file to a stub — arming it
before 0.3 would block the retire-to-stub write itself. Flip `enabled: true` as the final
action of 0.3, then prove-block with a test write.
