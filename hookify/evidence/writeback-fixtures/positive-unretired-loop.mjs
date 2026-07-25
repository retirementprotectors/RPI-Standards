#!/usr/bin/env node
// positive-unretired-loop.mjs — SYNTHETIC FIXTURE: SHOULD trip warn-unretired-writeback-loop
// and the writeback-retirement-gate CI check.
//
// A background writeback loop that full-table-replaces a BQ staging table on
// every tick, forever, with no retirement or liveness check anywhere in the
// file. This is the exact shape that burned _tmp-writeback-bq.mjs.
import { execFileSync } from 'node:child_process'

const bq = (args) => execFileSync('bq', ['--project_id=demo', ...args], { encoding: 'utf8' })

function pass() {
  bq(['load', '--replace', '--source_format=NEWLINE_DELIMITED_JSON', 'ds._stage', '/tmp/rows.ndjson'])
}

const loop = process.env.LOOP ? Number(process.env.LOOP) : 0
if (!loop) {
  pass()
} else {
  const tick = () => { try { pass() } catch (e) { console.error(String(e)) } }
  tick()
  setInterval(tick, loop * 1000)
}
