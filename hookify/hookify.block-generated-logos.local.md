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
owner: musashi
---

## BLOCKED: Generated SVG Logo Detected

You are attempting to write SVG markup with paths, circles, rects, or shapes. This looks like you are **generating a logo or icon from scratch**.

**This is absolutely forbidden.** JDM spent hours personally art-directing every logo in the suite. Generating a shitty SVG substitute is the single most disrespectful thing an agent can do.

### USE THE REAL LOGOS:

CANONICAL = the "-tm" set (these are the logos on theagentxstory.com).
They are WIDE horizontal logos -- there is no square-mark variant. Size to
fit; "wide is fine" (JDM, 2026-06-09).

```
packages/ui/src/logos/
  prodashx-tm/   (ProDashX)   riimo-tm/   (RIIMO)   sentinel-tm/  (SENTINEL)
      each contains: -tm-transparent.png (full logo) | -tm-icon-150w.png (small)
                     -tm-on-dark.png | -tm-on-white.png | -tm-small-300w.png
                     -tm-medium-600w.png

  agentx/  prodashx/  tomachina/     PNG exports, same -transparent / -icon-150w /
                                     -on-dark / -on-white / -*w naming
  rpi/                               rpi-logo-full-color.png | rpi-logo-v2-color.png
                                     rpi-logo-v2-white.png | rpi-shield-mark.png
  agentx-logo.svg | agentx-logo-dark.svg | agentx-mark.svg    (AgentX, SVG)
  LogoAgentX.tsx | LogoProDashX.tsx | LogoToMachina.tsx       (React components)
```

⛔ RETIRED 2026-06-09 (VOL-LOGOKILL-001, toMachina#1709 / c4daec0d): the old
gauge/compass/shield marks -- `prodashx-mark.svg`, `prodashx-logo.svg`,
`riimo-mark.svg`, `riimo-logo.svg`, `sentinel-mark.svg`, `sentinel-logo.svg`
-- were the WRONG logos and were deleted repo-wide. They are NOT on origin/main.
This rule pointed at those six filenames until 2026-07-26; if you were sent here
by an older copy of it, that is why the file was not found. Do NOT recreate them.

### If a logo doesn't exist yet:
**ASK JDM.** Use a text label as a temporary placeholder. NEVER generate SVG shapes.

### Exceptions:
- Inline SVG icons for UI elements (checkmarks, arrows, spinners) are fine
- Only LOGOS and BRAND MARKS are blocked
- If you need a small UI icon, use Material Icons (`<span class="material-icons-outlined">`)

**Do NOT proceed. Use the real logo assets.**
