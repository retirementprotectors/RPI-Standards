# Monitoring

> **Part of The Operating System** -- the governance layer of The Machine.
> See [OS.md](OS.md) for the full architecture.
> This document defines what's being watched -- automated and manual health checks.

**Version**: v2.0 (March 19, 2026 — OS Audit refresh for toMachina architecture)
**Merged from**: WEEKLY_HEALTH_CHECK.md + PROJECT_AUDIT.md + extractions from COMPLIANCE_STANDARDS.md and SECURITY_COMPLIANCE.md

---

## Cross-References

- For the rules being enforced, see [STANDARDS.md](STANDARDS.md)
- For the enforcement engine, see [IMMUNE_SYSTEM.md](IMMUNE_SYSTEM.md)
- For human processes triggered by findings, see [OPERATIONS.md](OPERATIONS.md)

---

## Part 1: Cadences Overview

Every monitoring activity in The Machine, from real-time code enforcement to annual security reviews.

| Cadence | What | System |
|---------|------|--------|
| Real-time | Hookify code enforcement | Immune System |
| Daily 3:30am | Analytics push to MATRIX | launchd (analytics-push) |
| Daily 4:00am | Knowledge promotion (MEMORY to CLAUDE.md) | launchd (knowledge-promote) |
| Sunday 3am | Session cleanup | launchd (claude-cleanup) |
| Monday 8am | Weekly Slack analytics report | launchd (mcp-analytics) |
| Monday | Weekly health check (all projects) | Manual (Claude Code) |
| Monthly 15th | Token hygiene scan | GAS trigger |
| Quarterly | Full compliance audit (posts to Slack) | GAS trigger |
| Quarterly | Stale user monitoring | GAS trigger (weekly, escalates quarterly) |
| Quarterly | Access permissions audit | Manual |
| Annual | Full security review | Manual |
| Annual | BAA / vendor security review | Manual |
| Annual | Policy review and update | Manual |
| Annual | Training completion verification | Manual |
| Every PR + push to main | E2E UI visual verification (Playwright — 10 modules) | GitHub Actions (e2e-ui) |
| Every push to main | E2E intake pipeline tests (Vitest — 4 wire tests) | GitHub Actions (e2e-intake) |
| Weekly (Mon) | Dependabot dependency vulnerability scan | GitHub (automated PRs) |
| Weekly (Sun) + every PR | CodeQL static security analysis | GitHub Actions |

---

## Part 2: Automated Monitoring

### 2.1 launchd Agents (macOS)

Six launchd agent plist files exist on JDM's machine. Status as of 2026-03-19:

| Agent | Schedule | Status | What It Does |
|-------|----------|--------|--------------|
| `com.rpi.document-watcher` | Always-on (KeepAlive) | DOWN (DNS errors — replaced by WIRE_INCOMING_CORRESPONDENCE Cloud Function) | Intake queue watcher for incoming correspondence |
| `com.rpi.knowledge-promote` | Daily 11:15pm | ACTIVE | Promotes MEMORY.md learnings into CLAUDE.md; Slack DM digest; compliance-history.json trend tracking |
| `com.rpi.claude-cleanup` | Sunday 3am | ACTIVE | Cleans up old Claude Code sessions |
| `com.rpi.mcp-analytics` | Monday 8am | ACTIVE | Generates weekly Slack analytics report |
| `com.rpi.analytics-push` | Daily 3:30am | DISABLED (replaced by BigQuery streaming Cloud Function in Sprint 5) | Was: push analytics to MATRIX sheets |
| `com.rpi.prodash-sync` | — | REMOVED 2026-03-19 (plist deleted, was crashed exit 78) | Was: ProDash sync — no longer needed |

**Verify status:**
```bash
launchctl list | grep com.rpi
```

### 2.2 GAS Triggers (RAPID_API)

Three automated GAS triggers run in RAPID_API:

