---
name: warn-plain-person-select
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: <select[^>]*id\s*=\s*['"][^'"]*(?:agent|owner|producer|client|specialist|advisor)[^'"]*['"]
---

**WARNING: Plain Dropdown for Person Selection**

Known-entity person fields should use Smart Lookup type-ahead, not plain `<select>` dropdowns. Use `buildSmartLookup()` or the toMachina equivalent component.
