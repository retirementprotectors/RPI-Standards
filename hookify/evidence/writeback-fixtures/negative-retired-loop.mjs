#!/usr/bin/env node
// negative-retired-loop.mjs — SYNTHETIC FIXTURE: must NOT trip the rule/gate.
//
// Same full-table-replace-in-a-loop shape as positive-unretired-loop.mjs, but
// this one carries an explicit RETIREMENT_CHECK: a hard kill-date past which
// the loop refuses to keep running. TRK-S-META-004's opt-out convention.
import { execFileSync } from 'node:child_process'

// RETIREMENT_CHECK: this loop retires itself after the P40 fullcorpus sweep's
// scheduled end. Past this date the loop refuses to run — someone forgetting
// to kill the process can no longer clobber the live table.
const RETIRE_AFTER = new Date('2026-08-01T00:00:00Z').getTime()

const bq = (args) => execFileSync('bq', ['--project_id=demo', ...args], { encoding: 'utf8' })

function pass() {
  bq(['load', '--replace', '--source_format=NEWLINE_DELIMITED_JSON', 'ds._stage', '/tmp/rows.ndjson'])
}

const loop = process.env.LOOP ? Number(process.env.LOOP) : 0
if (!loop) {
  pass()
} else {
  const tick = () => {
    if (Date.now() > RETIRE_AFTER) { console.error('retirement date passed — exiting'); process.exit(1) }
    try { pass() } catch (e) { console.error(String(e)) }
  }
  tick()
  setInterval(tick, loop * 1000)
}
