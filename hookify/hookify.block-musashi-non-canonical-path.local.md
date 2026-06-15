---
name: block-musashi-non-canonical-path
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (?:docs/warriors/musashi|!MUSASHI DOCS!)/(?!(?:agentx|rpi|tomachina|david|_meta)(?:/|$)|README\.md$|cmo-ownership-grid\.html$|_INDEX\.md$|\.gitkeep$)
owner: musashi
---

# BLOCKED: Non-canonical MUSASHI path

> Locked 2026-05-12 per MM-REG-V2-010. Disco: https://retirementprotectors.github.io/toMachina/docs/discoveries/mm-reg-v2-discovery-doc-v1.html
>
> JDM directive (2026-05-12): "I say block that shit now."

You attempted to write to a path that doesn't follow MUSASHI's canonical tree.

**MUSASHI's canonical tree:**
```
docs/warriors/musashi/<division>/<brand?>/<type>/<file>
!MUSASHI DOCS!/<division>/<brand?>/<type>/<file>
```

**Divisions (root-level only):**
- `agentx/` — AgentX brand assets, site, career paths
- `rpi/` — RPI brand assets, brochures, lead-magnets, medicare-division/
- `tomachina/` — Platform brand, UI specs, design system
- `david/` — DAVID brand, partner discos, midwest-medigap/
- `_meta/` — CMO roadmaps, decision records, claude-insights, templates

**Allowed at musashi/ root (NOT inside a division folder):**
- `README.md`
- `cmo-ownership-grid.html`
- `.gitkeep`

**Known type folders:**
brochures · lead-magnets · decks · jds · comp-calcs · audits · design-system · ui-specs · brand-assets · site · career-paths · recruiting-pages · myst-bios · tracks · brand-guides · roadmaps · decision-records · claude-insights · midwest-medigap · medicare-division · onboarding-kits · cobrand-pattern-library · partner-discos · trinity · scripts · org-docs · resource-hubs · templates · training · disco-renders · screenshots · visual-qa · audit-deliverables

**Legacy scatter folders (ALL DEPRECATED — do not use):**
`!MUSASHI DOCS!/Strategic/` · `!MUSASHI DOCS!/Print/` · `!MUSASHI DOCS!/Brand/` · `!MUSASHI DOCS!/Career-Path/` · `!MUSASHI DOCS!/Web/` · `!MUSASHI DOCS!/Digital/` · `!MUSASHI DOCS!/Social/` · `!MUSASHI DOCS!/Video/` · `!MUSASHI DOCS!/Logs/`

**Fix:** Pick the correct canonical home and retry.
```
docs/warriors/musashi/<division>/<brand?>/<type>/<filename>
```

Map: `docs/warriors/musashi/README.md`
Disco: https://retirementprotectors.github.io/toMachina/docs/discoveries/mm-reg-v2-discovery-doc-v1.html
