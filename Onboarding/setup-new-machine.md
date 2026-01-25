# MCP Setup for New Machine

> Complete guide to setting up MCPs on a fresh machine.

---

## Prerequisites

- [ ] macOS (these instructions assume Mac)
- [ ] Admin access to install software
- [ ] Access to Google account (joshd.millang@gmail.com or RPI account)
- [ ] Access to this repo (for config files)

---

## Step 1: Install Required Software

### Node.js
```bash
# With Homebrew (recommended)
brew install node

# Or download from https://nodejs.org
```

Verify:
```bash
node --version
# Should show v18+ or higher
```

### Cursor IDE
Download from https://cursor.sh and install.

---

## Step 2: Copy Configuration Files

### MCP Config
```bash
# Create Cursor config folder if it doesn't exist
mkdir -p ~/.cursor

# Copy mcp.json from this repo
cp /Users/joshd.millang/Projects/MCP-Hub/mcp.json ~/.cursor/mcp.json
```

### Google OAuth Credentials
```bash
# Create credentials folder
mkdir -p ~/.config/rpi-mcp

# Copy from backup or existing machine
# These files are NOT in git (sensitive)
cp [SOURCE]/gcp-oauth.keys.json ~/.config/rpi-mcp/gcp-oauth.keys.json
cp [SOURCE]/credentials.json ~/.config/rpi-mcp/credentials.json
```

**If you don't have these files:**
- Ask JDM for the Google Cloud OAuth credentials
- Or set up new OAuth credentials in Google Cloud Console

---

## Step 3: Authenticate Google Services

Each Google service needs you to log in via browser once.

### Google Drive
```bash
GOOGLE_DRIVE_OAUTH_CREDENTIALS=~/.config/rpi-mcp/gcp-oauth.keys.json \
npx @piotr-agier/google-drive-mcp auth
```
- Browser opens → Log in with Google → Authorize → Done

### Gmail
```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```
- Browser opens → Log in with Google → Authorize → Done

### Google Calendar
```bash
GOOGLE_OAUTH_CREDENTIALS=~/.config/rpi-mcp/credentials.json \
npx @cocal/google-calendar-mcp auth
```
- Browser opens → Log in with Google → Authorize → Done

---

## Step 4: Install RPI-Built MCPs

### Clone MCP-Hub (if not already done)
```bash
cd ~/Projects  # or wherever you keep projects
git clone https://github.com/retirementprotectors/MCP-Hub.git
cd MCP-Hub
```

### Healthcare MCPs
```bash
cd healthcare-mcps
npm install
```
**This automatically downloads ~2.5GB of CMS data** (plans, formulary, pharmacy networks). Takes a few minutes on first run.

### Commission Intelligence MCP
```bash
cd ../commission-intelligence
npm install
```

### Meeting Processor MCP
```bash
cd ../rpi-meeting-processor
npm install
```

---

## Step 5: Restart Cursor

Quit Cursor completely and reopen it. MCPs load on startup.

---

## Step 6: Verify Setup

In Cursor:
1. Go to **Settings** → **Tools & MCP**
2. You should see all servers listed:
   - `gdrive` - Connected
   - `gmail` - Connected
   - `google-calendar` - Connected
   - `slack` - Connected
   - `playwright` - Connected
   - `npi-registry` - Connected
   - `medicare-plans` - Connected
   - `commission-intelligence` - Connected

### Test Each MCP

**GDrive:**
> "Search my Google Drive for 'MATRIX'"

**Gmail:**
> "Check my inbox for the most recent email"

**Calendar:**
> "What's on my calendar today?"

**Slack:**
> "List Slack channels"

**Playwright:**
> "Take a screenshot of google.com"

**Healthcare:**
> "Look up NPI 1234567890"

**Commission Intelligence:**
> "What's Aetna Level 13 paying for Plan G in Iowa?"

---

## Slack Notes

Slack tokens are already in `mcp.json` - no additional auth needed.

The tokens work across machines. If they ever expire:
1. Go to api.slack.com/apps
2. Find the RPI Slack app
3. OAuth & Permissions
4. Copy new tokens
5. Update `~/.cursor/mcp.json`

---

## Quick Checklist

- [ ] Node.js installed (`node --version`)
- [ ] Cursor installed
- [ ] MCP-Hub repo cloned
- [ ] `~/.cursor/mcp.json` exists
- [ ] `~/.config/rpi-mcp/gcp-oauth.keys.json` exists
- [ ] `~/.config/rpi-mcp/credentials.json` exists
- [ ] GDrive auth completed (browser login)
- [ ] Gmail auth completed (browser login)
- [ ] Calendar auth completed (browser login)
- [ ] Healthcare MCPs installed (`cd healthcare-mcps && npm install`)
- [ ] Commission Intelligence MCP installed (`cd commission-intelligence && npm install`)
- [ ] Meeting Processor MCP installed (`cd rpi-meeting-processor && npm install`)
- [ ] Cursor restarted
- [ ] All MCPs show "Connected" in Settings

---

## Troubleshooting

### MCP shows "Error" in Settings

1. Check Node.js: `node --version`
2. Try running the MCP manually to see error:
   ```bash
   npx @piotr-agier/google-drive-mcp
   ```
3. Check credentials exist:
   ```bash
   ls -la ~/.config/rpi-mcp/
   ```

### "Command not found" for npx

Node.js not installed or not in PATH. Reinstall Node.js.

### OAuth "redirect_uri_mismatch"

The OAuth credentials may not be configured for localhost redirect. Ask JDM for updated credentials.

### Tokens expired after working previously

Re-run the auth commands in Step 3.

---

## If Something Breaks

Just tell Claude. Claude will fix it.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Jan 22, 2026 | Consolidated from various sources |
