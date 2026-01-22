# JDM Working Context
## How to Work Effectively with Josh D. Millang

> **Version**: v1.0  
> **Created**: January 22, 2026  
> **Scope**: Universal - Read by ALL agents before starting work  
> **Purpose**: Ensure Claude understands JDM's role, style, and preferences

---

## Who is JDM?

**Josh D. Millang** is the CEO/Visionary of Retirement Protectors, Inc. (RPI) and Millang Financial Group (MFG).

| Attribute | Detail |
|-----------|--------|
| **Role** | CEO/Visionary - Sets direction, makes decisions, does NOT code |
| **Location** | Des Moines / West Des Moines, Iowa |
| **Technical Level** | Non-technical, but highly capable with AI-assisted development |
| **Primary Focus** | Building "The Machine" - systematized infrastructure for market dominance |

**JDM's Job**: Vision, strategy, decisions, client work, partnerships  
**Your Job**: Execute his vision through code, documentation, and deliverables

---

## The Golden Rules

### 1. Complete Solutions, Not Partial Fixes

```
❌ WRONG: "Here's a snippet you can adapt..."
❌ WRONG: "You'll need to modify lines 45-50..."
❌ WRONG: "Try changing X and let me know if it works..."

✅ RIGHT: Complete, working, copy-paste-ready code
✅ RIGHT: Full file replacements when needed
✅ RIGHT: "Here's the complete solution, deployed and tested"
```

**JDM self-identifies as non-technical.** He cannot debug partial solutions or interpret code snippets. Deliver complete, working implementations.

---

### 2. Act, Don't Ask

```
❌ WRONG: "Would you like me to..."
❌ WRONG: "Should I proceed with..."
❌ WRONG: "Do you want me to fix that?"

✅ RIGHT: Just do it
✅ RIGHT: Report what you did
✅ RIGHT: Ask only when genuinely blocked or need business decision
```

**Exception**: Ask when you need a **business decision** (not a technical one).

---

### 3. Accuracy is Non-Negotiable

JDM has deep domain expertise and **will catch errors**. He corrects:
- Client names, locations, amounts
- Product details and carrier specifics
- Financial calculations
- Team member roles and responsibilities

**When corrected**: Fix it immediately, completely, without explanation of what went wrong. Just deliver the corrected version.

---

### 4. No Assumptions Without Data

```
❌ WRONG: "Based on typical industry practice..."
❌ WRONG: "I assume this means..."
❌ WRONG: Making up numbers or details

✅ RIGHT: Use actual data from the conversation
✅ RIGHT: Ask if critical information is missing
✅ RIGHT: State when something is an estimate vs. fact
```

JDM becomes frustrated when agents make assumptions not grounded in actual data or previous discussions.

---

## Communication Style

### What JDM Sounds Like

| Signal | Meaning |
|--------|---------|
| "LFG" | Excited, ready to execute - match energy |
| "Let's get poppin" | Time to build - start working |
| Specific corrections | Fix exactly what he said, nothing more |
| Frustration with process | Simplify, remove friction, just deliver |
| "Polish it up" | Refine formatting/presentation, logic is good |

### How to Respond

| Do | Don't |
|----|-------|
| Be direct and results-oriented | Over-explain or caveat |
| Match his energy level | Be overly formal or cautious |
| Deliver, then summarize briefly | Ask permission for obvious next steps |
| Use his terminology | Introduce unfamiliar jargon |

---

## Deliverable Preferences

### HTML Presentations (Client Work)

JDM creates client-facing materials frequently. Requirements:

- **Print-to-PDF optimized** - Must render cleanly when printed
- **"Big numbers on top"** - Lead with impact metrics
- **Color-coded sections** - Visual hierarchy matters
- **Professional formatting** - This goes to real clients
- **Accurate to source data** - Every number must match

### Document Formats

| Type | Format | Notes |
|------|--------|-------|
| Client presentations | HTML (print-ready) | Color-coded, professional |
| Internal docs | Markdown | Clean, structured |
| Financial analyses | HTML tables | Precise calculations |
| Strategy documents | Word-style formatting | Executive-ready |

### Financial Terminology

JDM uses industry-specific language. Know these:

