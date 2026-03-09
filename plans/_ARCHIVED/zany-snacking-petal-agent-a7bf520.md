# Plan: Read All 8 RPI Playbook & Onboarding Documents

## Status: BLOCKED - Need File IDs

### Problem
The `mcp__gdrive__search` tool returns file **names and MIME types** but NOT **file IDs**. The `mcp__gdrive__getGoogleDocContent` tool requires a `documentId` parameter. Without IDs, I cannot read any of the documents.

### Documents Found (confirmed they exist in Drive)
| # | Document Name | Type | ID Status |
|---|--------------|------|-----------|
| 1 | RPI Sales Team- Playbook | Google Doc | MISSING |
| 2 | RPI Support Team- Playbook | Google Doc | MISSING |
| 3 | RPI Service Team- Playbook | Google Doc | MISSING |
| 4 | DAVID (RPI B2B)- Playbook | Google Doc | MISSING |
| 5 | RPI Data Team- Playbook | Google Doc | MISSING |
| 6 | RPI- Leadership Team Playbook | Google Doc | MISSING |
| 7 | TEAM_ONBOARDING.docx | Word doc (uploaded) | MISSING |
| 8 | Org. Onboarding (internal).docx | Word doc (uploaded) | MISSING |

### Solution Options (Pick One)

#### Option A: JDM Provides File IDs (Fastest - 2 min)
JDM opens each Google Doc and copies the document ID from the URL:
`https://docs.google.com/document/d/THIS_IS_THE_ID/edit`

Once I have IDs, I read all 6 Google Docs in parallel using `getGoogleDocContent`.

For the 2 Word docs (#7, #8): These are .docx files uploaded to Drive. They may have been auto-converted to Google Docs format (in which case `getGoogleDocContent` works), or they're still .docx (in which case I'd need a different approach -- possibly download and parse, or JDM could open them and they auto-convert).

#### Option B: Use execute_script to Search Drive (5 min)
Write and run a GAS function on RAPID_API that uses `DriveApp.searchFiles()` to find files by name and return their IDs. Something like:

```javascript
function findPlaybookIds() {
  var names = [
    'RPI Sales Team- Playbook',
    'RPI Support Team- Playbook',
    'RPI Service Team- Playbook',
    'DAVID (RPI B2B)- Playbook',
    'RPI Data Team- Playbook',
    'RPI- Leadership Team Playbook',
    'TEAM_ONBOARDING',
    'Org. Onboarding (internal)'
  ];
  var results = {};
  names.forEach(function(name) {
    var files = DriveApp.getFilesByName(name);
    var found = [];
    while (files.hasNext()) {
      var f = files.next();
      found.push({ id: f.getId(), name: f.getName(), type: f.getMimeType() });
    }
    results[name] = found;
  });
  return results;
}
```

**Problem:** This requires a function to already exist in RAPID_API, or I need to push code first (which I can't do in plan mode). Also, RAPID_API may not have DriveApp permissions in its scope.

#### Option C: Browse Folders with listFolder (10-15 min)
Use `mcp__gdrive__listFolder` to navigate the Drive folder tree until I find the playbooks. This is slow but might work if I know the folder structure. The playbooks might be in a "Playbooks" or "Team" folder.

### Recommended Approach
**Option A** -- Ask JDM to provide the 8 file IDs (or URLs). This is the fastest path by far.

If JDM doesn't want to manually grab IDs, **Option B** is next best -- I'd need to exit plan mode to push a temporary GAS function.

### Execution Plan (Once IDs Are Available)

#### Step 1: Read All 6 Google Docs in Parallel
- Call `mcp__gdrive__getGoogleDocContent` for each of the 6 playbook docs simultaneously
- This tool returns full document content with text indices

#### Step 2: Handle the 2 Word Docs
- For TEAM_ONBOARDING.docx and Org. Onboarding (internal).docx:
  - If they've been converted to Google Docs, read with `getGoogleDocContent`
  - If still .docx format, try reading via the gdrive MCP or use execute_script to extract text

#### Step 3: Analyze and Report
For each document, report:
- Full structure (all headings, sections, subsections)
- Content/data in each section
- Tables, checklists, structured data
- Template pattern (reusable vs. person-specific)

Cross-document analysis:
- How job descriptions are structured across divisions/teams
- Onboarding process patterns in existing docs
- Data fields and metrics tracked
- How to systematize these into a RIIMO module

### What I Need From JDM
**Please provide the Google Doc URLs (or just the document IDs) for these 8 files.** You can get the ID from the URL bar when you have the doc open:

```
https://docs.google.com/document/d/COPY_THIS_PART/edit
```

Just paste the 8 URLs and I'll extract the IDs and read everything in parallel.
