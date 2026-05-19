---
name: block-disco-missing-canonical-tabs
event: pre-write, pre-edit
check: check_disco_canonical_tabs.sh
severity: BLOCK
scope: SCOPE-DISCO-TABS-001
introduced: 2026-05-18
owner: shinob1
---

# block-disco-missing-canonical-tabs

Blocks `Write` / `Edit` tool calls targeting `docs/discoveries/*.html` when the proposed content is missing any of the 8 canonical Discovery Doc tab panels.

## Why

JDM directive 2026-04-29 mandates that ALL new Discovery Docs follow the canonical 8-tab HTML template. The 8 tabs (Pain · Build · Architecture · Decisions · Phases · Tickets · Files · Gates) are a non-negotiable structure — a tab can be sparse but cannot be absent.

Without this rule, a warrior could accidentally:
- Copy a partial scaffold and forget to include all tabs
- Strip tabs while editing to "simplify" the doc
- Author from scratch and omit tabs they think are irrelevant

Any of these breaks the JDM-mandated format and makes the doc unusable as an audit artifact.

## Detection method

The check script (`check_disco_canonical_tabs.sh`) inspects the proposed file content for all 8 canonical panel ID markers:

```
id="panel-pain"
id="panel-build"
id="panel-arch"
id="panel-decisions"
id="panel-phases"
id="panel-tickets"
id="panel-files"
id="panel-gates"
```

These are the canonical HTML markers from `docs/templates/discovery-doc-template.html`. The markers are stable — they're the `<div class="panel" id="panel-*">` section anchors that the tab-switching JS targets.

## Effect

When the rule fires and blocks:
- The Write/Edit tool call is rejected before it executes
- The blocking message names every missing tab by number and ID
- Points to the template (`docs/templates/discovery-doc-template.html`) and format guide (`docs/templates/DISCOVERY_DOC_FORMAT.md`)
- A violation is logged to `~/.claude/hooks/violation-log.jsonl`

## Edit semantics

For `Edit` tool calls: if `new_string` contains NO `id="panel-*"` markers, the edit is considered a content-only change (not touching tab scaffold) and is allowed. Only edits that include panel-marker content but are missing one or more tabs are blocked. This prevents false positives on minor content edits within a valid doc.

## Allow path

Include all 8 panel IDs in the file content. Use the canonical template:

```bash
cp docs/templates/discovery-doc-template.html docs/discoveries/<sprint-name>.html
```

## Reference

- Template: `docs/templates/discovery-doc-template.html`
- Format guide: `docs/templates/DISCOVERY_DOC_FORMAT.md`
- JDM directive: 2026-04-29 (ratified in #shinob1 bilateral)
- toMachina CLAUDE.md § "Discovery Doc Format (Canonical v1.2)"
