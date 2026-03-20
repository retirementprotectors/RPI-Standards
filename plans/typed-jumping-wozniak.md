# Plan Audit — ProZONE UI/UX Overhaul

## Verdict: 2 MISMATCHES + 1 AMBIGUITY — patches needed

### MISMATCHES

**1. TRK-13533 Permission Gate (TEAM tab)**
- Ticket: "Permission gate: Owner/Executive edit, Leader+ view"
- Discovery: Same requirement
- Plan: "Add a comment noting Owner/Executive edit gate is a future enhancement"
- **Fix:** Builder 2 must implement the gate, not defer it. SpecialistConfigEditor needs `disabled` props based on user level.

**2. TRK-13535 API Pagination (TARGET tab)**
- Ticket: "MUST INCLUDE: Pagination — add offset/limit params to GET /api/prozone/prospects endpoint"
- Plan: "Client-side for now. API pagination = future item"
- **Fix:** Add `offset` + `limit` query params to prozone.ts prospects endpoint. Builder 4 or Phase 1 scope.

### AMBIGUITIES

**1. Scorecard Team/Pipeline Selector UX**
- Discovery: "mutually exclusive filter dimensions — radio-style toggle"
- Plan: Lists as state union type, implies dropdown
- **Fix:** Specify segmented button group (radio-style). Two rows: Row 1 = COR/AST/SPC/ALL, Row 2 = Retirement/Medicare/Legacy/ALL. One active at a time.

### All Other Checks: PASS
- 15/15 tickets have plan coverage
- All discovery requirements mapped
- No scope creep
- Builder instructions have file paths + patterns
- Dependencies correctly sequenced
