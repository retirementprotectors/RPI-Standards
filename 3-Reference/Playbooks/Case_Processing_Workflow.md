# Client Case Processing Workflow
## From Source Documents to ProDash Pipeline

> **Version**: v1.0  
> **Created**: February 3, 2026  
> **Status**: Active - Reference Workflow  
> **Owner**: RAPID (Shared Services)  
> **Destination**: ProDash Sales Pipeline (when built)

---

## Overview

This workflow documents how to process new client cases from source documents (PDFs, images, Slack messages) into structured data, deliverables, and eventually ProDash pipeline entries.

**Current State**: Manual workflow with AI assistance  
**Future State**: Automated intake feeding into ProDash Sales Pipeline

---

## Workflow Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CASE PROCESSING WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. INTAKE          2. EXTRACTION       3. ANALYSIS        4. OUTPUT        │
│  ─────────          ────────────        ──────────         ─────────        │
│                                                                              │
│  Source Docs        PDF → Images        Populate Ai3       ACF Folder       │
│  Slack DMs          OCR via Read        Calculate RMDs     Executive Sum    │
│  Email Fwds         Parse Statements    Flag Issues        MATRIX Records   │
│                                                                              │
│                                                                              │
│                     ↓                   ↓                  ↓                │
│                                                                              │
│  5. DELEGATION (Future)                                                      │
│  ────────────────────────                                                   │
│                                                                              │
│  Create Case in ProDash Pipeline → Assign to Unit Owner → Track to Close   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Intake

### Sources
- **PDFs**: Financial statements, carrier statements, tax documents
- **Images**: Slack DMs, screenshots, photos of documents
- **Email forwards**: Client correspondence with attachments

### Location
Store source documents in:
```
RPI-Command-Center/Docs/[Client Name]/
```

---

## Stage 2: Extraction

### PDF Processing

**For image-based PDFs** (scanned, no selectable text):

```python
# Using PyMuPDF to convert PDF pages to images
import fitz  # PyMuPDF

pdf_path = "/path/to/statement.pdf"
doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for quality
    pix = page.get_pixmap(matrix=mat)
    pix.save(f"/tmp/page_{page_num+1:02d}.png")
```

**For text-based PDFs**: Extract directly with `fitz.open().get_text()`.

### Image OCR

Use Claude's vision capability via the `Read` tool to extract text from images.

### Data Points to Extract

| Category | Fields |
|----------|--------|
| **Client Info** | Name, DOB, SSN (last 4), address, phone, email |
| **Accounts** | Account numbers, types, carriers, values, dates |
| **Income** | Social Security, pensions, annuity income |
| **Assets** | Real estate, other investments |

---

## Stage 3: Analysis

### Ai3 Template Population

Copy the Ai3 Template for each new household:
- **Template ID**: `1R6a4Bv9BrtkedRmC8u2KDcvfy6ZzVNJGejaSeFfF5Bg`

Populate sections:
1. **Client Information** (rows 7-17) - Demographics
2. **Income Sources** (rows 71-80) - SS, pensions, annuities
3. **Assets** (rows 58-66) - Real estate, investments
4. **Expenses** (rows 82-90) - Monthly obligations

### Calculations & Flags

- RMD calculations for clients 73+
- Beneficiary gaps
- Account concentration risk
- Upcoming policy anniversaries

---

## Stage 4: Output Deliverables

### Active Client File (ACF) Structure

Create in Google Drive:
```
[LastName], [FirstName] & [Spouse] ([client_id prefix])/
├── 1. Discovery & Intake/
├── 2. Statements & Documents/        ← Source PDFs go here
├── 3. Analysis & Planning/           ← Ai3 link, Executive Summary
├── 4. Proposals & Presentations/
└── 5. Paperwork & Compliance/
```

### Executive Summary

Generate a comprehensive markdown/Google Doc containing:
- Client profile (demographics, contact)
- Financial snapshot (total assets by type)
- Account inventory (all accounts with key details)
- Income/expense summary
- Critical observations (flags, deadlines)
- Delegation assignments (who owns what)

### MATRIX Updates

Update PRODASH_MATRIX:
- **_CLIENT_MASTER**: Add/update client records
- **_ACCOUNT_BDRIA**: Investment accounts
- **_ACCOUNT_ANNUITY**: Annuity accounts
- **_ACCOUNT_LIFE**: Life policies
- **_ACCOUNT_MEDICARE**: Medicare plans

Link client record to ACF via `gdrive_folder_url` field.

---

## Stage 5: Delegation (Future - ProDash Pipeline)

When ProDash Sales Pipeline is built, this workflow will automatically:

1. Create a Case record in the pipeline
2. Assign to appropriate Unit Owner based on product mix:
   - Medicare-heavy → MDJ-Service-Medicare queue
   - Retirement-heavy → MDJ-Service-Retirement queue
   - New prospect → Sales Pipeline
3. Attach ACF folder and Ai3 to the case
4. Track through pipeline stages to close

---

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `gdrive` | Create folders, search, create docs |
| `document-processor` | Upload PDFs to Drive |
| `getGoogleSheetContent` | Read Ai3 template, MATRIX data |
| `updateGoogleSheet` | Write to Ai3, MATRIX |

---

## Example: Demetry Case (Feb 2026)

**Input**:
- 5 PDF statements (Edward Jones x4, Corebridge x1)
- Slack DM with initial client info

**Processing**:
1. Converted 52 PDF pages to images
2. Extracted client data (Sara + Arthur), 5 accounts
3. Populated Ai3 with household data
4. Created ACF folder structure in Drive
5. Generated Executive Summary
6. Added to PRODASH_MATRIX (_CLIENT_MASTER, _ACCOUNT_BDRIA)
7. Uploaded source PDFs to ACF

**Output**:
- Ai3 Sheet: `1bKYo-Zkm725lazCnLbwEOkK-i100yGy9_yBcMJwG49M`
- ACF Folder: `1JV53YRstEao6ARV3JAaQM_31_6pWOOOi`
- Client IDs: `878bbf57...`, `a77b5ee8...`

---

## Related Documents

| Document | Location |
|----------|----------|
| Three-Platform Architecture | `_RPI_STANDARDS/0-Setup/THREE_PLATFORM_ARCHITECTURE.md` |
| MATRIX Configuration | `_RPI_STANDARDS/0-Setup/MATRIX_CONFIGURATION_STANDARDS.md` |
| MCP-Hub | `RAPID_TOOLS/MCP-Hub/` |
| Document Processor MCP | `RAPID_TOOLS/MCP-Hub/document-processor/` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 3, 2026 | Initial workflow documented from Demetry case |

---

*This workflow feeds into ProDash once the Sales Pipeline module is built.*
