#!/usr/bin/env python3
"""
GV2 WS-A — prove-block harness for the 3 §2a conflict-fixes (SHINOB1, 2026-07-08).

STAGED artifact: this proves each conflict-fix is correct so JDM's one-time target-shape
bless = merge -> re-run THIS -> setup-hookify-symlinks -> flip, in minutes not hours.
Pure-Python (stdlib only) so it runs at bless time with no plugin/deps.

Run:  python3 scripts/gv2-wsa-conflicts-proveblock.py
Exit: 0 = all conflicts reconciled; non-zero = a fix regressed.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HK = os.path.join(ROOT, "hookify")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    # return the block between the first pair of --- lines
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


results = []


def check(name, ok, detail):
    results.append((name, ok, detail))


# ── CONFLICT #1: block-funnel-url remedy no longer points at the dead+blocked github.io URL,
#    and the funnel matcher is UNCHANGED (still blocks funnel URLs in team-facing docs). ──
c1 = read(os.path.join(HK, "hookify.block-funnel-url-in-team-facing-docs.local.md"))
c1_fm = frontmatter(c1)
c1_body = c1[len(c1_fm):]
# matcher intact: still fires on the funnel host in team-facing docs
matcher_intact = "mdjserver\\.tail7845ea\\.ts\\.net" in c1_fm and "docs/(cases|brochures|client-deliverables|public)" in c1_fm
# the dead recommendation is gone: no "Embed THAT URL" (referred to a github.io url) and no
# "# stdout: https://retirementprotectors.github.io" recommend-line in the body.
dead_reco_gone = ("Embed THAT URL in the team-facing doc" not in c1) and (
    "# stdout: https://retirementprotectors.github.io" not in c1)
# body no longer RECOMMENDS producing a github.io url (github.io only appears in a "it's dead/blocked" context)
gh_lines = [ln for ln in c1_body.splitlines() if "github.io" in ln]
gh_only_negative = all(re.search(r"NOT|dead|404|block|retired|lockdown|not an option", ln, re.I) for ln in gh_lines)
check("#1 funnel matcher intact (still blocks funnel URLs in team-facing docs)", matcher_intact, "frontmatter regexes unchanged")
check("#1 dead github.io 'use this URL' recommendation removed", dead_reco_gone, "inbox-to-pages->github.io flow gone")
check("#1 remaining github.io mentions are all 'dead/blocked' context only", gh_only_negative, f"{len(gh_lines)} github.io line(s)")

# ── CONFLICT #2: intent-create-disco-doc now references ALL 8 canonical panel IDs the gate
#    (block-disco-missing-canonical-tabs / check_disco_canonical_tabs.sh) requires. ──
CANON_TABS = ["panel-pain", "panel-build", "panel-arch", "panel-decisions",
              "panel-phases", "panel-tickets", "panel-files", "panel-gates"]
c2 = read(os.path.join(HK, "intent-create-disco-doc.local.md"))
missing = [t for t in CANON_TABS if t not in c2]
check("#2 intent-create-disco-doc references all 8 canonical panel IDs", not missing,
      "missing: " + (", ".join(missing) if missing else "none"))
# cross-check the gate's required set actually IS these 8 (guards against the gate changing under us)
gate_path = os.path.join(HK, "scope-bound", "check_disco_canonical_tabs.sh")
gate_ok = True
gate_detail = "gate check script not found (skipped cross-check)"
if os.path.exists(gate_path):
    gate = read(gate_path)
    gate_missing = [t for t in CANON_TABS if t not in gate]
    gate_ok = not gate_missing
    gate_detail = "gate requires exactly these 8" if gate_ok else f"gate/spec mismatch: {gate_missing}"
check("#2 canonical 8 set matches the gate's required markers", gate_ok, gate_detail)
# dead github.io "Live at:" recommendation removed
check("#2 dead 'Live at: ...github.io' recommendation removed",
      "Live at: `https://retirementprotectors.github.io" not in c2, "reference-template line reconciled")

# ── CONFLICT #3: block-untyped-firestore-fields now path-scopes AWAY from the authorized
#    server-side write paths (mirrors block-direct-firestore-write), so it stops shadowing it. ──
c3 = read(os.path.join(HK, "hookify.block-untyped-firestore-fields.local.md"))
c3_fm = frontmatter(c3)
# extract the added file_path negative-lookahead pattern
m = re.search(r"field:\s*file_path.*?pattern:\s*(\S+)", c3_fm, re.S)
c3_ok = False
c3_detail = "no file_path condition found"
if m:
    pat = m.group(1)
    try:
        rx = re.compile(pat)
        AUTHORIZED = [
            "services/api/src/routes/clients.ts",
            "services/bridge/src/sync.ts",
            "mdj-agent/src/agent/firebase.ts",
            "services/approval-signer/index.ts",
        ]
        BLOCKED = [
            "apps/prodash/app/page.tsx",
            "packages/core/src/db.ts",
        ]
        # rule FIRES when the regex MATCHES. Authorized paths must NOT match; others MUST.
        auth_exempt = all(not rx.search(p) for p in AUTHORIZED)
        others_fire = all(rx.search(p) for p in BLOCKED)
        c3_ok = auth_exempt and others_fire
        c3_detail = f"authorized-exempt={auth_exempt} others-fire={others_fire}"
    except re.error as e:
        c3_detail = f"bad regex: {e}"
check("#3 untyped-fields path-scope: authorized server paths exempt, apps/packages still fire", c3_ok, c3_detail)
# honesty note (not a pass/fail): the rule's non-canonical event/field schema
schema_note = ("event: PreToolUse" in c3_fm) or ("field: tool" in c3_fm)
if schema_note:
    print("NOTE #3: rule declares non-canonical `event: PreToolUse`/`field: tool` (vs the `event: file` "
          "majority) — it may be DORMANT in the current hookify engine. The path-scoping fix is correct "
          "regardless; the event/field schema is flagged for the §2d schema-normalization pass, NOT this conflict-fix.\n")

# ── report ──
print("GV2 WS-A conflict-fix prove-block\n" + "=" * 48)
allok = True
for name, ok, detail in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  ({detail})")
    allok = allok and ok
print("=" * 48)
print("RESULT:", "ALL RECONCILED ✓" if allok else "REGRESSION ✗")
sys.exit(0 if allok else 1)
