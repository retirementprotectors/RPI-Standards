---
name: warn-bq-write-without-dedup-key
enabled: true
event: file
action: warn
conditions:
  # Fires on a raw BigQuery streaming insert — the unguarded append path. This is
  # the exact surface where the commission lane shipped ~67K phantom rows before
  # the anti-join landed. MERGE/INSERT-INTO-with-ON paths are inherently keyed and
  # are deliberately NOT matched here.
  - field: content
    operator: regex_match
    pattern: \.table\([^)]*\)\.insert\(
  # Opt-out by intent: any file that references the shared dedup harness or
  # declares a dedup key (dedupAndInsert / DedupConfig / computeDedupKey /
  # dedup_key / dedupKey) contains the substring "dedup" and is exempt. A raw
  # insert with NO dedup awareness anywhere in the file is what trips the warn.
  - field: content
    operator: not_contains
    pattern: dedup
  # Code only — TS/JS under services/ or packages/, never tests, dist, or docs.
  - field: file_path
    operator: regex_match
    pattern: ^(?!.*(\.(test|spec)\.(ts|js)|node_modules/|/dist/|docs/)).*(services|packages)/.*\.(ts|js)$
owner: ronin
co_sign: shinob1
---

⚠️ **WARN: BigQuery write without a declared dedup key.**

This file performs a raw `.table(...).insert(...)` BigQuery write but declares no dedup key. Un-keyed appends are how the commission lane shipped **~67K phantom rows** (213 duplicate files) before the anti-join landed.

**The BoB Machine law (Stream S0):** *no BQ write without a declared dedup key.* The dedup key is the trust gate that makes every downstream analysis trustworthy.

**Fix — route the write through the shared dedup harness** (`@tomachina/core` → `packages/core/src/ingestion/dedup-harness.ts`, BOB-S0-2):

```ts
import { dedupAndInsert } from '@tomachina/core'

await dedupAndInsert(bqClient, {
  target: { project, dataset, table },
  dedupKey: { keyCols: ['policy_number', 'payment_date', 'amount'] }, // the row identity
}, rows)
// stamps a composite SHA-256 key, anti-joins vs the target (and collapses
// intra-batch dupes), inserts only survivors, returns aggregate-only counts.
```

**Conscious opt-out** (genuinely append-only, no logical identity — e.g. an immutable event-log sink): keep the raw insert but reference the harness or a `dedup_key` rationale in the file so the intent is explicit (any mention of `dedup` clears this warn).

**Ratchet:** this is **WARN** today. Per the BoB disco (BOB-S0-3, RONIN·SH), SHINOB1's immune-system review ratchets it to **BLOCK** for new pipelines once the existing BQ-write surfaces (mwm loaders, objectionly/webinarkit ingress, bigquery-stream) have adopted a dedup key.

See: `docs/discoveries/zrd-scope-bob-machine-multi-domain-ingestion-ssot-v1.2.html` (BOB-S0-2/S0-3).