| Trigger | Frequency | Function | What It Does |
|---------|-----------|----------|--------------|
| Quarterly Audit | Feb, May, Aug, Nov 1st @ 7 AM | `runQuarterlyAuditIfDue_()` | Full compliance audit, posts results to Slack |
| Weekly Stale User Monitor | Mondays @ 7 AM | `runWeeklyStaleUserCheck_()` | Flags users inactive 30+ days |
| Monthly Token Hygiene | 15th @ 7 AM | `runMonthlyTokenHygiene_()` | Scans for unapproved apps with sensitive scopes |

**Setup:** Project: RAPID_API | File: API_Compliance.gs | Run: `SETUP_ComplianceTrigger`

### 2.3 Pending GAS Triggers (Not Yet Implemented)

| Trigger | Purpose | Status |
|---------|---------|--------|
| NewUserDetection | Detect new Workspace users, notify admin | Planned |
| AutoOffboard | Auto-suspend users moved to Archived OU | Planned |

### 2.4 Public Website Legal Pages

Three public-facing legal/compliance pages on retireprotected.com must remain accessible. These are referenced in A2P 10DLC campaign registration and toll-free SMS compliance.

| Page | URL | WP Page ID | Check |
|------|-----|------------|-------|
| Privacy Policy | https://retireprotected.com/privacy-policy/ | 639 | HTTP 200 |
| Terms of Service | https://retireprotected.com/terms-of-service/ | 640 | HTTP 200 |
| SMS Terms & Conditions | https://retireprotected.com/sms-terms/ | 641 | HTTP 200 |

**Frequency:** Monthly (manual or scripted `curl -sI <url> | head -1`). If any page returns non-200, investigate immediately — downtime affects A2P campaign compliance.

**Google Groups (referenced on legal pages):**

These groups are the contact addresses listed on the Privacy Policy, Terms of Service, and SMS Terms pages. If they stop receiving mail, privacy/compliance requests go unanswered.

| Group | Purpose | Check |
|-------|---------|-------|
| contact@retireprotected.com | General inquiries, client communications | Send test email, verify delivery |
| compliance@retireprotected.com | Privacy rights requests, HIPAA/security concerns | Send test email, verify delivery |

**Frequency:** Quarterly (alongside the access permissions audit). Verify: (1) groups still exist in Google Admin, (2) external posting is still enabled, (3) a test email from an external address is delivered to group members.

### 2.5 Immune System (Real-Time)

The hookify plugin provides real-time code enforcement during every Claude Code session. It operates at tool-call level, blocking or warning before violations reach the codebase.

- **Tier 1 (Block):** Prevents hardcoded secrets, PHI in logs, anonymous access, forbidden function calls
- **Tier 2 (Warn):** Flags missing serialization, non-flexbox modals, plain person selects
- **Quality Gates:** Post-bash reminders for deploy verification and commit/deploy pairing

For full details, see [IMMUNE_SYSTEM.md](IMMUNE_SYSTEM.md).

---

## Part 3: Weekly Health Check

> **When to Use**: Weekly audit of all active projects
> **Frequency**: Every Monday or first day of work week
> **Time Required**: 15-30 minutes (automated via Claude Code)
> **Trigger**: Tell Claude Code "weekly check" or "health check"

### Purpose

Quick verification that all projects maintain baseline health:
- Git status clean and synced
- No forbidden code patterns introduced
- MCP tools functioning
- Documentation current

This is a **quick check**, not a full audit. For comprehensive project audits, use Part 4.

### How to Run

Tell Claude Code: **"weekly check"** or **"health check"**

Claude Code will automatically:
1. Check git status across all 8 active projects (using SuperProject paths)
2. Scan for forbidden code patterns
3. Verify documentation status
4. Report results

### 3.1 Git Health (All Projects)

