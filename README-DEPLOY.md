# ViralMint — Full App Export (Phases 0–10)

This package is the **complete app** we built: base ViralMint + all custom
caption, clipping, removal, and finishing features.

**Git tip when exported:** `4238626`  
**Tests:** 453 passed  

---

## What's inside

```
ViralMint/                     # Full runnable project
  backend/                     # FastAPI + all new packages
  frontend/                    # React UI (dist/ already built)
  docs/                        # Design docs
  tests/                       # Full test suite
  run.py                       # Local launcher
VIRALMINT-COMPLETE-GUIDE.md    # Master guide + key code
ViralMint-phases-0-10-source.zip  # Packages-only archive
README-DEPLOY.md               # This file
```

New packages we added:
- `backend/caption_core/` — timing, animation, presets, ASS bridge
- `backend/clip_intelligence/` — scoring, hooks, enhancement
- `backend/caption_removal/` — detect/remove burned-in captions
- `backend/production_pipeline/` — reframe, audio, export, batch
- `frontend/src/pages/Studio.jsx` — Finish Studio
- CapCut-style captions UI, Clip Studio scoring panel

---

## Run locally (recommended first)

### Requirements
- Python **3.11+**
- Node **18+**
- FFmpeg + FFprobe on PATH
- ImageMagick (`convert` or `magick`)

### Steps

```bash
cd ViralMint

# 1) Python deps
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Frontend (dist/ is already built; rebuild if you change UI)
cd frontend
npm install
npm run build
cd ..

# 3) Env file
cp .env.example .env
# optional: add OPENAI_API_KEY / ANTHROPIC_API_KEY / OPENROUTER_API_KEY in .env
# or paste keys later in Settings UI

# 4) Launch
python run.py
```

Open: **http://127.0.0.1:16888**

### Key pages
| URL | What |
|-----|------|
| `/` | Chat |
| `/studio` | **Finish Studio** (reframe + export) |
| `/clips` | Clip Studio (score moments) |
| `/tools/captions` | CapCut-style caption templates |
| `/docs` | API docs |

---

## Deploy for a permanent link

You need a host that runs **Python + Node build + FFmpeg**.

### Option A — Railway / Render / Fly.io (easiest permanent URL)

1. Create a new project from this folder (or push to GitHub and connect).
2. Build command:
   ```bash
   pip install -r requirements.txt && cd frontend && npm install && npm run build && cd ..
   ```
3. Start command:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add system packages if the host allows: `ffmpeg`, `imagemagick`.
5. Set env vars: `HOST=0.0.0.0`, optional AI keys.
6. You get a permanent URL like `https://your-app.up.railway.app`.

### Option B — VPS (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv ffmpeg imagemagick nodejs npm nginx
# copy project, then same local steps
# put nginx reverse-proxy to 127.0.0.1:16888
# add your domain DNS A record → VPS IP
```

### Option C — Docker (if you add a Dockerfile later)

Use a image with Python 3.11 + Node + FFmpeg, run uvicorn on port 8000/16888.

---

## Why we couldn't deploy a permanent URL from the sandbox

The build environment only supports **temporary tunnels** (Cloudflare quick tunnel / localtunnel).  
Those URLs die when the session ends. A **permanent** link needs **your** hosting account or VPS.

---

## License

ViralMint is **AGPL-3.0**. Keep attribution and license files when you redistribute.

---

## Tests

```bash
cd ViralMint
source .venv/bin/activate
pytest tests/ -q
```

---

Enjoy — go ship it.
