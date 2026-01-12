# Production Launch Rollout Kit

> **Template Version**: 1.0  
> **Purpose**: Human-facing documentation to accompany AI-built projects  
> **When to Use**: After GA confirms project is feature-complete and OPS deploys final version

---

## Overview

When a project built by the AI Agent Team is ready for production, it needs **human-facing documentation** to complement the AI agent docs. This template defines the standard documentation suite for any production launch.

**AI Agent Docs** (`Docs/`) = Instructions for AI agents (Session Handoff, Agent Briefing, Scope docs)

**User Docs** (`Docs/User/`) = Instructions for human users (Guides, Overviews, Value Analysis)

---

## Standard Documentation Suite

Every production project should include these documents in `Docs/User/`:

### 1. System Overview
**File**: `{PROJECT}_Overview.html`

**Audience**: All users (first read for anyone new)

**Contents**:
- What the system does
- Core modules/features
- User roles
- Key workflows
- Getting started steps

---

### 2. Admin Guide
**File**: `Admin_Guide.html`

**Audience**: System administrators

**Contents**:
- Configuration options
- User management
- System settings
- Integration setup
- Troubleshooting

---

### 3. Role-Specific Guides
**Files**: `{Role}_Guide.html`

**Create one for each user persona** in your system:

| Example Roles | Guide Name |
|---------------|------------|
| Manager/Ops | `Manager_Guide.html` |
| Editor/Creator | `Editor_Guide.html` |
| Sales Agent | `Sales_Team_Guide.html` |
| Partner | `Partner_Guide.html` |
| Viewer | `Viewer_Guide.html` |

**Contents per guide**:
- What they can access
- What they can do
- Step-by-step workflows
- FAQs for their role

---

### 4. Development Value Analysis
**File**: `{PROJECT}_Development_Value.html`

**Audience**: Executives, stakeholders

**Contents**:
- Codebase statistics (lines of code, modules)
- Traditional development cost estimate
- Timeline comparison (traditional vs AI-assisted)
- Feature summary
- Technical specifications
- ROI/value proposition

---

## Design Guidelines

### Visual Standards
- Use consistent branding (RPI colors, fonts)
- Each guide should have a **unique accent color** for its header/badges
- Include the **version number** in footer
- Make all guides **print-friendly** with `@media print` CSS

### Recommended Colors by Role
| Role | Accent Color | Meaning |
|------|--------------|---------|
| Admin | Red (`#dc2626`) | High authority, caution |
| Manager | Green (`#059669`) | Operations, go |
| Sales/Agent | Blue (`#3b82f6`) | Trust, action |
| Partner | Gold (`#fbbf24`) | Value, partnership |
| Overview | Navy (`#1e3a5f`) | Brand, foundation |

### Required Sections in Every Guide
1. **Header** with logo, title, role badge
2. **Quick Start** or Getting Started section
3. **What You Can/Cannot Do** (permissions)
4. **Main Workflows** with step-by-step
5. **FAQs** addressing common questions
6. **Footer** with version, date, copyright

---

## Template Structure

```
Docs/
├── 0-SESSION_HANDOFF.md          # AI: Session state
├── 1-AGENT_BRIEFING.md           # AI: Project context
├── 2.x-AGENT_SCOPE_*.md          # AI: Role scopes
├── 3.x-AGENT_SCOPE_SPC*.md       # AI: Specialist scopes
│
└── User/                         # HUMAN: User documentation
    ├── {PROJECT}_Overview.html   # System overview
    ├── Admin_Guide.html          # Admin guide
    ├── Manager_Guide.html        # Manager/Ops guide
    ├── {Role}_Guide.html         # Role-specific guides
    └── {PROJECT}_Development_Value.html  # Investment analysis
```

---

## Checklist

Before declaring a project launch-ready:

### AI Agent Docs
- [ ] Session Handoff updated with final version
- [ ] Agent Briefing reflects actual deployed state
- [ ] All scope docs accurate

### User Docs
- [ ] Overview document created
- [ ] Admin guide created
- [ ] Guide for each user role created
- [ ] Development Value analysis created
- [ ] All docs have consistent branding
- [ ] All docs print correctly
- [ ] All docs committed and pushed

### Deployment
- [ ] Final version deployed via OPS
- [ ] Git committed with user docs
- [ ] Production URL documented

---

## Example: CAM Project

CAM's user documentation suite:

| Document | Purpose |
|----------|---------|
| `CAM_Overview.html` | System intro, modules, workflows |
| `Admin_Guide.html` | Tier config, MATRIX setup |
| `Manager_Guide.html` | Running cycles, analytics |
| `Sales_Team_Guide.html` | B2C agents, tier progression |
| `Partner_Guide.html` | B2B DAVID partners |
| `CAM_Development_Value.html` | $215K value, 15K LOC |

---

## Why This Matters

**For Humans**: Clear, role-specific documentation makes adoption faster and reduces support burden.

**For AI Agents**: Separating human docs from agent docs keeps scope clear and prevents confusion.

**For Leadership**: Development Value analysis quantifies the ROI of AI-assisted development.

---

*This template was created based on the CAM project launch (January 2026).*
