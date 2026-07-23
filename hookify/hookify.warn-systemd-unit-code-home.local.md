---
name: warn-systemd-unit-code-home
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(service|timer)$
  - field: content
    operator: regex_match
    pattern: ExecStart=.*/home/jdm/
owner: shinob1
---

**WARN: This unit runs code from a home directory. Does that code have a repo home?**

**Ask one question:** *if this file were deleted right now, could I restore it from a repo?*
If the answer is no, this unit is one `rm` away from a service that can never be rebuilt.

**Where the code belongs:**

| What it is | Home |
|---|---|
| Box / fleet ops — watchers, launchers, health checks, guards | `dojo-warriors/scripts/` |
| Platform / product code | `toMachina` |
| Warrior-owned tooling | that warrior's repo — **named, never implicit** |
| Credentials, vaults, PHI-adjacent data, model blobs | **never in a repo** — record the exclusion *and its reason* |

**Check this unit's target before you install it:**

```bash
python3 ~/Projects/dojo-warriors/scripts/git-coverage-scan.py --services
```

Five states, and **three of them are fine** — do not "fix" the ones that are not broken:

- `tracked` — in the local index or on `origin/main`. Good.
- `artifact` — build output under `dist/`, source tracked. **Fine.** A `git clean -x` costs a
  rebuild, not the code.
- `EXCLUDED-WITH-CAUSE` — creds, vaults, blobs. **Fine**, when the reason is recorded.
- `unmerged-branch` — **the dangerous one.** Committed but never merged, so it *looks*
  shipped. This is the `taiko-deliverability-watch` case: enabled in production, 5,385
  failures over 20 days, zero successes.
- `untracked` / `norepo` — the code exists in exactly one place on Earth: this disk.

**A stopgap that runs in production is production.** There is no "just a helper script"
tier that is exempt. `mdj-agent` got a home convention (it lives inside the
`dojo-warriors` repo). Everything that did not got found by an audit at 3am with 14
services running unversioned code.

**Also set the timezone explicitly if this is a `.timer`:**
a `--user` unit is evaluated in the **manager's** zone (`Etc/UTC` here), *not* the shell
you authored it in — and `systemd-analyze calendar` checks it in *your* shell's zone and
confidently confirms the wrong answer. Truth signal:
`systemctl --user show <timer> -p TimersCalendar`. See cross-warrior gotcha **#35**.

**Why this exists:**
OB1-CODE-HOME-CONVENTION-001 (2026-07-21). Full doctrine + the L1/L2/L3 model in
`docs/warriors/shared/toMachina-engineering-doctrine.md` § "EVERY RUNNING SERVICE'S CODE
HAS A REPO HOME". This rule is **L2** — the write-time layer.

**This is a WARN, not a BLOCK:** writing unit files is legitimate and routine. The rule
makes the repo-home question reflexive at authoring time, which is the cheapest possible
moment to answer it.
