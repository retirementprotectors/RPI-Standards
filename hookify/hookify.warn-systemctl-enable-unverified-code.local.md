---
name: warn-systemctl-enable-unverified-code
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: systemctl(\s+--user)?\s+(enable|link)
owner: shinob1
---

**WARN: You are putting a service into production. Is its code actually committed?**

This is the exact moment the `taiko-deliverability-watch` failure was created — and it
went undetected for **20 days**.

**What happened there:** the unit was installed and enabled while its pull request sat
unmerged. `ExecStart` therefore pointed at a file that did not exist on disk. The service
failed **5,385 consecutive times with zero successes**, while `systemctl is-enabled`
cheerfully reported `enabled` the entire time. Nobody noticed, because nothing read
systemd's failure state.

**Before you enable this unit, verify all three:**

```bash
# 1. What does it actually run?
systemctl [--user] show <unit> -p ExecStart --value

# 2. Does that file EXIST, and is it committed AND on main?
#    (not just "in a repo" — a branch that never merged looks shipped and is not)
python3 ~/Projects/dojo-warriors/scripts/git-coverage-scan.py --services | grep <unit>

# 3. After enabling, PROVE it ran. Do not trust is-enabled.
journalctl [--user] -u <unit> -n 20 --no-pager
```

**The bar for "it works" is a SUCCESS in the journal — never `is-enabled`.**
`is-enabled` describes your *intent*. It says nothing about whether the thing has ever
functioned. A unit pointing at a deleted file, a missing interpreter, or an unmerged
branch reports `enabled` exactly like a healthy one.

**If the code is not yet on `main`, land it first.** An enabled unit running from an
unmerged branch is the most dangerous coverage state there is, because it *looks*
shipped. One `git clean`, one fresh worktree, or one stale checkout and the running
service has no code at all.

**Why this exists:**
OB1-CODE-HOME-CONVENTION-001 / OB1-ALARM-READER-001 (2026-07-21). An audit found
**14 of 43 loaded services running code that was not tracked**, 10 of them in no git
repo whatsoever. See `docs/warriors/shared/toMachina-engineering-doctrine.md`
§ "EVERY RUNNING SERVICE'S CODE HAS A REPO HOME" for the full doctrine and the
L1/L2/L3 enforcement model — this rule is **L2**.

**This is a WARN, not a BLOCK:** enabling units is routine and legitimate. The rule
exists so the verification step becomes reflex, not so the operation is prevented.
