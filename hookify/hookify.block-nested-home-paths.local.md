---
name: block-nested-home-paths
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^/home/jdm/(home|jdm)/
---

**BLOCKED: Nested `/home/jdm/home/` or `/home/jdm/jdm/` path detected**

You're about to write to a path that duplicates the home segment. This is
the "accidental nested home dir" class-of-bug — confirmed in the 2026-05-11
hot-mess sweep (created by an unknown earlier session that wrote
`/home/jdm/home/jdm/Projects/toMachina/packages/core/tsconfig.tsbuildinfo`,
sat there orphaned for weeks).

**Common causes:**
- A build tool (tsc, webpack, esbuild) runs with the wrong CWD and writes
  to a relative path that already begins with `/home/jdm/`
- A `cd` confusion in a shell script creates a nested mistake
- A `mkdir -p` is fed a path that's already absolute but treated as relative

**Fix:** Verify your CWD with `pwd` before writing. The intended path almost
certainly drops the duplicated `home/jdm/` or `jdm/` segment.

If you genuinely need a subdirectory called `home` or `jdm`, name it
something distinct (`homedir`, `userhome`, etc.).