```bash
for repo in \
  ~/Projects/toMachina \
  ~/Projects/gas/RAPID_CORE \
  ~/Projects/gas/RAPID_IMPORT \
  ~/Projects/gas/DEX \
  ~/Projects/services/MCP-Hub \
  ~/Projects/services/PDF_SERVICE \
  ~/Projects/services/Marketing-Hub \
  ~/Projects/_RPI_STANDARDS; do
  name=$(echo "$repo" | sed "s|$HOME/Projects/||")
  git_short=$(git -C "$repo" status --short 2>/dev/null)
  branch=$(git -C "$repo" branch --show-current 2>/dev/null)
  last=$(git -C "$repo" log -1 --format="%ar" 2>/dev/null)
  if [ -z "$git_short" ]; then
    echo "$name | CLEAN | $branch | $last"
  else
    count=$(echo "$git_short" | wc -l | tr -d ' ')
    echo "$name | DIRTY ($count) | $branch | $last"
  fi
done
```

**Red Flags**:
- `DIRTY` -- Commit and push
- `fatal: not a git repository` -- Git not initialized (CRITICAL)
- Last commit > 2 weeks ago on active project -- Check if stale

### 3.2 Code Quality Scan

Scan for forbidden patterns across all GAS web apps:

```bash
# Forbidden function calls (actual calls only, excluding variable names/comments)
for repo in ~/Projects/toMachina ~/Projects/toMachina \
  ~/Projects/archive/C3 ~/Projects/archive/CAM ~/Projects/archive/CEO-Dashboard \
  ~/Projects/gas/DEX ~/Projects/archive/RIIMO ~/Projects/archive/RPI-Command-Center \
  ~/Projects/archive/RAPID_API ~/Projects/archive/RAPID_COMMS ~/Projects/gas/RAPID_CORE ~/Projects/gas/RAPID_IMPORT \
  ~/Projects/archive/sentinel-v1 ~/Projects/archive/sentinel-v2 ~/Projects/archive/DAVID-HUB; do
  name=$(basename "$repo")
  # Scan .html and .gs files for forbidden UI calls
  grep -rn 'showConfirm\|showToast\|showAlert' "$repo"/*.html "$repo"/*.gs 2>/dev/null | head -3
done

# Hardcoded inline colors
for repo in ~/Projects/toMachina ~/Projects/toMachina \
  ~/Projects/archive/C3 ~/Projects/archive/CAM ~/Projects/archive/CEO-Dashboard \
  ~/Projects/gas/DEX ~/Projects/archive/RIIMO ~/Projects/archive/RPI-Command-Center \
  ~/Projects/archive/RAPID_API ~/Projects/archive/RAPID_COMMS ~/Projects/gas/RAPID_CORE ~/Projects/gas/RAPID_IMPORT \
  ~/Projects/archive/sentinel-v1 ~/Projects/archive/sentinel-v2 ~/Projects/archive/DAVID-HUB; do
  name=$(basename "$repo")
  grep -rn 'style=.*hex-color-pattern' "$repo"/*.html 2>/dev/null | head -3
done
```

> **Note:** The actual grep patterns used at runtime include regex matching for forbidden
> function calls and hex color codes. See `reference/maintenance/WEEKLY_HEALTH_CHECK.md`
> for the exact regex patterns. They are omitted here to avoid triggering hookify rules
> on this documentation file.

**Known violations to track:**

| Project | Issue | Severity |
|---------|-------|----------|
| QUE-Medicare | 3x forbidden UI calls + 1x forbidden confirm in Scripts.html | HIGH -- real forbidden calls |
| PRODASHX | Hardcoded hex colors in Index.html + C3-Evolution.html | MEDIUM |
| QUE-Medicare | Hardcoded hex colors in Index.html + Scripts.html | MEDIUM |
| DEX | Hardcoded hex colors in Index.html (input modal) | LOW |
| sentinel | Hardcoded hex colors in Index.html (modals) | LOW |

### 3.3 Source Code Security Scan

