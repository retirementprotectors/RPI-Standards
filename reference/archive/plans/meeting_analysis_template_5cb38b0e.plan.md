---
name: Meeting Analysis Template
overview: Create a standardized Claude.ai meeting analysis output template that synthesizes the proposed format with patterns from existing Executive Team Roadmap documents, designed for team adoption and MCP layer integration.
todos:
  - id: review-template
    content: Review finalized template against team workflow needs
    status: completed
  - id: create-project-prompt
    content: Build Claude.ai Project prompt that enforces this template
    status: completed
  - id: test-with-transcript
    content: Test template with actual meeting transcript
    status: completed
  - id: document-in-drive
    content: Save final template to Executive Team Shared Drive
    status: completed
---

# Claude.ai Meeting Analysis Output Template

## Analysis Complete

After reviewing all 9 documents in `Executive Team Roadmaps/`, I've identified the consistent structural patterns your existing meeting artifacts use. The finalized template below merges my proposed structure with your proven patterns.

---

## Key Patterns Identified from Existing Documents

**Header Structure:**

- ALL CAPS name
- Role/Title + Purpose line
- Date reference

**Core Sections (in order):**

1. Executive Summary (2-3 sentences + KEY INSIGHT quote box)
2. Strategic Position / Role Definition tables
3. IS vs IS NOT comparison (when defining scope)
4. Meeting Architecture (cadence tables)
5. Key Initiatives (phased with status indicators)
6. Action Items (timeframe-grouped with Owner/Deadline)
7. Key Quotes (categorized by topic)
8. Strategic Implications (For Josh / For John / For the Team)
9. THE BOTTOM LINE (bold summary paragraph)
10. Footer with document identifier

**Status Indicators Used:**

- `ACTIVE` / `PENDING` / `COMPLETE` / `BY DESIGN`
- `✓` completed, `⟳` updated, `✚` new

---

## Finalized Standard Output Template

```markdown
# [PERSON/TOPIC NAME]
[Role/Context] | Meeting Analysis
[Date of Meeting]

---

## Executive Summary
[2-3 sentence overview of what was discussed and decided]

> **KEY INSIGHT**
> "[Direct quote that captures the core takeaway]"
> — [Speaker], [Date]

---

## Decisions Made
| Decision | Owner | Impact | Notes |
|----------|-------|--------|-------|
| [What was decided] | [Who owns it] | [High/Med/Low] | [Context] |

---

## Action Items

### Immediate (This Week)
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | [Specific task] | [Name] | [Date] | PENDING |

### Near-Term (2-4 Weeks)
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|

### Q1/Ongoing
| # | Action | Owner | Timeline | Status |
|---|--------|-------|----------|--------|

---

## Roadmap/Scope Updates
[What changed from previous understanding? New phases? Timeline shifts?]

### Updated Timeline
| Phase | Focus | Status | Change |
|-------|-------|--------|--------|
| [Phase name] | [Description] | ACTIVE/PENDING | [What shifted] |

---

## IS vs IS NOT
*(Include when clarifying scope or role definition)*

| IS | IS NOT |
|----|--------|
| [What this person/project DOES] | [What it does NOT do] |

---

## Relationship Status
| Person/Entity | Current State | Action Needed |
|---------------|---------------|---------------|
| [Name] | [Green/Yellow/Red] | [Follow-up item] |

---

## Key Quotes

**On [Topic 1]:**
> "[Quote]"

**On [Topic 2]:**
> "[Quote]"

---

## Strategic Implications

**For Josh:**
[How this affects Josh's priorities, what it frees him from, what it requires from him]

**For John:**
[How this affects John's coordination role, accountability relationships]

**For the Team:**
[What the team gains, what changes for them operationally]

---

## Open Questions
- [ ] [Unresolved question requiring follow-up]
- [ ] [Decision deferred to future meeting]

---

## Dev Context Notes
*(For MCP layer / Cursor integration)*
- **Systems Affected:** [ProDash, C3, SENTINEL, etc.]
- **Data Dependencies:** [What data sources are involved]
- **Integration Points:** [APIs, webhooks, automations mentioned]
- **Technical Decisions:** [Stack choices, architecture notes]

---

## THE BOTTOM LINE
[Bold summary paragraph - the "so what" in 2-3 sentences. What's the transformation? What's different now?]

---

*[Document Identifier] | [Date]*
```

---

## Usage Instructions for Team

**When to Use:**

- After any meeting with strategic decisions
- When roadmap or scope changes
- When role/responsibility shifts occur
- When relationships need documentation

**How to Use:**

1. Drop meeting transcript into relevant Claude.ai Project
2. Prompt: "Analyze this meeting using the standard output template"
3. Claude produces structured output
4. Copy to Google Doc in `Executive Team Shared Drive`
5. Key items flow to action tracking systems

**What Claude Needs:**

- The transcript (audio transcription or notes)
- Context on which Project this relates to
- Any specific focus areas to prioritize

---

## MCP Layer Integration

This template is designed so key sections can be programmatically extracted:

- **Action Items** → Task management systems
- **Decisions Made** → Decision log database
- **Dev Context Notes** → Cursor workspace context
- **Timeline Updates** → Roadmap tracking tools

The structured format enables automated parsing while remaining human-readable for team review.