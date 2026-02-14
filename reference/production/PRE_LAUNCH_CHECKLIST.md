# Pre-Launch Checklist

> **When to Use**: Before deploying any project to production  
> **Companion**: `PRODUCTION_LAUNCH_ROLLOUT_KIT.md` (user documentation)  
> **Version**: v1.1 (February 13, 2026)

---

## Purpose

Technical verification that a project is ready for production deployment. This checklist covers:
- Security review
- Code quality verification
- Performance baseline
- Rollback planning
- Compliance check

**Use this BEFORE** deploying to production.  
**Use `PRODUCTION_LAUNCH_ROLLOUT_KIT.md` AFTER** deployment for user documentation.

---

## Pre-Launch Checklist

### Phase 1: Security Review

#### 1.1 No Secrets in Code

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]

# Check for API keys, passwords, tokens
grep -rn "apikey\|api_key\|password\|secret\|token" *.gs *.html 2>/dev/null | grep -v "// " | grep -v "getScriptProperties"

# Check for hardcoded URLs that should be configurable
grep -rn "https://script.google.com" *.gs *.html 2>/dev/null
```

**Expected**: No hardcoded secrets. All sensitive values in Script Properties.

- [ ] No API keys in code
- [ ] No passwords in code
- [ ] No tokens in code
- [ ] Sensitive values use `PropertiesService.getScriptProperties()`

#### 1.2 Access Control

- [ ] Web app access set to "Anyone within RPI" (not "Anyone")
- [ ] Execute as "Me" or appropriate user
- [ ] MATRIX permissions reviewed (who can edit vs. view)

#### 1.3 Data Protection

- [ ] No PII logged to console unnecessarily
- [ ] Error messages don't expose internal paths
- [ ] SSN/DOB fields masked in UI where appropriate

---

### Phase 2: Code Quality Verification

#### 2.1 Forbidden Patterns Check

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]

# Check for banned dialogs
grep -rn "alert(\|confirm(\|prompt(" *.html *.gs 2>/dev/null | grep -v "showConfirm\|showToast"

# Check for hardcoded colors
grep -rn 'style=.*#[0-9a-fA-F]' *.html 2>/dev/null

# Check for console.log in production
grep -rn "console.log" *.gs *.html 2>/dev/null | wc -l
```

- [ ] No `alert()`, `confirm()`, `prompt()` calls
- [ ] No hardcoded colors (use CSS variables)
- [ ] Console.log usage is intentional/appropriate

#### 2.2 Error Handling

- [ ] All server functions return `{ success: true/false, data/error }`
- [ ] Client-side shows user-friendly error messages
- [ ] Failed operations don't leave data in inconsistent state

#### 2.3 UI Compliance

- [ ] Uses RPI brand colors (see `0-Setup/UI_DESIGN_GUIDELINES.md`)
- [ ] Mobile responsive (test at 375px width)
- [ ] Loading states shown for async operations
- [ ] Modals can be closed with Escape key

---

### Phase 3: Version Control Status

#### 3.1 Git Clean

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status
git remote -v
git log --oneline -5
```

- [ ] Working tree clean (all changes committed)
- [ ] All commits pushed to origin
- [ ] Remote URL is correct `retirementprotectors/[PROJECT]`

#### 3.2 Version Documented

- [ ] Version number in `Docs/0-SESSION_HANDOFF.md` matches deployed
- [ ] Version in OPS scope matches
- [ ] Changelog/version history updated

---

### Phase 4: GAS Deployment Verification

#### 4.1 Deployment ID

```bash
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
cat .clasp.json
```

- [ ] `.clasp.json` has correct `scriptId`
- [ ] Deployment ID documented in `Docs/2.2-AGENT_SCOPE_OPS.md`
- [ ] GCP project linked to `90741179392` (Settings → GCP Project in GAS editor)
- [ ] `appsscript.json` includes `"executionApi": { "access": "DOMAIN" }`

#### 4.2 Test Deployment

```bash
# Push to GAS
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force

# Create version
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - description"

