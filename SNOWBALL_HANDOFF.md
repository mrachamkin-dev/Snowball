# Snowball Handoff Document

**Date:** April 6, 2026
**App:** [snowball-ten.vercel.app](https://snowball-ten.vercel.app)
**Owner:** Matt (matt@threemightylions.com)

---

## What is Snowball

A social app that turns real-life stories into cinematic short videos with a viral share loop: **Tell > Make > Throw > Respond > Loop**. Users either speak/type a story or upload photos, AI shapes it into a narrated video with generated images, and they "throw" it to friends who can watch, respond, or remix.

---

## Architecture

**Single-file frontend.** The entire app lives in `index.html` (~663 lines). All screens, state, prompts, and logic are in one `<script>` block. This file is extremely fragile — a single mismatched brace or paren breaks everything.

**Key files:**

| File | Lines | Purpose |
|------|-------|---------|
| `index.html` | 663 | Entire app: all screens, AI prompts, state management |
| `player.html` | 223 | Receiver page at `/s/:id` with splat animation |
| `music.js` | 240 | Web Audio procedural music engine (SnowballMusic) — **DO NOT TOUCH** |
| `recorder.js` | 98 | Audio recording for speak flow |
| `api/claude.js` | — | Proxy to Claude API |
| `api/image.js` | — | Proxy to image generation |
| `api/voice.js` | — | Proxy to ElevenLabs TTS |
| `api/share.js` | — | Saves story to Vercel Blob |
| `api/story.js` | — | Fetches story JSON from Vercel Blob by ID |
| `api/og.js` | — | Server-side OG meta tag injection for link previews |
| `api/music.js` | — | AI music generation |
| `api/render.js` | — | Video render trigger |
| `api/track.js` | — | Analytics event tracking |
| `vercel.json` | — | Rewrites `/s/:id` → `/api/og?id=:id`, function configs |
| `manifest.json` | — | PWA manifest |

**Infrastructure:** Vercel serverless functions, Vercel Blob storage (`4fhlr2aepdibhwh7.public.blob.vercel-storage.com`), ElevenLabs for voice, Claude for story shaping, image generation API.

---

## Design System

- **Fonts:** Cormorant Garamond italic 300 (`--serif`), Plus Jakarta Sans 300-500 (`--sans`)
- **Background:** `#060402`
- **Colors:** `--gold: #E5B444`, `--ice: #C2E4EE`, `--cream: #EEE8DC`
- **Vibe:** Dark, cinematic, premium. Minimal UI.

---

## Critical Development Rules

### Safe Patch Protocol
1. **One change at a time** → health check → commit → never push broken code
2. **Health check after every edit** — verify paren/brace/backtick balance and no `</script>` inside template literals:
```python
python3 << 'PYEOF'
for fname in ['index.html','player.html']:
    with open(fname,'r',encoding='utf-8') as f: h=f.read()
    start=h.find('<script>')+8; end=h.find('</script>',start); js=h[start:end]
    p=b=bt=0
    for c in js:
        if c=='(':p+=1
        elif c==')':p-=1
        elif c=='{':b+=1
        elif c=='}':b-=1
        elif c=='`':bt=1-bt
    result="CLEAN" if p==0 and b==0 and bt==0 and js.count('</script>')==0 else "BROKEN"
    print(f"{fname}: {result}")
PYEOF
```

### Editing index.html
- Lines are extremely long (some 10K+ characters). The `Edit` tool often fails on exact string matches.
- **Use Python scripts for replacements** — they're more reliable for this file.
- Always re-read after Python edits before using the Edit tool.

### Git
- **Git push is blocked from sandbox** (HTTP 403 from proxy). Matt must push from his machine.
- Currently **4 commits ahead of origin/main**.

### Do Not Touch
- `music.js` — Web Audio engine, thoroughly tested, fragile
- Session 2 brief said DO NOT TOUCH `PHOTO_SYS` but Matt explicitly overrode this for the no-AI-people fix

---

## Current State of the Code

### Screens (in index.html)
- `home` — Landing with interactive snowball canvas, prompts
- `type` — Text input for story
- `speak` — Audio recording flow
- `photos` — Photo upload (up to 4 photos)
- `building` — Build animation while AI processes story
- `remixing` — Remix animation while AI re-shapes
- `playback` — Full video playback with images, audio, captions, share flow
- `history` — Past stories list
- `error` — Error screen

### Key Flows

**Story Creation (type/speak):**
1. User enters text or records audio → `rawStory`
2. Genre picker shown → `forcedGenre`
3. `renderBuilding` → `shapeStory()` → generates narration, scenes, image prompts
4. Images generated sequentially via `generateImage()`
5. Speech generated via `generateSpeech()` (ElevenLabs, returns word timings)
6. Music generated in parallel
7. Story saved to blob, video render triggered
8. → `renderPlayback`

**Story Creation (photos):**
1. User uploads 1-4 photos → `userPhotos` array
2. `renderBuilding` → `shapeStoryFromPhotos()` sends photos + context to Claude
3. Claude returns `visualPlan` with mix of `user_photo` and `ai_generate` steps
4. `executeVisualPlan()` builds image array (user photos + AI images)
5. Same speech/music pipeline as above
6. `userPhotos` stored on story object for remix preservation

**Remix Flow:**
1. From playback "Remix it" button or receiver `?remix=` URL
2. Fetches original story narration from `story._original`
3. `renderRemixing` → `shapeStory()` with new genre
4. Generates new AI images + interleaves user photos if available
5. `_original` preserved across remix chain
6. `userPhotos` carried forward from original story

**Receiver Flow (player.html / og.js):**
1. `/s/:id` → `api/og.js` injects OG meta tags → serves player.html
2. Splat animation plays on load (canvas, 4 phases)
3. Story audio plays with image cycling
4. Post-audio CTAs: "Throw one back" (→ home), "Keep it going" (forward to friend), "Remix this one" (→ genre picker with story data)

### Image Cycling in Playback
- Uses `audio.timeupdate` event with segment boundaries
- `segBoundaries` built from `_segments` word counts
- First boundary capped at 18% to prevent first image lingering
- `lead=0.7` seconds for anticipatory transitions
- Ken Burns animations cycle through 4 variants

### Key Global Variables
- `screen` — current screen name
- `story` — current story object (images, audioUrl, narration, hook, etc.)
- `rawStory` — raw text input
- `userPhotos` — array of uploaded photo data URLs
- `currentGenre` / `forcedGenre` — genre state
- `_visualStyle` — visual style for image generation
- `activeListeners` — tracked event listeners for cleanup

### PHOTO_SYS Prompt (line 139)
Comprehensive prompt for photo-based story shaping. Key rules:
- Mines for the most surprising specific detail as hook
- PEOPLE RULE: Never generate AI versions of people in user photos. AI images show environments, landscapes, objects, details only.
- TONE RULE: Default to joy. Match photo energy.
- INVENTION RULE: Never invent biographical details not visible in photos.
- PERSPECTIVE RULE: Present tense, first person, inside the experience.
- Returns JSON: `{hook, location, narration, visualStyle, characterDescription, hookImagePrompt, caption, visualPlan}`

### executeVisualPlan (line 164)
- Iterates visual plan steps
- `user_photo` → uses uploaded photo directly
- `ai_generate` / `ai_from_reference` → generates via image API
- **Skips character description injection when user photos are present** (prevents AI from recreating people)

---

## Recent Changes (This Session)

| Commit | Description |
|--------|-------------|
| `c93d626` | First image cycles faster — cap first segment boundary at 18% |
| `2b02bc8` | AI images skip character description when user has photos with people |
| `8fa29bf` | Preserve user photos through remix flow (store on story, carry into remix, save in blob, restore from receiver) |
| `243a988` | Receiver remix shows genre picker, fetches original story first |

**Unpushed:** 4 commits ahead of origin/main (the 4 above).

---

## Prior Session Changes (Already Pushed)

- Music gain bumped 0.12→0.20 for audibility
- Web Audio always starts first, AI music takes over if loaded
- Prompt shimmer/glow removed from home screen
- Share button rewritten with progress bar, immediate `navigator.share` on iOS
- Remix always uses `_original.narration` as source
- Build orb starts at 48px (was 80px)
- Apple touch icon → icon-180.png
- Server-side OG meta tags via `api/og.js`
- Funnel analytics events
- Splat plays every visit (sessionStorage block removed)
- Splat visual impact increased
- Player.html SMS bug fixed (`++` → `+" "+`)
- Duplicate OG tags removed from player.html
- Soft CTA added to receiver page
- Forward button added to receiver

---

## Known Issues / Future Work

1. **Git push from sandbox blocked** — Matt needs to push 4 commits from his machine
2. **player.html has unstaged changes** — minor modifications, check `git diff player.html`
3. **User photos are data URLs locally but HTTP URLs in blob** — the blob payload only saves HTTP-based userPhoto URLs. Data URL photos from the current session work for local remix but won't survive a page reload. This is acceptable since photos are embedded in the `images` array which does get saved.
4. **Video render** — `triggerVideoRender` calls `/api/render` but actual Remotion rendering infrastructure may need setup (see `Snowball-Remotion-Spec.docx` and `remotion/` directory)
5. **No offline support** — PWA manifest exists but no service worker
6. **History audio expiration** — Stories saved to history with blob: audio URLs expire on page reload. HTTP audio URLs from ElevenLabs persist.

---

## Environment & Secrets

- `.env.local` contains API keys (Anthropic, ElevenLabs, Vercel Blob token, etc.)
- Never commit `.env.local` (in `.gitignore`)
- Vercel environment variables must match for deployed functions

---

## How to Work on This Codebase

1. Read `index.html` in sections (it's too large to read at once — use offset/limit)
2. Use Python scripts for string replacements (Edit tool is unreliable on long lines)
3. Run health check after every single edit
4. Commit after each successful change
5. Test flows mentally by tracing the code — the app is live at snowball-ten.vercel.app
6. When in doubt, search for function names with Grep — everything is in one file
