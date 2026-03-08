---
name: quality-gate-phase-complete
enabled: true
event: prompt
action: block
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (phase\s+complete|sub-?phase\s+(done|complete)|ready\s+for\s+review|checkpoint\s+(reached|done|complete)|all\s+tasks\s+(done|complete)|deployed\s+and\s+verified)
---

**BLOCKED: Cannot report phase complete without evidence**

Before reporting a phase/sub-phase as complete, you MUST:

1. **Read the plan file** (`.claude/plans/*.md`)
2. **For EVERY task in the current sub-phase:**
   - Update status to done or not done with evidence
   - If done: include the audit evidence (grep result, line number, screenshot)
   - If not done: explain what's still needed
3. **Run the Audit Method** for each task (from the plan's Audit Method column)
4. **Update the plan file** with results BEFORE reporting
5. Only report complete when ALL tasks show evidence

The Phase 6 portal overhaul had a 21% success rate because the executor self-reported without evidence. This gate prevents that from happening again.

**After updating the plan file, report to JDM with:**
- Summary of what was done
- Any tasks that failed with reasons
- Link to updated plan file
