# Project Standards & Directory Structure

> **IMPORTANT**: All projects MUST be in `/Users/joshd.millang/Projects/`

## Directory Structure

```
/Users/joshd.millang/
└── Projects/                    ← ALL PROJECTS GO HERE
    ├── RAPID_CORE/             ← Core library
    ├── RAPID_IMPORT/           ← Import system
    ├── RAPID_API/              ← REST API
    ├── PRODASH/                ← Dashboard
    └── sentinel/               ← Monitoring
```

## Project Inventory

| Project | GitHub Repo | Local Path | GAS Script ID |
|---------|-------------|------------|---------------|
| RAPID_CORE | retirementprotectors/RAPID_CORE | `~/Projects/RAPID_CORE` | `1-HKxgcOIkx6Ov2uXk6TU-yJM24cvB4ctyCTuqS3NLEBs5XA-FFGWGJSI` |
| RAPID_IMPORT | retirementprotectors/RAPID_IMPORT | `~/Projects/RAPID_IMPORT` | - |
| RAPID_API | retirementprotectors/RAPID_API | `~/Projects/RAPID_API` | - |
| PRODASH | retirementprotectors/ProDash | `~/Projects/PRODASH` | - |
| sentinel | retirementprotectors/sentinel | `~/Projects/sentinel` | - |

## Cloning Projects (New Machine)

**ALWAYS clone into the Projects folder:**

```bash
# If projects exist at old locations, remove them first
rm -rf /Users/joshd.millang/RAPID_* /Users/joshd.millang/prodash /Users/joshd.millang/sentinel

# Create Projects folder and clone all
mkdir -p /Users/joshd.millang/Projects
cd /Users/joshd.millang/Projects
git clone https://github.com/retirementprotectors/RAPID_CORE.git
git clone https://github.com/retirementprotectors/RAPID_IMPORT.git
git clone https://github.com/retirementprotectors/RAPID_API.git
git clone https://github.com/retirementprotectors/ProDash.git PRODASH
git clone https://github.com/retirementprotectors/sentinel.git
```

## Deployment Workflow

### For GAS Projects (RAPID_API, RAPID_CORE, etc.)

Each project has a `push.sh` script that:
1. Pushes to Google Apps Script via `clasp push`
2. Commits to Git
3. Pushes to GitHub

```bash
cd /Users/joshd.millang/Projects/RAPID_API
./push.sh "Your commit message"
```

### Manual Deploy/Commit

```bash
cd /Users/joshd.millang/Projects/PROJECT_NAME

# Push to GAS
clasp push

# Commit and push to GitHub
git add -A
git commit -m "Your message"
git push
```

## Common Mistakes to Avoid

### ❌ DON'T: Clone to home directory root
```bash
cd /Users/joshd.millang
git clone https://github.com/...  # WRONG!
```

### ✅ DO: Clone to Projects folder
```bash
cd /Users/joshd.millang/Projects
git clone https://github.com/...  # CORRECT!
```

### ❌ DON'T: Have duplicate folders
```
/Users/joshd.millang/RAPID_API        ← WRONG
/Users/joshd.millang/Projects/RAPID_API  ← CORRECT
```

### ✅ DO: Keep one copy in Projects/
```
/Users/joshd.millang/Projects/RAPID_API  ← Only one copy here
```

## Verifying Your Setup

Run this to check all projects:

```bash
cd /Users/joshd.millang/Projects

for dir in RAPID_CORE RAPID_IMPORT RAPID_API PRODASH sentinel; do
  echo "=== $dir ==="
  cd "$dir" 2>/dev/null && git remote -v && git status --short && cd ..
  echo ""
done
```

## After clasp push

**IMPORTANT**: For GAS web apps, after `clasp push` you must:

1. Open GAS Editor
2. Deploy → Manage deployments
3. Edit existing deployment OR create new
4. Click Deploy

The deployed version doesn't auto-update from `clasp push`!

## RAPID_CORE Library Issue

The RAPID_CORE library tends to "disappear" from GAS projects. If you see errors about the library not being found:

1. GAS Editor → Resources → Libraries
2. Add: `1-HKxgcOIkx6Ov2uXk6TU-yJM24cvB4ctyCTuqS3NLEBs5XA-FFGWGJSI`
3. Version: 2
4. Identifier: `RAPID_CORE`
5. **Redeploy the web app** (required!)