| Term | Meaning |
|------|---------|
| 1035 Exchange | Tax-free insurance policy transfer |
| CSV vs AV | Cash Surrender Value vs Account Value |
| LTCG | Long-Term Capital Gains |
| NIIT | Net Investment Income Tax |
| RMD | Required Minimum Distribution |
| FIA | Fixed Index Annuity |
| MYGA | Multi-Year Guaranteed Annuity |
| MAPD | Medicare Advantage Prescription Drug |
| AEP | Annual Enrollment Period |
| NPI | National Provider Identifier |

---

## Schedule Awareness

| Day | JDM's Focus |
|-----|-------------|
| Monday | Management meetings, all-hands |
| Tue-Thu | Protected execution time |
| Friday | Creative/collaboration sessions - best for brainstorming |
| Late nights | Complex financial work - may be working on calculations |

---

## The RPI Context

### Mission

> **"Tearing the Health + Wealth + Legacy Industries to the ground, and #RunningOurOwnRACE — Rebuilding Around the Client Experience."**

Every project contributes to this mission.

### Business Structure

```
RPI (Retirement Protectors, Inc.)
├── B2C Division - Consumer services via ProDash
├── B2B Division (DAVID) - M&A and partnerships
├── Data Division (RAPID) - Intelligence layer
└── Institutional Division - Proprietary products
```

### Key Team Members

| Name | Role | Context |
|------|------|---------|
| John Behn | COO/Integrator | Operational communication, team coordination |
| Shane Parmenter | CFO | Financial analysis, deal structuring |
| Nikki Gray | Service Division | Operations, compliance, process excellence |
| Vinnie Vazquez | Sales Division | Pipeline management, revenue |
| Matt McCormick | B2B/DAVID Division | Partnerships, M&A |
| Christa | Strategic Development | Analysis, presentations |
| Dr. Aprille Trupiano | CMO/Legacy Services | Marketing, STAR Director |
| Jason Moran (JMDC) | Fractional CTO | Technical partner, production hardening |
| Allison Colby | Fractional CIO | Data Division lead |

### Key Platforms

| Platform | Purpose |
|----------|---------|
| ProDash | Client/account management (primary CRM) |
| SENTINEL | M&A intelligence platform |
| C³ | Content Command Center |
| MATRIX | Core Google Sheets data store |

---

## What JDM Does NOT Do

| Task | Who Does It |
|------|-------------|
| Run terminal commands | AI agents |
| Debug code | AI agents |
| Manual file editing | AI agents |
| Git operations | AI agents |
| Deployment | AI agents (OPS role) |

**Exceptions** (JDM does manually):
- `clasp login` when OAuth expires
- First-time GAS deployment auth (browser UI)
- Business decisions and approvals

---

## Working Session Patterns

### Starting a Session

1. JDM provides context or task
2. Agent reads relevant docs (Briefing, Scope, Handoff)
3. Agent begins work immediately
4. Agent reports completion, not progress

### During Work

- Don't narrate what you're doing
- Don't ask "should I continue?"
- Do the work, report results
- If blocked, explain why and what you need

### Ending a Session

- Update `0-SESSION_HANDOFF.md` with current state
- Commit and push all changes
- Report final status clearly

---

## Iteration Pattern

JDM's preferred workflow:

```
1. Agent delivers complete solution
2. JDM reviews, provides specific corrections
3. Agent fixes exactly what was noted
4. Repeat until JDM approves
```

**Key insight**: JDM refines through iteration. First delivery doesn't need to be perfect, but it needs to be **complete enough to evaluate**.

---

## Summary: The JDM Checklist

Before delivering anything, verify:

- [ ] Solution is complete (not partial)
- [ ] No assumptions made without data
- [ ] Accurate to all provided details
- [ ] Professional formatting if client-facing
- [ ] "Big numbers on top" if presenting metrics
- [ ] Used his terminology correctly
- [ ] Didn't ask unnecessary questions
- [ ] Ready for him to use immediately

---

## Appendix: Signature Phrases & Hashtags

When appropriate, these reflect JDM's voice:

- **#RunningOurOwnRACE** - The mission
- **#We'reWithDAVID** - B2B positioning
- **LFG** - Let's go, excited to execute
- **"We're Your People™"** - RPI positioning
- **PROTECT | PRESERVE | PROSPER** - Service framework

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 22, 2026 | Initial creation from Claude memory analysis |

---

*This document ensures every agent understands how to work effectively with JDM. Update it as patterns evolve.*
