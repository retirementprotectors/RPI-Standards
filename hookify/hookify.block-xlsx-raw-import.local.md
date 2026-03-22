---
name: block-xlsx-raw-import
description: Block XLSX imports that don't use raw:false — phone numbers and other numeric-looking text get silently corrupted by float precision loss
enabled: true
action: block
event: file
files: ["*.ts", "*.js"]
pattern: "sheet_to_json\\([^)]*(?!raw:\\s*false)[^)]*\\)"
message: |
  BLOCKED: XLSX sheet_to_json() without raw: false.

  SheetJS reads numeric-looking cells as JavaScript floats by default.
  Phone numbers, policy numbers, and ZIP codes SILENTLY LOSE DIGITS.

  TRK-441: 619 CoF client phone numbers were corrupted (last 1-3 digits wrong)
  because the import script used sheet_to_json() without raw: false.

  FIX: Always use { raw: false, defval: null }

  ❌ XLSX.utils.sheet_to_json(sheet, { defval: null })
  ✅ XLSX.utils.sheet_to_json(sheet, { raw: false, defval: null })
---
