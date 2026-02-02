# Google Apps Script Common Issues & Solutions

> **Version**: v1.0  
> **Created**: February 1, 2026  
> **Source**: DEX production deployment session  
> **Purpose**: Document common issues and their fixes for GAS projects

---

## 1. Data Disappears Between Server and Client

### The Problem

You call a server function with `google.script.run`, the server returns data correctly (visible in Logger), but the client-side receives `undefined` or an empty object.

### The Cause

Apps Script's internal serialization doesn't always handle complex objects correctly when passing from server-side GAS to client-side JavaScript.

### The Fix

Always wrap your return value with explicit JSON serialization:

```javascript
// ❌ BROKEN - Data may disappear
function getDataForUI() {
  const result = MyModule.getData();
  return result;
}

// ✅ FIXED - Force clean serialization
function getDataForUI() {
  const result = MyModule.getData();
  return JSON.parse(JSON.stringify(result));
}
```

**Apply this pattern to ALL `*ForUI()` wrapper functions.**

---

## 2. External Services Can't Access Private Drive Files

### The Problem

Your external service (PDF filler, image processor, etc.) returns blank results or "file not found" when you send it a Google Drive file URL.

### The Cause

Google Drive URLs like `https://drive.google.com/file/d/xxx/view` require authentication. External services can't access them even if "anyone with link" sharing is on (due to download restrictions).

### The Fix

Fetch the file server-side using Apps Script (which HAS auth) and send as base64:

```javascript
// ❌ BROKEN - External service can't access
const pdfUrl = 'https://drive.google.com/file/d/xxx/view';
sendToExternalService({ url: pdfUrl });

// ✅ FIXED - Fetch file with Apps Script auth, send base64
function getPdfAsBase64(driveUrl) {
  const fileId = extractFileId(driveUrl);
  const file = DriveApp.getFileById(fileId);
  const blob = file.getBlob();
  return Utilities.base64Encode(blob.getBytes());
}

const pdfBase64 = getPdfAsBase64(driveUrl);
sendToExternalService({ base64: pdfBase64 });
```

---

## 3. 413 Request Entity Too Large

### The Problem

When sending multiple files or large data to an external service, you get a `413` error.

### The Cause

Serverless functions (Cloud Functions, AWS Lambda, etc.) have payload limits, typically 6-10MB. Multiple PDFs easily exceed this.

### The Fix

Implement batch processing - send files one at a time, merge results client-side:

```javascript
// ❌ BROKEN - All files at once
function fillAllPdfs(forms) {
  return externalService.fill({ forms: forms }); // Payload too large
}

// ✅ FIXED - Batch processing
function fillAllPdfs(forms) {
  // Calculate payload size
  let totalSize = 0;
  forms.forEach(f => {
    if (f.pdfBase64) totalSize += f.pdfBase64.length;
  });
  
  // If over 3MB, process in batches
  if (totalSize > 3 * 1024 * 1024) {
    const results = [];
    for (const form of forms) {
      const result = externalService.fill({ forms: [form] });
      results.push(result);
    }
    return mergeResults(results);
  }
  
  // Under limit, send all at once
  return externalService.fill({ forms: forms });
}
```

---

## 4. PDF Fields Not Filling with Data

### The Problem

Your PDF service is working (returns filled PDFs), but fields are blank.

### The Cause

The field names in your `_FIELD_MAPPINGS` sheet don't EXACTLY match the actual PDF form field names. Common issues:
- Extra spaces: `"client_name "` vs `"client_name"`
- Case differences: `"Client_Name"` vs `"client_name"`
- Underscores vs spaces: `"client name"` vs `"client_name"`

### The Fix

1. **Create a debug function to list actual PDF fields:**

```javascript
function DEBUG_ListPdfFields(formId) {
  const form = DEX_FormLibrary.getForm(formId);
  const result = PdfService.analyze({ pdfUrl: form.gdrive_link });
  
  Logger.log('=== Actual PDF Fields ===');
  result.fields.forEach(f => Logger.log(f.name));
  
  return result.fields;
}
```

2. **Compare with your mappings:**

```javascript
function DEBUG_CompareFieldNames(formId) {
  const actualFields = getPdfFields(formId);
  const mappings = getMappingsForForm(formId);
  
  actualFields.forEach(actual => {
    const mapping = mappings.find(m => m.field_name === actual.name);
    if (!mapping) {
      Logger.log('MISSING MAPPING: ' + actual.name);
    }
  });
}
```

3. **Create a fix function to auto-correct mappings:**

```javascript
function SETUP_FixFieldMappings(formId) {
  const actualFields = getPdfFields(formId);
  const mappings = getMappingsForForm(formId);
  
  actualFields.forEach(actual => {
    // Find fuzzy match in existing mappings
    const fuzzyMatch = findFuzzyMatch(actual.name, mappings);
    if (fuzzyMatch && fuzzyMatch.field_name !== actual.name) {
      // Update to use actual name
      updateMapping(fuzzyMatch.id, { field_name: actual.name });
      Logger.log('Fixed: ' + fuzzyMatch.field_name + ' → ' + actual.name);
    }
  });
}
```

---

## 5. Modal Content Pushes Buttons Out of View

### The Problem

When modal content is long (many form fields), the Next/Back buttons scroll out of view.

### The Cause

The entire modal has `overflow-y: auto`, so both content AND footer scroll.

### The Fix

Use flexbox to make only the body scroll while header/footer stay fixed:

```css
/* ✅ CORRECT - Fixed header/footer, scrollable body */
.modal-content {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden; /* Prevent modal itself from scrolling */
}

.modal-header,
.modal-footer {
  flex-shrink: 0; /* Never shrink */
}

.modal-body {
  flex: 1;
  overflow-y: auto; /* Only body scrolls */
  min-height: 0; /* Required for flex scroll to work */
}
```

---

## 6. Storing Complex State Without Schema Changes

### The Problem

You need to store complex wizard state (prepared kit, user input, etc.) but don't want to add columns to the spreadsheet schema.

### The Solution

Use an existing text field (like `notes`) to store JSON:

```javascript
// Save draft with state
function saveDraft(packageId, wizardState) {
  const notes = JSON.stringify({
    _isDraftState: true, // Marker to identify JSON state
    wizardStep: wizardState.step,
    preparedKit: wizardState.kit,
    userInput: wizardState.input
  });
  
  sheet.getRange(row, NOTES_COL).setValue(notes);
}

// Load draft with state
function loadDraft(row) {
  const pkg = rowToPackage(row);
  
  // Try to parse notes as state
  if (pkg.notes && pkg.status === 'DRAFT') {
    try {
      const parsed = JSON.parse(pkg.notes);
      if (parsed._isDraftState) {
        pkg.draftState = parsed;
        pkg.notes = ''; // Clear since it was storage
      }
    } catch (e) {
      // Not JSON, leave notes as-is
    }
  }
  
  return pkg;
}
```

---

## Quick Reference Table

| Issue | Symptom | Fix |
|-------|---------|-----|
| Data disappears server→client | Client gets undefined | `JSON.parse(JSON.stringify(result))` |
| External service can't access files | Blank/missing files | Use base64 instead of URLs |
| 413 Payload Too Large | Server error on large sends | Batch processing |
| PDF fields not filling | Blank PDFs | Verify field names match exactly |
| Modal buttons scroll away | Can't see Next/Back | Flexbox with scrollable body only |
| Need to store complex state | Schema changes required | JSON in text field |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 1, 2026 | Initial release from DEX production session |
