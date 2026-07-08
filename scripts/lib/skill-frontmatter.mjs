#!/usr/bin/env node
/**
 * skill-frontmatter.mjs — the ONE parser + resolver for skill metadata.
 *
 * Single-file skills (OB1-GV2 skill-format lock, 2026-07-08): a skill IS a single
 * SKILL.md with rich YAML frontmatter carrying what skill.json used to carry
 * (id, owner_warrior, lane, version, hooks_enforcing, mcps_called). The runtime
 * only ever loads SKILL.md; the registry/surface read metadata from its frontmatter.
 *
 * ANTI-DIVERGENCE: both generate-skills-registry.mjs (import) and promote-skill.sh
 * (exec `--validate`) resolve metadata through THIS file — never a second impl.
 *
 * Resolution order (non-breaking migration): FRONTMATTER first; if a legacy 4-file
 * skill hasn't folded its fields into frontmatter yet, fall back to skill.json so it
 * doesn't drop off the registry mid-migration. Frontmatter wins where both are present.
 *
 * Usage as a CLI (used by promote-skill.sh):
 *   node scripts/lib/skill-frontmatter.mjs --validate <skill-dir>
 *     -> prints ✅ field lines + exits 0, or ❌ BLOCKED + exits 1.
 */

import { readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

export const REQUIRED_FIELDS = ['id', 'owner_warrior', 'lane', 'version']
export const ARRAY_FIELDS = ['hooks_enforcing', 'mcps_called']

/** Extract the raw text between the first pair of `---` fences. Returns null if none. */
export function extractFrontmatter(content) {
  // Frontmatter must be the first thing in the file (optional leading BOM/whitespace).
  const m = content.match(/^﻿?\s*---\r?\n([\s\S]*?)\r?\n---\s*(\r?\n|$)/)
  return m ? m[1] : null
}

/**
 * Minimal YAML-subset parser for skill frontmatter. Handles:
 *   key: scalar            (quotes stripped)
 *   key: [a, b, c]         (inline array; [] = empty)
 *   key:                   followed by indented "  - item" lines (block array)
 * Enough for the skill metadata shape; NOT a general YAML parser.
 */
export function parseFrontmatter(fm) {
  const out = {}
  const lines = fm.split(/\r?\n/)
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    if (!line.trim() || line.trim().startsWith('#')) { i++; continue }
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/)
    if (!kv) { i++; continue }
    const key = kv[1]
    const raw = kv[2].trim()
    if (raw === '') {
      // Possible block array: subsequent indented "- item" lines.
      const arr = []
      let j = i + 1
      while (j < lines.length && /^\s+-\s+/.test(lines[j])) {
        arr.push(stripQuotes(lines[j].replace(/^\s+-\s+/, '').trim()))
        j++
      }
      if (arr.length) { out[key] = arr; i = j; continue }
      out[key] = ''
      i++
      continue
    }
    if (raw.startsWith('[') && raw.endsWith(']')) {
      const inner = raw.slice(1, -1).trim()
      out[key] = inner === '' ? [] : inner.split(',').map(s => stripQuotes(s.trim()))
      i++
      continue
    }
    out[key] = stripQuotes(raw)
    i++
  }
  return out
}

function stripQuotes(s) {
  return s.replace(/^["']|["']$/g, '')
}

/** Read + parse frontmatter from a SKILL.md path. Returns {} if no frontmatter. */
export function readSkillFrontmatter(skillMdPath) {
  const content = readFileSync(skillMdPath, 'utf8')
  const fm = extractFrontmatter(content)
  return fm === null ? {} : parseFrontmatter(fm)
}

/**
 * Resolve skill metadata for a skill directory.
 * Returns { meta, source, hasSkillMd, hasSkillJson, missing }.
 *   meta     — resolved fields (frontmatter-primary, skill.json fallback/merge)
 *   source   — 'frontmatter' | 'skill.json' | 'frontmatter+skill.json' | null
 *   missing  — REQUIRED_FIELDS absent from the resolved meta
 */
export function resolveSkillMeta(skillDir) {
  const skillMdPath = join(skillDir, 'SKILL.md')
  const jsonPath = join(skillDir, 'skill.json')
  const hasSkillMd = existsSync(skillMdPath)
  const hasSkillJson = existsSync(jsonPath)

  let meta = {}
  let source = null

  if (hasSkillMd) {
    const fm = readSkillFrontmatter(skillMdPath)
    if (Object.keys(fm).length) { meta = { ...fm }; source = 'frontmatter' }
  }

  const hasAllRequired = REQUIRED_FIELDS.every(f => meta[f] != null && meta[f] !== '')
  if (!hasAllRequired && hasSkillJson) {
    try {
      const j = JSON.parse(readFileSync(jsonPath, 'utf8'))
      // Frontmatter wins where present-and-nonempty; skill.json fills the rest.
      const merged = { ...j }
      for (const [k, v] of Object.entries(meta)) {
        if (v != null && v !== '' && !(Array.isArray(v) && v.length === 0)) merged[k] = v
      }
      meta = merged
      source = source ? 'frontmatter+skill.json' : 'skill.json'
    } catch { /* invalid skill.json — leave meta as-is, will surface via `missing` */ }
  }

  // Normalize array fields to arrays (tolerate absent).
  for (const f of ARRAY_FIELDS) {
    if (meta[f] == null) meta[f] = []
    else if (!Array.isArray(meta[f])) meta[f] = [meta[f]]
  }

  const missing = REQUIRED_FIELDS.filter(f => meta[f] == null || meta[f] === '')
  return { meta, source, hasSkillMd, hasSkillJson, missing }
}

// ---- CLI: `--validate <skill-dir>` (used by promote-skill.sh) ----
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [flag, dir] = process.argv.slice(2)
  if (flag !== '--validate' || !dir) {
    console.error('Usage: node skill-frontmatter.mjs --validate <skill-dir>')
    process.exit(2)
  }
  const { meta, source, hasSkillMd, missing } = resolveSkillMeta(dir)
  if (!hasSkillMd) {
    console.error('❌ BLOCKED: SKILL.md is required and was not found.')
    process.exit(1)
  }
  if (missing.length) {
    console.error(`❌ BLOCKED: metadata missing required field(s): ${missing.join(', ')}`)
    console.error('   (put them in SKILL.md frontmatter: id / owner_warrior / lane / version)')
    process.exit(1)
  }
  for (const f of ARRAY_FIELDS) {
    if (!Array.isArray(meta[f])) {
      console.error(`❌ BLOCKED: ${f} must be a list.`)
      process.exit(1)
    }
  }
  console.log(`  ✅ Metadata valid (source: ${source}) — id: ${meta.id} | owner: ${meta.owner_warrior} | lane: ${meta.lane} | v${meta.version}`)
  console.log(`  ✅ hooks_enforcing: ${JSON.stringify(meta.hooks_enforcing)}`)
  console.log(`  ✅ mcps_called: ${JSON.stringify(meta.mcps_called)}`)
  process.exit(0)
}
