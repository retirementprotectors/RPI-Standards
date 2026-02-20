# The Data Operating System — Team Guide

> **What it is, why it matters, and what you need to know.**
> February 20, 2026

---

## The One-Sentence Version

**The Data Operating System is how The Machine keeps its data clean** — the rules, the normalizers, the quality gates, the health checks, and the playbooks that ensure every client record, every policy, and every account is accurate, complete, and trustworthy.

---

## Why We Built This

RPI manages thousands of client records across Medicare, Life, Annuity, and Advisory lines of business. That data comes from multiple sources — GoHighLevel exports, carrier feeds, manual entry, M&A partner systems, and legacy spreadsheets. Every source has its own formatting, its own typos, and its own way of getting things wrong.

Before the Data OS, we cleaned data by hand. Someone would notice "Heathcare" instead of "Healthcare" across 59 records, fix it, and move on. Next month, a new import would bring the same typo right back. We were fighting the same battles over and over.

We turned every manual correction into a permanent rule. Now when bad data shows up, the system catches it automatically — before it ever reaches the database. The same mistake never happens twice.

---

## The Architecture

Think of it like this:

```
The Machine = the business (our platforms, our data, our people)
    |
    +-- The Operating System = how we keep it secure (Security OS)
    |
    +-- The Data Operating System = how we keep it clean
            |
            +-- Standards        -- What the rules are
            +-- Posture          -- Current state of data quality
            +-- The Immune System -- Automatic normalization + quality gates
            +-- Monitoring       -- Health checks + drift detection
            +-- Operations       -- Playbooks for imports + maintenance
```

The Security OS protects access and compliance. The Data OS protects accuracy and completeness. Together, they govern The Machine.

---

## The 5 Pillars (What Each One Does)

### 1. Standards — The Rulebook

This is the foundation. It defines:
- Every field across all MATRIX tabs — what format it should be in, what values are allowed
- Canonical value lists — the "blessed" spellings of every carrier, product, plan, and status
- Known garbage patterns — epoch dates in dollar fields, CMS plan IDs in name fields, trademark symbols, systematic typos
- The Correction Log — every data fix we've ever made, documented for audit

**Why it matters to you:** If you ever see a carrier name that looks wrong, or a product name that doesn't match what you expect — Standards defines what the correct value should be. It's the single source of truth for "what does clean data look like?"

### 2. Posture — The Scoreboard

This tracks:
- Record counts and quality metrics for every MATRIX tab
- Which normalizers are active and what version they were added
- Known issues still being worked (CoF import, orphan accounts, etc.)
- Every M&A data import — source, date, quality score, issues found

**Why it matters to you:** When someone asks "how clean is our data?" or "what happened with the last import?" — Posture has the answer. It's the scoreboard that shows where we stand.

**Key facts from Posture:**
- ~9,750 records across 5 MATRIX tabs (clients + all product lines)
- 90+ fields auto-normalized on every write
- 16 normalizer types (names, phones, emails, dates, carriers, products, plans, amounts, and more)
- Contact validation APIs built and keyed (phone, email, address) — first full run pending

### 3. The Immune System — Automatic Enforcement

This is the part that runs in the background every time data enters MATRIX. 90+ field normalizers that automatically:
- **Fix names** — title case, handle McDonald/O'Brien patterns, strip extra spaces
- **Standardize phones** — (XXX) XXX-XXXX format, every time
- **Correct carriers** — 238+ aliases all map to the one correct spelling
- **Clean products** — 50+ product name corrections auto-applied
- **Clean plans** — 30+ plan name corrections + regex patterns for systematic typos
- **Guard amounts** — strips dollar signs/commas, catches epoch dates masquerading as money
- **Normalize everything else** — emails, dates, states, ZIPs, addresses, statuses, books of business

Plus the **Import Quality Gate** — a pre-import scan that grades incoming data A through F and recommends PROCEED, REVIEW FIRST, or REJECT before any records touch the database.

