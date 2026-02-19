---
name: warn-phi-in-error-message
enabled: true
event: file
action: warn
conditions:
  - field: content
    operator: regex_match
    pattern: catch\s*\([^)]*\)\s*\{[\s\S]*?(return|throw|log).*error\.(message|stack|toString)
---

**WARNING: Error Message May Expose PHI**

You are returning, throwing, or logging `error.message` or `error.stack` directly.

**Why this matters:**
- Error messages can contain PHI from database queries, API responses, etc.
- Stack traces may include sensitive data in variable names
- This could be a compliance violation

**Safer pattern:**
```javascript
// RISKY
catch (error) {
  return { success: false, error: error.message };  // May contain PHI!
}

// SAFER
catch (error) {
  Logger.log('Error in function X: ' + error.message);  // Log server-side only
  return { success: false, error: 'Operation failed. Please try again.' };  // Generic to client
}
```

**When to ignore this warning:**
- Internal/admin-only functions
- Server-side only code (not returned to client)
- Errors that definitely don't contain user data

See: `_RPI_STANDARDS/reference/os/STANDARDS.md`