```bash
# Check all appsscript.json for wrong access settings
grep -rn '"access"' ~/Projects/*/appsscript.json ~/Projects/*/*/appsscript.json 2>/dev/null | grep -v DOMAIN

# Check for hardcoded MATRIX IDs outside RAPID_CORE
# Uses RAPID_MATRIX + SENTINEL_MATRIX IDs from RAPID_CORE.getMATRIX_ID()
# Exact IDs omitted from this doc — see WEEKLY_HEALTH_CHECK.md for full grep

# Check for plaintext tokens/secrets in source
# Scans for Slack bot tokens, webhook URLs across .gs/.js/.json files
# Exact patterns omitted from this doc — see WEEKLY_HEALTH_CHECK.md for full grep

# Check GitHub repo privacy
gh repo list retirementprotectors --visibility public 2>/dev/null
```

**Red Flags**:
- Any `appsscript.json` NOT showing DOMAIN (except RAPID_API -- approved exception for SPARK webhook)
- Any MATRIX IDs outside RAPID_CORE
- Any plaintext tokens in source files
- Any public repos

### 3.4 MCP Tools Verification

```bash
claude mcp list
```

**Check these are running:**

| MCP | Type | What It Does |
|-----|------|--------------|
| rpi-workspace | Consolidated | GAS execution, Chat, People, WordPress, Canva, Video |
| rpi-business | Consolidated | Commission intelligence, Meeting processor |
| rpi-healthcare | Consolidated | NPI, ICD-10, CMS coverage |
| gdrive | Third-party | Google Drive access |
| google-calendar | Third-party | Calendar events |
| gmail | Third-party | Read/send email |
| slack | Third-party | Slack messages/channels |
| playwright | Plugin | Browser automation |

### 3.5 Documentation Spot Check

Pick one project each week and verify:

- [ ] `CLAUDE.md` exists and is current
- [ ] `Docs/0-SESSION_HANDOFF.md` reflects current state
- [ ] Version number in handoff matches deployed version

**Projects missing session handoffs (as of 2026-02-13):**
- QUE-Medicare, C3, MCP-Hub, PDF_SERVICE, RIIMO, RPI-Command-Center, sentinel-v2

**Projects missing Docs/ directory entirely:**
- PDF_SERVICE, RIIMO

### 3.6 Weekly Report Template

```markdown
## Weekly Health Check Report
**Date**: YYYY-MM-DD
**Checked by**: Claude Code GA

### Git Status
| Project | Status | Last Commit | Notes |
|---------|--------|-------------|-------|
| _RPI_STANDARDS | pass/warn | X ago | |
| toMachina | pass/warn | X ago | |
| toMachina (QUE is a module) | pass/warn | X ago | |
| gas/ or archive/C3 | pass/warn | X ago | |
| gas/ or archive/CAM | pass/warn | X ago | |
| gas/ or archive/CEO-Dashboard | pass/warn | X ago | |
| gas/ or archive/DEX | pass/warn | X ago | |
| gas/ or archive/MCP-Hub | pass/warn | X ago | |
| gas/ or archive/PDF_SERVICE | pass/warn | X ago | |
| gas/ or archive/RAPID_API | pass/warn | X ago | |
| gas/ or archive/RAPID_COMMS | pass/warn | X ago | |
| gas/ or archive/RAPID_CORE | pass/warn | X ago | |
| gas/ or archive/RAPID_IMPORT | pass/warn | X ago | |
| gas/ or archive/RIIMO | pass/warn | X ago | |
| gas/ or archive/RPI-Command-Center | pass/warn | X ago | |
| archive/DAVID-HUB | pass/warn | X ago | |
| archive/sentinel | pass/warn | X ago | |
| archive/sentinel-v2 | pass/warn | X ago | |

### Code Quality
- [ ] No new forbidden pattern violations

### MCP Tools
- [ ] All MCPs connected

### Documentation
- **Spot-checked**: [PROJECT_NAME]

### Issues Found
[List any issues and remediation taken]

### Status: HEALTHY / NEEDS ATTENTION
```

