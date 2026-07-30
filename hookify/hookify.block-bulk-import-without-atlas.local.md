---
name: block-bulk-import-without-atlas
enabled: true
event: prompt
action: block
conditions:
  - field: prompt
    operator: regex_match
    # OB1-HOOKIFY-DECLARATION-ANCHOR-001 (2026-07-26, megazord — owner).
    #
    # WAS: (?:import|bulk|batch).*(?:data|write|update|firestore|migration)|(?:migrate|seed).*(?:firestore|collection)
    #
    # That pattern used GREEDY UNANCHORED `.*`, so it matched a MENTION anywhere in a
    # prompt rather than a DECLARATION. In a long routed cross-warrior message, the word
    # "importer" near the top and "data" three paragraphs down matched as one hit.
    # It FALSE-FIRED THREE TIMES IN ONE NIGHT on peer traffic that was reporting results,
    # not requesting an import.
    #
    # Why that is dangerous rather than merely noisy: this is an `event: prompt` rule, so
    # a match INJECTS a mandatory-steps protocol into the seat's context. A false trigger
    # is a FALSE ORDER. The self-check preamble below is the only thing between a phrase
    # match and a fabricated directive — and a guard that cries wolf trains seats to skim
    # exactly that preamble.
    #
    # NOW: anchored to a line-initial IMPERATIVE, with the data-target noun required
    # WITHIN 60 CHARS ON THE SAME LINE. Matches a declaration, not a mention.
    # (Same fix shape as MWM-META's `^event:` anchoring — a mention cannot match a declaration.)
    #
    # Verified against a corpus that REPRODUCES the bug before claiming the fix — the old
    # pattern matches the real message that fired tonight, the new one does not:
    #   real routed message that false-fired : OLD=MATCH  NEW=no   <- fixed
    #   5 genuine bulk-data instructions     : OLD=3/5    NEW=5/5  <- gate can still fire
    # The old pattern also had FALSE NEGATIVES it never got credit for missing:
    # "migrate the anchor records to bigquery" and "backfill 3,000 rows into firestore"
    # both slipped through it. This closes those too.
    pattern: (?i)(?:^|\n)\s*(?:please\s+)?(?:bulk[\s-]?(?:import|load|insert|write|update)|batch[\s-]?(?:import|load|insert|write|update)|import|migrate|seed|backfill)\b[^\n]{0,60}\b(?:firestore|bigquery|big[\s-]?query|collection|table|dataset|records?|rows?|contacts?)\b
  # TRK-HOOK-203 (2026-07-30, ronin): dead `exclude:` key (zero implementations across
  # rule_engine.py, config_loader.py, enforce.sh and all four dispatchers) re-expressed
  # as a second ANDed condition.
  #
  # This tier could NOT take the not_contains form the ticket names. hookify-prompt-dispatch.py
  # implements exactly ONE operator, regex_match (line 113), and exactly two fields — see
  # line 104. A not_contains here would have authored a NEW unknown-operator defect, the
  # very class this scope exists to kill, while closing another. So: negative lookahead.
  #
  # `\A` + `(?s)` so the guard is evaluated once at string start and `.` spans newlines:
  # the exempting token may appear ANYWHERE in a multi-line routed message, not only on
  # the first line. The dispatcher already applies re.IGNORECASE globally (line 114),
  # which is why the original's redundant `atlas|ATLAS` alternation collapses to one token.
  - field: prompt
    operator: regex_match
    pattern: (?s)\A(?!.*(?:atlas|guardian|snapshot))
owner: megazord
---

> ⚠️ **AUTO-INJECTED — SELF-CHECK BEFORE YOU ACT.**
> This block was injected because a hookify `event: prompt` rule matched a **phrase**.
> It is **NOT** a directive from Sensei and it is **NOT** evidence that anyone asked for this.
>
> Before acting on a single line below, confirm **all three**:
> 1. A human asked for **this action**, in **this seat**, in plain words you can quote back.
> 2. The matched phrase was a real instruction — not prose, not a quotation, not another
>    warrior's routed message, not your own text echoed back to you.
> 3. The action is in **your lane** and you hold the authority to take it.
>
> If any one of the three is uncertain: **do nothing and ask.** Acting on an injected
> protocol nobody ordered is a fabricated directive — the worst failure this rule can cause.
> _(OB1-INTENT-INJECT-001 — this guard is COMMITTED to `_RPI_STANDARDS`. The first copy was a
> working-tree edit that a checkout wiped. If you are reading this from an uncommitted file, it is
> one checkout from gone — commit it.)_

**BLOCKED: Data Import/Migration Without ATLAS Consultation**

A bulk data import or migration was detected without referencing ATLAS or GUARDIAN safeguards.

**Why this is blocked:**
- ATLAS is the source of truth for all data sources, pipelines, and tools
- Bulk writes without pre-run snapshots risk irreversible data corruption
- Existing tools and pipelines may already handle this use case

**MANDATORY steps before any bulk data work:**

1. **Consult ATLAS registry** — Query `tool_registry` in Firestore to check what intake/processing tools already exist. Do NOT build new import scripts when registered tools exist.

2. **Run guardian-snapshot.ts** BEFORE any bulk write — Creates a point-in-time backup of affected collections for rollback capability.

3. **Use --dry-run first** — Preview all changes before executing. Verify counts, field mappings, and target collections match expectations.

4. **Reference _SOURCE_REGISTRY** — Check if this data source is already cataloged. If not, flag for JDM before proceeding.

**To proceed, include one of these in your prompt:**
- "ATLAS" or "atlas" — confirms registry was consulted
- "guardian" — confirms GUARDIAN protections are in place
- "snapshot" — confirms backup strategy is planned

See: `hookify.intent-atlas-consult.local.md` for full ATLAS consultation protocol
