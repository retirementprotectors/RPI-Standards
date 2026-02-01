# Google Apps Script Project Standards
## Structure, Naming, and DevTools Pattern

> **Version**: v1.0  
> **Created**: February 1, 2026  
> **Scope**: ALL Google Apps Script projects  
> **Author**: Josh D. Millang + Claude

---

## Executive Summary

This document defines the required structure and conventions for all RPI Google Apps Script projects. The primary goal: **never waste time hunting for debug/setup/test functions**.

---

## Part 1: The DevTools Pattern (REQUIRED)

### The Problem

Without standards, debug/setup/test functions get scattered across 10+ `.gs` files. Finding `SETUP_DocuSign()` means searching through `DEX_DocuSign.gs`, `DEX_Setup.gs`, `Code.gs`, etc. **This wastes ~1 hour per day.**

### The Solution

Every GAS project MUST have a `*_DevTools.gs` file that centralizes ALL development, debugging, and maintenance functions.

```
PROJECT_DevTools.gs
├── Section 1: DEBUG_* functions (alphabetical)
├── Section 2: FIX_* functions (alphabetical)
├── Section 3: SETUP_* functions (alphabetical)
└── Section 4: TEST_* functions (alphabetical)
```

### Function Prefix Conventions

| Prefix | Purpose | When to Use | Example |
|--------|---------|-------------|---------|
| `DEBUG_` | Diagnostic/inspection | Show config, list fields, compare data | `DEBUG_ShowConfig()` |
| `FIX_` | One-time data/config fixes | Fix corrupted data, reformat keys | `FIX_PrivateKeyFormat()` |
| `SETUP_` | Initial setup and configuration | Create tabs, configure APIs, import data | `SETUP_CreateTabs()` |
| `TEST_` | Integration/validation tests | Test API connections, validate flows | `TEST_ApiConnection()` |

### File Template

```javascript
/**
 * ============================================================================
 * PROJECT_DevTools.gs
 * ============================================================================
 * 
 * CENTRALIZED DEBUG, FIX, SETUP, AND TEST FUNCTIONS
 * 
 * All development, debugging, and maintenance functions in ONE place.
 * Alphabetically sorted by TYPE, then by NAME for easy discovery.
 * 
 * SECTIONS:
 *   1. DEBUG_*   - Diagnostic and debugging functions
 *   2. FIX_*     - One-time fixes for data/config issues
 *   3. SETUP_*   - Initial setup and configuration functions
 *   4. TEST_*    - Test functions for validating integrations
 * 
 * ============================================================================
 */

// ============================================================================
// SECTION 1: DEBUG FUNCTIONS
// ============================================================================

/**
 * DEBUG_ExampleFunction
 * Brief description of what this does
 * 
 * @param {string} param - Parameter description
 * @source OriginalFile.gs (if moved from another file)
 */
function DEBUG_ExampleFunction(param) {
  // Implementation
}

// ============================================================================
// SECTION 2: FIX FUNCTIONS
// ============================================================================

// ============================================================================
// SECTION 3: SETUP FUNCTIONS
// ============================================================================

// ============================================================================
// SECTION 4: TEST FUNCTIONS
// ============================================================================
```

### JSDoc Requirements

Every function MUST include:
1. **Brief description** - What it does in one line
2. **@param** tags - For any parameters
3. **@source** tag - If moved from another file (for traceability)

---

## Part 2: File Naming Conventions

### Standard GAS Project Structure

```
PROJECT/
├── Code.gs                 # Entry point, menu, UI triggers
├── PROJECT_Config.gs       # Configuration constants and getters
├── PROJECT_DevTools.gs     # DEBUG/FIX/SETUP/TEST functions
├── PROJECT_ModuleA.gs      # Feature module (namespace)
├── PROJECT_ModuleB.gs      # Feature module (namespace)
├── Index.html              # UI entry point
├── Scripts.html            # Client-side JavaScript
├── Styles.html             # CSS styles
└── appsscript.json         # Manifest
```

### Naming Rules

1. **Prefix with project name**: `DEX_`, `RAPID_`, `CAM_`, etc.
2. **Use PascalCase** for file names: `DEX_FormLibrary.gs`
3. **Match namespace to filename**: File `DEX_FormLibrary.gs` should contain namespace `DEX_FormLibrary`

---

