# Google Apps Script Web App Patterns

> **Created**: February 1, 2026  
> **Source**: PRODASH UI/UX development session  
> **Status**: CRITICAL - Follow these patterns for all GAS web apps

---

## 1. Date Serialization (CRITICAL)

### The Problem

When returning data from GAS to the browser via `google.script.run`, JavaScript `Date` objects **CANNOT be serialized**. This causes the **ENTIRE response to become `null`**.

```javascript
// ❌ This will return NULL to the browser
function uiGetData() {
  const sheet = SpreadsheetApp.openById(ID).getSheetByName('Data');
  const data = sheet.getDataRange().getValues();
  // data contains Date objects from date columns
  return { success: true, data: data };  // RETURNS NULL!
}
```

### The Solution

Convert all Date objects to ISO strings before returning:

```javascript
// ✅ CORRECT - Convert Date objects
function uiGetData() {
  const sheet = SpreadsheetApp.openById(ID).getSheetByName('Data');
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  
  const rows = data.slice(1).map(row => {
    const obj = {};
    headers.forEach((h, i) => {
      let val = row[i];
      // Convert Date objects to ISO strings
      if (val instanceof Date) {
        val = val.toISOString();
      }
      obj[h] = val;
    });
    return obj;
  });
  
  return { success: true, data: rows };
}
```

### Safety Net Pattern

For complex nested objects, use JSON roundtrip as a safety net:

```javascript
// ✅ BULLETPROOF - Forces everything to be JSON-serializable
function uiGetComplexData() {
  const response = buildComplexResponse();
  return JSON.parse(JSON.stringify(response));
}
```

---

## 2. Payload Size Limits

### The Problem

When using `UrlFetchApp` to call RAPID_API (or any GAS web app), large payloads hit size limits:

```
Error: Argument too large: value
```

This occurs around 2-3MB of response data (e.g., 3,500+ clients with 100+ fields).

### The Solution: Direct MATRIX Reads

For large datasets, bypass the API and read directly from the spreadsheet:

```javascript
// ❌ FAILS with large datasets
function uiGetClients() {
  const response = UrlFetchApp.fetch(RAPID_API_URL + '/clients');
  return JSON.parse(response.getContentText());
}

// ✅ CORRECT - Direct read, no size limits
const PRODASH_MATRIX_ID = '1byyXMJDpjzgqkhTjJ2GdvTclaGYMDKQ1BQEnz61Eg-w';

function uiGetClients() {
  const ss = SpreadsheetApp.openById(PRODASH_MATRIX_ID);
  const sheet = ss.getSheetByName('_CLIENT_MASTER');
  const data = sheet.getDataRange().getValues();
  // Transform and return...
}
```

### When to Use Each Pattern

| Scenario | Use |
|----------|-----|
| < 500 records | Either API or direct read |
| 500-2000 records | Direct read preferred |
| > 2000 records | Direct read required |
| Cross-project calls | API (accept size limits) |
| Same-project reads | Direct read always |

---

## 3. Module-Level Caching

### Pattern

Use module-level variables for caching frequently accessed data:

```javascript
// Use 'var' for GAS library compatibility (not 'let')
var _clientCache = null;
var _clientCacheTime = null;
const CACHE_TTL_MS = 60000; // 1 minute

function readClientsFromMatrix_() {
  // Return cached if fresh
  if (_clientCache && _clientCacheTime && 
      (Date.now() - _clientCacheTime < CACHE_TTL_MS)) {
    return _clientCache;
  }
  
  // Fetch fresh data
  const ss = SpreadsheetApp.openById(MATRIX_ID);
  const data = ss.getSheetByName('_CLIENT_MASTER').getDataRange().getValues();
  
  // Transform data...
  const clients = transformData(data);
  
  // Only cache if we got data (don't cache empty results)
  if (clients.length > 0) {
    _clientCache = clients;
    _clientCacheTime = Date.now();
  }
  
  return clients;
}

// Expose cache clear function
function clearClientCache() {
  _clientCache = null;
  _clientCacheTime = null;
}
```

### Important Notes

