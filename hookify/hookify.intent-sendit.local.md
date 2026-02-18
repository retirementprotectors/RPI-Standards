---
name: intent-sendit
enabled: true
event: prompt
action: warn
conditions:
  - field: user_prompt
    operator: regex_match
    pattern: (#SendIt|#sendit|send\s+it|ship\s+it)
---

**DEPLOY PROTOCOL TRIGGERED (#SendIt)**

Execute the 6-Step Deploy sequence:

```
1. git status && git remote -v                          # Pre-flight
2. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp push --force    # Push code
3. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp version "vX.X"  # Create version
4. NODE_TLS_REJECT_UNAUTHORIZED=0 clasp deploy -i [ID] -V [VER] -d "vX.X"  # Deploy
5. git add -A && git commit && git push                 # Commit + push
6. VERIFY: clasp deployments | grep "@[VERSION]"        # MANDATORY verify
```

Report results in the standard Deploy Report table format.
Do NOT skip the VERIFY step — confirm @version matches.
