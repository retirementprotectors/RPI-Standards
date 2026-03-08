---
name: quality-gate-plan-format
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.claude/plans/.*\.md$
  - field: content
    operator: not_contains
    pattern: Acceptance Criteria
  - field: content
    operator: not_contains
    pattern: Audit Method
---

**BLOCKED: Plan file missing required pipeline columns**

Plan files in `.claude/plans/` must contain ALL of the following:

1. **Acceptance Criteria** column or section — what "done" looks like for each task
2. **Audit Method** column or section — exact verification steps (grep patterns, line counts, Playwright checks)
3. **CHECKPOINT** markers between sub-phases — JDM reviews before next phase begins
4. Sub-phase labels with bounded scope (e.g., "1A:", "1B:")

**Kill means DELETE the code entirely.** Not merge, not hide, not stub, not rename, not comment out. If a task says "kill X", the acceptance criteria must verify ZERO references remain.

Every task must answer:
- What does DONE look like? (Acceptance Criteria)
- How does the AUDITOR verify it? (Audit Method — grep pattern, line number, screenshot)

Without these, the Phase IV Auditor cannot verify work and the pipeline fails.
