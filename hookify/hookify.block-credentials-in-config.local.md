---
name: block-credentials-in-config
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(gs|json|js)$
  - field: content
    operator: regex_match
    pattern: (xoxb-[a-zA-Z0-9\-]+|xoxp-[a-zA-Z0-9\-]+|hooks\.slack\.com/services/[A-Z0-9/]+|sk-[a-zA-Z0-9]{20,})
---

**BLOCKED: Plaintext Credential Detected**

You are writing a plaintext Slack token, webhook URL, or API key directly into a source file.

**Why this is blocked:**
- Slack tokens (`xoxb-`, `xoxp-`) grant full workspace access
- Webhook URLs allow anyone to post to Slack channels
- API keys (`sk-`) grant service access
- Secrets in source code get committed to git history and are nearly impossible to remove

**Fix:**
Use Script Properties (GAS) or environment variables (Node.js):

```javascript
// GAS — WRONG
const SLACK_TOKEN = 'xoxb-1234-5678-abcdef';

// GAS — CORRECT
const SLACK_TOKEN = PropertiesService.getScriptProperties().getProperty('SLACK_BOT_TOKEN');

// Node.js — WRONG
const API_KEY = 'sk-abcdefghijklmnopqrst';

// Node.js — CORRECT
const API_KEY = process.env.API_KEY;
```

See: `_RPI_STANDARDS/reference/os/POSTURE.md`
