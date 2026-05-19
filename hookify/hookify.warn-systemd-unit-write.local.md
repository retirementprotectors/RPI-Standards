---
name: warn-systemd-unit-write
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^/etc/systemd/system/.*\.(service|timer)$
owner: shinob1
---

**WARNING: Writing systemd unit to `/etc/systemd/system/`**

Direct writes to systemd units skip the project-source-of-truth and the
audit trail. Verified incident 2026-05-11: `claude-md-tracker.service` had
a stale `ExecStart` path pointing at `/home/jdm/mdj-agent/...` (a deleted
location) — the unit existed but would have failed on activation.

**The right pattern:**

1. Author the `.service` + `.timer` files in the project's `deploy/` dir
   (e.g., `services/learning-loop/deploy/<wire>.service`)
2. Verify `ExecStart` paths resolve on disk
3. Commit to the project repo so the unit is version-controlled
4. THEN `sudo cp deploy/*.{service,timer} /etc/systemd/system/`
5. `sudo systemctl daemon-reload && sudo systemctl enable --now <unit>.timer`
6. Verify with `systemctl list-timers <unit>.timer`

**Outputs to surface in your report:**
- The git path of the source unit file (so it can be re-deployed)
- `systemctl list-timers` output confirming next-run schedule
- Any path-resolution checks you ran

**Phase 1 of ZRD-SHINOB1-AUDIT-POSTURE-001** (Surface 8 — Process + Triggers
inventory) will catalog every active systemd unit on MDJ_SERVER. Until that
audit lands, every new unit you write should also be reported in the
project's bilateral so the inventory captures it.

If your write IS following all of the above: ignore this warning and proceed.

Why this exists: ZRD-SHINOB1-AUDIT-POSTURE-001 + 2026-05-11 hot-mess sweep.
