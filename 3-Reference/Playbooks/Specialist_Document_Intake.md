# Specialist Document Intake Workflow
## From Client Meeting to Case Pipeline

> **Version**: v1.0  
> **Created**: February 3, 2026  
> **Status**: Active  
> **Owner**: RAPID (Shared Services)

---

## Overview

This document describes how Retirement Specialists get client documents from meetings into the RPI case processing pipeline.

**Key Principle:** Specialists focus on client relationships. The system handles everything else.

---

## The Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SPECIALIST MEETING WORKFLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. MEETING                    2. DOCUMENTS                                │
│  ─────────                     ──────────                                  │
│                                                                             │
│  Google Meet                   During/after meeting:                       │
│  (Recording on)                - Photos of statements                      │
│       │                        - PDFs from client email                    │
│       │                        - Scanned documents                         │
│       │                              │                                     │
│       ▼                              ▼                                     │
│  ┌─────────────────┐          ┌─────────────────────┐                     │
│  │ Command Center  │          │ _INTAKE Folder      │                     │
│  │ (Auto-process)  │          │ (Drop & go)         │                     │
│  └────────┬────────┘          └──────────┬──────────┘                     │
│           │                              │                                 │
│           │   Case Detection             │   Document Queue                │
│           │                              │                                 │
│           └──────────────┬───────────────┘                                │
│                          │                                                 │
│                          ▼                                                 │
│              ┌───────────────────────┐                                    │
│              │ RAPID_IMPORT          │                                    │
│              │ - AI Extraction       │                                    │
│              │ - Validation          │                                    │
│              │ - Deduplication       │                                    │
│              │ - ACF Creation        │                                    │
│              └───────────┬───────────┘                                    │
│                          │                                                 │
│                          ▼                                                 │
│              ┌───────────────────────┐                                    │
│              │ ProDash Pipeline      │                                    │
│              │ (Case assigned)       │                                    │
│              └───────────────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## For Specialists: How to Use

### Step 1: Record Your Meeting

1. Use **Google Meet** for all client meetings (virtual or in-person screen share)
2. Turn on recording
3. The transcript auto-processes through Command Center

### Step 2: Drop Documents

During or after the meeting:

1. Open Google Drive (mobile or desktop)
2. Navigate to: `_INTAKE / [Your Name] /`
3. Drop files (drag & drop, upload, or share-to-Drive)
4. Done!

### File Naming (Recommended)

Format: `ClientName_DocType_Date.pdf`

Examples:
- `DoeJohn_EdwardJones_2026-01.pdf`
- `SmithJane_Fidelity401k_2026-01.pdf`
- `JohnsonBob_SocialSecurity_2026-01.pdf`

**Not required** - the system can parse any name, but consistent naming helps.

### What Happens Automatically

1. **File detected** in your _INTAKE folder
2. **Queued** for processing (every 5 minutes)
3. **AI extracts** client info, account data, values
4. **Matched** to existing client or new record created
5. **ACF folder** created/linked automatically
6. **Case created** in ProDash pipeline
7. **Documents moved** from _INTAKE to proper ACF location
8. **You're notified** when ready for review

---

## Folder Structure

```
/RPI/
├── _INTAKE/                          ← Drop zone root
│   ├── Alex Haase/                   ← Your personal drop folder
│   │   └── [drop files here]
│   ├── Christa Irwin/
│   ├── Lucas Dexter/
│   ├── Shane Parmenter/
│   └── Vincent Vazquez/
│
├── ACF/                              ← Active Client Files (auto-managed)
│   └── [Client folders created automatically]
│
└── LC3/                              ← Agent folders (your workspace)
```

---

## Meeting-to-Case Detection

When a Google Meet recording is processed, the system looks for:

| Indicator | Weight | Example |
|-----------|--------|---------|
| Meeting type | 30% | "Discovery Call", "Retirement Review" |
| Financial keywords | 30% | "401k", "IRA", "pension", "social security" |
| Client name mentioned | 25% | "Speaking with John Doe today" |
| Financial data discussed | 15% | Dollar amounts, account types |

**If confidence ≥ 50%**: Case auto-created in pending status, awaiting documents.

---

## Supported File Types

| Type | Extensions | Processing |
|------|------------|------------|
| **PDF** | .pdf | AI extraction (PyMuPDF → images → OCR) |
| **Images** | .jpg, .png, .gif | Direct AI vision processing |
| **Scans** | .pdf, .tiff | Converted to images, then processed |

---

## Case Status Flow

```
PENDING_DOCUMENTS → PENDING_EXTRACTION → READY_FOR_REVIEW → ASSIGNED → IN_PROGRESS → COMPLETED
```

| Status | Meaning |
|--------|---------|
| `PENDING_DOCUMENTS` | Meeting detected, awaiting document drop |
| `PENDING_EXTRACTION` | Documents received, AI processing |
| `READY_FOR_REVIEW` | Data extracted, needs specialist review |
| `ASSIGNED` | Assigned to service/sales queue |
| `IN_PROGRESS` | Being worked by assigned team |
| `COMPLETED` | Case closed |

---

## Queue Routing

Based on detected financial topics:

| Topics Detected | Queue |
|-----------------|-------|
| Medicare, Part D, Medigap | `MDJ-SERVICE-MEDICARE` |
| 401k, IRA, Pension, Annuity, Life | `MDJ-SERVICE-RETIREMENT` |
| General/Mixed | `PRODASH-SALES-PIPELINE` |

---

## Troubleshooting

### "My file isn't processing"

1. Check you dropped it in YOUR folder under `_INTAKE`
2. Queue processes every 5 minutes - wait a few minutes
3. Check the intake queue in Command Center for status

### "Case wasn't auto-created from meeting"

1. Ensure Google Meet recording was on
2. Meeting may not have triggered confidence threshold
3. Manually create case if needed, link documents

### "Wrong client matched"

1. Flag in the case for manual review
2. System will learn from corrections over time

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| Case_Processing_Workflow.md | Full case processing details |
| MCP_TOOLS_SETUP.md | MCP configuration |
| THREE_PLATFORM_ARCHITECTURE.md | Platform routing |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 3, 2026 | Initial workflow - _INTAKE folders + meeting detection |

---

*Questions? Reach out in #rapid-support on Slack.*
