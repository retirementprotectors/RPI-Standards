# Mineart Unified Casework Presentation — Plan

## Context

We have 7 HTML casework outputs for the Mineart case. The design system used across them included gold, green, and red colors that are **NOT part of the RPI brand**. Before building anything new, all client-facing materials must be corrected to the approved palette.

## PRIORITY #1: Color Correction (Before Monday)

### The Problem
All 7 HTML files (and especially today's 2 new builds) use gold (#c5a55a), green (#16a34a), and red (#dc2626). These are NOT approved RPI brand colors.

### The Approved Palette (from RPI-PORTFOLIO-INSIGHTS-HANDOFF.md)
| Token | Hex | Usage |
|-------|-----|-------|
| `--navy` | `#1a3158` | Primary — headers, dark sections, emphasis |
| `--rpi-blue` | `#4a7ab5` | Accent — borders, highlights, badges |
| `--rpi-blue-pale` | `#edf2f8` | Backgrounds — sections, cards |
| Header cooled | `#e5ecf6` | Headers with RPI shield only |
| `--charcoal` | `#5a6270` | Secondary icon strokes |
| `--text-primary` | `#1a1a1a` | Body text |
| `--text-secondary` | `#4a5568` | Descriptions |
| `--text-muted` | `#718096` | Labels, footers |
| `--border` | `#e2e5ea` | Card/table borders |
| `--bg-light` | `#f8f9fa` | Light section backgrounds |
| `--white` | `#ffffff` | White |

### Color Correction Rules
**Two layers, two rules:**

1. **Brand layer** (headers, logos, callouts, section backgrounds, badges, footers): Navy/Blue/Pale Blue ONLY. No gold, no green, no red.
2. **Data layer** (tables, delta banners, status indicators, flow diagrams): Traffic light colors (green/red) ARE acceptable for functional meaning.

**Gold `#c5a55a` is NEVER acceptable anywhere — brand or data. Kill it everywhere.**

| Current | Action | Context |
|---------|--------|---------|
| Gold `#c5a55a` in callout titles, gradient lines, recommended badges | **REPLACE** with RPI Blue | These are brand elements |
| Gold `#c5a55a` anywhere else | **REPLACE** with RPI Blue | Gold doesn't exist in our world |
| Green/Red in data tables, delta banners, surplus/deficit indicators | **KEEP** | Functional data visualization |
| Green/Red in callout headings, section backgrounds, badges | **REPLACE** with Navy/Blue | These are brand elements |

### What to Fix
- Kill ALL gold (`#c5a55a`) everywhere — callout titles, gradient lines, badges, recommended markers. Replace with RPI Blue.
- Green/red in brand elements (callout headings, section backgrounds) → replace with Navy/Blue.
- Green/red in data tables and indicators → leave alone, that's functional UX.

## PRIORITY #2: Unified Tabbed Presentation

### Architecture
Single HTML file. Tab navigation. Correct RPI palette. Mobile-friendly.

### Tab Structure
| Tab | Content | Interactive? |
|-----|---------|-------------|
| **Overview** | Full financial picture from Ai3 — net worth, accounts, insurance | Static |
| **Income** | Current income, MHP gap, withdrawal slider | Yes — slider |
| **Estate** | 3 GMIB options, flow math, Year 1 bridge | Static |
| **Reserves** | $760K+ safety net inventory | Static |

### Key Design Decisions
1. Hardcoded Ai3 snapshot (not live API)
2. RPI approved palette ONLY
3. Print support per tab
4. Mobile-first for tablet at kitchen table
5. Single URL on GitHub Pages

### Meeting Flow
1. Overview → "Here's everything you have"
2. Income → "Here's the gap and how we fill it"
3. Estate → "Here's the legacy play — pick one"
4. Reserves → "Here's your cushion no matter what"

## Files to Create/Modify
- Fix all 7 existing HTML files (color correction)
- Build unified tabbed `index.html`
- Push to GitHub Pages
- Copy to collateral folder

## Verification
- Zero gold anywhere
- Brand elements use RPI palette only; data indicators can use traffic light colors
- Mobile-friendly on tablet
- Each tab prints cleanly
- Numbers match Ai3 and Winflex
