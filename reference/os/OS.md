# The Operating System

> **v1.0 | February 19, 2026**

---

## Purpose

The Operating System is the governance layer of The Machine. It defines what's allowed (Standards), who has access (Posture), how rules are enforced (Immune System), what's being watched (Monitoring), and what humans do (Operations).

The Machine is the business -- the platforms, the code, the data, the people. The OS is the thing that keeps it all honest.

---

## Architecture

```
The Machine (the business)
  └── The Operating System (governance layer)
        ├── Standards    (STANDARDS.md)       ← the kernel -- what the rules ARE
        ├── Posture      (POSTURE.md)         ← access control -- who can do what
        ├── Immune System (IMMUNE_SYSTEM.md)  ← enforcement + learning loop
        ├── Monitoring   (MONITORING.md)      ← watchdogs + health checks
        └── Operations   (OPERATIONS.md)      ← human processes + checklists
```

All paths are relative to `reference/os/`.

---

## The Governance Cycle

The five subsystems form a closed loop:

```
Standards ──define──▶ Immune System ──enforce──▶ Monitoring
    ▲                                                │
    │                                             detect
    │                                                │
    └──evolve── Operations ◀──correct───────────────┘
```

1. **Standards** define the rules (data classification, code patterns, PHI policy).
2. **Immune System** enforces them in real time (hookify blocks, warns, learns).
3. **Monitoring** detects drift (scheduled scans, health checks, launchd agents).
4. **Operations** corrects what monitoring finds (human checklists, incident response).
5. **Standards** evolve based on what Operations encountered. Cycle repeats.

No subsystem works alone. A rule without enforcement is a suggestion. Enforcement without monitoring is blind. Monitoring without operations is noise.

---

## Quick Reference

| I need to...                                           | Read              |
|--------------------------------------------------------|-------------------|
| Understand data classification / HIPAA / PHI rules     | STANDARDS.md      |
| Check web app access / role tables / security posture  | POSTURE.md        |
| Understand hookify rules / code enforcement            | IMMUNE_SYSTEM.md  |
| Run a health check / audit / review schedules          | MONITORING.md     |
| Follow an offboarding / incident / training process    | OPERATIONS.md     |

---

## 9-Layer Compliance Grid

Every compliance concern maps to exactly one OS subsystem.

| Layer | Name                                  | OS Subsystem  |
|-------|---------------------------------------|---------------|
| 1     | Real-time code enforcement (Hookify)  | Immune System |
| 2     | Scheduled automation (launchd)        | Monitoring    |
| 3     | GAS-level compliance triggers         | Monitoring    |
| 4     | Web app access posture                | Posture       |
| 5     | Policy documents                      | Standards     |
| 6     | Knowledge pipeline data               | Immune System |
| 7     | Secrets management                    | Posture       |
| 8     | Completed security actions            | Posture       |
| 9     | Gaps / not yet live                   | Operations    |

If a compliance concern doesn't fit one of these layers, it's either already covered or needs a new layer (escalate to JDM).

---

## Cross-References

| Resource                        | Path                                              |
|---------------------------------|---------------------------------------------------|
| Global rules (source of truth)  | `~/.claude/CLAUDE.md`                             |
| Hookify rule files              | `_RPI_STANDARDS/hookify/`                         |
| Hookify system overview         | `_RPI_STANDARDS/reference/HOOKIFY_SYSTEM.md`      |
| Compliance standards            | `_RPI_STANDARDS/reference/compliance/`             |
| Weekly health check             | `_RPI_STANDARDS/reference/maintenance/WEEKLY_HEALTH_CHECK.md` |
| Project audit protocol          | `_RPI_STANDARDS/reference/maintenance/PROJECT_AUDIT.md`       |
| Security compliance tracker     | `_RPI_STANDARDS/reference/compliance/SECURITY_COMPLIANCE.md`  |

---

## Version History

| Version | Date       | Change                          |
|---------|------------|---------------------------------|
| 1.0     | 2026-02-19 | Initial OS architecture document |
