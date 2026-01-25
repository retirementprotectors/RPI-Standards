---
name: MCP Setup + CAM Testing
overview: Configure GDrive and Slack MCPs in Cursor to establish the MDJ infrastructure foundation, verify MATRIX integration, then proceed with CAM UI/UX testing.
todos:
  - id: mcp-config
    content: Create ~/.cursor/mcp.json with GDrive + Slack servers
    status: completed
  - id: mcp-verify
    content: Restart Cursor, verify MCP tools available, complete OAuth
    status: completed
    dependencies:
      - mcp-config
  - id: matrix-test
    content: Read MATRIX spreadsheet to confirm GDrive MCP works
    status: completed
    dependencies:
      - mcp-verify
  - id: cam-testing
    content: UI/UX test all 5 CAM modules, fix bugs found
    status: in_progress
    dependencies:
      - matrix-test
---

# MDJ Communication Infrastructure + CAM UI/UX Testing

## Phase 1: Google Cloud Setup (One-Time)

Before MCPs work, need Google Cloud project with APIs enabled:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project: `RPI-MDJ-Platform`
3. Enable APIs:

   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Meet API (if available separately)

4. Create OAuth 2.0 credentials (Desktop app type)
5. Download `credentials.json`

## Phase 2: MCP Server Installation

Install the MCP servers locally:

```bash
# Gmail + Calendar combo (includes Meet scheduling)
npm install -g @anthropic/gmail-calendar-mcp

# Google Drive (for MATRIX)
npm install -g @anthropic/gdrive-mcp

# Slack
npm install -g @anthropic/slack-mcp

# Google Meet (standalone for transcripts/metadata)
npm install -g mcp-meet
```

## Phase 3: MCP Configuration

Create Cursor MCP config at `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/gdrive-mcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    "gmail-calendar": {
      "command": "npx",
      "args": ["-y", "@anthropic/gmail-calendar-mcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/slack-mcp"],
      "env": {
        "SLACK_BOT_TOKEN": "<from_slack_app>",
        "SLACK_TEAM_ID": "<workspace_id>"
      }
    },
    "google-meet": {
      "command": "npx",
      "args": ["-y", "mcp-meet"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

After creating config:

- Restart Cursor to load MCP servers
- First use triggers OAuth consent flow

## Phase 4: Verify All Integrations

| MCP | Test Command | Expected Result |

|-----|--------------|-----------------|

| **GDrive** | Read MATRIX spreadsheet | See `_PIPELINE`, `_REVENUE_MASTER` tabs |

| **Gmail** | Search recent emails | List of threads |

| **Calendar** | Get today's events | Meeting list |

| **Meet** | List recent meetings | Meeting metadata |

| **Slack** | List channels | RPI workspace channels |

MATRIX Spreadsheet ID: `1XSQOIW6v-ntyGZKeDYOq8rssveViGiIrRiow5g3jSpQ`

## Phase 5: CAM UI/UX Testing

With full MCP access, test all 5 CAM modules against live data:

| Module | Test Focus |

|--------|------------|

| **Calculator** | B2B vs B2C tier dropdowns, calculation accuracy |

| **Pipeline** | Kanban board rendering, status transitions |

| **Revenue** | FYC/REN breakdown, policy lifecycle |

| **Commission** | Comp cycle dashboard, payout views |

| **Analytics** | KPI cards, leaderboard, charts |

Fix bugs as found, redeploy via `clasp push` + version.

## MDJ Communication Stack Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    MDJ AI INTERFACE                         │
├─────────────────────────────────────────────────────────────┤
│  gdrive-mcp    gmail-mcp    calendar-mcp    slack-mcp      │
│       │             │             │              │          │
│   MATRIX       Email        Meetings        Team Chat      │
│   Documents    Threads      Scheduling      Channels       │
│   Sheets       Attachments  Meet Links      Alerts         │
└─────────────────────────────────────────────────────────────┘
```

## Key Files

- MCP Config: `~/.cursor/mcp.json` (to create)
- Google Creds: `~/credentials.json` (from GCP)
- CAM Frontend: [`Index.html`](Index.html), [`Scripts.html`](Scripts.html), [`Styles.html`](Styles.html)
- CAM Backend: [`Code.gs`](Code.gs) (router)
- Production URL: https://script.google.com/macros/s/AKfycbyMYKIv_mRv9yf6exai1T-bLU-UsyDbAyCY9jbbdT8FXfuZHUOTZL9LLscIevB8J4oG/exec