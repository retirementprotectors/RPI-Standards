---
name: block-ghl-2fa-dto-widening
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: browser/super-tools/ghl-verification-(code|matcher)\.ts
  - field: content
    operator: regex_match
    pattern: interface\s+VerificationCodeResult\s*\{[^}]*\b(body|contact)\b
owner: megazord
---

🛑 **BLOCKED: `ghl:read_verification_code` return type widened to carry `body`/`contact`**

You just added a `body` or `contact` field to the `VerificationCodeResult` interface in
`ghl-verification-code.ts` / `ghl-verification-matcher.ts` (CP-1, ghl-2fa-supertool).

**Why this is blocked:** this super-tool is `phi:false` on a class judgment ("reading a 2FA
code out of GHL Conversations is not PHI") that has **no shared backstop underneath it** —
`phi-mask.ts` has no clinical key set today (SSN/DOB/Medicare-ID/name only). The narrow DTO —
`{code, sender, received_at}` with `body`/`contact` **absent from the type**, not just
unpopulated — is the ONLY thing standing between a clinical-text or contact-identity message
and the return value. Widening the type re-opens exactly the risk the adversarial matcher
(`extractVerificationCode`) was built to close, and does so silently for every caller that
trusts the DTO shape.

**If you have a real reason to widen this type** (e.g. compliance has since shipped a
clinical-PHI mask and a caller genuinely needs `body`), that is a reviewable decision, not a
quiet edit — it needs:
1. The clinical-PHI backstop this file's header calls out as missing (routed to
   SHINOB1/swarm4 separately) to actually exist and be applied to the new field.
2. SHINOB1's death-gate ACK on the PR (this recipe is already in his review path).
3. The adversarial tests in `ghl-verification-matcher.test.ts` updated to prove the new field
   still can't leak clinical text / contact identity.

Doctrine: `docs/warriors/shared/toMachina-engineering-doctrine.md` → 3-Layer Enforcement
(this is the L2 write-time layer; L1 is this file's own header comment, L3 is the
`ghl-verification-matcher.test.ts` DTO-shape assertion + the existing PHI death-gate).