## Part 3: Namespace Pattern

### Why Namespaces?

GAS has a flat global scope. Namespaces prevent collisions and organize code.

```javascript
/**
 * DEX_FormLibrary.gs
 * Form library management functions
 */
const DEX_FormLibrary = {
  
  /**
   * Get all forms from the library
   */
  getAllForms: function() {
    // Implementation
  },
  
  /**
   * Get a single form by ID
   */
  getForm: function(formId) {
    // Implementation
  }
  
};
```

### Usage Pattern

```javascript
// External call
const forms = DEX_FormLibrary.getAllForms();

// From DevTools
function DEBUG_ListAllForms() {
  const result = DEX_FormLibrary.getAllForms();
  Logger.log(JSON.stringify(result, null, 2));
  return result;
}
```

---

## Part 4: Adding to Existing Projects

### Step 1: Audit Current Functions

```bash
# Find all DEBUG/SETUP/TEST/FIX functions
grep -rn "function.*\(DEBUG_\|SETUP_\|TEST_\|FIX_\)" *.gs
```

### Step 2: Create DevTools File

Create `PROJECT_DevTools.gs` using the template above.

### Step 3: Move Functions

Copy each function to the appropriate section in DevTools. Add `@source` tag to document where it came from.

### Step 4: Verify

Run each function from DevTools to ensure it still works (dependencies are global in GAS, so this should "just work").

### Step 5: Remove Duplicates (REQUIRED)

**After verification, remove the original functions from their source files.**

This is NOT optional because:
1. **Avoids confusion** - duplicate functions make it unclear which is "the real one"
2. **Prevents drift** - if someone edits the wrong copy, changes are lost
3. **Reduces file size** - cleaner, more maintainable codebase

**Leave a redirect comment** in the original file:

```javascript
// ============================================================================
// UI WRAPPER FUNCTIONS
// ============================================================================
// NOTE: DEBUG/SETUP/TEST/FIX functions moved to PROJECT_DevTools.gs
```

**For files that were ONLY setup functions** (like `DEX_Setup.gs`), replace the entire file with a stub:

```javascript
/**
 * PROJECT_Setup.gs
 * 
 * ============================================================================
 * ALL SETUP FUNCTIONS HAVE MOVED TO PROJECT_DevTools.gs
 * ============================================================================
 * 
 * To find setup functions:
 *   1. Open PROJECT_DevTools.gs
 *   2. Go to Section 3: SETUP FUNCTIONS
 *   3. Functions are sorted alphabetically
 */

// This file intentionally left mostly empty.
// All functionality has been moved to PROJECT_DevTools.gs
```

### Step 6: Push Changes

```bash
# Push to GitHub
git add -A && git commit -m "Consolidate dev functions to DevTools, remove duplicates" && git push

# Push to Google Apps Script
clasp push
```

**Remember**: `git push` and `clasp push` are separate - you need both!

---

## Part 5: Cursor Rule

Add this rule to `.cursor/rules/gas-devtools.mdc` in each GAS project:

```markdown
---
description: Google Apps Script DevTools pattern - centralize DEBUG/FIX/SETUP/TEST functions
globs: "**/*.gs"
alwaysApply: false
---

# Google Apps Script DevTools Pattern

Every GAS project MUST have a `*_DevTools.gs` file that centralizes all development, debugging, and maintenance functions.

[See GAS_PROJECT_STANDARDS.md for full details]
```

---

## Checklist: New GAS Project Setup

- [ ] Create project folder with correct structure
- [ ] Create `Code.gs` with menu and triggers
- [ ] Create `PROJECT_Config.gs` with constants
- [ ] Create `PROJECT_DevTools.gs` with section headers
- [ ] Add `.cursor/rules/gas-devtools.mdc` rule
- [ ] As you add DEBUG/SETUP/TEST/FIX functions, put them in DevTools
- [ ] Keep functions alphabetical within each section

---

## Reference Implementation

See **DEX** project for a complete example:
- `/Users/joshd.millang/Projects/DEX/DEX_DevTools.gs`
- 40 functions consolidated from 6 files
- Alphabetically sorted by type, then name

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.1 | 2026-02-01 | Made duplicate removal REQUIRED (Step 5), added Step 6 push guidance |
| v1.0 | 2026-02-01 | Initial release - DevTools pattern documented |
