---
name: block-generated-logos
enabled: true
event: file
action: block
conditions:
  - field: new_text
    operator: regex_match
    pattern: <svg[^>]*viewBox[^>]*>[\s\S]*?<(path|circle|rect|polygon|ellipse)\s
  - field: file_path
    operator: regex_match
    pattern: \.(tsx|jsx)$
  - field: file_path
    operator: not_contains
    pattern: hookify
---

## BLOCKED: Generated SVG Logo Detected

You are attempting to write SVG markup with paths, circles, rects, or shapes. This looks like you are **generating a logo or icon from scratch**.

**This is absolutely forbidden.** JDM spent hours personally art-directing every logo in the suite. Generating a shitty SVG substitute is the single most disrespectful thing an agent can do.

### USE THE REAL LOGOS:
```
packages/ui/src/logos/
  prodashx-mark.svg / prodashx-logo.svg    (ProDashX)
  riimo-mark.svg / riimo-logo.svg          (RIIMO)
  sentinel-mark.svg / sentinel-logo.svg    (SENTINEL)
  LogoProDashX.tsx / LogoToMachina.tsx      (React components)
  PNG exports in prodashx/, riimo-tm/, sentinel-tm/, tomachina/
```

### If a logo doesn't exist yet:
**ASK JDM.** Use a text label as a temporary placeholder. NEVER generate SVG shapes.

### Exceptions:
- Inline SVG icons for UI elements (checkmarks, arrows, spinners) are fine
- Only LOGOS and BRAND MARKS are blocked
- If you need a small UI icon, use Material Icons (`<span class="material-icons-outlined">`)

**Do NOT proceed. Use the real logo assets.**
