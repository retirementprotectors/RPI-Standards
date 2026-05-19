---
name: block-disco-write-outside-discoveries-dir
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: /(zrd|disco)-[^/]+\.html$
  - field: file_path
    operator: not_contains
    pattern: docs/discoveries/
---

🛑 **BLOCKED: Discovery Doc written outside canonical directory**

Files named `zrd-*.html` or `disco-*.html` MUST live in `toMachina/docs/discoveries/`. Disco files scattered across warrior clusters, audits/ subdirs, or root paths create archeology problems — every future search has to know multiple locations.

**Canonical path:**
```
/home/jdm/Projects/toMachina/docs/discoveries/<filename>.html
```

**Override paths:**

- If this isn't actually a Discovery Doc, rename it. The block matches the literal `zrd-` or `disco-` prefix on the filename — a different prefix (e.g. `audit-`, `plan-`, `analysis-`) won't match.
- If it IS a Discovery Doc, move it to the canonical directory. The canonical Disco template lives at `docs/templates/discovery-doc-template.html` per CLAUDE.md.

**Belt-and-suspenders companion:** `block-disco-write-from-non-sub-session` (existing) enforces that a parent CXO must spawn a sub-warrior before writing a disco. This new rule covers the *path* dimension; the existing one covers the *authorship* dimension. Together they make wrong-place + wrong-author both impossible.

**Why BLOCK, not WARN:** scattered discos have caused the "where IS that disco again?" problem multiple times this year. One canonical directory + one canonical naming convention = searchable archive.
