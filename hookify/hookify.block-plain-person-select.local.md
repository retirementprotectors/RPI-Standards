---
name: block-plain-person-select
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: <select[^>]*id\s*=\s*['"][^'"]*(?:agent|owner|producer|client|specialist|advisor)[^'"]*['"]
---

🛑 **BLOCKED: Plain dropdown for known-entity person selection**

Known-entity person fields (agent / owner / producer / client / specialist / advisor) MUST use Smart Lookup type-ahead, not plain `<select>`. Plain dropdowns scale poorly past ~50 entries and break when the underlying data source changes — Smart Lookup is the canonical pattern.

**Canonical:**
- GAS: `buildSmartLookup(elementId, items, value, placeholder)`
- toMachina: `<SmartLookup>` component
- Reference: `_RPI_STANDARDS/reference/patterns/SMART_LOOKUP.md`

**Override (rare — when plain dropdown IS correct):**
- Field has <10 options and the list is hard-coded (e.g. `<select id="agent">` for "Active / Inactive / Pending")
- Add comment immediately above: `<!-- smart-lookup-exempt: <reason> -->`
- The block fires on `id=` so renaming the id (e.g. `id="status-select"` instead of `id="agent-select"`) is the natural escape — match the id to the actual entity it represents, not a person-name.

**Why BLOCK, not WARN:** the WARN version was invisible in tool output. Reverted plain-dropdown ships have cost real debugging time more than once. BLOCK forces the correct pattern to be used or the exemption to be explicit.