**Why it matters to you:** You don't need to do anything with this — it's automatic. Every record that enters MATRIX goes through normalization before it's written. The data you see in reports, dashboards, and client records is already cleaned. No more "is it Aetna or AETNA or aetna?" — the system handles it.

**The learning loop:** When we find a new garbage pattern, we fix the existing data, then promote the fix into a permanent normalizer. The next import auto-catches the same pattern. The system gets smarter with every correction.

### 4. Monitoring — The Watchdogs

This covers everything that's being watched:

| How Often | What's Happening |
|-----------|-----------------|
| Every write | Field normalization (Immune System) |
| On demand | Health check — record counts, blank field %, orphan count, garbage scan, drift detection |
| Pre-import | Quality gate — grades incoming data before it enters MATRIX |
| Monthly (planned) | Full normalization sweep + health check + Slack report |
| Quarterly (planned) | Dedup reconciliation + contact re-validation |

**Why it matters to you:** Nothing drifts silently. If a new carrier name appears that doesn't match any known alias, the health check catches it. If blank field percentages creep up, we see it. Data quality isn't a one-time cleanup — it's continuous monitoring.

### 5. Operations — The Playbooks

Four playbooks that cover every scenario:

1. **M&A Data Ingestion** — Step-by-step process for importing data from acquired partners. Receive export, run quality gate, fix issues, import, normalize, validate contacts. Every M&A intake follows the same process.

2. **Drive-Based Enrichment** (future) — Using policy PDFs and statements from Google Drive to fill gaps in MATRIX records. Extract structured data from documents, match to existing records, backfill missing fields.

3. **Periodic Maintenance** — Monthly health checks, normalization sweeps, and contact re-validation. Keeps data fresh as people move, change phones, and abandon emails.

4. **Correction to Permanent Rule** — The closed loop. Identify a pattern, build a fix, execute it, promote it to a normalizer, deploy, document. The same mistake never happens twice.

**Why it matters to you:** When a new M&A partner comes on board and hands us a CRM export, there's no guessing about what to do with it. The playbook exists. When it's time for monthly maintenance, the checklist exists. No tribal knowledge required.

---

## How It All Connects

The 5 pillars form a continuous loop:

```
Standards define what clean data looks like
    --> The Immune System enforces it automatically on every write
        --> Monitoring detects when something drifts or degrades
            --> Operations corrects what was found
                --> Standards evolve based on what we learned
                    --> (repeat)
```

No pillar works alone. Standards without enforcement is just a wish list. Enforcement without monitoring is blind. Monitoring without operations is noise. This loop is what makes the Data OS self-correcting.

---

## What Changed (Before vs. After)

| Before | After |
|--------|-------|
| Product names had 50+ spelling variations | One canonical spelling per product, enforced automatically |
| Plan names full of typos (Heathcare, PLATNIUM) | Regex + alias corrections on every write |
| Carrier names inconsistent (aetna vs AETNA vs Aetna) | 238+ aliases all resolve to one canonical name |
| Epoch dates showing up as premiums | Caught and cleared automatically |
| CMS plan IDs in plan name fields | Detected by pattern, cleared automatically |
| Manual cleanup after every import | Quality gate BEFORE import + auto-normalization during |
| Same corrections repeated import after import | Every correction promoted to permanent normalizer |
| No record of what was cleaned or when | Correction Log documents every fix with dates and counts |
| Data quality was "vibes" | Health check gives A-F score with specific metrics |
| No M&A import process | Step-by-step playbook for every acquisition |

**Nothing was lost.** Every manual correction we ever made is now a permanent rule in the system. The work we did cleaning ~700 records across 5 tabs didn't just fix those records — it created the rules that protect every future record.

---

## What This Means For You

### If you're on the Service Team (Nikki's division)
Client records you pull up in PRODASH are automatically cleaned — names properly capitalized, phones formatted, carriers spelled correctly. When you search for "Aetna" you get all Aetna records, not just the ones that happened to be spelled right. The data you see is the data you can trust.

