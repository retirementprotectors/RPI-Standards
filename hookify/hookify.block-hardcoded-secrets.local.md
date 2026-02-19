---
name: block-hardcoded-secrets
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: (api_key|apiKey|API_KEY|token|TOKEN|password|PASSWORD|secret|SECRET|access_key|ACCESS_KEY)\s*[:=]\s*['"][A-Za-z0-9_\-]{20,}['"]
---

**BLOCKED: Hardcoded Secret Detected**

You are hardcoding an API key, token, password, or secret directly in code.

**Why this is blocked:**
- Security vulnerability - secrets in code can be leaked
- Secrets in git history are nearly impossible to fully remove
- This violates RPI security standards

**Fix:**
Use Script Properties instead:
```javascript
// WRONG
const API_KEY = 'sk-1234567890abcdefghij';

// CORRECT
const API_KEY = PropertiesService.getScriptProperties().getProperty('API_KEY');
```

To set Script Properties:
1. GAS Editor → Project Settings → Script Properties
2. Add your secret as a property
3. Reference via `PropertiesService.getScriptProperties().getProperty('NAME')`

See: `_RPI_STANDARDS/reference/os/POSTURE.md`