### 3.7 Escalation Triggers

**Immediate Action Required**:
- Git not initialized on any project
- MCP tools all failing (auth issue)
- New forbidden UI function calls in production code

**Schedule Fix This Week**:
- Uncommitted changes older than 3 days
- Out-of-date session handoffs
- New hardcoded colors introduced

**Note for Next Week**:
- Minor documentation gaps
- Non-critical MCP failures

---

## Part 4: Project Audit

> **When to Use**: Verifying an EXISTING project follows RPI-Standards
> **Counterpart**: See CLAUDE.md "New Project Setup" section (for NEW projects)
> **How to Run**: Tell Claude Code "audit [PROJECT_NAME]"

### Purpose

This audit verifies an **existing project** is fully compliant with RPI-Standards. It checks everything the Kickoff Template establishes, but retroactively.

| Kickoff Template | This Audit |
|------------------|------------|
| "Build it right" | "Is it right?" |
| Day 0 | Any day after |
| Creates docs | Verifies docs |

### What Gets Checked

| Category | Items |
|----------|-------|
| **Git & Deployment** | Git initialized, remote set, on main branch, synced |
| **Document Structure** | CLAUDE.md, Docs/ with handoff + briefing |
| **Standards Reference** | References `_RPI_STANDARDS/`, doesn't copy |
| **Code Quality** | No forbidden UI calls, structured responses, no hardcoded colors |
| **Security** | Org-only access, no hardcoded credentials, Script Properties for secrets |
| **PHI Compliance** | No PHI in logs/errors, SSN masking, PHI only in Workspace |

### Phase 1: Git & Infrastructure

```bash
cd ~/Projects/[SUPERPROJECT]/[PROJECT_NAME]
git status
git remote -v
git log --oneline -5
```

**Expected**:
- On branch `main`
- Remote origin: `https://github.com/retirementprotectors/[REPO_NAME].git`
- Recent commits, clean working tree

**Note**: GitHub repo names may differ from local folder names.

### Phase 2: Document Structure

**Required documents:**

| Document | Required | Purpose |
|----------|----------|---------|
| `CLAUDE.md` | All projects | Project context for Claude Code |
| `Docs/0-SESSION_HANDOFF*.md` | GAS projects | Current state, continuity |
| `Docs/1-AGENT_BRIEFING.md` | GAS projects | Project context |
| `.clasp.json` | GAS projects | Script ID configuration |
| `appsscript.json` | GAS projects | GAS manifest |

### Phase 3: Standards Compliance

**CLAUDE.md must include or reference:**
- Project-specific context (what this project does, key modules)
- Required References section pointing to `_RPI_STANDARDS/reference/`
- Deployment ID for `clasp deploy -i`

**Must NOT contain:**
- Copies of global standards (reference `_RPI_STANDARDS/` instead)
- Outdated paths (`0-Setup/`, `1-Manage/`, `2-Production/`)

### Phase 4: Code Quality Scan

```bash
# Forbidden function calls — scan .html and .gs files
# Uses regex to find actual function calls while excluding
# variable names, CSS classes, comments, and parameter names

# Hardcoded colors — scan .html files for inline hex colors

# Plaintext credentials — scan for Slack tokens, webhook URLs, API keys
# in .gs, .js, .json files (excluding node_modules)

# Generic secret patterns — review manually for false positives
# Checks for api_key, apiKey, password, secret in .gs files
# (excluding PropertiesService references, comments, function names)
```

> **Note:** Exact grep regex patterns are in `reference/maintenance/PROJECT_AUDIT.md`
> and `reference/maintenance/WEEKLY_HEALTH_CHECK.md`. Omitted here to avoid triggering
> hookify enforcement rules on this documentation file.

### Phase 5: Security Check