### If you're on the Sales Team (Vinnie's division)
When you enter a new client or policy, the system normalizes it on the way in. You don't need to worry about whether you typed "United Healthcare" or "UHC" or "AARP/UHC" — the normalizer maps it to the canonical name. Less data entry friction, cleaner CRM.

### If you're on the B2B/DAVID Team (Matt's division)
This is your M&A secret weapon. When a new partner comes on board with a messy CRM export, there's a playbook. Run the quality gate, get a grade, fix what needs fixing, import with confidence. The normalizers catch the same garbage patterns we've already seen from other systems. Every acquisition gets easier because the system remembers what it learned from the last one.

### If you're in Leadership (John, Shane)
Data quality now has a measurable score. The health check returns specific metrics — not "data looks okay" but "4,650 clients, 0 garbage patterns, 399 orphan accounts, 65% missing emails." You can track improvement over time. The M&A import log shows exactly what came in from each source and what state it was in.

### If you're the CTO (Jason)
The full technical reference is in the Data OS directory. CORE_Normalize.gs has all normalizer functions. CORE_Database.gs has FIELD_NORMALIZERS mapping and assessDataQuality(). IMPORT_BoBEnrich.gs has DEBUG_DataHealthCheck() and FIX_ValidateContacts_(). Every normalizer is unit-testable. The alias maps are pure data — easy to extend, easy to audit.

---

## The Numbers

| Metric | Count |
|--------|-------|
| Total MATRIX records | ~9,750 |
| Fields auto-normalized | 90+ |
| Normalizer types | 16 |
| Carrier name aliases | 238+ |
| Product name aliases | 50+ |
| Plan name aliases | 30+ (plus regex patterns) |
| Clients normalized (Phase 1) | 4,649 |
| Statuses cleaned (Phase 2) | 4,617 |
| Client duplicates merged (Phase 3) | 270 |
| Annuity duplicates resolved (Phase 4) | 39 |
| Product/plan corrections (Phase 7) | ~700 records across 5 tabs |
| Garbage patterns detected (post-deploy) | 0 (normalizers working) |
| Validation APIs built | 6 (phone, email, address, city/state, bank routing, composite) |
| RAPID_CORE version | v1.12.0 |

---

## Quick Reference

| "I need to..." | Go to |
|-----------------|-------|
| Know what the correct carrier/product/plan name is | DATA_STANDARDS (Canonical Value Lists) |
| See current data quality metrics | DATA_POSTURE |
| Understand how a field gets normalized | DATA_STANDARDS (Field Registry) |
| Know what garbage patterns are caught | DATA_STANDARDS (Garbage Patterns) |
| See what corrections have been made | DATA_STANDARDS (Correction Log) |
| Understand the health check output | DATA_MONITORING |
| Follow the M&A import process | DATA_OPERATIONS (Playbook 1) |
| Run monthly maintenance | DATA_OPERATIONS (Playbook 3) |
| Turn a manual fix into a permanent rule | DATA_OPERATIONS (Playbook 4) |
| See the full architecture | This guide |

---

## The Bottom Line

The Data Operating System is how we prove — to ourselves, to our clients, to our M&A partners — that The Machine's data is governed. Not by manual cleanup, not by hoping someone catches the typo, but by normalizers that fire on every write, quality gates that score every import, and a learning loop that turns every correction into a permanent defense.

Every M&A acquisition we do from here forward starts with a quality gate and ends with clean data. Every carrier name, every product name, every plan name is standardized before it touches the database. The same mistake never happens twice because the system remembers.

We didn't just clean the data. We built the system that keeps it clean forever.

---

*Document location: `_RPI_STANDARDS/reference/data/DATA_TEAM_GUIDE.md`*
*Last updated: February 20, 2026*
*Questions? Ask Josh or John Behn.*
