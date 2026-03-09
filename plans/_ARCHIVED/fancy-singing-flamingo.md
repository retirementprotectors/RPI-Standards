# Plan: Add Google Veo (AI Video Generation) to MCP Hub

## Context
JDM wants AI video generation capabilities in the MCP Hub toolkit. Google's Veo 3.1 API (the engine behind Google Vids) enables text-to-video and image-to-video generation. Adding this to `rpi-workspace-mcp` gives us video creation alongside WordPress/Canva tools — useful for social media clips, marketing content, website visuals, and client-facing video snippets.

## Prerequisites
- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/apikey) using existing GCP project `90741179392`
- Store at `~/.config/rpi-mcp/gemini-credentials.json` as `{ "api_key": "..." }`

## Files to Create/Modify

### 1. Create `rpi-workspace-mcp/src/video-tools.js`

New tool module following existing `{ TOOLS, HANDLERS }` pattern (same as `wordpress-tools.js`).

**5 Tools:**

| Tool | Purpose |
|------|---------|
| `generate_video` | Text-to-video via Veo 3.1 — returns operation ID for async polling |
| `generate_video_from_image` | Image-to-video — provide image URL as starting frame |
| `check_video_status` | Poll an operation ID to check if video generation is complete |
| `download_video` | Download completed video MP4 to local path |
| `list_video_models` | List available Veo models and capabilities |

**Verified API Details:**
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning`
- **Models**: `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`
- **Auth**: `x-goog-api-key` header with Gemini API key
- **Parameters**: `prompt`, `aspectRatio` (16:9 / 9:16), `duration` (4s/6s/8s), `sampleCount` (1-4), `seed` (optional)
- **Polling**: GET `https://generativelanguage.googleapis.com/v1beta/{operation_name}`
- **Output**: MP4 with audio, 24fps, SynthID watermarked, expires in 2 days
- **Rate limits**: ~10-50 req/min depending on model variant

**Credential loading pattern** — reuses from `wordpress-tools.js`:
```javascript
import { ok, err } from "./auth.js";
import fs from "fs";
import path from "path";

const CREDS_FILE = path.join(process.env.HOME, ".config/rpi-mcp/gemini-credentials.json");

function loadApiKey() {
  if (!fs.existsSync(CREDS_FILE)) {
    throw new Error("No Gemini credentials found. Run: npm run setup:gemini");
  }
  return JSON.parse(fs.readFileSync(CREDS_FILE, "utf8")).api_key;
}
```

### 2. Modify `rpi-workspace-mcp/src/index.js`

Add import + spread (line 28-29 area):
```javascript
import { TOOLS as videoTools, HANDLERS as videoHandlers } from "./video-tools.js";

const ALL_TOOLS = [...gasTools, ...chatTools, ...peopleTools, ...wordpressTools, ...canvaTools, ...videoTools];
const ALL_HANDLERS = { ...gasHandlers, ...chatHandlers, ...peopleHandlers, ...wordpressHandlers, ...canvaHandlers, ...videoHandlers };
```

Update startup log (line 70):
```javascript
`RPI Workspace MCP running — ${ALL_TOOLS.length} tools (GAS: ${gasTools.length}, Chat: ${chatTools.length}, People: ${peopleTools.length}, WordPress: ${wordpressTools.length}, Canva: ${canvaTools.length}, Video: ${videoTools.length})`
```

### 3. Create `rpi-workspace-mcp/scripts/setup-gemini.js`

Interactive setup script matching `setup-wordpress.js` pattern:
- Prompts for Gemini API key
- Verifies by calling `GET /v1beta/models?key={key}`
- Saves to `~/.config/rpi-mcp/gemini-credentials.json`

### 4. Update `rpi-workspace-mcp/package.json`

Add script: `"setup:gemini": "node scripts/setup-gemini.js"`

### 5. Update `CLAUDE.md`

- Update rpi-workspace tool count and add Video to contains list
- Add `video-tools.js` to directory structure

## Implementation Notes

- Uses native `fetch()` — **no new npm dependencies**
- Async workflow: submit request → get operation name → poll → download when done
- Videos expire after 2 days — `download_video` saves MP4 locally
- Default output path: `~/Downloads/` (configurable per call)
- Credential file at `~/.config/rpi-mcp/gemini-credentials.json` (gitignored, same dir as other creds)

## Verification
1. `node -e "import('./src/video-tools.js').then(m => console.log(m.TOOLS.length))"` → should print `5`
2. `node src/index.js` → server starts, logs updated tool count
3. `list_video_models` → returns available Veo models (verifies API key works)
4. `generate_video` with simple prompt → returns operation ID
5. `check_video_status` → polls until done
6. `download_video` → saves MP4 locally