1. **Use `var` not `let`** at module level for GAS library compatibility
2. **Don't cache empty results** - they might indicate a transient error
3. **Provide cache clear function** - useful for debugging and forced refresh

---

## 4. Bulk Import Batching

### Pattern

For importing large datasets (1000+ records), batch processing with progress tracking:

```javascript
const BATCH_SIZE = 500;

function runBulkImport() {
  const props = PropertiesService.getScriptProperties();
  const startIndex = parseInt(props.getProperty('IMPORT_PROGRESS') || '0');
  
  // Get all IDs to process
  const allIds = getAllIds();  // e.g., 3,500 IDs
  
  if (startIndex >= allIds.length) {
    console.log('All records processed. Clearing progress.');
    props.deleteProperty('IMPORT_PROGRESS');
    return { success: true, message: 'Complete' };
  }
  
  // Process one batch
  const endIndex = Math.min(startIndex + BATCH_SIZE, allIds.length);
  const batchIds = allIds.slice(startIndex, endIndex);
  
  console.log(`Processing ${startIndex + 1} to ${endIndex} of ${allIds.length}...`);
  
  // Process batch
  const results = processBatch(batchIds);
  
  // Save progress
  props.setProperty('IMPORT_PROGRESS', String(endIndex));
  
  // Check if more to do
  if (endIndex < allIds.length) {
    console.log(`Run again to process remaining ${allIds.length - endIndex} records.`);
  } else {
    console.log('All records processed!');
    props.deleteProperty('IMPORT_PROGRESS');
  }
  
  return results;
}

function resetImportProgress() {
  PropertiesService.getScriptProperties().deleteProperty('IMPORT_PROGRESS');
  console.log('Progress reset. Next run will start from beginning.');
}
```

### Why 500 Records?

- GAS execution timeout: 6 minutes (360 seconds)
- API rate limits: ~10 requests/second
- 500 records with API calls takes ~3-5 minutes
- Leaves buffer for transformation and writing

---

## 5. Status Normalization

### The Problem

External APIs often return lowercase status values, but UIs typically expect Title Case:

```javascript
// API returns:
{ status: "active" }

// UI filter expects:
accountsState.data.filter(a => a.status === 'Active')  // No matches!
```

### The Solution

Normalize during transformation:

```javascript
function transformAccount(raw) {
  // Normalize status to Title Case
  const rawStatus = String(raw.status || 'active').toLowerCase();
  const status = rawStatus.charAt(0).toUpperCase() + rawStatus.slice(1);
  
  return {
    ...raw,
    status: status  // "Active" not "active"
  };
}
```

### Common Status Values

| Raw | Normalized |
|-----|------------|
| `active` | `Active` |
| `pending` | `Pending` |
| `inactive` | `Inactive` |
| `terminated` | `Terminated` |

---

## 6. Error Handling in Web Apps

### Always Return Objects, Never Null

```javascript
function uiGetData(id) {
  // BULLETPROOF: Always return an object
  try {
    if (!id) {
      return { success: false, error: 'ID is required' };
    }
    
    const data = fetchData(id);
    
    if (!data) {
      return { success: false, error: 'Data not found' };
    }
    
    return { success: true, data: data };
    
  } catch (error) {
    console.error('uiGetData error:', error);
    // ALWAYS return an object, never let exception bubble
    return { success: false, error: error.message || String(error) };
  }
}
```

### Client-Side Handling

```javascript
async function loadData(id) {
  try {
    const response = await callServer('uiGetData', id);
    
    // Handle null response (serialization failure)
    if (!response) {
      showToast('Server returned no response', 'error');
      return;
    }
    
    if (response.success) {
      renderData(response.data);
    } else {
      showToast(response.error || 'Failed to load data', 'error');
    }
  } catch (error) {
    showToast('Connection error: ' + error.message, 'error');
  }
}
```

---

## Related Documents

- `GHL_INTEGRATION_BEST_PRACTICES.md` - GHL-specific patterns
- `MATRIX_CONFIGURATION_STANDARDS.md` - MATRIX access patterns
- `UI_DESIGN_GUIDELINES.md` - Frontend patterns

---

*This document captures critical GAS web app patterns learned through production debugging.*
