---
name: warn-new-md-outside-canonical
enabled: true
event: file
action: warn
severity: WARN
scope: OB1-MD-SPRAWL-001
introduced: 2026-07-27
owner: shinob1
# JDM, 2026-07-27: "I fucking hate .mds because we have 92k of them, they rot and die
# without being referenced ever again and are a total waste of time."
#
# MEASURED (DOJOv3 disco, zrd-scope-dojov3-canonical-governance-v1.0.html §01):
#   93,704 .md files on this box · 4,255 unique · "no warrior — including the one that
#   wrote a given file — can reliably find it again."
#
# DOJOv3 PRIME DIRECTIVE, quoted in that same disco:
#   "A markdown file is not a durable surface — it is a note to the seat that wrote it.
#    If a thing must be found or enforced, it lives in DATA and renders to a SURFACE."
#
# WARN, NOT BLOCK — deliberately. Two of the .md gates that came before this one
# (block-canonical-doctrine-write-outside-ssot, block-disco-write-outside-discoveries-dir)
# are both enabled:false, switched off in SHIN-FRICTION-LAND-001. A hard block on .md
# writes would wall legitimate doctrine work on its first hour and be disabled by
# tomorrow, which is how those two died. This one asks a question the author must answer
# and lets them proceed.
conditions:
  # A new/edited markdown file...
  - field: file_path
    operator: regex_match
    pattern: \.md$
  # ...outside every canonical home. Canonical = somewhere a reader can FIND it:
  #   docs/warriors/**      Scroll shared streams + per-warrior doctrine SSOT
  #   doctrine/             boot atoms
  #   _RPI_STANDARDS/hookify/  the rules themselves
  #   briefs/               launch briefs (tracked, referenced by a spawn)
  #   discoveries/          disco docs
  #   warriors/<w>/         soul / spirit / WORKFLOW / templates
  #   README / CLAUDE.md    entry points
  - field: file_path
    operator: regex_not_match
    pattern: (docs/warriors/|/doctrine/|_RPI_STANDARDS/hookify/|/briefs/|/discoveries/|/warriors/[a-z0-9-]+/|README\.md$|CLAUDE\.md$|/node_modules/|/\.github/)
---

⚠️ **You are writing a `.md` outside every canonical home. Will anyone ever find this?**

There are **93,704 `.md` files on this box — 4,255 unique** — and per the DOJOv3 disco,
*"no warrior, including the one that wrote a given file, can reliably find it again."*
This is the single largest source of rot in the system.

**DOJOv3 prime directive:**
> *"A markdown file is not a durable surface — it is a note to the seat that wrote it.
> If a thing must be found or enforced, it lives in **DATA** and renders to a **SURFACE**."*

**Answer one before you continue:**

1. **Does this need to be FOUND later?** → then it is data + a surface, not a file.
   Write the record (Firestore / BigQuery / `tracker_items`) and render it — the way
   `comms-corpus-reference.py` generates its page from live state instead of being typed.
2. **Does this need to be ENFORCED?** → then it is a hookify rule or a CI gate, not prose.
   Doctrine nobody executes is decoration: 68 of 82 enabled rules had no engine at all
   until 2026-07-27.
3. **Is it genuinely a note to yourself for this session?** → fine. Put it in
   `/tmp` or the session scratchpad, not in the repo, so it dies when it should.

**Canonical homes** (these do not warn): `docs/warriors/**` · `doctrine/` ·
`_RPI_STANDARDS/hookify/` · `briefs/` · `discoveries/` · `warriors/<name>/` ·
`README.md` · `CLAUDE.md`

If it belongs in one of those, move it there. If it belongs in none of them, it probably
should not be a file.
