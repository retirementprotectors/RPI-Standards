#!/usr/bin/env node
// negative-ordinary-load.mjs — SYNTHETIC FIXTURE: must NOT trip the rule/gate.
//
// An ordinary bq load in a loop, no replace flag — it's an append, not
// a full-table swap, so the invariant this rule enforces doesn't apply.
import { execFileSync } from 'node:child_process'

const bq = (args) => execFileSync('bq', ['--project_id=demo', ...args], { encoding: 'utf8' })

function pass() {
  bq(['load', '--source_format=NEWLINE_DELIMITED_JSON', 'ds.events', '/tmp/rows.ndjson'])
}

const loop = process.env.LOOP ? Number(process.env.LOOP) : 0
if (!loop) {
  pass()
} else {
  const tick = () => { try { pass() } catch (e) { console.error(String(e)) } }
  tick()
  setInterval(tick, loop * 1000)
}
