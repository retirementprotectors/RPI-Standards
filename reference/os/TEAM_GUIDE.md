# The Operating System — Team Guide

> **What it is, why it matters, and what you need to know.**
> February 19, 2026

---

## The One-Sentence Version

**The Operating System is how The Machine governs itself** — the rules, the enforcement, the watchdogs, the checklists, and the access controls that keep everything running right.

---

## Why We Built This

RPI runs on a lot of technology. 18 projects. 3 platforms. Client data. Medicare data. Commission data. Financial records. PHI.

Before The OS, our governance was scattered across 5 different policy documents, 21 enforcement rules, 4 automated schedulers, and pieces of instructions embedded in various project files. It all worked, but finding the right answer meant knowing which doc to check — and sometimes the same rule existed in three places with slightly different wording.

We consolidated everything into one system with one architecture. Every rule, every process, every check now lives in exactly one place, organized by what it does.

---

## The Architecture

Think of it like this:

```
The Machine = the business (our platforms, our data, our people)
    |
    └── The Operating System = how we keep it honest
            |
            ├── Standards        — What the rules are
            ├── Posture          — Who has access to what
            ├── The Immune System — Automatic enforcement
            ├── Monitoring       — What's being watched
            └── Operations       — What humans do
```

The Machine is everything we've built. The OS is the governance layer that makes sure it stays secure, compliant, and running correctly.

---

## The 5 Subsystems (What Each One Does)

### 1. Standards — The Rulebook

This is the foundation. It defines:
- How we classify data (what's sensitive, what's not)
- HIPAA and PHI handling requirements
- How data should be stored, transmitted, and displayed
- Rules for AI systems, vendor management, and disaster recovery

**Why it matters to you:** If you ever wonder "are we allowed to do X with client data?" — the answer is in Standards. This is the document that protects us and our clients.

### 2. Posture — The Access Map

This tracks:
- Who has access to which systems
- Security settings and their current state (2FA, encryption, app access)
- The ready-made answers for when clients or partners ask about our security
- Every security action we've completed (audit trail)

**Why it matters to you:** If a client asks "is our data secure?" or a partner asks "are you HIPAA compliant?" — the answers are scripted and ready in Posture. It also tracks that everyone's access is correct and current.

**Key facts from Posture:**
- 2FA is mandatory for all users (enforced org-wide)
- All 13 web apps are restricted to RPI organization members only
- Super Admin access is locked to Josh + John Behn
- BAA with Google signed February 4, 2026
- All data encrypted in transit (TLS 1.3) and at rest (AES-256)

### 3. The Immune System — Automatic Enforcement

This is the part that runs in the background every time code is written or deployed. 21 rules that automatically:
- **Block** dangerous patterns before they ever make it into the system (hardcoded passwords, exposed credentials, PHI in log files, public-facing app access)
- **Warn** about risky patterns that need review (dates that might break, missing response formats, accessibility issues)
- **Learn** from every session and get smarter over time

**Why it matters to you:** You don't need to do anything with this — it's automatic. But it's why our codebase stays clean. Every piece of code goes through 21 checkpoints before it reaches production. Think of it as the antibodies in The Machine's bloodstream.

**The learning loop:** When the Immune System catches something, it gets logged. Every morning at 4am, a pipeline reviews what was caught, updates the rules if needed, and reports to Josh. The system literally gets smarter every day.

### 4. Monitoring — The Watchdogs

This covers everything that's being watched, from real-time to annual:

| How Often | What's Happening |
|-----------|-----------------|
| Real-time | Code enforcement (Immune System) |
| Daily | Data pipeline health, knowledge promotion |
| Weekly | Analytics reports, stale user checks |
| Monthly | Token hygiene, credential review |
| Quarterly | Full security audit, access review |
| Annually | DR plan review, vendor re-evaluation |

**Why it matters to you:** Nothing falls through the cracks. If a user account goes stale, if a token expires, if a deployment drifts — monitoring catches it.

### 5. Operations — The Human Checklists