- [ ] `appsscript.json` contains `"access": "DOMAIN"` (source file, not just GAS editor UI)
- [ ] `appsscript.json` contains `"executionApi": { "access": "DOMAIN" }` (if project needs MCP execute_script)
- [ ] No hardcoded credentials in code (all in Script Properties)
- [ ] No plaintext secrets in `.gs`, `.json`, `.js` files
- [ ] `.gitignore` includes `credentials.json`, `.env`, `tokens.json`
- [ ] GCP project linked to `90741179392` (manual GAS editor verification: Settings > GCP Project)
- [ ] No PHI in console.log/Logger.log statements
- [ ] Error messages don't expose sensitive data

### Audit Report Format

```markdown
## Standards Audit Report: [PROJECT_NAME]
**Date**: YYYY-MM-DD
**Path**: ~/Projects/[SUPERPROJECT]/[PROJECT_NAME]

### Git
| Check | Status |
|-------|--------|
| Git initialized | pass/fail |
| Remote set correctly | pass/fail |
| On main branch | pass/fail |
| Clean working tree | pass/fail |

### Documentation
| Document | Status |
|----------|--------|
| CLAUDE.md | pass/fail |
| Docs/0-SESSION_HANDOFF.md | pass/fail/N/A |
| .clasp.json | pass/fail/N/A |

### Code Quality
| Check | Status |
|-------|--------|
| No forbidden UI calls | pass/fail |
| No hardcoded colors | pass/fail |
| No hardcoded credentials | pass/fail |
| Structured responses | pass/fail |

### Security
| Check | Status |
|-------|--------|
| Org-only access | pass/fail/pending |
| Script Properties for secrets | pass/fail |
| No PHI in logs | pass/fail |

### Final Status: COMPLIANT / PARTIAL / NEEDS WORK
```

### Project Tracker

| Project | Path | Last Audit | Status |
|---------|------|------------|--------|
| _RPI_STANDARDS | `_RPI_STANDARDS` | 2026-02-13 | Compliant |
| PRODASHX | `toMachina` | 2026-02-04 | Compliant |
| QUE-Medicare | `toMachina (QUE is a module)` | -- | Pending |
| C3 | `gas/ or archive/C3` | 2026-02-04 | Compliant |
| CAM | `gas/ or archive/CAM` | 2026-02-04 | Compliant |
| CEO-Dashboard | `gas/ or archive/CEO-Dashboard` | -- | Pending |
| DEX | `gas/ or archive/DEX` | -- | Pending |
| MCP-Hub | `gas/ or archive/MCP-Hub` | -- | Pending |
| PDF_SERVICE | `gas/ or archive/PDF_SERVICE` | -- | Pending |
| RAPID_API | `gas/ or archive/RAPID_API` | 2026-02-04 | Compliant |
| RAPID_COMMS | `gas/ or archive/RAPID_COMMS` | -- | Pending |
| RAPID_CORE | `gas/ or archive/RAPID_CORE` | 2026-02-04 | Compliant |
| RAPID_IMPORT | `gas/ or archive/RAPID_IMPORT` | -- | Pending |
| RIIMO | `gas/ or archive/RIIMO` | -- | Pending |
| RPI-Command-Center | `gas/ or archive/RPI-Command-Center` | -- | Pending |
| DAVID-HUB | `archive/DAVID-HUB` | 2026-02-04 | Compliant |
| sentinel | `archive/sentinel` | 2026-02-04 | Compliant |
| sentinel-v2 | `archive/sentinel-v2` | -- | Pending |
| SPARK_WEBHOOK_PROXY | `gas/ or archive/SPARK_WEBHOOK_PROXY` | -- | Pending |

### Batch Audit Tips

1. **Parallel Execution**: Claude Code spawns sub-agents per project -- independent audits run simultaneously
2. **Fix as you go**: Don't just report -- fix issues when found
3. **Commit per project**: Each project gets its own commit with message `docs: RPI-Standards audit - [summary]`
4. **Update tracker**: Mark projects as compliant after successful audit

---

## Part 5: Periodic Review Schedule