# Deploy to specific deployment
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOYMENT_ID] -V [VERSION] -d "vX.X"
```

- [ ] `clasp push` succeeds
- [ ] `clasp version` creates new version
- [ ] `clasp deploy` updates production deployment

#### 4.3 Production URL Test

- [ ] Open production URL in browser
- [ ] App loads without errors
- [ ] Test core functionality manually
- [ ] Check browser console for errors

---

### Phase 5: Performance Baseline

#### 5.1 Load Time

- [ ] Initial page load < 5 seconds
- [ ] Key operations complete < 3 seconds
- [ ] Large data loads show progress indicator

#### 5.2 GAS Limits Awareness

| Limit | Value | Project Status |
|-------|-------|----------------|
| Execution time | 6 minutes | ✅ / ⚠️ |
| URL fetch calls | 20,000/day | ✅ / ⚠️ |
| Simultaneous executions | 30 | ✅ / ⚠️ |
| Triggers | 20 per user | ✅ / ⚠️ |

- [ ] No single operation at risk of timeout
- [ ] API calls not at risk of daily limit

---

### Phase 6: Rollback Plan

#### 6.1 Previous Version Documented

- [ ] Previous deployment ID recorded
- [ ] Previous version number known
- [ ] Previous version still accessible

#### 6.2 Rollback Command Ready

```bash
# Rollback command (fill in before launch)
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOYMENT_ID] -V [PREVIOUS_VERSION] -d "Rollback to vX.X"
```

- [ ] Rollback command documented in OPS scope
- [ ] JDM knows how to request rollback

---

### Phase 7: Documentation Complete

#### 7.1 Technical Docs

- [ ] `Docs/0-SESSION_HANDOFF.md` current
- [ ] `Docs/2.2-AGENT_SCOPE_OPS.md` has all deployment info
- [ ] All agent scope docs accurate

#### 7.2 User Docs (if applicable)

- [ ] `Docs/User/` folder created
- [ ] System overview document exists
- [ ] Role-specific guides created

See `PRODUCTION_LAUNCH_ROLLOUT_KIT.md` for user documentation requirements.

#### 7.3 Module Testing Guide (MANDATORY for major modules)

**Every major module rollout gets a testing guide. Make one of these fuckers.**

**Template**: `_RPI_STANDARDS/reference/production/TESTING_GUIDE_TEMPLATE.md` — copy it, fill in the blanks.
**Reference example**: `PRODASH/Docs/TESTING_GUIDE_MEDICARE_CENTER.md` (and its HTML counterpart on Desktop).

- [ ] Testing guide created in `Docs/TESTING_GUIDE_[MODULE_NAME].md`
- [ ] HTML version generated on Desktop for interactive use (`~/Desktop/TESTING_GUIDE_[MODULE_NAME].html`)
- [ ] Covers ALL tabs/views/features of the module with checkbox items
- [ ] Includes prerequisite checklist (what must be running/configured before testing)
- [ ] Includes data verification tables (expected values in sheets/systems)
- [ ] Includes cross-feature end-to-end workflow test
- [ ] Includes error handling / edge case section
- [ ] Includes post-test summary with Pass/Fail per section + signature block
- [ ] Version number matches the deployed version

**What counts as a "major module":**
- New Sales Center (Medicare, Life, Annuity, Advisory)
- New Service Center or major Service Center upgrade
- New integration (SPARK, carrier APIs, webhook endpoints)
- AI3 or Strategy Output Engine upgrades
- Any feature that touches 3+ files and creates new UI tabs/views

**HTML version requirements:**
- Interactive checkboxes with progress bar
- RPI branding (Navy/Light Blue/Poppins)
- Print-friendly (clean page breaks, visible checkbox squares)
- Pass/Fail buttons in summary section
- Self-contained single file (no external dependencies beyond Google Fonts)

---

## Pre-Launch Report Template

```markdown
## Pre-Launch Report: [PROJECT_NAME] vX.X

**Date**: YYYY-MM-DD  
**Prepared by**: [Agent]

### Security Review
- [ ] No secrets in code
- [ ] Access control configured
- [ ] Data protection verified

### Code Quality
- [ ] No forbidden patterns
- [ ] Error handling complete
- [ ] UI compliance verified

### Version Control
- [ ] Git clean and synced
- [ ] Version documented

### Deployment
- [ ] GAS deployment verified
- [ ] Production URL tested

### Performance
- [ ] Load times acceptable
- [ ] GAS limits checked

### Rollback
- [ ] Previous version: vX.X
- [ ] Rollback command documented

### Documentation
- [ ] Technical docs current
- [ ] User docs created (if applicable)
- [ ] Module testing guide created (if major module — see 7.3)

---

### Status: ✅ READY FOR PRODUCTION / ❌ NOT READY

**Blocking Issues** (if any):
1. [Issue and remediation needed]

**Notes**:
[Any special considerations for this deployment]
```

---

## Quick Reference

### Deployment Commands

```bash
# Pre-flight
cd /Users/joshd.millang/Projects/[PROJECT_NAME]
git status && git remote -v

# Deploy sequence
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X - description"
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [VERSION] -d "vX.X"

# Git sync
git add -A && git commit -m "vX.X - description" && git push
```

### Rollback Command

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [DEPLOY_ID] -V [PREVIOUS_VERSION] -d "Rollback to vX.X"
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 25, 2026 | Initial pre-launch checklist |
| v1.1 | Feb 13, 2026 | Added Phase 7.3: Module Testing Guide requirement (mandatory for major modules) |

---

*Ship with confidence. This checklist ensures every production deployment is secure, stable, and reversible.*