This is the stuff that requires a person:
- **Offboarding:** When someone leaves RPI, there's a same-day checklist (disable account, revoke tokens, transfer files, update access lists)
- **Incident Response:** If something goes wrong, there's a step-by-step procedure (contain, assess, notify, remediate, document)
- **Training:** PHI handling training requirements for anyone who touches client data
- **Documentation Updates:** When the codebase changes, which docs get updated

**Why it matters to you:** If you're ever involved in handling an employee departure, a security incident, or onboarding — the checklist is in Operations. No guessing.

---

## How It All Connects

The 5 subsystems form a continuous loop:

```
Standards define the rules
    → The Immune System enforces them automatically
        → Monitoring detects when something drifts
            → Operations corrects what was found
                → Standards evolve based on what we learned
                    → (repeat)
```

No subsystem works alone. A rule without enforcement is just a suggestion. Enforcement without monitoring is blind. Monitoring without operations is noise. This loop is what makes The OS self-correcting.

---

## What Changed (Before vs. After)

| Before | After |
|--------|-------|
| 5 separate policy documents | 6 organized OS documents (one per subsystem + master) |
| Same rule in multiple places | Every rule in exactly one place |
| Had to know which doc to check | One routing table: "I need to..." → go here |
| Security and compliance scattered | All posture/access in one doc |
| Processes buried in different files | All human checklists in one doc |
| Immune System was its own thing | Immune System is a named subsystem of The OS |

**Nothing was deleted.** Everything from the old documents is in the new ones — it's just organized by function instead of by when it was written.

**Old links still work.** The old file locations now redirect to the new OS documents automatically. No broken references anywhere.

---

## What This Means For You

### If you're on the Service Team (Nikki's division)
You handle PHI daily. Standards defines exactly how to handle it — storage, display, transmission. The rules haven't changed, they're just easier to find now.

### If you're on the Sales Team (Vinnie's division)
When prospects or clients ask about security, Posture has scripted answers ready. "Are you HIPAA compliant?" "Do you encrypt data?" "Can you sign a BAA?" — all answered.

### If you're on the B2B/DAVID Team (Matt's division)
When onboarding M&A partners, Standards is the compliance baseline. Operations has the checklists. Posture proves we practice what we preach.

### If you're in Leadership (John, Shane)
The 9-layer compliance grid in the master document maps every compliance concern to exactly one OS subsystem. Quarterly audits now run automatically and report to Slack. The audit trail in Posture documents every security action taken.

### If you're the CTO (Jason)
The full technical reference is in the OS directory. Immune System has the complete rule reference. Monitoring has every automated cadence. The governance cycle diagram shows how it all connects.

---

## The Numbers

| Metric | Count |
|--------|-------|
| Enforcement rules (automatic) | 21 |
| Automated monitoring agents | 4 (daily, weekly schedules) |
| GAS compliance triggers | 3 (quarterly, weekly, monthly) |
| Web apps verified org-only | 13 of 13 |
| Tokens revoked (Q1 audit) | 26 |
| Super Admins (locked down) | 2 (Josh + John Behn) |
| 2FA enforcement | 100% of users |
| Policy documents (unified) | 6 (was 5, now organized) |
| Projects covered | 18 |

---

## Quick Reference

| "I need to..." | Go to |
|-----------------|-------|
| Know the data handling rules | Standards |
| Answer a client's security question | Posture (Part 1) |
| Check who has access to what | Posture (Part 3) |
| Understand what's being monitored | Monitoring |
| Follow an offboarding checklist | Operations |
| Follow an incident response procedure | Operations |
| Understand the enforcement rules | Immune System |
| See the full architecture | OS (master document) |

---

## The Bottom Line

The Operating System is how we prove — to ourselves, to our clients, to our partners, and to regulators — that The Machine is governed. Not by hope, not by good intentions, but by rules that enforce themselves, monitoring that never sleeps, and processes that leave nothing to chance.

We're not a tech company that bolted on compliance. We built compliance into the machine from the ground up. The OS is the proof.

---

*Document location: `_RPI_STANDARDS/reference/os/TEAM_GUIDE.md`*
*Last updated: February 19, 2026*
*Questions? Ask Josh or John Behn.*