Extracted from COMPLIANCE_STANDARDS.md. These are manual reviews that supplement automated monitoring.

### Quarterly Reviews

| Review | When | Owner | Deliverable |
|--------|------|-------|-------------|
| Access permissions audit | Feb, May, Aug, Nov | JDM + John Behn | Verified user list, removed stale access |
| Compliance audit results review | After each GAS trigger run | JDM | Slack post acknowledgment, remediation if needed |

### Annual Reviews

| Review | When | Owner | Deliverable |
|--------|------|-------|-------------|
| Full security review | January | JDM + JMDC | Security posture report |
| Vendor security review | January | JDM + Shane | Vendor risk assessment |
| BAA review | January | JDM + John Behn | Updated BAA documentation |
| Policy review and update | January | JDM | Updated COMPLIANCE_STANDARDS.md |
| Training completion verification | January | JDM + Nikki | Training records for all staff |

### Manual Quarterly Tasks (From SECURITY_COMPLIANCE.md)

These tasks are triggered by the automated quarterly audit but require human follow-through:

- Review and act on `runQuarterlyAuditIfDue_()` Slack output
- Verify all web apps still show org-only access in GAS editor UI
- Confirm GCP project linkage for any new projects
- Review Script Properties for any projects that changed credentials
- Update Project Tracker table (Part 4) with audit dates

### Manual Annual Tasks (From SECURITY_COMPLIANCE.md)

- Full penetration test / security review of all web apps
- Review all OAuth scopes across MCP servers
- Audit all launchd agents and GAS triggers for relevance
- Review and update PHI_POLICY.md
- Verify BAA coverage for all vendors handling PHI
- Confirm training records for HIPAA/compliance

---

## Part 6: Current Logging Status

Extracted from COMPLIANCE_STANDARDS.md. Understanding what's logged helps identify blind spots.

| System | Logging Available | Implemented |
|--------|-------------------|-------------|
| MATRIX (Sheets) | Edit history | Native |
| GAS Web Apps | Execution logs | Native |
| MCP Tools | Query logging | Not yet |
| MDJ Instances | Conversation logging | Future |

### Logging Gaps to Address

1. **MCP query logging** -- Currently no record of what MCP tools query or when. Future: add structured logging to rpi-workspace, rpi-business, rpi-healthcare MCPs.
2. **MDJ conversation logging** -- Claude Code sessions generate knowledge (MEMORY.md, compliance-history.json) but full conversation logs are not retained beyond session exports.
3. **launchd agent logging** -- Agents write to stdout/stderr but centralized log review is not automated. Future: aggregate into a monitoring dashboard.

---

## Integration with Other Standards

| Related Document | When to Use |
|-----------------|-------------|
| [STANDARDS.md](STANDARDS.md) | What the rules ARE (code standards, PHI rules, deploy rules) |
| [IMMUNE_SYSTEM.md](IMMUNE_SYSTEM.md) | How rules are ENFORCED in real-time (hookify engine) |
| [OPERATIONS.md](OPERATIONS.md) | Human processes triggered by monitoring findings |
| `reference/compliance/COMPLIANCE_STANDARDS.md` | Full compliance policy (source for Parts 5-6) |
| `reference/compliance/SECURITY_COMPLIANCE.md` | Full security procedures (source for GAS triggers) |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 19, 2026 | Initial creation. Merged from WEEKLY_HEALTH_CHECK.md + PROJECT_AUDIT.md + extractions from COMPLIANCE_STANDARDS.md and SECURITY_COMPLIANCE.md |
| v1.1 | Mar 8, 2026 | Added Section 2.4: Public Website Legal Pages monitoring (Privacy Policy, ToS, SMS Terms on retireprotected.com) |
| v1.2 | Mar 8, 2026 | Added Google Groups monitoring (contact@ and compliance@) to Section 2.4 — quarterly delivery verification |

---

*What gets measured gets managed. What gets automated gets done.*
