---
name: block-forui-no-json-serialize
enabled: true
event: file
action: block
conditions:
  - field: content
    operator: regex_match
    pattern: function\s+\w+ForUI\s*\(
  - field: file_path
    operator: regex_match
    pattern: \.gs$
---

**WARNING: ForUI function detected**

GAS ForUI functions MUST serialize return values with `JSON.parse(JSON.stringify(result))` to prevent Date objects becoming NULL on the client side.
