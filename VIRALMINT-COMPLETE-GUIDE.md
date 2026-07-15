# ViralMint — Complete Build Guide (Phases 0–10)

**Single master document** covering architecture, features, APIs, design notes, and core source code.

| Field | Value |
|-------|--------|
| Project | ViralMint (Crayo-style clipping + CapCut-style captions) |
| Fork with work | https://github.com/abxhjok/ViralMint |
| Final commit (Phase 10) | `4238626` |
| Tests | 453 passed |
| Generated | 2026-07-15 08:10 UTC |

> **Note:** This file is a **guide + key source**. The full monorepo is also provided as `ViralMint-phases-0-10-source.zip` (all new packages + docs + frontend pieces).  
> Permanent hosting still needs your own server/domain — see “Deploy” section.

---

## Table of contents

1. [What this product is](#what-this-product-is)
2. [Phase commits](#phase-commits)
3. [Features by phase](#features-by-phase)
4. [Architecture overview](#architecture-overview)
5. [Package / file tree](#package--file-tree)
6. [API map](#complete-api-map-new-endpoints)
7. [How to run](#how-to-run-locally)
8. [UI routes](#key-ui-routes)
9. [Caption templates](#caption-templates-phase-8)
10. [Deploy / permanent URL](#deploy--permanent-url)
11. [Design documents (full text)](#design-documents)
12. [Core source code](#core-source-code)

---

## What this product is

A **local-first** AI short-form workstation built on ViralMint:

- **Clipping intelligence** — score viral moments, hooks, enhancement plans  
- **CapCut-style captions** — animated presets, live preview, ASS/overlay export  
- **Caption removal** — detect/remove burned-in subs before re-captioning  
- **Finishing** — auto-reframe 9:16, audio polish, platform export, covers, batch  

Stack: **Python FastAPI backend** + **React/Vite frontend** + **FFmpeg**.

---

## Phase commits

| Phase | Commit | Message |
|-------|--------|---------|
| 0 | `5a4e9d5` | docs: analyze existing architecture and licenses |
| 1 | `b64941d` | feat(captions): add deterministic caption timing core |
| 2 | `9f434a4` | feat(captions): add deterministic animation composition engine |
| 3 | `8f79a12` | feat(captions): add deterministic animated caption preview |
| 4 | `0a20ed9` | feat(captions): unify preview and export caption rendering |
| 5 | `f68348c` | feat(captions): expand preset and customization system |
| 6 | `fca6bad` | feat(clipping): add deterministic viral clip scoring engine |
| 7 | `e9e7115` | feat(clipping): add intelligent clip enhancement pipeline |
| 8 | `c9f99ca` | feat(captions): add advanced CapCut-style caption effects |
| 9 | `815568e` | feat(video): add AI caption removal foundation |
| 10 | `4238626` | feat(video): add professional short-form finishing pipeline |


---


## Features by phase (what we built)

### Phase 0 — Research & baseline
- Repository analysis, license notes, research docs for caption/clip engines

### Phase 1 — Caption timing core
- `CaptionWord`, `CaptionSegment`, `CaptionStyle`, `CaptionPreset`
- Clip-local timing, active-word lookup, segmentation
- ASS bridge to existing FFmpeg burn path

### Phase 2 — Animation engine
- Frame-based deterministic evaluator
- Primitives: fade, scale, spring, bounce, glitch, typewriter, karaoke
- Composition rules, easing, events, registry

### Phase 3 — Animated preview
- Backend batch frame evaluation
- Frontend `AnimatedCaptionPreview` (renders state only, no JS formulas)
- Captions tool gallery

### Phase 4 — Unified preview + export
- Single `evaluate_frame_states` path for preview and export
- ASS-compat export + overlay export mode
- Generator/tools route animation presets through unified path

### Phase 5 — Preset registry & customization
- Validated `PresetRegistry` (no silent fallback)
- `ActiveWordConfig`, renderer compatibility
- Override merge: base preset + custom settings
- APIs: list / get / validate / resolve presets

### Phase 6 — Viral clip scoring
- Multi-signal deterministic scores (hook, emotion, energy, keywords, story, curiosity, pacing)
- Rule-based hook detection
- Candidate ranking, dedupe, overlap removal
- Clip Studio “Score moments” panel

### Phase 7 — Clip enhancement
- Silence analysis from transcript gaps
- Word/sentence boundary optimization
- Pacing metrics
- Enhancement plan (no render): bounds, captions, export settings

### Phase 8 — CapCut-style captions
- New primitives: pop, slide, glow, zoom, pulse, word_reveal
- Templates: TikTok Bold, MrBeast Style, Minimal, Gaming, Podcast, Karaoke Box
- Rounded active-word highlight boxes in preview
- Category + tag filters in UI

### Phase 9 — Burned-in caption removal
- Detect caption regions (priors + optional frame heuristics)
- Mask plans + preview PNG
- Pluggable removal: FFmpeg delogo (default), boxblur, noop
- Never overwrites source video

### Phase 10 — Finishing pipeline
- Auto-reframe plans (center / face / speaker / subject)
- Audio enhance (loudnorm, denoise, speech band)
- Optional video FX (sharpen, denoise, EQ)
- Export presets: TikTok, YouTube Shorts, Instagram Reels
- Batch jobs with retry
- Thumbnail/cover planning
- **Finish Studio** UI at `/studio`


---

## Architecture overview

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (React / Vite / MUI)                              │
│  /clips  /studio  /tools/captions  Library  Chat            │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP /api/*
┌───────────────────────────▼─────────────────────────────────┐
│  FastAPI                                                     │
│  captions · clip-intelligence · caption-removal · production │
└───┬─────────────┬──────────────┬──────────────┬─────────────┘
    │             │              │              │
    ▼             ▼              ▼              ▼
 caption_core  clip_intel   caption_removal  production_pipeline
 (timing +     (score +     (detect + mask  (reframe + audio
  animation +   enhance)     + delogo)        + export + batch)
  presets)
    │
    ▼
 caption_service (ASS) + ffmpeg_service (encode / burn / extract)
```

**Determinism principle:** animation and scoring are pure functions of inputs  
(frame, fps, words, weights) — no random wall-clock in the core evaluators.

---

## Package / file tree


### `backend/caption_core/`
```backend/caption_core/__init__.pybackend/caption_core/active_word.pybackend/caption_core/animation/__init__.pybackend/caption_core/animation/composition.pybackend/caption_core/animation/context.pybackend/caption_core/animation/easing.pybackend/caption_core/animation/evaluator.pybackend/caption_core/animation/events.pybackend/caption_core/animation/presets.pybackend/caption_core/animation/preview.pybackend/caption_core/animation/primitives.pybackend/caption_core/animation/registry.pybackend/caption_core/animation/render.pybackend/caption_core/animation/state.pybackend/caption_core/ass_bridge.pybackend/caption_core/enums.pybackend/caption_core/models.pybackend/caption_core/overrides.pybackend/caption_core/preset_registry.pybackend/caption_core/segmentation.pybackend/caption_core/timing.pybackend/caption_core/transcription.py```
### `backend/clip_intelligence/`
```backend/clip_intelligence/__init__.pybackend/clip_intelligence/boundaries.pybackend/clip_intelligence/enhancement.pybackend/clip_intelligence/hooks.pybackend/clip_intelligence/models.pybackend/clip_intelligence/pacing.pybackend/clip_intelligence/pipeline.pybackend/clip_intelligence/scoring.pybackend/clip_intelligence/selection.pybackend/clip_intelligence/silence.py```
### `backend/caption_removal/`
```backend/caption_removal/__init__.pybackend/caption_removal/detection.pybackend/caption_removal/masking.pybackend/caption_removal/models.pybackend/caption_removal/pipeline.pybackend/caption_removal/removal.py```
### `backend/production_pipeline/`
```backend/production_pipeline/__init__.pybackend/production_pipeline/audio.pybackend/production_pipeline/batch.pybackend/production_pipeline/export_presets.pybackend/production_pipeline/finisher.pybackend/production_pipeline/models.pybackend/production_pipeline/reframe.pybackend/production_pipeline/thumbnail.pybackend/production_pipeline/video_fx.py```

### Frontend pieces added/updated
```
frontend/src/pages/Studio.jsx
frontend/src/pages/tools/Captions.jsx
frontend/src/pages/ClipStudio.jsx
frontend/src/components/captions/AnimatedCaptionPreview.jsx
frontend/src/components/clips/ClipScorePanel.jsx
frontend/src/hooks/useCaptionPreview.js
frontend/src/App.jsx          # /studio route
frontend/src/components/Layout.jsx  # Finish Studio nav
```

### Docs
```
docs/CAPTION_CORE_DESIGN.md
docs/CLIP_SCORING_DESIGN.md
docs/CLIP_ENHANCEMENT_DESIGN.md
docs/CAPTION_REMOVAL_DESIGN.md
docs/PRODUCTION_PIPELINE_DESIGN.md
docs/REPOSITORY_ANALYSIS.md
docs/CAPTION_ENGINE_RESEARCH.md
docs/CLIPPING_ENGINE_RESEARCH.md
...
```


## Complete API map (new endpoints)

### Captions (Phases 1–5, 8)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/captions/styles` | Built-in + custom ASS styles |
| GET | `/api/captions/presets` | Registry presets + templates |
| GET | `/api/captions/presets/{id}` | Full preset config |
| POST | `/api/captions/presets/validate` | Validate overrides |
| POST | `/api/captions/presets/resolve` | Merged preset JSON |
| GET | `/api/captions/preview/presets` | Preview preset list |
| POST | `/api/captions/preview` | Animated frame-state preview |
| POST | `/api/captions/export/evaluate` | Shared evaluate path |
| POST | `/api/captions/export/ass` | ASS from unified path |

### Clip intelligence (Phases 6–7)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/clip-intelligence/weights` | Scoring weights |
| POST | `/api/clip-intelligence/score-window` | Score one window |
| POST | `/api/clip-intelligence/detect-hooks` | Hook detection |
| POST | `/api/clip-intelligence/analyze` | Rank clips from segments |
| POST | `/api/clip-intelligence/analyze/{video_id}` | Analyze stored transcript |
| POST | `/api/clip-intelligence/silence` | Silence intervals |
| POST | `/api/clip-intelligence/pacing` | Pacing metrics |
| POST | `/api/clip-intelligence/optimize-boundaries` | Boundary snap |
| POST | `/api/clip-intelligence/enhance-plan` | Full enhancement plan |

### Caption removal (Phase 9)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/caption-removal/backends` | delogo / boxblur / noop |
| POST | `/api/caption-removal/detect` | Region detection |
| POST | `/api/caption-removal/analyze-path` | Detect + mask for storage video |
| POST | `/api/caption-removal/mask` | Mask from regions |
| POST | `/api/caption-removal/process` | Upload → clean video |

### Production finishing (Phase 10)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/production/export-presets` | TikTok / Shorts / Reels |
| GET | `/api/production/track-modes` | Reframe modes |
| POST | `/api/production/reframe-plan` | Auto-reframe plan |
| POST | `/api/production/audio-filter` | Audio filter chain |
| POST | `/api/production/finish-plan` | Full finish plan |
| POST | `/api/production/thumbnail-plan` | Cover frame plan |
| POST | `/api/production/batch` | Create batch |
| GET | `/api/production/batch` | List batches |
| GET | `/api/production/batch/{id}` | Batch status |
| POST | `/api/production/batch/{id}/items/{item}/retry` | Retry item |
| POST | `/api/production/finish` | Upload → finished vertical video |



## How to run locally

```bash
git clone https://github.com/abxhjok/ViralMint.git   # or your fork with phases 1–10
cd ViralMint
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
python run.py
# open http://127.0.0.1:16888
```

### Key UI routes
| Route | Feature |
|-------|---------|
| `/` | Chat home |
| `/clips` | Clip Studio — score viral moments |
| `/studio` | **Finish Studio** — reframe + export |
| `/tools/captions` | CapCut-style caption templates |
| `/tools` | Other tools hub |
| `/docs` | OpenAPI docs |

### Tests
```bash
pytest tests/ -q          # 453+ passed at Phase 10
ruff check backend tests --select=E9,F63,F7,F82
cd frontend && npm run build
```


## Caption templates (Phase 8)

| ID | Name | Vibe |
|----|------|------|
| `bounce` | Bounce | Spring bounce |
| `explosive` | Explosive | Scale + fade entry |
| `glitch` | Glitch | Deterministic jitter |
| `typewriter` | Typewriter | Char reveal |
| `karaoke` | Karaoke | Highlight wipe |
| `tiktok_bold` | TikTok Bold | Pop + yellow active |
| `mrbeast_style` | MrBeast Style | Huge red bounce |
| `minimal_clean` | Minimal | Soft bottom captions |
| `gaming_neon` | Gaming | Neon glitch glow |
| `podcast_soft` | Podcast | Word reveal + box |
| `karaoke_box` | Karaoke Box | Wipe + rounded box |

Animation primitives:  
`fade`, `scale`, `spring`, `bounce`, `glitch`, `typewriter`, `karaoke`,  
`slide`, `pop`, `glow`, `zoom`, `pulse`, `word_reveal`

---

## Deploy / permanent URL

Temporary tunnels (`trycloudflare.com`, `loca.lt`, serveo) are **not permanent**.

For a permanent link:

1. Deploy this repo to Railway / Render / Fly.io / a VPS  
2. Optional: attach your domain  
3. Or use Cloudflare **Named Tunnel** with your domain  

See also the zip + this guide for full code ownership.

---

## Design documents

The following sections embed the project design docs written during Phases 0–10.



---

# Included design doc: `docs/CAPTION_CORE_DESIGN.md`

# Caption-Core Design

This document describes the deterministic caption timing core introduced in
Phase 1 and the deterministic frame-based animation engine added in Phase 2.
Both layers live under the existing ASS/FFmpeg pipeline and do not replace it.

## Scope

Phase 1 intentionally stopped at timing, structure, and an ASS compatibility bridge.
Phase 2 adds a renderer-independent animation composition engine:

- **In scope:** `CaptionWord`, `CaptionSegment`, timing coordinate systems,
  active-word lookup, deterministic segmentation, a bridge to the current
  ASS renderer, and the `backend/caption_core/animation/` engine.
- **Out of scope:** Remotion rendering, 60 presets, clipping scoring,
  boundary snapping, and smart reframe. The ASS pipeline does not yet consume
  the animation state.

## Core models

Defined in `backend/caption_core/models.py` as Pydantic v2 models:

- `CaptionWord`: `id`, `text`, `start_ms`, `end_ms`, `confidence`, `speaker_id`,
  `tags`, `emphasis`. Rejects `end_ms < start_ms`; zero-duration words are valid.
- `CaptionSegment`: `id`, `start_ms`, `end_ms`, `words`, `speaker_id`. Derives
  its time bounds from the ordered words it contains.
- `CaptionStyle`: ASS-compatible fields (`font_family`, `font_size_*`, `font_weight`,
  `text_color`, `active_word_color`, `stroke_*`, `alignment`, `words_per_group`,
  etc.) plus future-animation fields (`shadow_blur`, `background_color`,
  `letter_spacing`, `line_height`, `text_transform`). The `to_ass_style_dict()`
  method converts only the supported subset to the legacy ASS dict shape.
- `CaptionAnimation`: pure configuration (`type`, `duration_ms`, `delay_ms`,
  `easing`, `spring`, `intensity`, `parameters`).
- `CaptionPreset`: `id`, `name`, `category`, `description`, `style`, `layout`,
  `entry_animation`, `active_word_animation`, `exit_animation`, `effects`,
  `tag_rules`.

## Timing coordinate systems

All core timestamps are integer milliseconds.

- Source time: milliseconds from the original media start.
- Clip-local time: `source_ms - clip_start_ms`.
- `to_clip_local_time` / `to_source_time` are pure arithmetic.
- `shift_words` returns new `CaptionWord` objects with shifted timestamps.
- `trim_words_to_clip` selects words that overlap the clip window using a
  half-open interval (`word.start < clip_end` and `word.end > clip_start`).
- `normalize_words_to_clip` trims and rewrites timestamps to clip-local time,
  clamping partial overlaps to `[0, clip_duration]` and dropping any word that
  becomes zero-duration at a boundary.

## Active-word boundary behavior

`find_active_word_index(words, current_time_ms)` in
`backend/caption_core/active_word.py`:

- Uses `start_ms <= current_time_ms < end_ms` (half-open).
- Returns `None` for empty arrays or times in gaps.
- For overlapping words, deterministic priority is:
  1. non-zero-duration words over zero-duration marker words,
  2. earlier `start_ms`,
  3. shorter duration,
  4. lower list index.
- Zero-duration words (`start_ms == end_ms`) are active only at that exact
  millisecond when no non-zero-duration word covers it.

## Segmentation rules

`segment_words(words, SegmentationConfig)` in `backend/caption_core/segmentation.py`:

- Input: ordered `CaptionWord` list.
- Output: ordered `CaptionSegment` list.
- Constraint order:
  1. `max_gap_ms` — a silence gap larger than this forces a new segment.
  2. `max_words_per_segment`.
  3. `max_chars_per_segment` (calculated on joined text including spaces).
  4. `max_duration_ms`.
  5. `prefer_punctuation` — when a hard limit is reached, the segment is closed
     at the most recent sentence-ending punctuation split point if one exists;
     otherwise it is closed immediately before the word that would exceed the
     limit.
- Words are never reordered, duplicated, or silently dropped.

## Transcription adapter

`words_from_transcription` in `backend/caption_core/transcription.py` converts the
existing faster-whisper / legacy segment format into `CaptionWord` objects:

- Reads `word` or `text`, `start`, `end`, `probability`/`confidence`, and
  `speaker`/`speaker_id`.
- Rounds seconds to integer milliseconds.
- Preserves confidence and speaker when present; uses safe `None` defaults when
  they are missing.
- Falls back to evenly splitting segment `text` when per-word timestamps are not
  available.

## ASS compatibility bridge

`backend/caption_core/ass_bridge.py` provides:

- `words_to_legacy_segments`: converts `list[CaptionWord]` into the
  `{"start", "end", "text", "words"}` shape consumed by `caption_service`.
- `core_style_to_legacy_dict`: converts `CaptionStyle` to the legacy style dict.
- `generate_captions_from_core`: generates an ASS file from core data by calling
  the existing `caption_service.generate_captions_ass` with a `style_config`
  override.

`backend/services/caption_service.py` was updated to accept an optional
`style_config` dict. When supplied, it bypasses the style-name lookup and uses
that config directly, so the existing ASS renderer can consume the new core
structures without being rewritten.

## File layout

```text
backend/caption_core/
  __init__.py
  enums.py          # CaptionCategory, CaptionAnimationType, CaptionEasing
  models.py         # Pydantic models
  timing.py         # source/clip-local utilities
  active_word.py    # deterministic active word
  segmentation.py   # deterministic segmentation
  transcription.py  # Whisper -> CaptionWord adapter
  ass_bridge.py     # bridge to existing ASS pipeline
```

Tests live in `tests/caption_core/` and `tests/caption_core/animation/`.

## Visual-state model

`CaptionVisualState` in `backend/caption_core/animation/state.py` is an
immutable Pydantic model that describes how one word is drawn at one frame.

Renderer-neutral units:

| property | default | unit | clamp |
|----------|---------|------|-------|
| `opacity` | `1.0` | dimensionless | `[0, 1]` |
| `scale` | `1.0` | multiplier | `>= 0` |
| `translate_x` / `translate_y` | `0.0` | screen units (logical px) | none |
| `rotation` | `0.0` | degrees | none |
| `blur` | `0.0` | screen units | final `>= 0` |
| `glow` | `0.0` | screen units | final `>= 0` |
| `letter_spacing` | `0.0` | screen units | none |
| `highlight_progress` | `0.0` | dimensionless | `[0, 1]` |
| `reveal_progress` | `0.0` | dimensionless | `[0, 1]` |

`reveal_progress` is a Phase 2 extension used by the typewriter primitive.

## Frame/time conversion

`backend/caption_core/animation/context.py` provides:

- `frame_to_ms(frame, fps) -> int`: rounds to the nearest millisecond.
- `ms_to_frame(ms, fps) -> int`: rounds to the nearest frame.
- `AnimationContext`: the deterministic context passed to every primitive,
  containing `frame`, `fps`, `current_time_ms`, the target `word`, `segment`,
  `word_index`, `active_word_index`, `animation_config`, `trigger`, and
  `trigger_time_ms`.

No `time.time()`, `datetime.now()`, JavaScript timers, or browser state is used.

## Animation composition rules

`compose_animations(base, contributions)` in
`backend/caption_core/animation/composition.py` applies an ordered list of
primitive outputs to a base state:

- `opacity` → multiplicative
- `scale` → multiplicative
- `translate_x` / `translate_y` → additive
- `rotation` → additive
- `blur` / `glow` → additive, clamped to a final minimum of `0`
- `letter_spacing` → additive
- `highlight_progress` → maximum
- `reveal_progress` → maximum

The base object is never mutated.

## Easing

`backend/caption_core/animation/easing.py` provides pure functions:

- `ease_linear`, `ease_in`, `ease_out`, `ease_in_out`
- `clamp01`, `lerp(start, end, t)`
- `calculate_progress(start_ms, duration_ms, current_time_ms)` with handling for
  zero duration, negative time, and post-completion.

## Primitives

All primitives are pure functions `AnimationContext -> CaptionVisualState` in
`backend/caption_core/animation/primitives.py`:

- `evaluate_fade` — fade in or out (`direction`, `duration_ms`, `delay_ms`, `easing`).
- `evaluate_scale` — scale between `from_scale` and `to_scale`.
- `evaluate_spring` / `_spring_displacement` — deterministic underdamped
  harmonic oscillator `x(t) = A * exp(-zeta * omega * t) * sin(omega_d * t)`.
- `evaluate_bounce` — vertical or scale bounce using the spring function.
- `evaluate_glitch` — deterministic jitter derived from a SHA-256 seed of
  `word.id`, `word_index`, and `frame`.
- `evaluate_typewriter` — computes `reveal_progress`.
- `evaluate_karaoke` — computes `highlight_progress` over a word.

`visible_character_count` and `visible_text` support Unicode grapheme clusters.

## Spring implementation

The spring uses the standard underdamped equation:

```
omega = sqrt(k / m)
zeta  = c / (2 * sqrt(m * k))
omega_d = omega * sqrt(1 - zeta^2)
x(t) = A * exp(-zeta * omega * t) * sin(omega_d * t)
```

Invalid or unstable parameters are protected by clamping `zeta` to `< 1` and
ensuring `omega` and `mass` are positive.

## Deterministic glitch seeding

`evaluate_glitch` builds a stable SHA-256 seed from:

```
{seed_offset}:{word_index}:{word.id}:{frame // frequency}
```

The digest is converted to deterministic signed floats. The same
`(word, word_index, frame, frequency, seed_offset)` tuple always returns the
same `translate_x`, `translate_y`, `rotation`, `opacity`, `glow`, and `blur`
values.

## Animation registry

`backend/caption_core/animation/registry.py` maps these animation type
identifiers to primitive implementations:

`fade`, `scale`, `spring`, `bounce`, `glitch`, `typewriter`, `karaoke`.

Unknown types raise `ValueError` from `dispatch_animation`.

## Event evaluation semantics

`backend/caption_core/animation/events.py` provides `is_event_active(trigger,
word, segment, current_time_ms, animation, ...)`. Conceptual triggers are:

- `SEGMENT_ENTER`
- `SEGMENT_EXIT`
- `WORD_ENTER`
- `WORD_ACTIVE`
- `WORD_EXIT`

This is a pure timing check, not a runtime event emitter. `WORD_ACTIVE` is
active for the inclusive word interval and is restricted to the active word.
Enter/exit/segment events are active for their configured `duration_ms` after
a trigger-time plus `delay_ms`.

## Frame-state evaluator

`evaluate_caption_word_state(word, word_index, segment, preset, frame, fps)`
in `backend/caption_core/animation/evaluator.py` is the canonical API:

1. Convert `frame`/`fps` to `current_time_ms`.
2. Find `active_word_index`.
3. Collect applicable `AnimationContext` objects by checking each trigger.
4. Dispatch each context through `dispatch_animation`.
5. `compose_animations` into a final `CaptionVisualState`.

A word is visible (base opacity `1`) when it is the active word or is affected
by an enter/exit/segment event; otherwise the base opacity is `0` so
word-by-word presets hide inactive words.

## Initial presets

`backend/caption_core/animation/presets.py` defines five engine-verification
presets via configuration only:

- `Bounce` — spring vertical bounce on active word.
- `Explosive` — fade in + scale up + scale bounce on entry.
- `Glitch` — deterministic jitter while active.
- `Typewriter` — character reveal by active word.
- `Karaoke` — highlight progress mapped to word duration.

## Phase 3: Animated caption preview

### Preview transport architecture

The frontend does not run animation formulas. Instead, it requests a short,
pre-computed frame-state timeline from the backend and renders it:

```
frontend AnimatedCaptionPreview
  -> useCaptionPreview
  -> POST /api/captions/preview
  -> backend PreviewRequest validation
  -> evaluate_preview_batch
  -> evaluate_caption_word_state per word, per frame
  -> JSON array of frames, each with per-word CaptionVisualState
  -> frontend maps state to CSS (opacity, transform, filter, text-shadow, etc.)
```

This keeps the canonical evaluator as the single source of truth for all
animation math.

### Batch evaluation

`backend/caption_core/animation/preview.py` provides `evaluate_preview_batch`.
It accepts a `PreviewRequest` (`words`, `preset_id`, `fps`, `start_frame`,
`end_frame`, `frame_step`) and returns every requested frame. To keep requests
small and responsive:

- Maximum 180 frames per preview.
- Maximum 6,000ms preview duration.
- Maximum 50 words per preview.
- Optional `frame_step` lets the client trade smoothness for payload size
  (preset cards use `frame_step=2`).

Batch results are verified against direct `evaluate_caption_word_state` calls
in `tests/caption_core/animation/test_preview.py`.

### Preview API contract

`POST /api/captions/preview` returns:

```json
{
  "preset_id": "bounce",
  "fps": 30,
  "start_frame": 0,
  "end_frame": 72,
  "frame_step": 1,
  "frame_count": 73,
  "frames": [
    {
      "frame": 0,
      "time_ms": 0,
      "words": [
        {
          "text": "Create",
          "word_index": 0,
          "active": true,
          "opacity": 1.0,
          "scale": 1.0,
          "translate_x": 0.0,
          "translate_y": 0.0,
          "rotation": 0.0,
          "blur": 0.0,
          "glow": 0.0,
          "letter_spacing": 0.0,
          "highlight_progress": 0.0,
          "reveal_progress": 0.0
        }
      ]
    }
  ]
}
```

`GET /api/captions/preview/presets` lists the five Phase 2 presets.
`POST /api/captions/preview/invalidate-cache` clears the process-local cache.

### Frontend renderer mapping

`frontend/src/components/captions/AnimatedCaptionPreview.jsx` maps each
backend state field to browser presentation:

| state field | CSS / DOM mapping |
|-------------|-------------------|
| `opacity` | `style.opacity` |
| `scale`, `translate_*`, `rotation` | `transform: translate(...) scale(...) rotate(...)` |
| `blur` | `filter: blur(...)` |
| `glow` | `text-shadow: 0 0 ${glow}px currentColor` |
| `letter_spacing` | `letterSpacing` |
| `reveal_progress` | `visibleText(text, reveal_progress)` slices Unicode grapheme clusters |
| `highlight_progress` | overlay span clipped to `progress * 100%` width |

No spring, bounce, glitch, typewriter, or karaoke math is performed in JS.

### Video-time-to-frame conversion

The current preview is standalone (sample caption) and not tied to a loaded
`<video>`. When integrated with a video element in the future, the rule is:

```
frame = round(currentTime * fps)
```

The frame is always derived from `video.currentTime` on each `timeupdate` or
`requestAnimationFrame` tick, not by incrementing a fake counter. This avoids
cumulative drift. The same `frame` and `fps` always resolve to the same
`current_time_ms` on the backend.

### Preview cache

`PreviewCache` in `backend/caption_core/animation/preview.py` is an in-process,
bounded LRU with TTL:

- Key = SHA-256 of the serialized preview request (words, preset, fps, frame
  range, frame step).
- `maxsize` = 128 entries.
- `ttl_seconds` = 300.
- Invalidation is implicit because any input change produces a new key; the
  `invalidate` endpoint clears all entries.

### Known preview limitations

- The preview uses a short sample caption in the `ToolCaptions` page; real clip
  transcripts are not yet wired in (that requires clip-local timing + transcript
  storage on generated clips, which is out of Phase 3 scope).
- Video playback scrubbing is not yet implemented because the preview is not
  currently attached to a video element. The deterministic frame-state evaluator
  supports it; only the player glue is missing.
- Preset cards intentionally use `frame_step=2` and a 1.6s duration to keep
  payloads small and avoid per-card full-FFmpeg rendering.
- The front-end `Intl.Segmenter` is the preferred grapheme splitter; the
  fallback `Array.from(text)` splits by code point, which is safe but not
  cluster-perfect for complex combining marks.

## ASS integration status (Phases 1–3)

Through Phase 3 the existing `caption_service.py` ASS renderer remained the
export path, while the animation engine was a parallel, renderer-neutral state
layer used only by the interactive preview.

## Phase 4: Unified preview and export rendering

Phase 4 makes the Phase 2 evaluator the **single source of truth** for caption
visual state across preview and export.

### Shared evaluation path

```
words + preset + frame + fps
  → evaluate_frame_states / evaluate_frame_range
       (backend/caption_core/animation/render.py)
  → FrameWordStates (per-word CaptionVisualState fields)

Preview:  evaluate_preview_batch → evaluate_frame_range
Export:   generate_captions_for_style / export_captions_unified
            → same evaluate_frame_states (overlay)
            → or active-word timing aligned with find_active_word_index (ASS)
```

`backend/caption_core/animation/preview.py` no longer calls
`evaluate_caption_word_state` directly; it delegates to `evaluate_frame_range`
so the JSON preview payload is byte-for-byte the same shape as export
evaluation.

### Export modes

| Mode | Module entry | Fidelity | Runtime deps |
|------|--------------|----------|--------------|
| **`ass_compat`** (default) | `generate_ass_from_evaluator` → `burn_captions` | Active-word color + grouping from preset layout; timing uses `find_active_word_index` (same half-open rule as the engine). Bounce/glitch/scale/typewriter motion is **approximated** (not pixel-perfect ASS motion). | FFmpeg `ass` filter (existing) |
| **`overlay`** | `burn_animated_overlay` | Full evaluator motion rasterized with Pillow per frame, then FFmpeg overlay. | FFmpeg + Pillow |

`visual_state_to_ass_overrides` maps a subset of state (`opacity`, `scale`,
`rotation`, `blur`) to ASS tags when richer tagging is needed; the default
ASS-compat path relies on active-word color for player compatibility.

### Pipeline wiring

Call sites that previously always used `caption_service.generate_captions_ass`
now go through `generate_captions_for_style`:

- `backend/agents/generator.py` (`_burn_captions`)
- `backend/core/tool_runners.py` (`run_tool_captions`, translate captions)

Routing rule:

- Style id ∈ `{bounce, explosive, glitch, typewriter, karaoke}` → unified
  ASS-compat generator (evaluator timing).
- Any other style id (classic ASS presets, custom DB styles) → legacy
  `generate_captions_ass` unchanged.

### API

| Endpoint | Purpose |
|----------|---------|
| `POST /api/captions/preview` | Unchanged contract; implementation uses shared path. |
| `POST /api/captions/export/evaluate` | Same frames as preview for a given range (parity check). |
| `POST /api/captions/export/ass` | Returns ASS text generated from unified active-word timing. |

### Files

```text
backend/caption_core/animation/render.py   # shared evaluate + ASS/overlay export
backend/caption_core/animation/preview.py  # delegates to evaluate_frame_range
backend/api/captions.py                    # export/evaluate + export/ass
tests/caption_core/animation/test_render.py
tests/api/test_caption_export.py
```

### Guarantees

1. **Determinism:** same `(words, preset, frame, fps)` → same state for preview
   and export evaluation.
2. **No formula duplication:** frontend still only maps state → CSS; export
   rasterizer only maps state → pixels/ASS.
3. **Legacy safety:** non-animation styles keep the Phase 0 ASS visual output
   path; existing caption_service tests remain authoritative for that path.
4. **Remotion not introduced.** Overlay mode is Pillow + FFmpeg only.

## Phase 5: Preset registry and customization

Phase 5 expands the configuration layer around presets without changing the
Phase 1–4 evaluation or export engines.

### Architecture

```
Built-in factories (presets.py)
        │
        ▼
PresetRegistry  (preset_registry.py)  ← unique ids, discovery, no silent fallback
        │
        ├── get_preset(id) → deep copy
        ├── list_metadata()
        └── merge_preset_overrides(base, overrides)  (overrides.py)
                │
                ▼
        preview / export / API all resolve through the registry
```

### CaptionPreset fields (Phase 5)

| Group | Fields |
|-------|--------|
| Metadata | `id` (slug), `name`, `category`, `description`, `tags`, `version` |
| Visual | `style` (typography, colors, stroke, shadow, alignment, spacing) |
| Layout | `layout` (max words/line, position, wrap_mode, gaps) |
| Animation | `entry_animation`, `active_word_animation`, `exit_animation`, `effects` |
| Active word | `active_word` (`ActiveWordConfig`: highlight, scale, glow, bounce, karaoke) |
| Renderer | `renderer` (`RendererCompatibility`: ass_compat, animated_preview, animated_export, notes) |

### Configuration hierarchy

```
registry base preset
  + optional overrides (style / layout / active_word / animations / tags)
  = validated CaptionPreset (new object; base never mutated)
```

Override rules:

- Nested dicts (`style`, `layout`, `active_word`, `renderer`) deep-merge.
- Lists (`tags`, `effects`, `tag_rules`) replace when provided.
- Scalars overwrite.
- `id` / `version` cannot be changed via overrides.
- Unknown top-level keys are rejected.
- Result is always re-validated as `CaptionPreset`.

### ASS property support

| Property | ASS | Animated preview/export |
|----------|-----|-------------------------|
| font family / size / bold | yes | yes |
| text / active / stroke colors | yes | yes |
| stroke width / shadow depth | yes | yes |
| alignment / margin_v / words_per_group | yes | yes |
| letter_spacing / line_height / text_transform | **no** (stored only) | partial |
| shadow_blur / background_color | **no** (stored only) | partial |
| bounce / glitch / scale motion | approx (color only) | yes |
| typewriter reveal / karaoke wipe | approx | yes |

Unsupported ASS properties remain on the model for future renderers and are
**not** faked in the ASS path.

### API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/captions/presets` | List metadata (+ style_summary, tags, categories) |
| GET | `/api/captions/presets/{id}` | Full preset config |
| POST | `/api/captions/presets/validate` | Validate id + overrides |
| POST | `/api/captions/presets/resolve` | Return merged preset JSON |
| GET | `/api/captions/preview/presets` | Registry metadata (compat) |

### Frontend

`frontend/src/pages/tools/Captions.jsx` loads presets from
`GET /api/captions/presets`, supports category chips, shows tags/renderer notes,
and exposes a local font-size override panel that calls `/presets/validate`.
Burn export still uses classic ASS style selection; animated presets drive the
preview gallery.

### Files

```text
backend/caption_core/preset_registry.py
backend/caption_core/overrides.py
backend/caption_core/animation/presets.py   # catalog + registry populate
backend/caption_core/models.py              # ActiveWordConfig, RendererCompatibility
backend/api/captions.py                     # preset endpoints
frontend/src/pages/tools/Captions.jsx
tests/caption_core/test_preset_registry.py
tests/caption_core/test_overrides.py
tests/api/test_caption_presets.py
```

## Phase 8: CapCut-style caption effects & templates

Phase 8 expands the **configuration-driven** caption stack for a CapCut-like
animated subtitle experience without replacing the Phase 1–4 engine or Phase 5
registry.

### New animation primitives

Registered in `animation/registry.py` (pure functions in `primitives.py`):

| Type | Effect |
|------|--------|
| `slide` | Axis translation + fade (in/out) |
| `pop` | Overshoot scale pop-in |
| `glow` | Glow pulse/hold + optional scale boost |
| `zoom` | Punchy scale (CapCut zoom-in defaults) |
| `pulse` | Rhythmic scale + glow emphasis |
| `word_reveal` | Whole-word rise/fade/scale (vs typewriter chars) |
| `explosive` | Alias → `pop` for config convenience |

Existing: `fade`, `scale`, `spring`, `bounce`, `glitch`, `typewriter`, `karaoke`.

### Active-word configuration (expanded)

`ActiveWordConfig` now supports:

- `background_highlight` + `background_color` (rounded box in preview/overlay)
- `color_transition`, `smooth_scale`
- prior fields: highlight color/intensity, scale emphasis, glow, bounce, karaoke

### Style hierarchy

```
CaptionTemplate (= CaptionPreset in registry)
  ├── style (typography, outline, shadow, background box fields)
  ├── layout (wrapping, position)
  ├── entry / active / exit animations + effects[]
  ├── active_word (highlight behavior)
  └── renderer (ASS / preview / export compatibility notes)
```

Optional UI overrides still merge via Phase 5 `merge_preset_overrides`.

### CapCut-style templates (data-only)

| ID | Name | Vibe |
|----|------|------|
| `tiktok_bold` | TikTok Bold | Thick outline, yellow active, pop |
| `mrbeast_style` | MrBeast Style | Huge Impact, red active, bounce+pulse |
| `minimal_clean` | Minimal | Soft fade, bottom, subtle |
| `gaming_neon` | Gaming | Neon, slide, glitch, glow, box |
| `podcast_soft` | Podcast | Word reveal, rounded active box |
| `karaoke_box` | Karaoke Box | Wipe + box + glow |
| *(plus original five)* | Bounce, Explosive, Glitch, Typewriter, Karaoke | Engine baselines |

### ASS vs animated fidelity

| Feature | ASS | Preview / overlay |
|---------|-----|-------------------|
| Font/size/weight/outline/basic shadow | yes | yes |
| Active color | yes | yes |
| Pop/bounce/slide/glitch/glow motion | approx (color only) | yes |
| Typewriter / karaoke wipe | approx | yes |
| Rounded background highlight boxes | **no** (documented) | yes |
| letter-spacing / blur polish | limited | yes |

### Frontend

`Captions.jsx` loads the full registry, supports **category + tag filters**,
shows template metadata, and passes active-word background settings into
`AnimatedCaptionPreview` (outline stroke simulation + rounded highlight).

### Tests

`tests/caption_core/animation/test_advanced_effects.py` covers primitives,
template registration, evaluator runs, and preview/export frame consistency.


---

# Included design doc: `docs/CLIP_SCORING_DESIGN.md`

# Clip Scoring Design (Phase 6)

Deterministic, explainable viral-moment scoring for ViralMint. This layer
**does not replace** the existing LLM clip extractor; it provides a local,
weight-driven foundation and a fallback when AI selection returns nothing.

## Existing pipeline (audit)

| Step | Implementation |
|------|----------------|
| Ingestion | `DownloadedVideo` + yt-dlp |
| Transcription | `WhisperService` → segment JSON on the video row |
| Clip selection (primary) | LLM via `CLIP_SELECTION_PROMPT` in `clip_extractor.py` |
| Score (legacy) | Single `virality_score` 1–10 from the model response |
| Overlap removal | `_remove_overlapping_clips` (2s tolerance) |
| Export | FFmpeg extract + captions + thumbnail |

### Limitations addressed by Phase 6

- LLM scores are opaque and non-reproducible without the same model/prompt.
- No per-signal breakdown for the UI.
- No offline path when the AI provider fails or returns empty.

## Architecture

```
Whisper segments
      │
      ▼
generate_candidates  (sliding windows)
      │
      ▼
score_transcript_window  (multi-signal)
      │
      ├── detect_hooks (rule-based)
      │
      ▼
select_clips  (rank → dedupe → de-overlap → duration filter)
      │
      ├── API: /api/clip-intelligence/*
      ├── UI: ClipScorePanel + Clip Studio "Score moments"
      └── Fallback inside extract_viral_clips when AI returns []
```

## Signals and default weights

Positive signals are normalized to sum to 1.0 at score time:

| Signal | Default weight | Source |
|--------|----------------|--------|
| hook_strength | 0.30 | Hook pattern catalog |
| emotional_intensity | 0.15 | Emotion keyword density |
| speech_energy | 0.10 | WPM + filler ratio |
| keyword_importance | 0.10 | Topic keywords + numbers |
| story_completeness | 0.15 | Arc markers / sentences |
| audience_curiosity | 0.10 | Questions, secrets, "you" |
| pacing | 0.10 | Seconds per sentence |

Penalties (subtracted after weighted sum):

| Penalty | Default weight |
|---------|----------------|
| silence_penalty | 0.15 |
| repetition_penalty | 0.10 |

`final_score ∈ [0, 1]`. Display also maps to legacy 1–10 via  
`1 + final_score * 9`.

## Hook detection

Rule-based regex catalog in `hooks.py` with categories:

- opening, curiosity, question, claim, emotion, story

Matches are **evidence of language patterns**, not claims about future views.
Catalog is extendable by appending `HookPattern` entries.

## Selection algorithm

1. Generate windows at `step_ms` with duration ladder `{min, mid, max}`.
2. Score each window.
3. Drop near-duplicates (time + text prefix).
4. Greedy non-overlap keep (score desc, earlier start, id).
5. Enforce duration bounds and `max_clips`.

Fully deterministic for fixed inputs.

## API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/clip-intelligence/weights` | Default weights + signal docs |
| POST | `/api/clip-intelligence/score-window` | Score one text window |
| POST | `/api/clip-intelligence/detect-hooks` | Hook matches for text |
| POST | `/api/clip-intelligence/analyze` | Full candidate + selection from segments |
| POST | `/api/clip-intelligence/analyze/{video_id}` | Analyze stored transcript on a downloaded video |

## Files

```text
backend/clip_intelligence/
  models.py
  hooks.py
  scoring.py
  selection.py
  pipeline.py
backend/api/clip_intelligence.py
frontend/src/components/clips/ClipScorePanel.jsx
docs/CLIP_SCORING_DESIGN.md
tests/clip_intelligence/
tests/api/test_clip_intelligence.py
```

## Non-goals (Phase 6)

- Full clip editor
- Face/speaker reframe
- Paid external scoring APIs
- Replacing the LLM path when it succeeds


---

# Included design doc: `docs/CLIP_ENHANCEMENT_DESIGN.md`

# Clip Enhancement Design (Phase 7)

Phase 7 adds an **intelligent enhancement plan** layer on top of Phase 6 scoring.
It improves selected clips **before export** without building a full editor and
**without rendering video** in this layer.

## Integration with existing pipeline

```
Phase 6: analyze_transcript → selected ClipCandidate
                │
                ▼
Phase 7: build_enhancement_plan(segments, start_ms, end_ms)
                │
                ├── silence analysis (transcript gaps)
                ├── boundary optimization (speech / sentence / hooks)
                ├── pacing metrics
                ├── score before/after
                ├── caption configuration suggestion
                └── export settings (trim bounds on source timeline)
                │
                ▼
        Existing extract/export (unchanged render path)
```

Non-destructive: source media is never modified by Phase 7 modules.

## Silence detection

**Module:** `backend/clip_intelligence/silence.py`

- Builds speech units from word timestamps when available, else segments.
- Gaps ≥ `min_silence_ms` become intervals (`leading` / `trailing` / `internal` / `gap`).
- `silence_ratio` = uncovered time / window duration.
- `suggest_trim_bounds` trims leading/trailing silence while keeping
  `max_keep_silence_ms` of natural pad.

Configurable via `SilenceConfig`. Fully deterministic.

## Boundary optimization

**Module:** `backend/clip_intelligence/boundaries.py`

Order of operations:

1. Silence trim (edges)
2. Snap to word starts/ends (never mid-word when words exist)
3. Prefer sentence boundaries (expand/contract within `max_expand_ms`)
4. Preserve short lead-in before detected hooks
5. Enforce min/max duration

If only segment-level timings exist, `cut_word_risk=True` is reported.

## Pacing analysis

**Module:** `backend/clip_intelligence/pacing.py`

Metrics:

| Metric | Meaning |
|--------|---------|
| words_per_second / words_per_minute | Speech rate |
| silence_ratio | Fraction silent |
| speech_density | Fraction covered by speech units |
| sentence_count / avg_seconds_per_sentence | Idea cadence |
| energy_changes / energy_variance | Local WPM shifts across ~3s buckets |
| filler_ratio | um/uh/like density |
| rating | slow \| balanced \| fast \| sparse \| dense |

All values ship with human-readable `explanations`.

## Enhancement pipeline

**Module:** `backend/clip_intelligence/enhancement.py`

`build_enhancement_plan(...)` → `EnhancementPlan`:

- original vs optimized bounds
- silence + pacing + boundary reports
- hooks on optimized window
- deterministic score before/after
- `CaptionPlan` (style / optional animation preset / emoji intensity)
- `ExportPlan` (aspect ratio, source_start/end, trim offsets)
- `recommendations[]` actionable bullets

No FFmpeg calls in this layer.

## API

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/clip-intelligence/silence` | Silence intervals for a window |
| POST | `/api/clip-intelligence/pacing` | Pacing metrics |
| POST | `/api/clip-intelligence/optimize-boundaries` | Optimized start/end |
| POST | `/api/clip-intelligence/enhance-plan` | Full enhancement plan |

Phase 6 endpoints remain unchanged.

## Files

```text
backend/clip_intelligence/silence.py
backend/clip_intelligence/pacing.py
backend/clip_intelligence/boundaries.py
backend/clip_intelligence/enhancement.py
backend/api/clip_intelligence.py          # extended
docs/CLIP_ENHANCEMENT_DESIGN.md
tests/clip_intelligence/test_enhancement.py
tests/api/test_clip_enhancement.py
```

## Non-goals

- Full NLE editor
- Automatic jump-cut rendering of internal pauses
- Face reframe / loudness processing (separate tools already exist)


---

# Included design doc: `docs/CAPTION_REMOVAL_DESIGN.md`

# Caption Removal Design (Phase 9)

Foundation for removing **burned-in** captions/subtitles from short-form video
so new CapCut-style captions can be applied cleanly.

This is **not** a full video restoration product. It focuses on:

1. Detecting likely caption bands  
2. Building masks  
3. Applying a safe baseline remover  
4. Leaving hooks for future AI inpainting models  

## Integration points

| Existing system | Role |
|-----------------|------|
| `ffmpeg_service` / FFmpeg | Encode cleaned video; `delogo` / `boxblur` filters |
| `storage/` + tools upload paths | Safe I/O; never overwrite sources |
| Caption **generation** stack (Phases 1–8) | Unchanged — removal runs *before* re-captioning |
| Jobs / tools patterns | Optional async jobs can wrap `remove_burned_captions` later |

## Detection approach (`detection.py`)

**Method:** `heuristic_v1`

1. Short-form **position priors** (bottom center band is default).  
2. Optional **frame sampling** via FFmpeg + Pillow edge/contrast/bright-pixel scores in each band.  
3. Confidence blend: `0.55 * heuristic + 0.45 * prior`.  
4. `force_region` for manual/normalized boxes.  

Output region shape:

```json
{
  "region": {"x": 54, "y": 1382, "width": 972, "height": 384},
  "confidence": 0.71,
  "type": "bottom_center",
  "normalized": {"x": 0.05, "y": 0.72, "width": 0.9, "height": 0.2}
}
```

Detection **never** modifies the video.

## Mask architecture (`masking.py`)

`MaskPlan` holds:

- padded regions  
- feather metadata  
- optional PNG preview (overlay visualization)  
- `delogo_boxes()` for FFmpeg  

Masks are plans + previews only — not destructive edits.

## Removal pipeline (`removal.py` + `pipeline.py`)

```
video
  → detect regions
  → build mask plan
  → backend.remove(video, mask, output)
  → cleaned copy (source untouched)
```

### Backends

| ID | Behavior | Limitation |
|----|----------|------------|
| `delogo` | FFmpeg spatial interpolation | Not generative; artifacts on complex backgrounds |
| `boxblur` | Blur cropped band + overlay | Obvious blur; last-resort cleanup |
| `noop` | Byte copy | Tests / dry wiring |

### Preserve

- Audio stream copy when possible (`-c:a copy`)  
- Resolution from source (delogo does not scale)  
- Duration  
- FPS (encoder may remux; timestamps preserved by full-stream filter)  

### Safety

- Refuse `output_path == source_path`  
- Dry-run mode analyzes only  
- API path access limited to `storage/`  

## API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/caption-removal/backends` | List backends + limitations |
| POST | `/api/caption-removal/detect` | Synthetic / prior detection |
| POST | `/api/caption-removal/analyze-path` | Detect + mask for storage video |
| POST | `/api/caption-removal/mask` | Mask from explicit regions |
| POST | `/api/caption-removal/process` | Upload → detect → optional clean file |

## Future AI model integration

`CaptionRemovalBackend` ABC:

```python
class CaptionRemovalBackend(ABC):
    def remove(self, video_path, mask, output_path, *, config) -> RemovalResult: ...
```

A future `InpaintBackend` (e.g. ProPainter / LaMa / proprietary) can:

1. Export masked frames  
2. Run temporal inpainting  
3. Re-mux audio from the original  

without changing detection/mask APIs.

## Limitations (explicit)

- Not magic eraser-level quality on neon/moving captions.  
- Heuristic detection can miss unusual placements without `force_region`.  
- `delogo` assumes roughly static rectangular bands.  
- No automatic re-application of new captions in this phase (use existing caption tools after cleanup).  

## Files

```text
backend/caption_removal/
  models.py
  detection.py
  masking.py
  removal.py
  pipeline.py
backend/api/caption_removal.py
docs/CAPTION_REMOVAL_DESIGN.md
tests/caption_removal/
tests/api/test_caption_removal.py
```


---

# Included design doc: `docs/PRODUCTION_PIPELINE_DESIGN.md`

# Production Pipeline Design (Phase 10)

Professional short-form **finishing** pipeline: turn analyzed clips into
ready-to-post TikTok / YouTube Shorts / Instagram Reels videos.

Does **not** rewrite caption generation, clip scoring, or caption removal —
it composes them via configuration + FFmpeg.

## End-to-end flow

```
Upload
  → (optional) analyze / score / enhance / caption  [existing systems]
  → Auto reframe plan (9:16 crop path)
  → Audio enhance filter (optional)
  → Video quality filters (optional)
  → Platform export encode
  → Cover thumbnail
  → Review / download
```

Batch variant queues many sources through the same finish config with
per-item status, failures, and retries.

## Reframing system

**Module:** `production_pipeline/reframe.py`

- `AutoReframePlan`: crop region, keyframes, confidence, movement path, notes  
- Modes: `center`, `face_center`, `speaker`, `subject`, `custom`  
- Face/speaker use **upper-third heuristics** (deterministic, no ML required at plan time)  
- Smoothing + max-step clamp avoid sudden jumps  
- Rendering uses primary mid-keyframe crop + scale (stable); path retained for future dynamic pan  

## Audio pipeline

**Module:** `production_pipeline/audio.py`

| Option | Effect |
|--------|--------|
| `preserve_original` | Passthrough |
| `loudness_normalize` | `loudnorm` (default −14 LUFS) |
| `denoise` | `afftdn` |
| `voice_clarity` | highpass/lowpass speech band |
| `silence_cleanup` | Flag for integration with remove-silence tool |

## Video enhancements

**Module:** `production_pipeline/video_fx.py`

Optional modular filters: `hqdn3d`, `eq`, `unsharp`.  
`upscale` is an integration point (not forced).

## Export presets

| ID | Platform | Resolution | Notes |
|----|----------|------------|-------|
| `tiktok` | TikTok | 1080×1920 @ 30 | CRF 18 |
| `youtube_shorts` | YouTube Shorts | 1080×1920 @ 30 | CRF 17, 60s hint |
| `instagram_reels` | Instagram Reels | 1080×1920 @ 30 | CRF 18 |

## Batch architecture

In-process registry (`batch.py`):

- `create_batch(paths, FinishConfig)`  
- per-item: pending → running → success | failed → retrying  
- `mark_retry` respects `max_attempts`  
- No new broker/queue service — fits existing asyncio job style  

## Thumbnail / cover

- Strategy: hook time if known, else mid-clip (avoid first/last 10%)  
- Optional text overlay via FFmpeg `drawtext`  
- Not a design editor  

## API

| Method | Path |
|--------|------|
| GET | `/api/production/export-presets` |
| GET | `/api/production/track-modes` |
| POST | `/api/production/reframe-plan` |
| POST | `/api/production/audio-filter` |
| POST | `/api/production/finish-plan` |
| POST | `/api/production/thumbnail-plan` |
| POST | `/api/production/batch` |
| GET | `/api/production/batch` / `{id}` |
| POST | `/api/production/batch/{id}/items/{item}/retry` |
| POST | `/api/production/finish` (upload → encode) |

## Frontend

- Route: `/studio` — **Finish Studio**  
- Steps: Upload → Processing → Review → Export  
- Platform / track mode / enhance toggles + plan chips  

## Files

```text
backend/production_pipeline/
  models.py reframe.py audio.py video_fx.py
  export_presets.py thumbnail.py finisher.py batch.py
backend/api/production.py
frontend/src/pages/Studio.jsx
docs/PRODUCTION_PIPELINE_DESIGN.md
tests/production_pipeline/
tests/api/test_production.py
```


---

## Core source code

Selected critical modules (full packages also in the zip archive).



---

## Source: `backend/caption_core/models.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Validated Pydantic models for the deterministic caption core."""
from __future__ import annotations

import re
from typing import Any, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from backend.caption_core.enums import CaptionAnimationType, CaptionCategory, CaptionEasing


def _new_id() -> str:
    return str(uuid4())


def _to_ass_color(color: str) -> str:
    """Convert #RRGGBB or #AARRGGBB (and &H pass-through) to ASS BGR &H format.

    ASS colors are stored as ``&HAABBGGRR``. The alpha byte is ``00`` for
    fully opaque unless an 8-character hex string supplies one.
    """
    color = (color or "#FFFFFF").strip()
    if color.startswith("&H"):
        return color
    if not color.startswith("#"):
        raise ValueError(f"Unsupported color format: {color!r}. Expected hex (#RRGGBB) or ASS (&H...).")
    hex_part = color[1:]
    if len(hex_part) == 6:
        r, g, b = hex_part[0:2], hex_part[2:4], hex_part[4:6]
        return f"&H00{b}{g}{r}"
    if len(hex_part) == 8:
        a, r, g, b = hex_part[0:2], hex_part[2:4], hex_part[4:6], hex_part[6:8]
        return f"&H{a}{b}{g}{r}"
    raise ValueError(f"Unsupported hex color length: {color!r}")


class CaptionWord(BaseModel):
    """A single timed word.

    Timestamps are in milliseconds. ``end_ms`` may equal ``start_ms`` to
    represent a zero-duration marker word.
    """

    id: str = Field(default_factory=_new_id)
    text: str
    start_ms: int = Field(ge=0)
    end_ms: int
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    speaker_id: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    emphasis: bool = False

    @field_validator("text")
    @classmethod
    def _text_must_be_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("CaptionWord.text cannot be empty")
        return value

    @model_validator(mode="after")
    def _end_must_not_be_before_start(self) -> "CaptionWord":
        if self.end_ms < self.start_ms:
            raise ValueError(
                f"CaptionWord end_ms ({self.end_ms}) must be >= start_ms ({self.start_ms})"
            )
        return self

    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    def is_zero_duration(self) -> bool:
        return self.end_ms == self.start_ms

    def model_copy(self, **kwargs: Any) -> "CaptionWord":
        return super().model_copy(**kwargs)


class CaptionSegment(BaseModel):
    """A contiguous display segment containing an ordered list of words."""

    id: str = Field(default_factory=_new_id)
    start_ms: int = Field(default=0, ge=0)
    end_ms: int = Field(default=0, ge=0)
    words: list[CaptionWord] = Field(default_factory=list)
    speaker_id: Optional[str] = None

    @model_validator(mode="after")
    def _sync_from_words(self) -> "CaptionSegment":
        if self.words:
            # Preserve stable order; sort by start, then end, then original index.
            indexed = list(enumerate(self.words))
            indexed.sort(key=lambda item: (item[1].start_ms, item[1].end_ms, item[0]))
            self.words = [item[1] for item in indexed]
            self.start_ms = min(self.start_ms, self.words[0].start_ms)
            self.end_ms = max(self.end_ms, self.words[-1].end_ms)
        if self.end_ms < self.start_ms:
            raise ValueError(
                f"CaptionSegment end_ms ({self.end_ms}) must be >= start_ms ({self.start_ms})"
            )
        return self

    def text(self) -> str:
        return " ".join(w.text for w in self.words)

    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms


class CaptionStyle(BaseModel):
    """A caption style definition.

    This model stores both ASS-compatible properties and future animation
    properties. Properties that cannot be represented directly by the current
    ASS renderer are preserved for later renderers but ignored by the ASS
    bridge (see ``to_ass_style_dict``).
    """

    id: str = Field(default_factory=_new_id)
    name: str
    font_family: str = "Arial"
    font_size_portrait: int = Field(default=56, ge=1)
    font_size_landscape: int = Field(default=42, ge=1)
    font_weight: Literal["normal", "bold"] = "bold"
    text_color: str = "#FFFFFF"
    active_word_color: str = "#FFFF00"
    stroke_color: str = "#000000"
    stroke_width: int = Field(default=3, ge=0)
    shadow_color: Optional[str] = None
    shadow_blur: float = Field(default=0.0, ge=0.0)
    shadow_offset_x: float = 0.0
    shadow_offset_y: float = 1.0
    background_color: Optional[str] = None
    background_opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    background_radius: float = Field(default=6.0, ge=0.0)
    """Corner radius for rounded highlight boxes (preview/overlay; not ASS)."""
    background_padding_x: float = Field(default=10.0, ge=0.0)
    background_padding_y: float = Field(default=4.0, ge=0.0)
    alignment: int = Field(default=5, ge=1, le=9)
    letter_spacing: float = 0.0
    line_height: float = Field(default=1.2, ge=0.0)
    text_transform: Literal["none", "uppercase", "lowercase", "capitalize"] = "none"
    words_per_group: int = Field(default=3, ge=1)
    margin_v: int = Field(default=80, ge=0)

    @field_validator("text_color", "active_word_color", "stroke_color")
    @classmethod
    def _colors_must_be_valid(cls, value: str) -> str:
        _to_ass_color(value)
        return value

    @field_validator("name")
    @classmethod
    def _name_must_be_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("CaptionStyle.name cannot be empty")
        return value

    def is_bold(self) -> bool:
        return self.font_weight == "bold"

    def to_ass_style_dict(self) -> dict[str, Any]:
        """Return a dict compatible with ``backend.services.caption_service`` ASS rendering.

        Unsupported properties (``shadow_blur``, ``background_color``,
        ``letter_spacing``, ``line_height``, ``text_transform``, etc.) are not
        included in the returned dict because the current ASS renderer does not
        implement them.
        """
        font = self.font_family
        if self.is_bold() and not re.search(r"\bbold\b", font, re.IGNORECASE):
            font = f"{font} Bold"

        # Map shadow offset to the integer depth value used by the ASS renderer.
        shadow_depth = int(max(abs(self.shadow_offset_x), abs(self.shadow_offset_y)))

        return {
            "font": font,
            "font_size_portrait": self.font_size_portrait,
            "font_size_landscape": self.font_size_landscape,
            "primary_color": _to_ass_color(self.text_color),
            "highlight_color": _to_ass_color(self.active_word_color),
            "outline_color": _to_ass_color(self.stroke_color),
            "outline_width": self.stroke_width,
            "shadow_depth": shadow_depth,
            "alignment": self.alignment,
            "margin_v": self.margin_v,
            "words_per_group": self.words_per_group,
        }


class CaptionAnimation(BaseModel):
    """A reusable animation configuration.

    This is data only — no rendering code. It is used for entry, active-word,
    exit, and effect animations.
    """

    id: str = Field(default_factory=_new_id)
    type: CaptionAnimationType = CaptionAnimationType.FADE
    duration_ms: int = Field(default=300, ge=0)
    delay_ms: int = Field(default=0, ge=0)
    easing: CaptionEasing = CaptionEasing.LINEAR
    spring: Optional[dict] = None
    intensity: float = Field(default=1.0, ge=0.0, le=2.0)
    parameters: dict = Field(default_factory=dict)


class CaptionLayout(BaseModel):
    """Layout and segmentation constraints for a preset."""

    max_words_per_line: int = Field(default=3, ge=1)
    max_chars_per_line: Optional[int] = Field(default=None, ge=1)
    max_line_duration_ms: Optional[int] = Field(default=None, ge=1)
    max_gap_ms: Optional[int] = Field(default=None, ge=0)
    position: str = "center-center"
    line_spacing: float = Field(default=1.2, ge=0.0)
    padding_x: int = Field(default=0, ge=0)
    padding_y: int = Field(default=0, ge=0)
    wrap_mode: Literal["word", "none", "char"] = "word"


class ActiveWordConfig(BaseModel):
    """Configuration for how the active word is emphasized.

    This is pure data. The animation engine still evaluates motion via
    ``CaptionAnimation`` primitives; these fields drive color/intensity
    emphasis for ASS-compat and overlay presentation.
    """

    highlight_color: Optional[str] = None  # defaults to style.active_word_color when None
    highlight_intensity: float = Field(default=1.0, ge=0.0, le=2.0)
    scale_emphasis: float = Field(default=1.0, ge=0.5, le=2.0)
    glow_amount: float = Field(default=0.0, ge=0.0, le=32.0)
    bounce_intensity: float = Field(default=1.0, ge=0.0, le=2.0)
    karaoke_enabled: bool = False
    karaoke_fill_color: Optional[str] = None
    background_highlight: bool = False
    """When True, preview/overlay draw a rounded box behind the active word."""
    background_color: Optional[str] = None
    color_transition: bool = True
    """Smoothly favor active color while the word is active (preview)."""
    smooth_scale: bool = True

    @field_validator("highlight_color", "karaoke_fill_color", "background_color")
    @classmethod
    def _optional_color(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        _to_ass_color(value)
        return value


class RendererCompatibility(BaseModel):
    """Declares which render paths can consume this preset."""

    ass_compat: bool = True
    animated_preview: bool = True
    animated_export: bool = True
    notes: Optional[str] = None


class CaptionPreset(BaseModel):
    """A complete caption preset: style + layout + animations + rules.

    Phase 5 adds metadata tags, active-word configuration, and renderer
    compatibility flags. Presets remain pure configuration — no renderer
    classes per preset.
    """

    id: str = Field(default_factory=_new_id)
    name: str
    category: CaptionCategory = CaptionCategory.VIRAL
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    style: CaptionStyle
    layout: CaptionLayout = Field(default_factory=CaptionLayout)
    entry_animation: Optional[CaptionAnimation] = None
    active_word_animation: Optional[CaptionAnimation] = None
    exit_animation: Optional[CaptionAnimation] = None
    effects: list[CaptionAnimation] = Field(default_factory=list)
    active_word: ActiveWordConfig = Field(default_factory=ActiveWordConfig)
    renderer: RendererCompatibility = Field(default_factory=RendererCompatibility)
    tag_rules: list[str] = Field(default_factory=list)
    version: int = Field(default=1, ge=1)

    @field_validator("name")
    @classmethod
    def _name_must_be_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("CaptionPreset.name cannot be empty")
        return value

    @field_validator("id")
    @classmethod
    def _id_must_be_slug(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("CaptionPreset.id cannot be empty")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_\-]{0,63}", value):
            raise ValueError(
                f"CaptionPreset.id {value!r} must be a lowercase slug "
                "(letters, digits, underscore, hyphen)"
            )
        return value

    @field_validator("tags")
    @classmethod
    def _normalize_tags(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for tag in value or []:
            t = str(tag).strip().lower()
            if t and t not in cleaned:
                cleaned.append(t)
        return cleaned

    def resolved_highlight_color(self) -> str:
        """Return the effective active-word highlight color."""
        if self.active_word.highlight_color:
            return self.active_word.highlight_color
        return self.style.active_word_color

    def metadata(self) -> dict[str, Any]:
        """Lightweight metadata for list endpoints (no full style dump)."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value if isinstance(self.category, CaptionCategory) else self.category,
            "description": self.description,
            "tags": list(self.tags),
            "version": self.version,
            "renderer": self.renderer.model_dump(),
        }

```


---

## Source: `backend/caption_core/animation/evaluator.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Frame-state evaluator: the canonical animation calculation API."""
from __future__ import annotations

from backend.caption_core.active_word import find_active_word_index
from backend.caption_core.animation.composition import compose_animations
from backend.caption_core.animation.context import AnimationContext, frame_to_ms
from backend.caption_core.animation.events import _is_active_word, is_event_active
from backend.caption_core.animation.registry import dispatch_animation
from backend.caption_core.animation.state import CaptionVisualState
from backend.caption_core.models import CaptionAnimation, CaptionPreset, CaptionSegment, CaptionWord


def _trigger_time_ms(trigger: str, word: CaptionWord, segment: CaptionSegment) -> int:
    """Return the absolute time at which ``trigger`` fires."""
    if trigger == "WORD_ENTER":
        return word.start_ms
    if trigger == "WORD_EXIT":
        return word.end_ms
    if trigger == "WORD_ACTIVE":
        return word.start_ms
    if trigger == "SEGMENT_ENTER":
        return segment.start_ms
    if trigger == "SEGMENT_EXIT":
        return segment.end_ms
    return word.start_ms


def _collect_applicable_contexts(
    word: CaptionWord,
    word_index: int,
    segment: CaptionSegment,
    preset: CaptionPreset,
    frame: int,
    fps: float,
) -> list[AnimationContext]:
    """Build the ordered list of active ``AnimationContext`` objects for ``word``."""
    current_time_ms = frame_to_ms(frame, fps)
    active_word_index = find_active_word_index(segment.words, current_time_ms)

    contexts: list[AnimationContext] = []

    def add(animation: CaptionAnimation, trigger: str):
        contexts.append(
            AnimationContext.from_word(
                word=word,
                word_index=word_index,
                active_word_index=active_word_index,
                segment=segment,
                animation_config=animation,
                frame=frame,
                fps=fps,
                trigger=trigger,
                trigger_time_ms=_trigger_time_ms(trigger, word, segment),
            )
        )

    if preset.entry_animation is not None:
        if is_event_active("WORD_ENTER", word, segment, current_time_ms, preset.entry_animation):
            add(preset.entry_animation, "WORD_ENTER")

    if preset.active_word_animation is not None:
        if is_event_active(
            "WORD_ACTIVE",
            word,
            segment,
            current_time_ms,
            preset.active_word_animation,
            word_index=word_index,
            active_word_index=active_word_index,
        ):
            add(preset.active_word_animation, "WORD_ACTIVE")

    if preset.exit_animation is not None:
        if is_event_active("WORD_EXIT", word, segment, current_time_ms, preset.exit_animation):
            add(preset.exit_animation, "WORD_EXIT")

    for effect in preset.effects:
        trigger = str(effect.parameters.get("trigger", "WORD_ACTIVE")).upper()
        kwargs = {}
        if trigger == "WORD_ACTIVE":
            kwargs = {"word_index": word_index, "active_word_index": active_word_index}
        if is_event_active(trigger, word, segment, current_time_ms, effect, **kwargs):
            add(effect, trigger)

    return contexts


def evaluate_caption_word_state(
    word: CaptionWord,
    word_index: int,
    segment: CaptionSegment,
    preset: CaptionPreset,
    frame: int,
    fps: float,
) -> CaptionVisualState:
    """Return the deterministic visual state of ``word`` at ``frame``/``fps``.

    This is the canonical animation calculation API. It is renderer-independent
    and depends only on caption timing, the preset, frame, and fps.

    A word is visible (base opacity ``1``) when it is the active word or when
    an enter/exit/segment event is currently affecting it. Otherwise the base
    opacity is ``0`` so inactive words stay hidden for word-by-word presets.
    """
    current_time_ms = frame_to_ms(frame, fps)
    active_word_index = find_active_word_index(segment.words, current_time_ms)
    contexts = _collect_applicable_contexts(word, word_index, segment, preset, frame, fps)
    contributions = [dispatch_animation(ctx) for ctx in contexts]

    has_non_active_event = any(ctx.trigger != "WORD_ACTIVE" for ctx in contexts)
    if active_word_index is not None:
        is_active = active_word_index == word_index
    else:
        # At exact boundaries/zero-duration markers no interval covers the time,
        # but the inclusive animation layer may still consider this word active.
        is_active = _is_active_word(word, current_time_ms)
    base_opacity = 1.0 if (is_active or has_non_active_event) else 0.0
    base = CaptionVisualState(opacity=base_opacity)
    return compose_animations(base, contributions)

```


---

## Source: `backend/caption_core/animation/registry.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Animation primitive registry and dispatcher."""
from __future__ import annotations

from backend.caption_core.animation.context import AnimationContext
from backend.caption_core.animation.primitives import (
    evaluate_bounce,
    evaluate_fade,
    evaluate_glitch,
    evaluate_glow,
    evaluate_karaoke,
    evaluate_pop,
    evaluate_pulse,
    evaluate_scale,
    evaluate_slide,
    evaluate_spring,
    evaluate_typewriter,
    evaluate_word_reveal,
    evaluate_zoom,
)
from backend.caption_core.animation.state import CaptionVisualState
from backend.caption_core.enums import CaptionAnimationType


AnimationPrimitive = "callable[[AnimationContext], CaptionVisualState]"

ANIMATION_PRIMITIVES: dict[str, AnimationPrimitive] = {
    "fade": evaluate_fade,
    "scale": evaluate_scale,
    "spring": evaluate_spring,
    "bounce": evaluate_bounce,
    "glitch": evaluate_glitch,
    "typewriter": evaluate_typewriter,
    "karaoke": evaluate_karaoke,
    "slide": evaluate_slide,
    "pop": evaluate_pop,
    "glow": evaluate_glow,
    "zoom": evaluate_zoom,
    "pulse": evaluate_pulse,
    "word_reveal": evaluate_word_reveal,
    "explosive": evaluate_pop,  # config alias used by some presets
}


def dispatch_animation(ctx: AnimationContext) -> CaptionVisualState:
    """Evaluate ``ctx.animation_config`` through the registered primitive."""
    type_value = ctx.animation_config.type
    anim_type = type_value.value if isinstance(type_value, CaptionAnimationType) else str(type_value)
    primitive = ANIMATION_PRIMITIVES.get(anim_type)
    if primitive is None:
        known = ", ".join(sorted(ANIMATION_PRIMITIVES.keys()))
        raise ValueError(f"Unknown animation type {anim_type!r}. Known: {known}")
    return primitive(ctx)

```


---

## Source: `backend/caption_core/preset_registry.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Validated caption preset registry (Phase 5).

The registry is the single discovery surface for animation presets used by
preview, export, and API. Presets are pure configuration objects; no per-preset
renderer classes are registered here.

Unknown preset IDs raise ``UnknownPresetError`` — there is no silent fallback.
"""
from __future__ import annotations

from typing import Iterable, Optional

from backend.caption_core.models import CaptionPreset


class UnknownPresetError(ValueError):
    """Raised when a preset id is not registered."""

    def __init__(self, preset_id: str, known: Iterable[str] | None = None):
        known_list = sorted(known or [])
        self.preset_id = preset_id
        self.known = known_list
        super().__init__(
            f"Unknown preset {preset_id!r}"
            + (f"; known: {known_list}" if known_list else "")
        )


class DuplicatePresetError(ValueError):
    """Raised when two presets claim the same id."""

    def __init__(self, preset_id: str):
        self.preset_id = preset_id
        super().__init__(f"Duplicate preset id {preset_id!r}")


class PresetRegistry:
    """In-memory registry of validated ``CaptionPreset`` instances.

    Registration is deterministic: later registration of the same id is rejected
    unless ``replace=True``. Lookups are case-insensitive on the slug id.
    """

    def __init__(self) -> None:
        self._presets: dict[str, CaptionPreset] = {}

    def clear(self) -> None:
        self._presets.clear()

    def register(self, preset: CaptionPreset, *, replace: bool = False) -> CaptionPreset:
        """Validate and store ``preset``. Returns the stored copy."""
        if not isinstance(preset, CaptionPreset):
            raise TypeError(f"Expected CaptionPreset, got {type(preset)!r}")
        # Re-validate through model_validate for defensive copy.
        stored = CaptionPreset.model_validate(preset.model_dump())
        key = stored.id.lower()
        if key in self._presets and not replace:
            raise DuplicatePresetError(key)
        self._presets[key] = stored
        return stored

    def register_many(self, presets: Iterable[CaptionPreset], *, replace: bool = False) -> None:
        for preset in presets:
            self.register(preset, replace=replace)

    def get(self, preset_id: str) -> CaptionPreset:
        """Return a deep copy of the registered preset (base is never mutated)."""
        if not preset_id or not str(preset_id).strip():
            raise UnknownPresetError(str(preset_id), self.ids())
        key = str(preset_id).strip().lower()
        preset = self._presets.get(key)
        if preset is None:
            raise UnknownPresetError(key, self.ids())
        return preset.model_copy(deep=True)

    def has(self, preset_id: str) -> bool:
        if not preset_id:
            return False
        return str(preset_id).strip().lower() in self._presets

    def ids(self) -> list[str]:
        return sorted(self._presets.keys())

    def list_presets(self) -> list[CaptionPreset]:
        """Return deep copies of all presets, sorted by id."""
        return [self._presets[k].model_copy(deep=True) for k in self.ids()]

    def list_metadata(self) -> list[dict]:
        return [p.metadata() for p in self.list_presets()]

    def list_by_category(self, category: str) -> list[CaptionPreset]:
        cat = str(category).strip().lower()
        return [
            p.model_copy(deep=True)
            for p in self.list_presets()
            if str(p.category.value if hasattr(p.category, "value") else p.category).lower() == cat
        ]

    def validate_id(self, preset_id: str) -> str:
        """Return normalized id if registered, else raise."""
        preset = self.get(preset_id)
        return preset.id

    def __len__(self) -> int:
        return len(self._presets)

    def __contains__(self, preset_id: object) -> bool:
        return self.has(str(preset_id)) if preset_id is not None else False


# Process-global registry used by preview/export/API.
_default_registry = PresetRegistry()


def get_default_registry() -> PresetRegistry:
    return _default_registry


def reset_default_registry() -> PresetRegistry:
    """Clear and return the global registry (tests only)."""
    _default_registry.clear()
    return _default_registry

```


---

## Source: `backend/caption_core/overrides.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Deterministic preset override merging (Phase 5).

Users (or the UI) may apply a shallow/deep override dict on top of a base
preset without mutating the registry copy.

Merge rules
-----------
- Dict fields are deep-merged (style, layout, active_word, renderer, spring, parameters).
- List fields (tags, effects, tag_rules) are replaced when provided.
- Scalar fields overwrite.
- Empty override ``{}`` returns an identical deep copy of the base.
- The result is always re-validated as ``CaptionPreset``.
- Base preset objects are never mutated.
"""
from __future__ import annotations

from typing import Any, Mapping

from pydantic import BaseModel, Field, ValidationError

from backend.caption_core.models import CaptionPreset


class PresetOverrides(BaseModel):
    """Optional partial override payload.

    All fields optional. Nested dicts map onto the corresponding preset
    sub-models. Unknown top-level keys are rejected by Pydantic ``extra=forbid``
    when validated through this model; raw dict merge uses an allow-list.
    """

    model_config = {"extra": "forbid"}

    name: str | None = None
    category: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    style: dict[str, Any] | None = None
    layout: dict[str, Any] | None = None
    entry_animation: dict[str, Any] | None = None
    active_word_animation: dict[str, Any] | None = None
    exit_animation: dict[str, Any] | None = None
    effects: list[dict[str, Any]] | None = None
    active_word: dict[str, Any] | None = None
    renderer: dict[str, Any] | None = None
    tag_rules: list[str] | None = None


_ALLOWED_TOP = frozenset(PresetOverrides.model_fields.keys())


def _deep_merge_dict(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively merge ``override`` onto ``base`` without mutating inputs."""
    result = dict(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, Mapping)
            and not isinstance(value, (str, bytes))
        ):
            result[key] = _deep_merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def merge_preset_overrides(
    base: CaptionPreset,
    overrides: Mapping[str, Any] | PresetOverrides | None,
) -> CaptionPreset:
    """Return a new ``CaptionPreset`` = base + overrides.

    Raises
    ------
    ValueError
        If overrides contain unknown top-level keys or fail validation.
    """
    if overrides is None:
        return base.model_copy(deep=True)

    if isinstance(overrides, PresetOverrides):
        override_dict = overrides.model_dump(exclude_none=True)
    else:
        if not isinstance(overrides, Mapping):
            raise TypeError(f"overrides must be a mapping, got {type(overrides)!r}")
        unknown = set(overrides.keys()) - _ALLOWED_TOP
        # Always allow id passthrough only if it matches base — never change id
        # via overrides (identity is registry-owned).
        unknown -= {"id", "version"}
        if unknown:
            raise ValueError(f"Unknown override fields: {sorted(unknown)}")
        # Drop id/version from overrides if present.
        override_dict = {k: v for k, v in overrides.items() if k in _ALLOWED_TOP and v is not None}

    if not override_dict:
        return base.model_copy(deep=True)

    base_dict = base.model_dump()
    # Nested models that deep-merge:
    for nested in ("style", "layout", "active_word", "renderer"):
        if nested in override_dict and isinstance(override_dict[nested], Mapping):
            base_dict[nested] = _deep_merge_dict(base_dict.get(nested) or {}, override_dict[nested])
            del override_dict[nested]

    # Animation blocks: if provided as dict, deep-merge onto existing or replace None.
    for anim_key in ("entry_animation", "active_word_animation", "exit_animation"):
        if anim_key in override_dict:
            ov = override_dict.pop(anim_key)
            if ov is None:
                base_dict[anim_key] = None
            elif isinstance(ov, Mapping):
                existing = base_dict.get(anim_key) or {}
                base_dict[anim_key] = _deep_merge_dict(existing, ov)
            else:
                base_dict[anim_key] = ov

    # Remaining top-level scalars / lists replace.
    for key, value in override_dict.items():
        base_dict[key] = value

    # Preserve registry identity.
    base_dict["id"] = base.id
    base_dict["version"] = base.version

    try:
        return CaptionPreset.model_validate(base_dict)
    except ValidationError as e:
        raise ValueError(f"Invalid preset after applying overrides: {e}") from e


def apply_style_override(
    base: CaptionPreset,
    *,
    font_size_portrait: int | None = None,
    font_size_landscape: int | None = None,
    text_color: str | None = None,
    active_word_color: str | None = None,
    font_family: str | None = None,
    stroke_width: int | None = None,
    **extra_style: Any,
) -> CaptionPreset:
    """Convenience helper for common typography overrides."""
    style: dict[str, Any] = dict(extra_style)
    if font_size_portrait is not None:
        style["font_size_portrait"] = font_size_portrait
    if font_size_landscape is not None:
        style["font_size_landscape"] = font_size_landscape
    if text_color is not None:
        style["text_color"] = text_color
    if active_word_color is not None:
        style["active_word_color"] = active_word_color
    if font_family is not None:
        style["font_family"] = font_family
    if stroke_width is not None:
        style["stroke_width"] = stroke_width
    return merge_preset_overrides(base, {"style": style} if style else {})

```


---

## Source: `backend/clip_intelligence/scoring.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Deterministic multi-signal clip scoring (Phase 6).

All scores are pure functions of transcript text, timing, and weights.
No external AI calls. No wall-clock randomness.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Optional

from backend.clip_intelligence.hooks import detect_hooks, hook_strength_score
from backend.clip_intelligence.models import ScoreBreakdown, ScoringWeights

# Lightweight keyword sets (English short-form content heuristics).
_EMOTION_WORDS = frozenset(
    """
    love hate fear scared angry mad happy sad cry crazy insane shocking
    amazing incredible terrible worst best never always secret danger
    warning risk fail failed success rich poor broke free money die death
    kill fight win lose heartbreak betrayed shocked stunned
    """.split()
)

_IMPORTANCE_WORDS = frozenset(
    """
    money invest save profit income business strategy growth market stock
    health fitness diet sleep brain science research study proof data
    secret tip hack mistake avoid never always key critical important
    free viral algorithm content creator youtube tiktok
    """.split()
)

_FILLER_WORDS = frozenset(
    """
    um uh like basically actually literally youknow you know kind of kinda
    sort of right okay so yeah
    """.split()
)

_STORY_MARKERS = frozenset(
    """
    because so then finally realized learned discovered happened result
    turned out ended up therefore
    """.split()
)

_WORD_RE = re.compile(r"[a-z0-9']+", re.IGNORECASE)


def _tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD_RE.finditer(text or "")]


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _speech_energy_score(
    text: str,
    duration_ms: int,
    *,
    words: Optional[list[str]] = None,
) -> tuple[float, str]:
    words = words if words is not None else _tokenize(text)
    if duration_ms <= 0:
        return 0.0, "Zero-duration window."
    duration_s = duration_ms / 1000.0
    wpm = (len(words) / duration_s) * 60.0 if duration_s > 0 else 0.0
    # Target short-form energy ~140–190 wpm.
    if wpm <= 0:
        score = 0.0
        note = "No spoken words detected."
    elif wpm < 80:
        score = wpm / 80.0 * 0.45
        note = f"Slow speech (~{wpm:.0f} wpm)."
    elif wpm < 140:
        score = 0.45 + (wpm - 80) / 60.0 * 0.35
        note = f"Moderate pace (~{wpm:.0f} wpm)."
    elif wpm <= 200:
        score = 0.80 + (wpm - 140) / 60.0 * 0.20
        note = f"Strong speech energy (~{wpm:.0f} wpm)."
    else:
        # Too fast can hurt clarity
        score = max(0.4, 1.0 - (wpm - 200) / 200.0)
        note = f"Very fast speech (~{wpm:.0f} wpm); clarity risk."

    filler = sum(1 for w in words if w in _FILLER_WORDS)
    filler_ratio = filler / max(1, len(words))
    if filler_ratio > 0.08:
        score *= max(0.5, 1.0 - filler_ratio)
        note += f" Filler ratio {filler_ratio:.0%}."
    return _clamp01(score), note


def _emotion_score(words: list[str]) -> tuple[float, str]:
    if not words:
        return 0.0, "No words for emotion analysis."
    hits = sum(1 for w in words if w in _EMOTION_WORDS)
    density = hits / len(words)
    # Map density to 0–1 with soft saturation
    score = _clamp01(1.0 - math.exp(-density * 25.0))
    return score, f"Emotion keyword density {density:.2%} ({hits} hits)."


def _keyword_score(words: list[str]) -> tuple[float, str]:
    if not words:
        return 0.0, "No words for keyword analysis."
    hits = sum(1 for w in words if w in _IMPORTANCE_WORDS)
    density = hits / len(words)
    score = _clamp01(1.0 - math.exp(-density * 30.0))
    # Bonus for concrete numbers
    number_hits = sum(1 for w in words if re.fullmatch(r"\d+%?", w))
    if number_hits:
        score = _clamp01(score + min(0.15, number_hits * 0.05))
    return score, f"Importance keywords {hits}, numbers {number_hits}."


def _story_completeness_score(text: str, words: list[str]) -> tuple[float, str]:
    if not words:
        return 0.0, "Empty text."
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    n_sent = len(sentences)
    markers = sum(1 for w in words if w in _STORY_MARKERS)
    has_start = bool(re.search(r"\b(when i|one day|years ago|let me tell|i used to)\b", text, re.I))
    has_end = bool(re.search(r"\b(so |therefore|finally|the result|ended up|that's why)\b", text, re.I))

    score = 0.2
    if n_sent >= 2:
        score += 0.2
    if n_sent >= 4:
        score += 0.15
    if markers >= 1:
        score += 0.15
    if markers >= 3:
        score += 0.1
    if has_start:
        score += 0.1
    if has_end:
        score += 0.1
    # Prefer windows that aren't truncated mid-thought (end punctuation)
    if text.strip()[-1:] in ".!?":
        score += 0.05
    return _clamp01(score), f"{n_sent} sentences, {markers} story markers, arc_start={has_start}, arc_end={has_end}."


def _curiosity_score(text: str, hooks_categories: set[str]) -> tuple[float, str]:
    score = 0.2
    reasons = []
    if "curiosity" in hooks_categories or "question" in hooks_categories:
        score += 0.35
        reasons.append("curiosity/question hooks")
    if re.search(r"\b(but|however|except|secret|hidden|nobody)\b", text, re.I):
        score += 0.2
        reasons.append("contrast/secret language")
    if "?" in text:
        score += 0.15
        reasons.append("contains questions")
    if re.search(r"\b(you|your)\b", text, re.I):
        score += 0.1
        reasons.append("direct address")
    return _clamp01(score), ("Signals: " + ", ".join(reasons) + ".") if reasons else "Low curiosity markers."


def _pacing_score(text: str, duration_ms: int, words: list[str]) -> tuple[float, str]:
    if duration_ms <= 0:
        return 0.0, "Zero duration."
    duration_s = duration_ms / 1000.0
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    # Ideal short-form: new idea every ~6–12s
    if not sentences:
        return 0.2, "No sentence boundaries."
    avg_sent_s = duration_s / len(sentences)
    if 5 <= avg_sent_s <= 12:
        score = 0.9
        note = f"Good idea cadence (~{avg_sent_s:.1f}s/sentence)."
    elif 3 <= avg_sent_s < 5 or 12 < avg_sent_s <= 18:
        score = 0.65
        note = f"Acceptable cadence (~{avg_sent_s:.1f}s/sentence)."
    else:
        score = 0.35
        note = f"Uneven cadence (~{avg_sent_s:.1f}s/sentence)."
    # Penalize very short or very long clips outside sweet spot later in selection;
    # here only internal pacing.
    return _clamp01(score), note


def _silence_penalty(
    duration_ms: int,
    words: list[str],
    *,
    segment_gaps_ms: Optional[list[int]] = None,
) -> tuple[float, str]:
    """Return penalty in [0,1] (higher = worse)."""
    if duration_ms <= 0:
        return 1.0, "Empty duration."
    duration_s = duration_ms / 1000.0
    wpm = (len(words) / duration_s) * 60.0 if duration_s else 0.0
    penalty = 0.0
    notes = []
    if wpm < 60:
        penalty += 0.5
        notes.append(f"low density ({wpm:.0f} wpm)")
    elif wpm < 90:
        penalty += 0.25
        notes.append(f"somewhat sparse ({wpm:.0f} wpm)")
    if segment_gaps_ms:
        long_gaps = [g for g in segment_gaps_ms if g >= 1500]
        if long_gaps:
            gap_ratio = min(1.0, sum(long_gaps) / duration_ms)
            penalty = _clamp01(penalty + gap_ratio * 0.6)
            notes.append(f"{len(long_gaps)} long gaps")
    return _clamp01(penalty), ("Silence issues: " + ", ".join(notes) + ".") if notes else "No major silence issues."


def _repetition_penalty(words: list[str]) -> tuple[float, str]:
    if len(words) < 8:
        return 0.0, "Too short to measure repetition."
    # Bigram repetition
    bigrams = list(zip(words, words[1:]))
    if not bigrams:
        return 0.0, "No bigrams."
    counts = Counter(bigrams)
    most_common_n = counts.most_common(1)[0][1]
    ratio = most_common_n / len(bigrams)
    # Unique word ratio
    unique_ratio = len(set(words)) / len(words)
    penalty = 0.0
    notes = []
    if ratio > 0.08:
        penalty += min(0.6, (ratio - 0.08) * 4)
        notes.append(f"repeated phrases (top bigram {ratio:.0%})")
    if unique_ratio < 0.45:
        penalty += 0.3
        notes.append(f"low lexical diversity ({unique_ratio:.0%})")
    return _clamp01(penalty), ("Repetition: " + ", ".join(notes) + ".") if notes else "Low repetition."


def score_transcript_window(
    text: str,
    start_ms: int,
    end_ms: int,
    *,
    weights: Optional[ScoringWeights] = None,
    segment_gaps_ms: Optional[list[int]] = None,
) -> ScoreBreakdown:
    """Score a single transcript window. Pure and deterministic."""
    weights = weights or ScoringWeights()
    duration_ms = max(0, end_ms - start_ms)
    words = _tokenize(text)
    hooks = detect_hooks(text, start_ms=start_ms, end_ms=end_ms)
    hook_s, hook_e = hook_strength_score(hooks)
    emotion_s, emotion_e = _emotion_score(words)
    energy_s, energy_e = _speech_energy_score(text, duration_ms, words=words)
    keyword_s, keyword_e = _keyword_score(words)
    story_s, story_e = _story_completeness_score(text, words)
    curiosity_s, curiosity_e = _curiosity_score(text, {h.category for h in hooks})
    pacing_s, pacing_e = _pacing_score(text, duration_ms, words)
    silence_p, silence_e = _silence_penalty(duration_ms, words, segment_gaps_ms=segment_gaps_ms)
    rep_p, rep_e = _repetition_penalty(words)

    pos_weights = weights.normalized_positive()
    weighted = (
        hook_s * pos_weights["hook_strength"]
        + emotion_s * pos_weights["emotional_intensity"]
        + energy_s * pos_weights["speech_energy"]
        + keyword_s * pos_weights["keyword_importance"]
        + story_s * pos_weights["story_completeness"]
        + curiosity_s * pos_weights["audience_curiosity"]
        + pacing_s * pos_weights["pacing"]
    )
    final = weighted
    final -= silence_p * weights.silence_penalty_weight
    final -= rep_p * weights.repetition_penalty_weight
    final = _clamp01(final)

    return ScoreBreakdown(
        hook_strength=round(hook_s, 4),
        emotional_intensity=round(emotion_s, 4),
        speech_energy=round(energy_s, 4),
        keyword_importance=round(keyword_s, 4),
        story_completeness=round(story_s, 4),
        audience_curiosity=round(curiosity_s, 4),
        pacing=round(pacing_s, 4),
        silence_penalty=round(silence_p, 4),
        repetition_penalty=round(rep_p, 4),
        final_score=round(final, 4),
        weights_used={
            **{k: round(v, 4) for k, v in pos_weights.items()},
            "silence_penalty_weight": weights.silence_penalty_weight,
            "repetition_penalty_weight": weights.repetition_penalty_weight,
        },
        explanations={
            "hook_strength": hook_e,
            "emotional_intensity": emotion_e,
            "speech_energy": energy_e,
            "keyword_importance": keyword_e,
            "story_completeness": story_e,
            "audience_curiosity": curiosity_e,
            "pacing": pacing_e,
            "silence_penalty": silence_e,
            "repetition_penalty": rep_e,
        },
    )


def score_clip(
    text: str,
    start_ms: int,
    end_ms: int,
    *,
    weights: Optional[ScoringWeights] = None,
    segment_gaps_ms: Optional[list[int]] = None,
) -> ScoreBreakdown:
    """Public alias for scoring a clip window."""
    return score_transcript_window(
        text,
        start_ms,
        end_ms,
        weights=weights,
        segment_gaps_ms=segment_gaps_ms,
    )


def extract_topics(text: str, *, max_topics: int = 5) -> list[str]:
    """Heuristic topic tags from importance keywords present in text."""
    words = _tokenize(text)
    found = []
    for w in words:
        if w in _IMPORTANCE_WORDS and w not in found:
            found.append(w)
        if len(found) >= max_topics:
            break
    return found

```


---

## Source: `backend/clip_intelligence/hooks.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Rule-based hook detection foundation (Phase 6).

No external AI APIs. Patterns are configurable lists of regexes / keyword
groups with strengths. Matches are evidence of *patterns*, not predictions
of virality.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional

from backend.clip_intelligence.models import HookMatch


@dataclass(frozen=True)
class HookPattern:
    pattern_id: str
    label: str
    category: str
    strength: float
    regex: re.Pattern[str]
    confidence: float = 0.75


def _p(
    pattern_id: str,
    label: str,
    category: str,
    strength: float,
    pattern: str,
    confidence: float = 0.75,
    flags: int = re.IGNORECASE,
) -> HookPattern:
    return HookPattern(
        pattern_id=pattern_id,
        label=label,
        category=category,
        strength=max(0.0, min(1.0, strength)),
        regex=re.compile(pattern, flags),
        confidence=confidence,
    )


# Default pattern catalog — extend by appending HookPattern instances.
DEFAULT_HOOK_PATTERNS: list[HookPattern] = [
    # Strong openings
    _p("open_did_you_know", "Did you know", "opening", 0.85, r"\bdid you know\b"),
    _p("open_here_is_why", "Here's why", "opening", 0.80, r"\bhere'?s why\b"),
    _p("open_the_truth", "The truth is", "opening", 0.75, r"\bthe truth (is|about)\b"),
    _p("open_nobody_talks", "Nobody talks about", "opening", 0.85, r"\bnobody (talks|tells|wants)\b"),
    _p("open_stop_doing", "Stop doing", "opening", 0.80, r"\bstop (doing|saying|buying|using)\b"),
    _p("open_i_was_wrong", "I was wrong", "opening", 0.78, r"\bi was (wrong|lying|mistaken)\b"),
    _p("open_secret", "Secret", "opening", 0.72, r"\b(secret|secrets) (to|of|about)\b"),
    # Curiosity gaps
    _p("curiosity_but", "But...", "curiosity", 0.70, r"\bbut (here'?s|what|the|then)\b"),
    _p("curiosity_wait", "Wait until", "curiosity", 0.82, r"\bwait (until|till|for)\b"),
    _p("curiosity_what_happened", "What happened next", "curiosity", 0.80, r"\bwhat happened (next|was)\b"),
    _p("curiosity_you_wont_believe", "You won't believe", "curiosity", 0.85, r"\byou (won'?t|will not) believe\b"),
    _p("curiosity_most_people", "Most people", "curiosity", 0.72, r"\bmost people (don'?t|never|think|believe)\b"),
    # Questions
    _p("question_why", "Why question", "question", 0.75, r"\bwhy (do|does|did|is|are|can|would|should)\b.+\?"),
    _p("question_how", "How question", "question", 0.72, r"\bhow (do|does|did|can|to|would)\b.+\?"),
    _p("question_what_if", "What if", "question", 0.78, r"\bwhat if\b"),
    _p("question_generic", "Direct question", "question", 0.55, r"\?\s*$"),
    # Surprising claims
    _p("claim_never", "Never / always absolute", "claim", 0.70, r"\b(never|always) (do|say|use|buy|tell)\b"),
    _p("claim_number", "Big number claim", "claim", 0.68, r"\b\d{2,}%\b|\b\d+\s*(million|billion|thousand)\b"),
    _p("claim_scientists", "Authority claim", "claim", 0.74, r"\b(scientists|research|study|studies) (show|found|prove|say)\b"),
    _p("claim_everyone_wrong", "Everyone is wrong", "claim", 0.80, r"\beveryone (is wrong|thinks|believes)\b"),
    # Emotional phrases
    _p("emotion_shock", "Shock / insane", "emotion", 0.70, r"\b(insane|shocking|unbelievable|crazy|mind[- ]?blowing)\b"),
    _p("emotion_fear", "Fear / warning", "emotion", 0.72, r"\b(warning|danger|risk|scared|afraid|terrified)\b"),
    _p("emotion_anger", "Anger / frustration", "emotion", 0.68, r"\b(furious|angry|hate|outrageous|ridiculous)\b"),
    _p("emotion_joy", "Excitement", "emotion", 0.60, r"\b(amazing|incredible|awesome|life[- ]?changing)\b"),
    _p("emotion_vulnerability", "Personal vulnerability", "emotion", 0.74, r"\bi (cried|failed|lost everything|hit rock bottom)\b"),
    # Story beginnings
    _p("story_years_ago", "Years ago", "story", 0.70, r"\b\d+\s+years ago\b|\byears ago\b"),
    _p("story_when_i", "When I...", "story", 0.72, r"\bwhen i (was|first|started|realized)\b"),
    _p("story_one_day", "One day", "story", 0.68, r"\b(one day|the day|that day)\b"),
    _p("story_let_me_tell", "Let me tell you", "story", 0.75, r"\blet me tell you\b"),
    _p("story_true_story", "True story", "story", 0.78, r"\btrue story\b"),
]


def detect_hooks(
    text: str,
    *,
    patterns: Optional[Iterable[HookPattern]] = None,
    start_ms: Optional[int] = None,
    end_ms: Optional[int] = None,
    max_matches: int = 12,
) -> list[HookMatch]:
    """Return hook matches found in ``text``.

    Deterministic: same text + patterns → same ordered results.
    Ordering: strength desc, then pattern_id asc for stable ties.
    """
    if not text or not text.strip():
        return []

    catalog = list(patterns) if patterns is not None else DEFAULT_HOOK_PATTERNS
    matches: list[HookMatch] = []
    seen_ids: set[str] = set()

    for pattern in catalog:
        m = pattern.regex.search(text)
        if not m:
            continue
        if pattern.pattern_id in seen_ids:
            continue
        seen_ids.add(pattern.pattern_id)
        matched = m.group(0).strip()
        matches.append(
            HookMatch(
                pattern_id=pattern.pattern_id,
                label=pattern.label,
                category=pattern.category,
                strength=pattern.strength,
                matched_text=matched[:200],
                start_ms=start_ms,
                end_ms=end_ms,
                confidence=pattern.confidence,
            )
        )

    matches.sort(key=lambda h: (-h.strength, h.pattern_id))
    return matches[:max_matches]


def hook_strength_score(hooks: list[HookMatch], *, opening_window_bonus: float = 0.1) -> tuple[float, str]:
    """Aggregate hook matches into a [0,1] score + explanation."""
    if not hooks:
        return 0.15, "No strong hook patterns detected in the window."

    # Best match dominates; secondary matches add diminishing returns.
    best = hooks[0].strength
    extra = 0.0
    for h in hooks[1:4]:
        extra += h.strength * 0.12
    score = min(1.0, best + extra)

    # Small bonus if any opening/curiosity category present
    cats = {h.category for h in hooks}
    if "opening" in cats or "curiosity" in cats:
        score = min(1.0, score + opening_window_bonus * 0.5)

    labels = ", ".join(h.label for h in hooks[:3])
    return round(score, 4), f"Detected hooks: {labels}."

```


---

## Source: `backend/clip_intelligence/selection.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Deterministic candidate generation and clip selection (Phase 6)."""
from __future__ import annotations

from typing import Any, Optional

from backend.clip_intelligence.hooks import detect_hooks
from backend.clip_intelligence.models import ClipCandidate, ScoringWeights
from backend.clip_intelligence.scoring import extract_topics, score_transcript_window


def _segment_bounds_ms(seg: dict[str, Any]) -> tuple[int, int]:
    """Read start/end from a Whisper-like segment (seconds or ms)."""
    if "start_ms" in seg and "end_ms" in seg:
        return int(seg["start_ms"]), int(seg["end_ms"])
    start = float(seg.get("start", 0.0))
    end = float(seg.get("end", start))
    return int(start * 1000 + 0.5), int(end * 1000 + 0.5)


def _segment_text(seg: dict[str, Any]) -> str:
    return (seg.get("text") or seg.get("word") or "").strip()


def windows_overlap(
    a_start: int,
    a_end: int,
    b_start: int,
    b_end: int,
    *,
    tolerance_ms: int = 2000,
) -> bool:
    """Return True if intervals overlap beyond ``tolerance_ms`` on each side.

    Mirrors legacy clip_extractor 2s tolerance: intervals may touch within
    tolerance without counting as overlap.
    """
    return a_start < b_end - tolerance_ms and a_end > b_start + tolerance_ms


def remove_overlapping_candidates(
    candidates: list[ClipCandidate],
    *,
    tolerance_ms: int = 2000,
) -> list[ClipCandidate]:
    """Keep highest-scoring non-overlapping candidates.

    Input should preferably be sorted by score desc; if not, we sort first.
    Deterministic: ties broken by earlier start_ms, then id.
    """
    ordered = sorted(
        candidates,
        key=lambda c: (-c.final_score(), c.start_ms, c.id),
    )
    kept: list[ClipCandidate] = []
    for cand in ordered:
        if any(
            windows_overlap(
                cand.start_ms, cand.end_ms, k.start_ms, k.end_ms, tolerance_ms=tolerance_ms
            )
            for k in kept
        ):
            continue
        kept.append(cand)
    return kept


def dedupe_near_identical(
    candidates: list[ClipCandidate],
    *,
    time_tolerance_ms: int = 1500,
    text_prefix: int = 80,
) -> list[ClipCandidate]:
    """Drop near-duplicate windows (same rough start and same text prefix)."""
    ordered = sorted(candidates, key=lambda c: (-c.final_score(), c.start_ms, c.id))
    kept: list[ClipCandidate] = []
    for cand in ordered:
        prefix = (cand.text or "")[:text_prefix].strip().lower()
        dup = False
        for k in kept:
            if abs(cand.start_ms - k.start_ms) <= time_tolerance_ms:
                k_prefix = (k.text or "")[:text_prefix].strip().lower()
                if prefix and prefix == k_prefix:
                    dup = True
                    break
                if abs(cand.end_ms - k.end_ms) <= time_tolerance_ms and abs(
                    cand.duration_ms - k.duration_ms
                ) <= time_tolerance_ms:
                    dup = True
                    break
        if not dup:
            kept.append(cand)
    return kept


def _build_window_text(
    segments: list[dict[str, Any]],
    start_ms: int,
    end_ms: int,
) -> tuple[str, list[int]]:
    """Join segment texts overlapping [start_ms, end_ms); return text + internal gaps."""
    parts: list[str] = []
    gaps: list[int] = []
    prev_end: Optional[int] = None
    for seg in segments:
        s, e = _segment_bounds_ms(seg)
        if e <= start_ms or s >= end_ms:
            continue
        t = _segment_text(seg)
        if not t:
            continue
        if prev_end is not None and s > prev_end:
            gaps.append(s - prev_end)
        parts.append(t)
        prev_end = e
    return " ".join(parts).strip(), gaps


def generate_candidates(
    segments: list[dict[str, Any]],
    *,
    min_duration_ms: int = 15_000,
    max_duration_ms: int = 60_000,
    step_ms: int = 5_000,
    weights: Optional[ScoringWeights] = None,
    max_candidates: int = 80,
) -> list[ClipCandidate]:
    """Slide windows across the transcript and score each candidate.

    Deterministic sliding windows anchored to segment starts when possible.
    """
    weights = weights or ScoringWeights()
    if not segments:
        return []

    # Collect ordered segment starts
    bounds = []
    for seg in segments:
        s, e = _segment_bounds_ms(seg)
        if e > s:
            bounds.append((s, e))
    if not bounds:
        return []

    bounds.sort(key=lambda x: x[0])
    timeline_start = bounds[0][0]
    timeline_end = bounds[-1][1]

    # Candidate window starts: every step from timeline_start, plus each segment start
    starts: list[int] = []
    t = timeline_start
    while t + min_duration_ms <= timeline_end:
        starts.append(t)
        t += step_ms
    for s, _ in bounds:
        if s + min_duration_ms <= timeline_end:
            starts.append(s)
    starts = sorted(set(starts))

    # Duration ladder: min, mid, max
    mid = (min_duration_ms + max_duration_ms) // 2
    durations = sorted({min_duration_ms, mid, max_duration_ms})

    candidates: list[ClipCandidate] = []
    for start in starts:
        for dur in durations:
            end = start + dur
            if end > timeline_end + 500:
                continue
            text, gaps = _build_window_text(segments, start, end)
            if len(text.split()) < 8:
                continue
            score = score_transcript_window(
                text, start, end, weights=weights, segment_gaps_ms=gaps
            )
            hooks = detect_hooks(text, start_ms=start, end_ms=end)
            topics = extract_topics(text)
            # Confidence: blend score with word coverage
            conf = min(1.0, 0.4 + score.final_score * 0.5 + min(0.1, len(text.split()) / 200.0))
            title = None
            if hooks:
                title = hooks[0].matched_text[:60]
            elif text:
                title = " ".join(text.split()[:8])
            candidates.append(
                ClipCandidate(
                    start_ms=start,
                    end_ms=end,
                    text=text,
                    score=score,
                    hooks=hooks,
                    topics=topics,
                    title_suggestion=title,
                    confidence=round(conf, 4),
                )
            )

    # Keep top raw candidates before selection
    candidates.sort(key=lambda c: (-c.final_score(), c.start_ms, c.id))
    return candidates[:max_candidates]


def select_clips(
    candidates: list[ClipCandidate],
    *,
    max_clips: int = 5,
    min_duration_ms: int = 5_000,
    max_duration_ms: int = 120_000,
    min_score: float = 0.0,
    overlap_tolerance_ms: int = 2000,
) -> list[ClipCandidate]:
    """Rank, filter duration, dedupe, remove overlaps, return top clips."""
    filtered = [
        c
        for c in candidates
        if c.duration_ms >= min_duration_ms
        and c.duration_ms <= max_duration_ms
        and c.final_score() >= min_score
    ]
    filtered = dedupe_near_identical(filtered)
    filtered = remove_overlapping_candidates(filtered, tolerance_ms=overlap_tolerance_ms)
    filtered.sort(key=lambda c: (-c.final_score(), c.start_ms, c.id))
    return filtered[: max(0, max_clips)]


def candidates_to_legacy_windows(candidates: list[ClipCandidate]) -> list[dict[str, Any]]:
    """Convert selected candidates to clip_extractor window dict shape."""
    out = []
    for c in candidates:
        reason_parts = []
        if c.score.explanations.get("hook_strength"):
            reason_parts.append(c.score.explanations["hook_strength"])
        if c.hooks:
            reason_parts.append("Hooks: " + ", ".join(h.label for h in c.hooks[:3]))
        reason_parts.append(f"Deterministic score {c.final_score():.2f}")
        out.append(
            {
                "start": round(c.start_s, 1),
                "end": round(c.end_s, 1),
                "title": c.title_suggestion or "Clip",
                "hook": c.hooks[0].matched_text if c.hooks else (c.text.split(".")[0][:120] if c.text else ""),
                "reason": " ".join(reason_parts),
                "virality_score": c.score.to_virality_10(),
                "score_breakdown": c.score.as_display_dict(),
                "topics": list(c.topics),
                "confidence": c.confidence,
                "clip_candidate_id": c.id,
                "selection_method": "deterministic_v1",
            }
        )
    return out

```


---

## Source: `backend/clip_intelligence/enhancement.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Intelligent clip enhancement pipeline (Phase 7).

Produces an enhancement *plan* (no video rendering). Combines silence
analysis, boundary optimization, pacing metrics, caption/export settings.
"""
from __future__ import annotations

from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.clip_intelligence.boundaries import (
    BoundaryConfig,
    BoundaryOptimization,
    optimize_boundaries,
)
from backend.clip_intelligence.pacing import PacingMetrics, analyze_pacing
from backend.clip_intelligence.silence import SilenceAnalysis, SilenceConfig, detect_silence
from backend.clip_intelligence.hooks import detect_hooks
from backend.clip_intelligence.scoring import score_transcript_window
from backend.clip_intelligence.models import ScoringWeights


class CaptionPlan(BaseModel):
    """Caption configuration suggestion for export (not rendered here)."""

    enabled: bool = True
    style: str = "viral"
    animation_preset_id: Optional[str] = None
    emoji_style: str = "moderate"
    reason: str = ""


class ExportPlan(BaseModel):
    """Export settings suggestion."""

    aspect_ratio: str = "9:16"
    target_duration_ms: Optional[int] = None
    trim_start_ms: int = 0
    trim_end_ms: int = 0
    # Relative to original source timeline
    source_start_ms: int = 0
    source_end_ms: int = 0
    notes: list[str] = Field(default_factory=list)


class EnhancementConfig(BaseModel):
    """Pipeline configuration."""

    silence: SilenceConfig = Field(default_factory=SilenceConfig)
    boundaries: BoundaryConfig = Field(default_factory=BoundaryConfig)
    caption_style: str = "viral"
    animation_preset_id: Optional[str] = None
    prefer_animation_preset: bool = False
    aspect_ratio: str = "9:16"
    scoring_weights: Optional[ScoringWeights] = None


class EnhancementPlan(BaseModel):
    """Full enhancement plan for one selected clip."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    video_id: Optional[str] = None
    original_start_ms: int
    original_end_ms: int
    optimized_start_ms: int
    optimized_end_ms: int
    boundaries: BoundaryOptimization
    silence: SilenceAnalysis
    pacing: PacingMetrics
    hooks: list[dict[str, Any]] = Field(default_factory=list)
    score_before: Optional[dict[str, Any]] = None
    score_after: Optional[dict[str, Any]] = None
    captions: CaptionPlan = Field(default_factory=CaptionPlan)
    export: ExportPlan = Field(default_factory=ExportPlan)
    recommendations: list[str] = Field(default_factory=list)
    method: str = "enhancement_v1"

    def as_summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "original": {
                "start_ms": self.original_start_ms,
                "end_ms": self.original_end_ms,
                "duration_ms": self.original_end_ms - self.original_start_ms,
            },
            "optimized": {
                "start_ms": self.optimized_start_ms,
                "end_ms": self.optimized_end_ms,
                "duration_ms": self.optimized_end_ms - self.optimized_start_ms,
            },
            "changed": self.boundaries.changed,
            "pacing_rating": self.pacing.rating,
            "silence_ratio": self.silence.silence_ratio,
            "recommendations": list(self.recommendations),
            "captions": self.captions.model_dump(),
            "export": self.export.model_dump(),
        }


def _text_for_window(
    segments: list[dict[str, Any]], start_ms: int, end_ms: int
) -> str:
    from backend.clip_intelligence.silence import speech_units_in_window

    units = speech_units_in_window(segments, start_ms, end_ms)
    return " ".join(t for _, _, t in units if t).strip()


def _caption_plan(
    pacing: PacingMetrics,
    hooks: list,
    config: EnhancementConfig,
) -> CaptionPlan:
    style = config.caption_style
    preset = config.animation_preset_id
    reason_parts = []

    if config.prefer_animation_preset or (hooks and pacing.words_per_minute >= 120):
        if not preset:
            # Suggest animation preset from content
            if any(getattr(h, "category", None) == "question" or (isinstance(h, dict) and h.get("category") == "question") for h in hooks):
                preset = "karaoke"
            elif pacing.rating in ("fast", "dense"):
                preset = "bounce"
            else:
                preset = "explosive"
        reason_parts.append(f"Suggested animation preset '{preset}' for short-form energy.")
    else:
        reason_parts.append(f"Using ASS style '{style}'.")

    if pacing.filler_ratio > 0.1:
        reason_parts.append("Consider moderate emojis only — high filler speech.")
        emoji = "minimal"
    else:
        emoji = "moderate"

    return CaptionPlan(
        enabled=True,
        style=style,
        animation_preset_id=preset,
        emoji_style=emoji,
        reason=" ".join(reason_parts),
    )


def _recommendations(
    silence: SilenceAnalysis,
    pacing: PacingMetrics,
    boundaries: BoundaryOptimization,
    score_before: Optional[float],
    score_after: Optional[float],
) -> list[str]:
    recs: list[str] = []
    if boundaries.changed:
        recs.append(
            f"Use optimized bounds "
            f"{boundaries.optimized_start_ms}–{boundaries.optimized_end_ms} ms "
            f"(was {boundaries.original_start_ms}–{boundaries.original_end_ms})."
        )
    if silence.leading_ms() >= 500:
        recs.append(f"Remove ~{silence.leading_ms()} ms leading silence.")
    if silence.trailing_ms() >= 500:
        recs.append(f"Remove ~{silence.trailing_ms()} ms trailing silence.")
    if silence.internal_ms() >= 1200:
        recs.append(
            f"Consider tightening {silence.internal_ms()} ms of long internal pauses "
            "(plan only — not auto-cut in Phase 7)."
        )
    if pacing.rating == "slow":
        recs.append("Pacing is slow; prefer a tighter window or higher-energy section.")
    if pacing.rating == "fast":
        recs.append("Pacing is fast; captions with fewer words-per-group may read better.")
    if pacing.silence_ratio > 0.3:
        recs.append("Silence ratio is high; trim pauses before export.")
    if score_before is not None and score_after is not None:
        if score_after > score_before + 0.02:
            recs.append(
                f"Deterministic score improved {score_before:.2f} → {score_after:.2f} after optimization."
            )
        elif score_after + 0.02 < score_before:
            recs.append(
                f"Score slightly lower after trim ({score_before:.2f} → {score_after:.2f}); review hook lead-in."
            )
    if not recs:
        recs.append("Clip is already well-paced; proceed to export.")
    return recs


def build_enhancement_plan(
    segments: list[dict[str, Any]],
    start_ms: int,
    end_ms: int,
    *,
    video_id: Optional[str] = None,
    config: Optional[EnhancementConfig] = None,
    source_duration_ms: Optional[int] = None,
) -> EnhancementPlan:
    """Run the full enhancement pipeline and return a plan (no rendering)."""
    if end_ms < start_ms:
        raise ValueError("end_ms must be >= start_ms")

    config = config or EnhancementConfig()
    # Align boundary silence config
    boundary_cfg = config.boundaries.model_copy(
        update={"silence": config.silence}
    )

    silence = detect_silence(
        segments, start_ms, end_ms, config=config.silence
    )
    boundaries = optimize_boundaries(
        segments,
        start_ms,
        end_ms,
        config=boundary_cfg,
        source_duration_ms=source_duration_ms,
    )
    opt_s, opt_e = boundaries.optimized_start_ms, boundaries.optimized_end_ms

    pacing = analyze_pacing(
        segments, opt_s, opt_e, silence_config=config.silence
    )

    text_before = _text_for_window(segments, start_ms, end_ms)
    text_after = _text_for_window(segments, opt_s, opt_e)
    weights = config.scoring_weights or ScoringWeights()

    sb = score_transcript_window(text_before, start_ms, end_ms, weights=weights)
    sa = score_transcript_window(text_after, opt_s, opt_e, weights=weights)

    hooks = detect_hooks(text_after, start_ms=opt_s, end_ms=opt_e)
    hook_dicts = [h.model_dump() for h in hooks]

    captions = _caption_plan(pacing, hooks, config)
    export = ExportPlan(
        aspect_ratio=config.aspect_ratio,
        target_duration_ms=opt_e - opt_s,
        trim_start_ms=max(0, opt_s - start_ms),
        trim_end_ms=max(0, end_ms - opt_e),
        source_start_ms=opt_s,
        source_end_ms=opt_e,
        notes=list(boundaries.reasons),
    )

    recs = _recommendations(
        silence, pacing, boundaries, sb.final_score, sa.final_score
    )

    return EnhancementPlan(
        video_id=video_id,
        original_start_ms=start_ms,
        original_end_ms=end_ms,
        optimized_start_ms=opt_s,
        optimized_end_ms=opt_e,
        boundaries=boundaries,
        silence=silence,
        pacing=pacing,
        hooks=hook_dicts,
        score_before=sb.as_display_dict(),
        score_after=sa.as_display_dict(),
        captions=captions,
        export=export,
        recommendations=recs,
    )

```


---

## Source: `backend/caption_removal/detection.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Heuristic burned-in caption region detection (Phase 9).

Does not modify video. Uses optional frame sampling + short-form position priors.
When frames cannot be sampled, falls back to deterministic position templates.
"""
from __future__ import annotations

import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Optional

from backend.caption_removal.models import (
    CaptionRegion,
    CaptionRegionType,
    DetectionConfig,
    DetectionResult,
)

logger = logging.getLogger(__name__)


def probe_video(path: Path) -> dict[str, Any]:
    """Return width, height, fps, duration_s via ffprobe when available."""
    meta = {"width": 1080, "height": 1920, "fps": 30.0, "duration_s": 0.0}
    if not path.exists():
        return meta
    try:
        import json

        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,duration",
            "-show_entries", "format=duration",
            "-of", "json",
            str(path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return meta
        data = json.loads(result.stdout or "{}")
        streams = data.get("streams") or []
        if streams:
            s0 = streams[0]
            meta["width"] = int(s0.get("width") or meta["width"])
            meta["height"] = int(s0.get("height") or meta["height"])
            rate = s0.get("r_frame_rate") or "30/1"
            if "/" in str(rate):
                num, den = str(rate).split("/", 1)
                if float(den) != 0:
                    meta["fps"] = float(num) / float(den)
            if s0.get("duration"):
                meta["duration_s"] = float(s0["duration"])
        if meta["duration_s"] <= 0:
            fmt = data.get("format") or {}
            if fmt.get("duration"):
                meta["duration_s"] = float(fmt["duration"])
    except Exception as e:
        logger.debug("ffprobe failed for %s: %s", path, e)
    return meta


def _band_to_region(
    frame_w: int,
    frame_h: int,
    y0: float,
    y1: float,
    x_margin: float,
    region_type: CaptionRegionType,
    confidence: float,
    notes: Optional[list[str]] = None,
    score_detail: Optional[dict[str, float]] = None,
) -> CaptionRegion:
    x = int(round(frame_w * x_margin))
    y = int(round(frame_h * y0))
    w = max(1, int(round(frame_w * (1.0 - 2 * x_margin))))
    h = max(1, int(round(frame_h * (y1 - y0))))
    # Keep inside frame
    y = min(max(0, y), max(0, frame_h - 1))
    h = min(h, frame_h - y)
    w = min(w, frame_w - x)
    return CaptionRegion(
        x=x,
        y=y,
        width=w,
        height=h,
        confidence=max(0.0, min(1.0, confidence)),
        type=region_type,
        x_norm=x / frame_w if frame_w else 0,
        y_norm=y / frame_h if frame_h else 0,
        w_norm=w / frame_w if frame_w else 0,
        h_norm=h / frame_h if frame_h else 0,
        score_detail=score_detail or {},
        notes=notes or [],
    )


def _sample_frame_paths(
    video_path: Path,
    *,
    count: int,
    duration_s: float,
    out_dir: Path,
) -> list[Path]:
    """Extract evenly spaced JPEG frames for heuristics. Best-effort."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    if duration_s <= 0:
        duration_s = max(1.0, count * 0.5)
    for i in range(count):
        t = (i + 0.5) / count * duration_s
        out = out_dir / f"sample_{i:03d}.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{t:.3f}",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "5",
            str(out),
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if r.returncode == 0 and out.exists():
                paths.append(out)
        except Exception as e:
            logger.debug("frame sample failed: %s", e)
    return paths


def _luma_edge_score(image_path: Path, region: CaptionRegion) -> dict[str, float]:
    """Cheap contrast/edge proxy in a crop — high values often indicate burned text.

    Uses Pillow only. Returns component scores in [0,1].
    """
    try:
        from PIL import Image, ImageFilter, ImageStat, ImageOps
    except ImportError:
        return {"edge": 0.0, "contrast": 0.0, "bright_ratio": 0.0}

    try:
        im = Image.open(image_path).convert("L")
        crop = im.crop((region.x, region.y, region.x + region.width, region.y + region.height))
        if crop.size[0] < 4 or crop.size[1] < 4:
            return {"edge": 0.0, "contrast": 0.0, "bright_ratio": 0.0}
        # Downscale for speed
        crop = crop.resize((min(320, crop.size[0]), min(120, crop.size[1])))
        edges = crop.filter(ImageFilter.FIND_EDGES)
        estat = ImageStat.Stat(edges)
        edge_mean = float(estat.mean[0]) / 255.0
        cstat = ImageStat.Stat(crop)
        # RMS contrast proxy
        contrast = min(1.0, float(cstat.stddev[0]) / 64.0)
        # High-luma pixel ratio (white subtitles)
        hist = crop.histogram()
        total = sum(hist) or 1
        bright = sum(hist[200:]) / total
        return {
            "edge": min(1.0, edge_mean * 3.0),
            "contrast": contrast,
            "bright_ratio": bright,
        }
    except Exception as e:
        logger.debug("luma score failed: %s", e)
        return {"edge": 0.0, "contrast": 0.0, "bright_ratio": 0.0}


def _combine_confidence(parts: dict[str, float], prior: float) -> float:
    edge = parts.get("edge", 0.0)
    contrast = parts.get("contrast", 0.0)
    bright = parts.get("bright_ratio", 0.0)
    heuristic = 0.45 * edge + 0.30 * contrast + 0.25 * bright
    # Blend with position prior
    return max(0.0, min(1.0, 0.55 * heuristic + 0.45 * prior))


def detect_caption_regions(
    *,
    frame_width: int,
    frame_height: int,
    config: Optional[DetectionConfig] = None,
    video_path: Optional[Path] = None,
    fps: float = 30.0,
    duration_s: float = 0.0,
    sample_dir: Optional[Path] = None,
) -> DetectionResult:
    """Detect likely caption regions. Never mutates the video file."""
    config = config or DetectionConfig()
    notes: list[str] = []
    regions: list[CaptionRegion] = []

    if frame_width <= 0 or frame_height <= 0:
        raise ValueError("frame_width and frame_height must be positive")

    # Forced region short-circuit
    if config.force_region:
        fr = config.force_region
        xn = float(fr.get("x", 0.05))
        yn = float(fr.get("y", 0.75))
        wn = float(fr.get("width", 0.9))
        hn = float(fr.get("height", 0.18))
        region = CaptionRegion(
            x=int(xn * frame_width),
            y=int(yn * frame_height),
            width=max(1, int(wn * frame_width)),
            height=max(1, int(hn * frame_height)),
            confidence=1.0,
            type=CaptionRegionType.CUSTOM,
            x_norm=xn,
            y_norm=yn,
            w_norm=wn,
            h_norm=hn,
            notes=["Forced region from config."],
        )
        return DetectionResult(
            video_path=str(video_path) if video_path else None,
            frame_width=frame_width,
            frame_height=frame_height,
            fps=fps,
            duration_s=duration_s,
            regions=[region],
            config=config,
            notes=["Using force_region; heuristic sampling skipped."],
        )

    candidates: list[tuple[CaptionRegionType, float, float, float, float]] = []
    # type, prior, y0, y1
    if config.prefer_bottom or True:
        candidates.append(
            (CaptionRegionType.BOTTOM_CENTER, 0.72, config.bottom_band_top, config.bottom_band_bottom)
        )
        candidates.append(
            (CaptionRegionType.BOTTOM_FULL, 0.55, max(0.65, config.bottom_band_top - 0.05), config.bottom_band_bottom)
        )
    if config.include_center:
        candidates.append(
            (CaptionRegionType.CENTER, 0.45, config.center_band_top, config.center_band_bottom)
        )
    if config.include_top:
        candidates.append(
            (CaptionRegionType.TOP_CENTER, 0.40, config.top_band_top, config.top_band_bottom)
        )

    # Build base regions from priors
    base_regions: list[CaptionRegion] = []
    for rtype, prior, y0, y1 in candidates:
        base_regions.append(
            _band_to_region(
                frame_width,
                frame_height,
                y0,
                y1,
                config.x_margin,
                rtype,
                confidence=prior,
                notes=[f"Position prior {prior:.2f} for {rtype.value}."],
                score_detail={"prior": prior},
            )
        )

    # Optional frame sampling to refine confidence
    sample_paths: list[Path] = []
    if video_path and Path(video_path).exists() and sample_dir is not None:
        sample_paths = _sample_frame_paths(
            Path(video_path),
            count=config.sample_frames,
            duration_s=duration_s or 0.0,
            out_dir=sample_dir,
        )
        if sample_paths:
            notes.append(f"Sampled {len(sample_paths)} frames for contrast/edge heuristics.")
        else:
            notes.append("Frame sampling unavailable; using position priors only.")
    else:
        notes.append("No frame samples; using short-form position priors only.")

    for region in base_regions:
        parts_acc = {"edge": 0.0, "contrast": 0.0, "bright_ratio": 0.0}
        if sample_paths:
            for sp in sample_paths:
                parts = _luma_edge_score(sp, region)
                for k in parts_acc:
                    parts_acc[k] += parts.get(k, 0.0)
            n = len(sample_paths)
            parts_acc = {k: v / n for k, v in parts_acc.items()}
            prior = region.score_detail.get("prior", 0.5)
            conf = _combine_confidence(parts_acc, prior)
            region = region.model_copy(
                update={
                    "confidence": conf,
                    "score_detail": {**region.score_detail, **parts_acc, "combined": conf},
                    "notes": region.notes + [
                        f"edge={parts_acc['edge']:.2f}",
                        f"contrast={parts_acc['contrast']:.2f}",
                        f"bright={parts_acc['bright_ratio']:.2f}",
                    ],
                }
            )
        if region.confidence >= config.min_confidence:
            regions.append(region)

    # Always keep best bottom prior if nothing passed threshold (safe default for short-form)
    if not regions and base_regions:
        best = max(base_regions, key=lambda r: r.confidence)
        best = best.model_copy(
            update={
                "confidence": max(best.confidence, config.min_confidence),
                "notes": best.notes + ["Kept as fallback short-form bottom caption band."],
            }
        )
        regions.append(best)
        notes.append("No region exceeded min_confidence; returned fallback bottom band.")

    regions.sort(key=lambda r: -r.confidence)

    return DetectionResult(
        video_path=str(video_path) if video_path else None,
        frame_width=frame_width,
        frame_height=frame_height,
        fps=fps,
        duration_s=duration_s,
        regions=regions,
        config=config,
        notes=notes,
    )


def detect_from_video(
    video_path: Path,
    *,
    config: Optional[DetectionConfig] = None,
    sample_dir: Optional[Path] = None,
) -> DetectionResult:
    """Probe video then run detection."""
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    meta = probe_video(video_path)
    return detect_caption_regions(
        frame_width=meta["width"],
        frame_height=meta["height"],
        config=config,
        video_path=video_path,
        fps=meta["fps"],
        duration_s=meta["duration_s"],
        sample_dir=sample_dir,
    )

```


---

## Source: `backend/caption_removal/removal.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Pluggable burned-in caption removal backends (Phase 9).

Baseline uses FFmpeg ``delogo`` (spatial interpolation). This is not true
generative inpainting — quality varies. Interfaces stay model-agnostic so a
future AI inpainting backend can plug in without changing callers.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from backend.caption_removal.models import (
    MaskPlan,
    RemovalBackend,
    RemovalConfig,
    RemovalResult,
)

logger = logging.getLogger(__name__)


class CaptionRemovalBackend(ABC):
    """Renderer-independent removal interface."""

    name: str

    @abstractmethod
    def remove(
        self,
        video_path: Path,
        mask: MaskPlan,
        output_path: Path,
        *,
        config: RemovalConfig,
    ) -> RemovalResult:
        ...


class NoopBackend(CaptionRemovalBackend):
    name = "noop"

    def remove(
        self,
        video_path: Path,
        mask: MaskPlan,
        output_path: Path,
        *,
        config: RemovalConfig,
    ) -> RemovalResult:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video_path, output_path)
        return RemovalResult(
            success=True,
            backend=self.name,
            input_path=str(video_path),
            output_path=str(output_path),
            mask=mask,
            notes=["NOOP backend copied input without modification."],
            preserved={"note": "identical copy"},
        )


class DelogoBackend(CaptionRemovalBackend):
    """FFmpeg delogo baseline — fills rectangle via surrounding pixels."""

    name = "delogo"

    def remove(
        self,
        video_path: Path,
        mask: MaskPlan,
        output_path: Path,
        *,
        config: RemovalConfig,
    ) -> RemovalResult:
        if shutil.which("ffmpeg") is None:
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error="ffmpeg not found on PATH",
                mask=mask,
            )

        boxes = mask.delogo_boxes()
        if not boxes:
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error="No valid delogo boxes in mask plan",
                mask=mask,
            )

        # Chain delogo filters for each box
        show = 1 if config.show_delogo else 0
        filters = []
        for b in boxes:
            filters.append(
                f"delogo=x={b['x']}:y={b['y']}:w={b['w']}:h={b['h']}:show={show}"
            )
        vf = ",".join(filters)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vf", vf,
            "-c:a", "copy",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart",
            str(output_path),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error="ffmpeg delogo timed out",
                mask=mask,
            )

        if result.returncode != 0 or not output_path.exists():
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error=(result.stderr or "delogo failed")[:500],
                mask=mask,
            )

        return RemovalResult(
            success=True,
            backend=self.name,
            input_path=str(video_path),
            output_path=str(output_path),
            mask=mask,
            notes=[
                f"Applied FFmpeg delogo to {len(boxes)} region(s).",
                "delogo is spatial interpolation, not generative inpainting.",
            ],
            preserved={
                "audio": "copy",
                "video_codec": "libx264",
            },
        )


class BoxBlurBackend(CaptionRemovalBackend):
    """Blur caption band as a stronger visual fallback."""

    name = "boxblur"

    def remove(
        self,
        video_path: Path,
        mask: MaskPlan,
        output_path: Path,
        *,
        config: RemovalConfig,
    ) -> RemovalResult:
        if shutil.which("ffmpeg") is None:
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error="ffmpeg not found on PATH",
                mask=mask,
            )
        boxes = mask.delogo_boxes()
        if not boxes:
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error="No boxes for blur mask",
                mask=mask,
            )
        # Use first primary box: split, blur crop, overlay
        b = boxes[0]
        # boxblur on cropped region then overlay
        vf = (
            f"split[main][tmp];"
            f"[tmp]crop={b['w']}:{b['h']}:{b['x']}:{b['y']},"
            f"boxblur=10:1[blur];"
            f"[main][blur]overlay={b['x']}:{b['y']}"
        )
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-filter_complex", vf,
            "-c:a", "copy",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if result.returncode != 0 or not output_path.exists():
            return RemovalResult(
                success=False,
                backend=self.name,
                input_path=str(video_path),
                error=(result.stderr or "boxblur failed")[:500],
                mask=mask,
            )
        return RemovalResult(
            success=True,
            backend=self.name,
            input_path=str(video_path),
            output_path=str(output_path),
            mask=mask,
            notes=["Applied regional boxblur fallback (not true inpainting)."],
            preserved={"audio": "copy"},
        )


_BACKENDS: dict[str, CaptionRemovalBackend] = {
    RemovalBackend.DELOGO.value: DelogoBackend(),
    RemovalBackend.BOXBLUR.value: BoxBlurBackend(),
    RemovalBackend.NOOP.value: NoopBackend(),
}


def get_removal_backend(name: str | RemovalBackend) -> CaptionRemovalBackend:
    key = name.value if isinstance(name, RemovalBackend) else str(name)
    backend = _BACKENDS.get(key)
    if backend is None:
        known = ", ".join(sorted(_BACKENDS))
        raise ValueError(f"Unknown removal backend {key!r}. Known: {known}")
    return backend


def list_removal_backends() -> list[dict[str, str]]:
    return [
        {
            "id": "delogo",
            "name": "FFmpeg delogo",
            "description": "Spatial interpolation baseline (fast, imperfect).",
        },
        {
            "id": "boxblur",
            "name": "Regional boxblur",
            "description": "Blurs caption band as a stronger fallback.",
        },
        {
            "id": "noop",
            "name": "No-op copy",
            "description": "Copies input; for dry-run / tests.",
        },
    ]

```


---

## Source: `backend/caption_removal/pipeline.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""End-to-end caption removal foundation pipeline (Phase 9)."""
from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from backend.caption_removal.detection import detect_from_video, probe_video
from backend.caption_removal.masking import build_mask_plan, write_mask_preview_png
from backend.caption_removal.models import (
    DetectionConfig,
    DetectionResult,
    MaskPlan,
    RemovalConfig,
    RemovalResult,
)
from backend.caption_removal.removal import get_removal_backend

logger = logging.getLogger(__name__)


def analyze_caption_burnin(
    video_path: Path,
    *,
    detection_config: Optional[DetectionConfig] = None,
    sample_dir: Optional[Path] = None,
    write_mask_preview: bool = False,
    mask_preview_path: Optional[Path] = None,
    pad_px: int = 8,
    feather_px: int = 4,
) -> tuple[DetectionResult, MaskPlan]:
    """Detect caption regions and build a mask plan without modifying the video."""
    video_path = Path(video_path)
    cleanup_sample = False
    if sample_dir is None:
        sample_dir = Path(tempfile.mkdtemp(prefix="vm_capdetect_"))
        cleanup_sample = True
    try:
        detection = detect_from_video(
            video_path, config=detection_config, sample_dir=sample_dir
        )
        mask = build_mask_plan(
            detection,
            pad_px=pad_px,
            feather_px=feather_px,
            primary_only=True,
            min_confidence=detection_config.min_confidence if detection_config else 0.0,
        )
        if write_mask_preview:
            if mask_preview_path is None:
                mask_preview_path = sample_dir / "mask_preview.png"
            write_mask_preview_png(mask, Path(mask_preview_path))
        return detection, mask
    finally:
        if cleanup_sample and not write_mask_preview:
            shutil.rmtree(sample_dir, ignore_errors=True)


def remove_burned_captions(
    video_path: Path,
    output_path: Path,
    *,
    detection_config: Optional[DetectionConfig] = None,
    removal_config: Optional[RemovalConfig] = None,
    mask: Optional[MaskPlan] = None,
    detection: Optional[DetectionResult] = None,
) -> RemovalResult:
    """Analyze (if needed) and produce a cleaned copy of the video.

    Source file is never overwritten. Audio is copied when using delogo/boxblur.
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    removal_config = removal_config or RemovalConfig()
    detection_config = detection_config or DetectionConfig(
        min_confidence=removal_config.min_confidence
    )

    if not video_path.exists():
        return RemovalResult(
            success=False,
            backend=removal_config.backend.value,
            input_path=str(video_path),
            error=f"Input video not found: {video_path}",
        )

    meta = probe_video(video_path)

    if mask is None or detection is None:
        detection, mask = analyze_caption_burnin(
            video_path,
            detection_config=detection_config,
            pad_px=removal_config.pad_px,
            feather_px=removal_config.feather_px,
        )
    else:
        # Rebuild mask padding from config
        mask = build_mask_plan(
            detection,
            pad_px=removal_config.pad_px,
            feather_px=removal_config.feather_px,
            primary_only=removal_config.prefer_primary_region_only,
            min_confidence=removal_config.min_confidence,
        )

    if removal_config.dry_run:
        return RemovalResult(
            success=True,
            backend="dry_run",
            input_path=str(video_path),
            output_path=None,
            detection=detection,
            mask=mask,
            notes=["Dry run — no video written."],
            preserved={
                "width": meta["width"],
                "height": meta["height"],
                "fps": meta["fps"],
                "duration_s": meta["duration_s"],
            },
        )

    if output_path.resolve() == video_path.resolve():
        return RemovalResult(
            success=False,
            backend=removal_config.backend.value,
            input_path=str(video_path),
            error="Refusing to overwrite source video; choose a different output_path.",
            detection=detection,
            mask=mask,
        )

    backend = get_removal_backend(removal_config.backend)
    result = backend.remove(video_path, mask, output_path, config=removal_config)
    result.detection = detection
    result.mask = mask
    result.preserved = {
        **(result.preserved or {}),
        "width": meta["width"],
        "height": meta["height"],
        "fps": meta["fps"],
        "duration_s": meta["duration_s"],
        "source_untouched": True,
    }
    return result

```


---

## Source: `backend/production_pipeline/reframe.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Deterministic auto-reframe planning for 9:16 short-form (Phase 10).

Tracking logic is pure math over source dimensions + mode — no rendering here.
Face/speaker modes use upper-third / center heuristics suitable for talking-head
content without requiring MediaPipe at plan time (optional sample refinement later).
"""
from __future__ import annotations

from typing import Optional

from backend.production_pipeline.models import (
    AutoReframePlan,
    CropKeyframe,
    CropRect,
    TrackMode,
)


def list_track_modes() -> list[dict]:
    return [
        {"id": "center", "name": "Center crop", "description": "Static centered 9:16 crop"},
        {"id": "face_center", "name": "Face center", "description": "Upper-third bias for talking heads"},
        {"id": "speaker", "name": "Speaker", "description": "Slower-smoothed face-center path"},
        {"id": "subject", "name": "Subject", "description": "Mid-frame subject bias with gentle pan"},
        {"id": "custom", "name": "Custom", "description": "Uses provided focus_x_norm"},
    ]


def _target_crop_size(src_w: int, src_h: int, target_aspect: float = 9 / 16) -> tuple[int, int]:
    """Largest crop inside source matching target aspect (width/height)."""
    src_aspect = src_w / src_h if src_h else target_aspect
    if src_aspect > target_aspect:
        # Source wider than 9:16 — full height, crop width
        h = src_h
        w = max(2, int(round(h * target_aspect)))
        w -= w % 2
        h -= h % 2
    else:
        # Source taller or equal — full width, crop height
        w = src_w
        h = max(2, int(round(w / target_aspect)))
        w -= w % 2
        h -= h % 2
    w = min(w, src_w - (src_w % 2))
    h = min(h, src_h - (src_h % 2))
    return max(2, w), max(2, h)


def _clamp_crop(x: int, y: int, w: int, h: int, src_w: int, src_h: int) -> CropRect:
    x = max(0, min(x, max(0, src_w - w)))
    y = max(0, min(y, max(0, src_h - h)))
    return CropRect(x=x, y=y, width=w, height=h)


def _focus_to_crop(
    src_w: int,
    src_h: int,
    crop_w: int,
    crop_h: int,
    focus_x: float,
    focus_y: float,
) -> CropRect:
    """Place crop so focus point (normalized 0–1) sits near crop center."""
    cx = focus_x * src_w
    cy = focus_y * src_h
    x = int(round(cx - crop_w / 2))
    y = int(round(cy - crop_h / 2))
    return _clamp_crop(x, y, crop_w, crop_h, src_w, src_h)


def _mode_focus(mode: TrackMode, t_norm: float = 0.5) -> tuple[float, float, float]:
    """Return (focus_x, focus_y, confidence) for mode at normalized time t∈[0,1]."""
    if mode == TrackMode.CENTER:
        return 0.5, 0.5, 0.9
    if mode == TrackMode.FACE_CENTER:
        # Talking-head: faces sit upper-center; slight horizontal stillness
        return 0.5, 0.38, 0.72
    if mode == TrackMode.SPEAKER:
        return 0.5, 0.36, 0.70
    if mode == TrackMode.SUBJECT:
        # Gentle horizontal drift simulation (deterministic sine-free: piecewise)
        # Use triangle path left-center-right-center for motion interest
        phase = (t_norm * 2) % 2
        if phase < 1:
            fx = 0.45 + 0.10 * phase
        else:
            fx = 0.55 - 0.10 * (phase - 1)
        return fx, 0.45, 0.60
    # custom defaults to center unless overridden by caller
    return 0.5, 0.5, 0.5


def _smooth_path(
    keyframes: list[CropKeyframe],
    smoothing: float,
    center_crop: CropRect,
) -> list[CropKeyframe]:
    """Blend each keyframe toward the previous and the center crop to avoid jumps."""
    if not keyframes:
        return []
    s = max(0.0, min(1.0, smoothing))
    out: list[CropKeyframe] = []
    prev = keyframes[0].crop
    src_w = center_crop.x + center_crop.width + max(center_crop.x, 1)  # unused fallback
    # Prefer dimensions from crop size (same for all keyframes)
    cw, ch = keyframes[0].crop.width, keyframes[0].crop.height
    # Infer source bounds from center crop placement (center is clamped already)
    # Callers re-clamp with real source size after smooth — keep non-negative here.
    for i, kf in enumerate(keyframes):
        if i == 0:
            x = int(round(kf.crop.x * (1 - s * 0.3) + center_crop.x * (s * 0.3)))
            y = int(round(kf.crop.y * (1 - s * 0.3) + center_crop.y * (s * 0.3)))
            crop = CropRect(x=max(0, x), y=max(0, y), width=cw, height=ch)
            out.append(kf.model_copy(update={"crop": crop}))
            prev = crop
            continue
        x = int(round(prev.x * s + kf.crop.x * (1 - s)))
        y = int(round(prev.y * s + kf.crop.y * (1 - s)))
        x = int(round(x * (1 - s * 0.2) + center_crop.x * (s * 0.2)))
        y = int(round(y * (1 - s * 0.2) + center_crop.y * (s * 0.2)))
        crop = CropRect(x=max(0, x), y=max(0, y), width=cw, height=ch)
        out.append(kf.model_copy(update={"crop": crop}))
        prev = crop
    return out


def build_reframe_plan(
    source_width: int,
    source_height: int,
    *,
    duration_s: float = 0.0,
    track_mode: TrackMode | str = TrackMode.FACE_CENTER,
    target_width: int = 1080,
    target_height: int = 1920,
    smoothing: float = 0.65,
    keyframe_count: int = 5,
    focus_x_norm: Optional[float] = None,
    focus_y_norm: Optional[float] = None,
) -> AutoReframePlan:
    """Build an AutoReframePlan for source → 9:16 (or custom target)."""
    if source_width <= 0 or source_height <= 0:
        raise ValueError("source dimensions must be positive")
    if isinstance(track_mode, str):
        track_mode = TrackMode(track_mode)

    target_aspect = target_width / target_height
    crop_w, crop_h = _target_crop_size(source_width, source_height, target_aspect)

    # Already 9:16-ish: identity crop
    notes: list[str] = []
    src_aspect = source_width / source_height
    if abs(src_aspect - target_aspect) < 0.02 and source_width >= target_width * 0.9:
        notes.append("Source already near target aspect; using full-frame crop.")
        crop = CropRect(x=0, y=0, width=source_width - source_width % 2, height=source_height - source_height % 2)
        return AutoReframePlan(
            source_width=source_width,
            source_height=source_height,
            target_width=target_width,
            target_height=target_height,
            track_mode=track_mode,
            keyframes=[CropKeyframe(t_s=0.0, crop=crop, confidence=1.0)],
            primary_crop=crop,
            confidence=1.0,
            smoothing=smoothing,
            notes=notes,
            tracking={"mode": track_mode.value, "path": "identity"},
        )

    # Center reference
    center_crop = _focus_to_crop(source_width, source_height, crop_w, crop_h, 0.5, 0.5)

    n = max(1, keyframe_count)
    duration_s = max(0.0, duration_s)
    keyframes: list[CropKeyframe] = []
    for i in range(n):
        t_norm = i / max(1, n - 1) if n > 1 else 0.5
        t_s = t_norm * duration_s if duration_s > 0 else float(i)
        if track_mode == TrackMode.CUSTOM and focus_x_norm is not None:
            fx = focus_x_norm
            fy = focus_y_norm if focus_y_norm is not None else 0.5
            conf = 0.85
        else:
            fx, fy, conf = _mode_focus(track_mode, t_norm)
            if focus_x_norm is not None:
                fx = focus_x_norm
            if focus_y_norm is not None:
                fy = focus_y_norm
        crop = _focus_to_crop(source_width, source_height, crop_w, crop_h, fx, fy)
        keyframes.append(CropKeyframe(t_s=round(t_s, 3), crop=crop, confidence=conf))

    # Speaker mode uses higher smoothing by default
    sm = min(1.0, smoothing + 0.15) if track_mode == TrackMode.SPEAKER else smoothing
    keyframes = _smooth_path(keyframes, sm, center_crop)
    # Re-clamp after smooth
    fixed: list[CropKeyframe] = []
    for kf in keyframes:
        c = _clamp_crop(kf.crop.x, kf.crop.y, crop_w, crop_h, source_width, source_height)
        fixed.append(kf.model_copy(update={"crop": c}))
    keyframes = fixed

    primary = keyframes[len(keyframes) // 2].crop if keyframes else center_crop
    conf = sum(k.confidence for k in keyframes) / len(keyframes) if keyframes else 0.5

    notes.append(
        f"Track mode={track_mode.value}, crop={crop_w}x{crop_h}, "
        f"keyframes={len(keyframes)}, smoothing={sm:.2f}."
    )
    if track_mode in (TrackMode.FACE_CENTER, TrackMode.SPEAKER):
        notes.append(
            "Face/speaker modes use upper-third heuristics (no ML runtime required for planning)."
        )

    # Ensure no sudden jumps: max step limited
    for i in range(1, len(keyframes)):
        dx = abs(keyframes[i].crop.x - keyframes[i - 1].crop.x)
        dy = abs(keyframes[i].crop.y - keyframes[i - 1].crop.y)
        max_step = max(crop_w, crop_h) * 0.15
        if dx > max_step or dy > max_step:
            # Pull back toward previous
            px, py = keyframes[i - 1].crop.x, keyframes[i - 1].crop.y
            nx = int(px + max(-max_step, min(max_step, keyframes[i].crop.x - px)))
            ny = int(py + max(-max_step, min(max_step, keyframes[i].crop.y - py)))
            keyframes[i] = keyframes[i].model_copy(
                update={"crop": _clamp_crop(nx, ny, crop_w, crop_h, source_width, source_height)}
            )
            notes.append(f"Limited jump at keyframe {i} for stability.")

    return AutoReframePlan(
        source_width=source_width,
        source_height=source_height,
        target_width=target_width,
        target_height=target_height,
        track_mode=track_mode,
        keyframes=keyframes,
        primary_crop=primary,
        confidence=round(conf, 4),
        smoothing=sm,
        notes=notes,
        tracking={
            "mode": track_mode.value,
            "movement_path": [
                {"t_s": k.t_s, "x": k.crop.x, "y": k.crop.y, "confidence": k.confidence}
                for k in keyframes
            ],
        },
    )


def reframe_filter_complex(plan: AutoReframePlan) -> str:
    """Build FFmpeg filter for primary crop + scale to target (static crop baseline).

    Dynamic pan across keyframes can be added later via sendcmd/zoompan; Phase 10
    uses the primary (mid) crop for stable export quality.
    """
    c = plan.primary_crop
    return (
        f"crop={c.width}:{c.height}:{c.x}:{c.y},"
        f"scale={plan.target_width}:{plan.target_height}:flags=lanczos,"
        f"setsar=1"
    )

```


---

## Source: `backend/production_pipeline/finisher.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Finish plan builder + optional FFmpeg execution (Phase 10)."""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Any, Optional

from backend.caption_removal.detection import probe_video
from backend.production_pipeline.audio import audio_plan_notes, build_audio_filter, validate_audio_config
from backend.production_pipeline.export_presets import preset_for_platform
from backend.production_pipeline.models import (
    FinishConfig,
    FinishPlan,
    PlatformKind,
    TrackMode,
)
from backend.production_pipeline.reframe import build_reframe_plan, reframe_filter_complex
from backend.production_pipeline.thumbnail import plan_thumbnail, render_thumbnail
from backend.production_pipeline.video_fx import build_video_filters, video_plan_notes

logger = logging.getLogger(__name__)


def build_finish_plan(
    *,
    source_width: int,
    source_height: int,
    duration_s: float = 0.0,
    config: Optional[FinishConfig] = None,
    input_path: Optional[str] = None,
    analysis: Optional[dict[str, Any]] = None,
) -> FinishPlan:
    """Compose a full finishing plan without rendering."""
    config = config or FinishConfig()
    export = config.custom_export or preset_for_platform(config.platform)

    steps: list[str] = []
    notes: list[str] = []
    reframe_plan = None
    vf: list[str] = []

    if config.reframe_enabled:
        reframe_plan = build_reframe_plan(
            source_width,
            source_height,
            duration_s=duration_s,
            track_mode=config.track_mode,
            target_width=export.width,
            target_height=export.height,
        )
        vf.append(reframe_filter_complex(reframe_plan))
        steps.append("reframe")
        notes.extend(reframe_plan.notes)
    else:
        steps.append("skip_reframe")
        notes.append("Reframe disabled.")

    # Optional visual FX after reframe/scale
    fx = build_video_filters(config.video)
    vf.extend(fx)
    if config.video.enabled:
        steps.append("video_enhance")
    notes.extend(video_plan_notes(config.video))

    af = build_audio_filter(config.audio)
    if af:
        steps.append("audio_enhance")
    notes.extend(audio_plan_notes(config.audio))
    errs = validate_audio_config(config.audio)
    if errs:
        notes.append("Audio config warnings: " + "; ".join(errs))

    if config.caption_enabled:
        steps.append(f"caption:{config.caption_style}")
        notes.append(
            f"Captions flagged style={config.caption_style} "
            "(apply via existing caption tools / burn step)."
        )

    steps.append(f"export:{export.id}")
    thumb = plan_thumbnail(
        duration_s,
        text_overlay=config.thumbnail_text,
        analysis=analysis,
    )
    steps.append("thumbnail")
    notes.append(f"Cover @ {thumb.time_s}s ({thumb.source}): {thumb.reason}")

    return FinishPlan(
        input_path=input_path,
        reframe=reframe_plan,
        audio=config.audio,
        video=config.video,
        export=export,
        thumbnail=thumb,
        audio_filter=af,
        video_filters=vf,
        steps=steps,
        notes=notes,
    )


def run_finish_plan(
    video_path: Path,
    output_path: Path,
    plan: FinishPlan,
    *,
    thumbnail_path: Optional[Path] = None,
) -> dict[str, Any]:
    """Execute reframe + audio/video filters + encode using the plan.

    Does not burn captions (separate system). Writes a new file only.
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    if not video_path.exists():
        raise FileNotFoundError(str(video_path))
    if output_path.resolve() == video_path.resolve():
        raise ValueError("Refusing to overwrite source video")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    exp = plan.export
    vf = ",".join(plan.video_filters) if plan.video_filters else None

    cmd = ["ffmpeg", "-y", "-i", str(video_path)]
    if vf:
        cmd.extend(["-vf", vf])
    if plan.audio_filter:
        cmd.extend(["-af", plan.audio_filter])
        cmd.extend(["-c:a", "aac", "-b:a", exp.audio_bitrate])
    else:
        cmd.extend(["-c:a", "aac", "-b:a", exp.audio_bitrate])
    cmd.extend(
        [
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", str(exp.crf),
            "-r", str(exp.fps),
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_path),
        ]
    )
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    if result.returncode != 0 or not output_path.exists():
        raise RuntimeError(f"Finish encode failed: {(result.stderr or '')[:500]}")

    thumb_out = None
    if thumbnail_path is not None:
        try:
            thumb_out = str(
                render_thumbnail(
                    output_path if output_path.exists() else video_path,
                    Path(thumbnail_path),
                    plan.thumbnail,
                    width=exp.width,
                    height=exp.height,
                )
            )
        except Exception as e:
            logger.warning("Thumbnail generation failed: %s", e)

    return {
        "output_path": str(output_path),
        "thumbnail_path": thumb_out,
        "export_preset": exp.id,
        "steps": plan.steps,
    }


def build_finish_plan_for_video(
    video_path: Path,
    config: Optional[FinishConfig] = None,
    analysis: Optional[dict[str, Any]] = None,
) -> FinishPlan:
    """Probe video then build plan."""
    meta = probe_video(Path(video_path))
    return build_finish_plan(
        source_width=meta["width"],
        source_height=meta["height"],
        duration_s=meta["duration_s"],
        config=config,
        input_path=str(video_path),
        analysis=analysis,
    )

```


---

## Source: `backend/production_pipeline/export_presets.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Multi-platform export presets for short-form video (Phase 10)."""
from __future__ import annotations

from backend.production_pipeline.models import ExportPreset, PlatformKind

_PRESETS: dict[str, ExportPreset] = {
    "tiktok": ExportPreset(
        id="tiktok",
        name="TikTok",
        platform=PlatformKind.TIKTOK,
        width=1080,
        height=1920,
        fps=30,
        video_bitrate="8M",
        audio_bitrate="192k",
        crf=18,
        aspect_ratio="9:16",
        max_duration_s=180,
        notes=["9:16 vertical", "1080×1920 recommended", "H.264 + AAC"],
    ),
    "youtube_shorts": ExportPreset(
        id="youtube_shorts",
        name="YouTube Shorts",
        platform=PlatformKind.YOUTUBE_SHORTS,
        width=1080,
        height=1920,
        fps=30,
        video_bitrate="10M",
        audio_bitrate="192k",
        crf=17,
        aspect_ratio="9:16",
        max_duration_s=60,
        notes=["9:16 vertical", "Up to 60s classic Shorts limit", "Higher bitrate default"],
    ),
    "instagram_reels": ExportPreset(
        id="instagram_reels",
        name="Instagram Reels",
        platform=PlatformKind.INSTAGRAM_REELS,
        width=1080,
        height=1920,
        fps=30,
        video_bitrate="8M",
        audio_bitrate="192k",
        crf=18,
        aspect_ratio="9:16",
        max_duration_s=90,
        notes=["9:16 vertical", "1080×1920", "Reels-friendly encode"],
    ),
}


def list_export_presets() -> list[ExportPreset]:
    return [p.model_copy(deep=True) for p in _PRESETS.values()]


def get_export_preset(preset_id: str) -> ExportPreset:
    key = (preset_id or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "shorts": "youtube_shorts",
        "yt_shorts": "youtube_shorts",
        "reels": "instagram_reels",
        "ig": "instagram_reels",
        "instagram": "instagram_reels",
    }
    key = aliases.get(key, key)
    if key not in _PRESETS:
        known = ", ".join(sorted(_PRESETS))
        raise ValueError(f"Unknown export preset {preset_id!r}. Known: {known}")
    return _PRESETS[key].model_copy(deep=True)


def preset_for_platform(platform: PlatformKind | str) -> ExportPreset:
    if isinstance(platform, PlatformKind):
        pid = platform.value
    else:
        pid = str(platform)
    if pid == "youtube_shorts" or pid == PlatformKind.YOUTUBE_SHORTS.value:
        return get_export_preset("youtube_shorts")
    if pid in ("instagram_reels", PlatformKind.INSTAGRAM_REELS.value):
        return get_export_preset("instagram_reels")
    return get_export_preset("tiktok")

```


---

## Source: `backend/production_pipeline/batch.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""In-memory batch finishing workflow (Phase 10).

Uses existing asyncio job patterns — no new infrastructure services.
"""
from __future__ import annotations

import logging
import threading
from typing import Optional

from backend.production_pipeline.models import (
    BatchItem,
    BatchItemStatus,
    BatchJobSpec,
    FinishConfig,
)

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_BATCHES: dict[str, BatchJobSpec] = {}


def create_batch(
    source_paths: list[str],
    config: Optional[FinishConfig] = None,
    *,
    max_attempts: int = 2,
) -> BatchJobSpec:
    """Register a batch of sources for the finishing pipeline."""
    if not source_paths:
        raise ValueError("source_paths cannot be empty")
    config = config or FinishConfig()
    items = [
        BatchItem(source_path=p, max_attempts=max_attempts)
        for p in source_paths
    ]
    batch = BatchJobSpec(
        items=items,
        config=config,
        status=BatchItemStatus.PENDING,
        created_notes=[
            f"{len(items)} item(s) queued for platform={config.platform.value}.",
            "Pipeline: analyze → score → enhance → caption → reframe → export (as enabled).",
        ],
    )
    with _lock:
        _BATCHES[batch.id] = batch
    return batch.model_copy(deep=True)


def get_batch(batch_id: str) -> BatchJobSpec:
    with _lock:
        b = _BATCHES.get(batch_id)
        if b is None:
            raise KeyError(f"Unknown batch {batch_id!r}")
        return b.model_copy(deep=True)


def list_batches() -> list[dict]:
    with _lock:
        return [b.summary() for b in _BATCHES.values()]


def update_item(
    batch_id: str,
    item_id: str,
    *,
    status: Optional[BatchItemStatus] = None,
    progress_pct: Optional[float] = None,
    current_step: Optional[str] = None,
    error: Optional[str] = None,
    output_path: Optional[str] = None,
    plan_id: Optional[str] = None,
    inc_attempt: bool = False,
) -> BatchJobSpec:
    with _lock:
        b = _BATCHES.get(batch_id)
        if b is None:
            raise KeyError(f"Unknown batch {batch_id!r}")
        found = False
        new_items = []
        for it in b.items:
            if it.id != item_id:
                new_items.append(it)
                continue
            found = True
            data = it.model_dump()
            if status is not None:
                data["status"] = status
            if progress_pct is not None:
                data["progress_pct"] = progress_pct
            if current_step is not None:
                data["current_step"] = current_step
            if error is not None:
                data["error"] = error
            if output_path is not None:
                data["output_path"] = output_path
            if plan_id is not None:
                data["plan_id"] = plan_id
            if inc_attempt:
                data["attempts"] = it.attempts + 1
            new_items.append(BatchItem.model_validate(data))
        if not found:
            raise KeyError(f"Unknown item {item_id!r} in batch {batch_id}")
        # Roll up batch status
        statuses = {it.status for it in new_items}
        if all(s == BatchItemStatus.SUCCESS for s in statuses):
            b_status = BatchItemStatus.SUCCESS
        elif any(s == BatchItemStatus.RUNNING for s in statuses):
            b_status = BatchItemStatus.RUNNING
        elif any(s == BatchItemStatus.FAILED for s in statuses) and not any(
            s in (BatchItemStatus.PENDING, BatchItemStatus.RUNNING, BatchItemStatus.RETRYING)
            for s in statuses
        ):
            b_status = BatchItemStatus.FAILED
        elif any(s == BatchItemStatus.RETRYING for s in statuses):
            b_status = BatchItemStatus.RETRYING
        else:
            b_status = BatchItemStatus.PENDING
        updated = b.model_copy(update={"items": new_items, "status": b_status})
        _BATCHES[batch_id] = updated
        return updated.model_copy(deep=True)


def mark_retry(batch_id: str, item_id: str) -> BatchJobSpec:
    """Mark a failed item for retry if attempts remain."""
    with _lock:
        b = _BATCHES.get(batch_id)
        if b is None:
            raise KeyError(batch_id)
        for it in b.items:
            if it.id == item_id:
                if it.attempts >= it.max_attempts:
                    raise ValueError("Max retry attempts reached")
                break
        else:
            raise KeyError(item_id)
    return update_item(
        batch_id,
        item_id,
        status=BatchItemStatus.RETRYING,
        error=None,
        progress_pct=0.0,
        current_step="queued_for_retry",
        inc_attempt=True,
    )


def clear_batches() -> None:
    """Test helper."""
    with _lock:
        _BATCHES.clear()

```


---

## Source: `backend/api/production.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""API for professional short-form finishing pipeline (Phase 10)."""
from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.agents.job_helper import create_job
from backend.caption_removal.detection import probe_video
from backend.config import settings
from backend.core.task_runner import dispatch
from backend.production_pipeline.audio import build_audio_filter, validate_audio_config
from backend.production_pipeline.batch import create_batch, get_batch, list_batches, mark_retry
from backend.production_pipeline.export_presets import get_export_preset, list_export_presets
from backend.production_pipeline.finisher import build_finish_plan, build_finish_plan_for_video, run_finish_plan
from backend.production_pipeline.models import (
    AudioEnhanceConfig,
    FinishConfig,
    PlatformKind,
    TrackMode,
    VideoEnhanceConfig,
)
from backend.production_pipeline.reframe import build_reframe_plan, list_track_modes
from backend.production_pipeline.thumbnail import plan_thumbnail, render_thumbnail

logger = logging.getLogger(__name__)
router = APIRouter()


class ReframeRequest(BaseModel):
    source_width: int = Field(gt=0)
    source_height: int = Field(gt=0)
    duration_s: float = Field(default=0.0, ge=0.0)
    track_mode: str = "face_center"
    target_width: int = 1080
    target_height: int = 1920
    smoothing: float = Field(default=0.65, ge=0.0, le=1.0)
    keyframe_count: int = Field(default=5, ge=1, le=30)
    focus_x_norm: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    focus_y_norm: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class AudioConfigIn(BaseModel):
    enabled: bool = True
    preserve_original: bool = False
    loudness_normalize: bool = True
    target_i: float = -14.0
    denoise: bool = True
    denoise_nr: float = 10.0
    highpass_hz: int = 80
    lowpass_hz: int = 12000
    silence_cleanup: bool = False
    voice_clarity: bool = True


class VideoConfigIn(BaseModel):
    enabled: bool = False
    sharpen: bool = False
    sharpen_amount: float = 0.5
    denoise: bool = False
    denoise_luma: float = 2.0
    brightness: float = 0.0
    contrast: float = 1.0
    saturation: float = 1.0
    upscale: bool = False
    upscale_factor: float = 1.0


class FinishPlanRequest(BaseModel):
    source_width: int = Field(default=1920, gt=0)
    source_height: int = Field(default=1080, gt=0)
    duration_s: float = Field(default=30.0, ge=0.0)
    platform: str = "tiktok"
    track_mode: str = "face_center"
    reframe_enabled: bool = True
    audio: Optional[AudioConfigIn] = None
    video: Optional[VideoConfigIn] = None
    caption_style: str = "viral"
    caption_enabled: bool = False
    thumbnail_text: Optional[str] = None


class BatchCreateRequest(BaseModel):
    source_paths: list[str] = Field(min_length=1)
    platform: str = "tiktok"
    track_mode: str = "face_center"
    reframe_enabled: bool = True
    max_attempts: int = Field(default=2, ge=1, le=5)


class ThumbnailPlanRequest(BaseModel):
    duration_s: float = Field(ge=0.0)
    text_overlay: Optional[str] = None
    hook_time_s: Optional[float] = None


def _finish_config_from_body(body: FinishPlanRequest) -> FinishConfig:
    try:
        platform = PlatformKind(body.platform)
    except ValueError:
        platform = PlatformKind.TIKTOK
    try:
        track = TrackMode(body.track_mode)
    except ValueError:
        track = TrackMode.FACE_CENTER
    audio = AudioEnhanceConfig(**(body.audio.model_dump() if body.audio else {}))
    video = VideoEnhanceConfig(**(body.video.model_dump() if body.video else {}))
    return FinishConfig(
        platform=platform,
        track_mode=track,
        reframe_enabled=body.reframe_enabled,
        audio=audio,
        video=video,
        caption_style=body.caption_style,
        caption_enabled=body.caption_enabled,
        thumbnail_text=body.thumbnail_text,
    )


@router.get("/production/export-presets")
async def api_list_export_presets():
    presets = list_export_presets()
    return {"presets": [p.model_dump() for p in presets]}


@router.get("/production/export-presets/{preset_id}")
async def api_get_export_preset(preset_id: str):
    try:
        p = get_export_preset(preset_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e
    return p.model_dump()


@router.get("/production/track-modes")
async def api_track_modes():
    return {"modes": list_track_modes()}


@router.post("/production/reframe-plan")
async def api_reframe_plan(body: ReframeRequest):
    try:
        plan = build_reframe_plan(
            body.source_width,
            body.source_height,
            duration_s=body.duration_s,
            track_mode=body.track_mode,
            target_width=body.target_width,
            target_height=body.target_height,
            smoothing=body.smoothing,
            keyframe_count=body.keyframe_count,
            focus_x_norm=body.focus_x_norm,
            focus_y_norm=body.focus_y_norm,
        )
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    return {
        "plan": plan.model_dump(mode="json"),
        "movement_path": plan.movement_path(),
        "primary_crop": plan.primary_crop.model_dump(),
        "confidence": plan.confidence,
    }


@router.post("/production/audio-filter")
async def api_audio_filter(body: AudioConfigIn):
    cfg = AudioEnhanceConfig(**body.model_dump())
    errs = validate_audio_config(cfg)
    if errs:
        raise HTTPException(422, {"errors": errs})
    return {"filter": build_audio_filter(cfg), "config": cfg.model_dump()}


@router.post("/production/finish-plan")
async def api_finish_plan(body: FinishPlanRequest):
    cfg = _finish_config_from_body(body)
    plan = build_finish_plan(
        source_width=body.source_width,
        source_height=body.source_height,
        duration_s=body.duration_s,
        config=cfg,
    )
    return {
        "plan": plan.model_dump(mode="json"),
        "steps": plan.steps,
        "export": plan.export.model_dump(),
        "notes": plan.notes,
    }


@router.post("/production/thumbnail-plan")
async def api_thumbnail_plan(body: ThumbnailPlanRequest):
    plan = plan_thumbnail(
        body.duration_s,
        text_overlay=body.text_overlay,
        hook_time_s=body.hook_time_s,
    )
    return plan.model_dump()


@router.post("/production/batch")
async def api_create_batch(body: BatchCreateRequest):
    try:
        platform = PlatformKind(body.platform)
    except ValueError:
        raise HTTPException(422, f"Unknown platform {body.platform!r}")
    try:
        track = TrackMode(body.track_mode)
    except ValueError:
        raise HTTPException(422, f"Unknown track_mode {body.track_mode!r}")
    cfg = FinishConfig(
        platform=platform,
        track_mode=track,
        reframe_enabled=body.reframe_enabled,
    )
    try:
        batch = create_batch(body.source_paths, cfg, max_attempts=body.max_attempts)
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    return {"batch": batch.model_dump(mode="json"), "summary": batch.summary()}


@router.get("/production/batch")
async def api_list_batches():
    return {"batches": list_batches()}


@router.get("/production/batch/{batch_id}")
async def api_get_batch(batch_id: str):
    try:
        b = get_batch(batch_id)
    except KeyError:
        raise HTTPException(404, "Batch not found")
    return {"batch": b.model_dump(mode="json"), "summary": b.summary()}


@router.post("/production/batch/{batch_id}/items/{item_id}/retry")
async def api_retry_item(batch_id: str, item_id: str):
    try:
        b = mark_retry(batch_id, item_id)
    except KeyError:
        raise HTTPException(404, "Batch or item not found")
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    return {"batch": b.model_dump(mode="json"), "summary": b.summary()}


@router.post("/production/finish")
async def api_finish_upload(
    file: UploadFile = File(...),
    platform: str = Form("tiktok"),
    track_mode: str = Form("face_center"),
    reframe_enabled: bool = Form(True),
    audio_enhance: bool = Form(True),
    video_enhance: bool = Form(False),
    thumbnail_text: Optional[str] = Form(None),
):
    """Upload → finish plan → encode ready-to-post vertical video + cover."""
    try:
        plat = PlatformKind(platform)
    except ValueError:
        raise HTTPException(422, f"Unknown platform {platform!r}")
    try:
        track = TrackMode(track_mode)
    except ValueError:
        raise HTTPException(422, f"Unknown track_mode {track_mode!r}")

    settings.TMP_DIR.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="vm_finish_", dir=str(settings.TMP_DIR)))
    try:
        suffix = Path(file.filename or "input.mp4").suffix or ".mp4"
        in_path = work / f"input{suffix}"
        data = await file.read()
        if not data:
            raise HTTPException(422, "Empty upload")
        in_path.write_bytes(data)

        cfg = FinishConfig(
            platform=plat,
            track_mode=track,
            reframe_enabled=reframe_enabled,
            audio=AudioEnhanceConfig(enabled=audio_enhance),
            video=VideoEnhanceConfig(enabled=video_enhance),
            thumbnail_text=thumbnail_text,
        )
        plan = build_finish_plan_for_video(in_path, cfg)
        out_path = work / f"finished{suffix}"
        thumb_path = work / "cover.jpg"
        result = run_finish_plan(in_path, out_path, plan, thumbnail_path=thumb_path)

        # Persist under storage/generated
        gen = settings.GENERATED_DIR
        gen.mkdir(parents=True, exist_ok=True)
        final = gen / f"finish_{plan.id}{suffix}"
        shutil.move(result["output_path"], final)
        final_thumb = None
        if result.get("thumbnail_path") and Path(result["thumbnail_path"]).exists():
            final_thumb = gen / f"finish_{plan.id}_cover.jpg"
            shutil.move(result["thumbnail_path"], final_thumb)

        return {
            "success": True,
            "output_path": str(final),
            "thumbnail_path": str(final_thumb) if final_thumb else None,
            "plan": plan.model_dump(mode="json"),
            "steps": plan.steps,
            "export": plan.export.model_dump(),
        }
    except Exception as e:
        logger.exception("finish upload failed")
        raise HTTPException(500, str(e)[:400]) from e
    finally:
        shutil.rmtree(work, ignore_errors=True)

```


---

## Source: `backend/api/caption_removal.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""API foundation for burned-in caption detection and removal (Phase 9)."""
from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.caption_removal.detection import detect_caption_regions, detect_from_video, probe_video
from backend.caption_removal.masking import build_mask_plan, write_mask_preview_png
from backend.caption_removal.models import DetectionConfig, RemovalBackend, RemovalConfig
from backend.caption_removal.pipeline import analyze_caption_burnin, remove_burned_captions
from backend.caption_removal.removal import list_removal_backends
from backend.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class RegionNorm(BaseModel):
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    width: float = Field(gt=0.0, le=1.0)
    height: float = Field(gt=0.0, le=1.0)


class AnalyzeByPathRequest(BaseModel):
    """Analyze a server-side path under storage/ (never arbitrary system paths)."""

    path: str
    sample_frames: int = Field(default=6, ge=1, le=24)
    min_confidence: float = Field(default=0.35, ge=0.0, le=1.0)
    include_center: bool = True
    include_top: bool = False
    write_mask_preview: bool = False


class MaskFromRegionsRequest(BaseModel):
    frame_width: int = Field(gt=0)
    frame_height: int = Field(gt=0)
    regions: list[dict[str, Any]]
    pad_px: int = Field(default=8, ge=0, le=128)
    feather_px: int = Field(default=4, ge=0, le=64)
    primary_only: bool = True


class DetectSyntheticRequest(BaseModel):
    """Detection without a video file — pure geometry/priors (for tests & UI)."""

    frame_width: int = Field(default=1080, gt=0)
    frame_height: int = Field(default=1920, gt=0)
    min_confidence: float = Field(default=0.35, ge=0.0, le=1.0)
    include_center: bool = True
    include_top: bool = False
    force_region: Optional[RegionNorm] = None


def _safe_storage_path(path_str: str) -> Path:
    """Resolve path only if it stays under STORAGE_ROOT."""
    root = settings.STORAGE_ROOT.resolve()
    raw = Path(path_str)
    candidate = (raw if raw.is_absolute() else (root / raw)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as e:
        raise HTTPException(400, "Path must be under application storage/") from e
    if not candidate.exists():
        raise HTTPException(404, f"File not found: {candidate.name}")
    return candidate


@router.get("/caption-removal/backends")
async def get_backends():
    """List available removal backends and their limitations."""
    return {
        "backends": list_removal_backends(),
        "default": "delogo",
        "limitations": [
            "Baseline delogo uses spatial interpolation, not generative AI inpainting.",
            "Works best on static caption bands; moving/styled captions may leave artifacts.",
            "Source videos are never overwritten.",
        ],
    }


@router.post("/caption-removal/detect")
async def detect_synthetic(body: DetectSyntheticRequest):
    """Return caption region candidates for a frame size (no file I/O required)."""
    cfg = DetectionConfig(
        min_confidence=body.min_confidence,
        include_center=body.include_center,
        include_top=body.include_top,
        force_region=body.force_region.model_dump() if body.force_region else None,
        sample_frames=1,
    )
    result = detect_caption_regions(
        frame_width=body.frame_width,
        frame_height=body.frame_height,
        config=cfg,
    )
    return {
        "method": result.method,
        "frame_width": result.frame_width,
        "frame_height": result.frame_height,
        "regions": [r.as_dict() for r in result.regions],
        "notes": result.notes,
    }


@router.post("/caption-removal/analyze-path")
async def analyze_path(body: AnalyzeByPathRequest):
    """Detect caption regions for a video under storage/."""
    path = _safe_storage_path(body.path)
    cfg = DetectionConfig(
        sample_frames=body.sample_frames,
        min_confidence=body.min_confidence,
        include_center=body.include_center,
        include_top=body.include_top,
    )
    sample_dir = settings.TMP_DIR / "caption_removal" / path.stem
    sample_dir.mkdir(parents=True, exist_ok=True)
    detection, mask = analyze_caption_burnin(
        path,
        detection_config=cfg,
        sample_dir=sample_dir,
        write_mask_preview=body.write_mask_preview,
        mask_preview_path=sample_dir / "mask_preview.png" if body.write_mask_preview else None,
    )
    return {
        "detection": {
            "method": detection.method,
            "frame_width": detection.frame_width,
            "frame_height": detection.frame_height,
            "fps": detection.fps,
            "duration_s": detection.duration_s,
            "regions": [r.as_dict() for r in detection.regions],
            "notes": detection.notes,
        },
        "mask": {
            "id": mask.id,
            "frame_width": mask.frame_width,
            "frame_height": mask.frame_height,
            "pad_px": mask.pad_px,
            "feather_px": mask.feather_px,
            "regions": [r.as_dict() for r in mask.regions],
            "delogo_boxes": mask.delogo_boxes(),
            "mask_preview_path": mask.mask_preview_path,
            "notes": mask.notes,
        },
    }


@router.post("/caption-removal/mask")
async def generate_mask(body: MaskFromRegionsRequest):
    """Build a mask plan from explicit regions (pixel or nested region dicts)."""
    from backend.caption_removal.models import CaptionRegion, CaptionRegionType, DetectionResult

    regions: list[CaptionRegion] = []
    for raw in body.regions:
        if "region" in raw:
            box = raw["region"]
            conf = float(raw.get("confidence", 1.0))
            rtype = raw.get("type", "custom")
        else:
            box = raw
            conf = float(raw.get("confidence", 1.0))
            rtype = raw.get("type", "custom")
        x, y = int(box["x"]), int(box["y"])
        w, h = int(box.get("width", box.get("w", 0))), int(box.get("height", box.get("h", 0)))
        if w <= 0 or h <= 0:
            raise HTTPException(422, "Each region needs positive width/height")
        regions.append(
            CaptionRegion(
                x=x,
                y=y,
                width=w,
                height=h,
                confidence=max(0.0, min(1.0, conf)),
                type=CaptionRegionType(rtype) if rtype in CaptionRegionType._value2member_map_ else CaptionRegionType.CUSTOM,
                x_norm=x / body.frame_width,
                y_norm=y / body.frame_height,
                w_norm=w / body.frame_width,
                h_norm=h / body.frame_height,
            )
        )
    detection = DetectionResult(
        frame_width=body.frame_width,
        frame_height=body.frame_height,
        regions=regions,
        notes=["Mask built from caller-supplied regions."],
    )
    mask = build_mask_plan(
        detection,
        pad_px=body.pad_px,
        feather_px=body.feather_px,
        primary_only=body.primary_only,
    )
    return {
        "mask": {
            "id": mask.id,
            "regions": [r.as_dict() for r in mask.regions],
            "delogo_boxes": mask.delogo_boxes(),
            "pad_px": mask.pad_px,
            "feather_px": mask.feather_px,
            "notes": mask.notes,
        }
    }


@router.post("/caption-removal/process")
async def process_removal(
    file: UploadFile = File(...),
    backend: str = Form("delogo"),
    dry_run: bool = Form(False),
    min_confidence: float = Form(0.35),
    pad_px: int = Form(10),
):
    """Upload a video, detect caption band, optionally produce cleaned copy.

    Always writes outputs under storage/tmp — never overwrites the upload name
    in place as the source of truth (upload is saved then processed to a new file).
    """
    if backend not in {b["id"] for b in list_removal_backends()}:
        raise HTTPException(422, f"Unknown backend {backend!r}")

    settings.TMP_DIR.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="vm_caprm_", dir=str(settings.TMP_DIR)))
    try:
        suffix = Path(file.filename or "input.mp4").suffix or ".mp4"
        in_path = work / f"input{suffix}"
        data = await file.read()
        if not data:
            raise HTTPException(422, "Empty upload")
        in_path.write_bytes(data)

        out_path = work / f"cleaned{suffix}"
        result = remove_burned_captions(
            in_path,
            out_path,
            detection_config=DetectionConfig(min_confidence=min_confidence, sample_frames=6),
            removal_config=RemovalConfig(
                backend=RemovalBackend(backend),
                dry_run=dry_run,
                pad_px=pad_px,
                min_confidence=min_confidence,
            ),
        )
        payload: dict[str, Any] = {
            "success": result.success,
            "backend": result.backend,
            "error": result.error,
            "notes": result.notes,
            "preserved": result.preserved,
            "dry_run": dry_run,
        }
        if result.detection:
            payload["regions"] = [r.as_dict() for r in result.detection.regions]
            payload["detection_notes"] = result.detection.notes
        if result.mask:
            payload["delogo_boxes"] = result.mask.delogo_boxes()
        if result.success and result.output_path and not dry_run:
            # Move cleaned file to stable tools output location
            from backend.api.tools import tools_out_dir

            tools_out_dir().mkdir(parents=True, exist_ok=True)
            final = tools_out_dir() / f"caption_removed_{in_path.stem}{suffix}"
            shutil.move(result.output_path, final)
            payload["output_path"] = str(final)
            payload["download_hint"] = final.name
        return payload
    finally:
        # Keep outputs moved out; clean workdir best-effort
        shutil.rmtree(work, ignore_errors=True)

```


---

## Source: `backend/api/clip_intelligence.py`

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""REST API for deterministic viral clip scoring (Phase 6)."""
from __future__ import annotations

import json
import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from backend.clip_intelligence.models import ScoringWeights
from backend.clip_intelligence.pipeline import analyze_transcript
from backend.clip_intelligence.hooks import detect_hooks
from backend.clip_intelligence.scoring import score_transcript_window
from backend.database import AsyncSessionLocal
from backend.models.downloaded_video import DownloadedVideo

logger = logging.getLogger(__name__)
router = APIRouter()


class TranscriptSegmentIn(BaseModel):
    start: Optional[float] = None
    end: Optional[float] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    text: str = ""


class WeightsIn(BaseModel):
    hook_strength: Optional[float] = None
    emotional_intensity: Optional[float] = None
    speech_energy: Optional[float] = None
    keyword_importance: Optional[float] = None
    story_completeness: Optional[float] = None
    audience_curiosity: Optional[float] = None
    pacing: Optional[float] = None
    silence_penalty_weight: Optional[float] = None
    repetition_penalty_weight: Optional[float] = None


class AnalyzeTranscriptRequest(BaseModel):
    segments: list[TranscriptSegmentIn]
    max_clips: int = Field(default=5, ge=1, le=30)
    min_duration_s: float = Field(default=15.0, ge=5.0, le=120.0)
    max_duration_s: float = Field(default=60.0, ge=10.0, le=180.0)
    min_score: float = Field(default=0.25, ge=0.0, le=1.0)
    weights: Optional[WeightsIn] = None
    video_id: Optional[str] = None


class ScoreWindowRequest(BaseModel):
    text: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    weights: Optional[WeightsIn] = None


class DetectHooksRequest(BaseModel):
    text: str


def _weights_from_body(body: Optional[WeightsIn]) -> ScoringWeights:
    base = ScoringWeights()
    if not body:
        return base
    data = base.model_dump()
    for k, v in body.model_dump(exclude_none=True).items():
        data[k] = v
    return ScoringWeights.model_validate(data)


def _segments_to_dicts(segments: list[TranscriptSegmentIn]) -> list[dict[str, Any]]:
    out = []
    for s in segments:
        d: dict[str, Any] = {"text": s.text}
        if s.start_ms is not None and s.end_ms is not None:
            d["start_ms"] = s.start_ms
            d["end_ms"] = s.end_ms
        else:
            d["start"] = float(s.start or 0.0)
            d["end"] = float(s.end if s.end is not None else d["start"])
        out.append(d)
    return out


def _candidate_payload(c) -> dict[str, Any]:
    return {
        "id": c.id,
        "start_ms": c.start_ms,
        "end_ms": c.end_ms,
        "start": round(c.start_s, 2),
        "end": round(c.end_s, 2),
        "duration_s": round(c.duration_ms / 1000.0, 2),
        "text": c.text,
        "title_suggestion": c.title_suggestion,
        "confidence": c.confidence,
        "topics": c.topics,
        "hooks": [h.model_dump() for h in c.hooks],
        "score": c.score.as_display_dict(),
        "virality_score_10": c.score.to_virality_10(),
        "final_score": c.final_score(),
    }


@router.get("/clip-intelligence/weights")
async def get_default_weights():
    """Return default scoring weights and signal descriptions."""
    w = ScoringWeights()
    return {
        "weights": w.model_dump(),
        "normalized_positive": w.normalized_positive(),
        "signals": [
            {"id": "hook_strength", "label": "Hook strength", "description": "Opening hooks, curiosity gaps, questions"},
            {"id": "emotional_intensity", "label": "Emotional intensity", "description": "Emotion keyword density"},
            {"id": "speech_energy", "label": "Speech energy", "description": "Words-per-minute and filler ratio"},
            {"id": "keyword_importance", "label": "Keyword importance", "description": "High-value topic keywords and numbers"},
            {"id": "story_completeness", "label": "Story completeness", "description": "Arc markers and sentence structure"},
            {"id": "audience_curiosity", "label": "Audience curiosity", "description": "Questions, secrets, direct address"},
            {"id": "pacing", "label": "Pacing", "description": "Idea cadence across the window"},
            {"id": "silence_penalty", "label": "Silence penalty", "description": "Sparse speech / long gaps"},
            {"id": "repetition_penalty", "label": "Repetition penalty", "description": "Repeated phrases / low diversity"},
        ],
        "method": "deterministic_v1",
    }


@router.post("/clip-intelligence/score-window")
async def score_window(body: ScoreWindowRequest):
    """Score a single text window with full breakdown (no AI)."""
    if body.end_ms < body.start_ms:
        raise HTTPException(422, "end_ms must be >= start_ms")
    if not body.text.strip():
        raise HTTPException(422, "text cannot be empty")
    weights = _weights_from_body(body.weights)
    breakdown = score_transcript_window(
        body.text, body.start_ms, body.end_ms, weights=weights
    )
    return {
        "score": breakdown.as_display_dict(),
        "virality_score_10": breakdown.to_virality_10(),
        "hooks": [h.model_dump() for h in detect_hooks(body.text, start_ms=body.start_ms, end_ms=body.end_ms)],
    }


@router.post("/clip-intelligence/detect-hooks")
async def detect_hooks_endpoint(body: DetectHooksRequest):
    """Run rule-based hook detection on text."""
    if not body.text.strip():
        raise HTTPException(422, "text cannot be empty")
    hooks = detect_hooks(body.text)
    return {"hooks": [h.model_dump() for h in hooks], "count": len(hooks)}


@router.post("/clip-intelligence/analyze")
async def analyze_segments(body: AnalyzeTranscriptRequest):
    """Analyze transcript segments and return ranked clip candidates + selection."""
    if not body.segments:
        raise HTTPException(422, "segments cannot be empty")
    if body.max_duration_s < body.min_duration_s:
        raise HTTPException(422, "max_duration_s must be >= min_duration_s")

    segments = _segments_to_dicts(body.segments)
    weights = _weights_from_body(body.weights)
    analysis = analyze_transcript(
        segments,
        video_id=body.video_id,
        max_clips=body.max_clips,
        min_duration_ms=int(body.min_duration_s * 1000),
        max_duration_ms=int(body.max_duration_s * 1000),
        min_score=body.min_score,
        weights=weights,
    )
    return {
        "id": analysis.id,
        "video_id": analysis.video_id,
        "method": analysis.method,
        "source_duration_ms": analysis.source_duration_ms,
        "weights": analysis.weights.model_dump(),
        "notes": analysis.notes,
        "candidates": [_candidate_payload(c) for c in analysis.candidates[:40]],
        "selected": [_candidate_payload(c) for c in analysis.selected],
        "candidate_count": len(analysis.candidates),
        "selected_count": len(analysis.selected),
    }


@router.post("/clip-intelligence/analyze/{video_id}")
async def analyze_downloaded_video(
    video_id: str,
    max_clips: int = 5,
    min_duration_s: float = 15.0,
    max_duration_s: float = 60.0,
    min_score: float = 0.25,
):
    """Analyze a downloaded video's stored transcript (no re-transcription)."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(DownloadedVideo).where(DownloadedVideo.id == video_id)
        )
        video = result.scalar_one_or_none()
        if not video:
            raise HTTPException(404, "Downloaded video not found")

        segments: list[dict] = []
        if video.transcript_segments_json:
            try:
                segments = json.loads(video.transcript_segments_json)
            except (json.JSONDecodeError, TypeError):
                raise HTTPException(422, "Stored transcript is corrupt")

        if not segments:
            raise HTTPException(
                422,
                "No transcript segments on this video. Run analysis/transcription first.",
            )

    analysis = analyze_transcript(
        segments,
        video_id=video_id,
        max_clips=max(1, min(max_clips, 30)),
        min_duration_ms=int(min_duration_s * 1000),
        max_duration_ms=int(max_duration_s * 1000),
        min_score=min_score,
    )
    return {
        "id": analysis.id,
        "video_id": video_id,
        "video_title": getattr(video, "title", None),
        "method": analysis.method,
        "source_duration_ms": analysis.source_duration_ms,
        "weights": analysis.weights.model_dump(),
        "notes": analysis.notes,
        "candidates": [_candidate_payload(c) for c in analysis.candidates[:40]],
        "selected": [_candidate_payload(c) for c in analysis.selected],
        "candidate_count": len(analysis.candidates),
        "selected_count": len(analysis.selected),
    }

# ── Phase 7: clip enhancement (silence / pacing / boundaries / plan) ─────────

from backend.clip_intelligence.silence import SilenceConfig, detect_silence
from backend.clip_intelligence.pacing import analyze_pacing
from backend.clip_intelligence.boundaries import BoundaryConfig, optimize_boundaries
from backend.clip_intelligence.enhancement import (
    EnhancementConfig,
    build_enhancement_plan,
)


class ClipWindowRequest(BaseModel):
    segments: list[TranscriptSegmentIn]
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    min_silence_ms: int = Field(default=400, ge=50, le=10000)
    max_keep_silence_ms: int = Field(default=350, ge=0, le=5000)


class OptimizeBoundariesRequest(BaseModel):
    segments: list[TranscriptSegmentIn]
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    source_duration_ms: Optional[int] = Field(default=None, ge=0)
    prefer_sentence_boundaries: bool = True
    min_duration_ms: int = Field(default=5000, ge=1000)
    max_duration_ms: int = Field(default=90000, ge=5000)


class EnhancePlanRequest(BaseModel):
    segments: list[TranscriptSegmentIn]
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    video_id: Optional[str] = None
    source_duration_ms: Optional[int] = Field(default=None, ge=0)
    caption_style: str = "viral"
    animation_preset_id: Optional[str] = None
    prefer_animation_preset: bool = False
    aspect_ratio: str = "9:16"
    min_silence_ms: int = Field(default=400, ge=50, le=10000)
    weights: Optional[WeightsIn] = None


@router.post("/clip-intelligence/silence")
async def analyze_silence_endpoint(body: ClipWindowRequest):
    """Detect silence intervals in a clip window from transcript timings."""
    if body.end_ms < body.start_ms:
        raise HTTPException(422, "end_ms must be >= start_ms")
    if not body.segments:
        raise HTTPException(422, "segments cannot be empty")
    segments = _segments_to_dicts(body.segments)
    cfg = SilenceConfig(
        min_silence_ms=body.min_silence_ms,
        max_keep_silence_ms=body.max_keep_silence_ms,
    )
    analysis = detect_silence(segments, body.start_ms, body.end_ms, config=cfg)
    return analysis.model_dump(mode="json")


@router.post("/clip-intelligence/pacing")
async def analyze_pacing_endpoint(body: ClipWindowRequest):
    """Return explainable pacing metrics for a clip window."""
    if body.end_ms < body.start_ms:
        raise HTTPException(422, "end_ms must be >= start_ms")
    if not body.segments:
        raise HTTPException(422, "segments cannot be empty")
    segments = _segments_to_dicts(body.segments)
    cfg = SilenceConfig(
        min_silence_ms=body.min_silence_ms,
        max_keep_silence_ms=body.max_keep_silence_ms,
    )
    metrics = analyze_pacing(segments, body.start_ms, body.end_ms, silence_config=cfg)
    return metrics.as_display_dict() | {
        "window_start_ms": metrics.window_start_ms,
        "window_end_ms": metrics.window_end_ms,
        "explanations": metrics.explanations,
        "rating": metrics.rating,
    }


@router.post("/clip-intelligence/optimize-boundaries")
async def optimize_boundaries_endpoint(body: OptimizeBoundariesRequest):
    """Optimize clip start/end using speech, silence, and sentence boundaries."""
    if body.end_ms < body.start_ms:
        raise HTTPException(422, "end_ms must be >= start_ms")
    if not body.segments:
        raise HTTPException(422, "segments cannot be empty")
    segments = _segments_to_dicts(body.segments)
    cfg = BoundaryConfig(
        prefer_sentence_boundaries=body.prefer_sentence_boundaries,
        min_duration_ms=body.min_duration_ms,
        max_duration_ms=body.max_duration_ms,
    )
    result = optimize_boundaries(
        segments,
        body.start_ms,
        body.end_ms,
        config=cfg,
        source_duration_ms=body.source_duration_ms,
    )
    return result.model_dump(mode="json")


@router.post("/clip-intelligence/enhance-plan")
async def enhance_plan_endpoint(body: EnhancePlanRequest):
    """Generate a full enhancement plan (boundaries, pacing, captions, export settings).

    Does not render or mutate video files.
    """
    if body.end_ms < body.start_ms:
        raise HTTPException(422, "end_ms must be >= start_ms")
    if not body.segments:
        raise HTTPException(422, "segments cannot be empty")
    segments = _segments_to_dicts(body.segments)
    weights = _weights_from_body(body.weights)
    cfg = EnhancementConfig(
        silence=SilenceConfig(min_silence_ms=body.min_silence_ms),
        caption_style=body.caption_style,
        animation_preset_id=body.animation_preset_id,
        prefer_animation_preset=body.prefer_animation_preset,
        aspect_ratio=body.aspect_ratio,
        scoring_weights=weights,
    )
    plan = build_enhancement_plan(
        segments,
        body.start_ms,
        body.end_ms,
        video_id=body.video_id,
        config=cfg,
        source_duration_ms=body.source_duration_ms,
    )
    return {
        "plan": plan.model_dump(mode="json"),
        "summary": plan.as_summary(),
    }

```


---

## Source: `frontend/src/pages/Studio.jsx`

```jsx
import { useEffect, useMemo, useState } from "react"
import {
  Box, Typography, Paper, Stack, Button, Stepper, Step, StepLabel,
  FormControl, InputLabel, Select, MenuItem, Switch, FormControlLabel,
  Chip, LinearProgress, Alert, Divider, TextField, CircularProgress,
} from "@mui/material"
import MovieFilterOutlinedIcon from "@mui/icons-material/MovieFilterOutlined"
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined"
import http from "../api/http"
import useDocumentTitle from "../hooks/useDocumentTitle"
import useAppStore from "../store/appStore"

const STEPS = ["Upload", "Processing", "Review", "Export"]

export default function Studio() {
  useDocumentTitle("Finish Studio")
  const showSnackbar = useAppStore((s) => s.showSnackbar)

  const [activeStep, setActiveStep] = useState(0)
  const [file, setFile] = useState(null)
  const [platform, setPlatform] = useState("tiktok")
  const [trackMode, setTrackMode] = useState("face_center")
  const [reframeEnabled, setReframeEnabled] = useState(true)
  const [audioEnhance, setAudioEnhance] = useState(true)
  const [videoEnhance, setVideoEnhance] = useState(false)
  const [thumbnailText, setThumbnailText] = useState("")

  const [presets, setPresets] = useState([])
  const [modes, setModes] = useState([])
  const [plan, setPlan] = useState(null)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    Promise.all([
      http.get("/api/production/export-presets"),
      http.get("/api/production/track-modes"),
    ]).then(([p, m]) => {
      setPresets(p.data?.presets || [])
      setModes(m.data?.modes || [])
    }).catch(() => {})
  }, [])

  const selectedPreset = useMemo(
    () => presets.find(p => p.id === platform) || null,
    [presets, platform],
  )

  const buildLocalPlan = async () => {
    // Default landscape source assumptions for plan preview before upload probe
    const res = await http.post("/api/production/finish-plan", {
      source_width: 1920,
      source_height: 1080,
      duration_s: 30,
      platform,
      track_mode: trackMode,
      reframe_enabled: reframeEnabled,
      audio: { enabled: audioEnhance, preserve_original: !audioEnhance },
      video: { enabled: videoEnhance },
      thumbnail_text: thumbnailText || null,
    })
    setPlan(res.data)
  }

  useEffect(() => {
    if (activeStep >= 1) return
    buildLocalPlan().catch(() => {})
  }, [platform, trackMode, reframeEnabled, audioEnhance, videoEnhance, thumbnailText])

  const onFile = (e) => {
    const f = e.target.files?.[0]
    if (f) {
      setFile(f)
      setResult(null)
      setError(null)
      setActiveStep(0)
    }
  }

  const runFinish = async () => {
    if (!file) {
      showSnackbar("Choose a video first", "warning")
      return
    }
    setBusy(true)
    setError(null)
    setActiveStep(1)
    setProgress(15)
    try {
      const fd = new FormData()
      fd.append("file", file)
      fd.append("platform", platform)
      fd.append("track_mode", trackMode)
      fd.append("reframe_enabled", String(reframeEnabled))
      fd.append("audio_enhance", String(audioEnhance))
      fd.append("video_enhance", String(videoEnhance))
      if (thumbnailText) fd.append("thumbnail_text", thumbnailText)

      setProgress(40)
      const res = await http.post("/api/production/finish", fd, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 600000,
      })
      setProgress(100)
      setResult(res.data)
      setPlan({ plan: res.data.plan, steps: res.data.steps, export: res.data.export, notes: res.data.plan?.notes })
      setActiveStep(2)
      showSnackbar("Finish complete — review & export", "success")
    } catch (e) {
      const detail = e.response?.data?.detail || e.message
      setError(detail)
      setActiveStep(0)
      showSnackbar(`Finish failed: ${detail}`, "error")
    } finally {
      setBusy(false)
    }
  }

  return (
    <Box sx={{ p: { xs: 2, md: 3 }, maxWidth: 960, mx: "auto" }}>
      <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 2 }}>
        <MovieFilterOutlinedIcon color="primary" />
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>Finish Studio</Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Upload → reframe → enhance → export ready TikTok / Shorts / Reels
          </Typography>
        </Box>
      </Stack>

      <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
        {STEPS.map(label => (
          <Step key={label}><StepLabel>{label}</StepLabel></Step>
        ))}
      </Stepper>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Stack spacing={2}>
        {/* Settings */}
        <Paper elevation={0} sx={{ p: 2, border: 1, borderColor: "divider", borderRadius: 2 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1.5 }}>Export settings</Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <FormControl size="small" sx={{ minWidth: 180 }}>
              <InputLabel>Platform</InputLabel>
              <Select label="Platform" value={platform} onChange={e => setPlatform(e.target.value)}>
                <MenuItem value="tiktok">TikTok</MenuItem>
                <MenuItem value="youtube_shorts">YouTube Shorts</MenuItem>
                <MenuItem value="instagram_reels">Instagram Reels</MenuItem>
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 180 }}>
              <InputLabel>Track mode</InputLabel>
              <Select label="Track mode" value={trackMode} onChange={e => setTrackMode(e.target.value)}>
                {(modes.length ? modes : [
                  { id: "center", name: "Center" },
                  { id: "face_center", name: "Face center" },
                  { id: "speaker", name: "Speaker" },
                  { id: "subject", name: "Subject" },
                ]).map(m => (
                  <MenuItem key={m.id} value={m.id}>{m.name}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              size="small"
              label="Cover text (optional)"
              value={thumbnailText}
              onChange={e => setThumbnailText(e.target.value)}
              sx={{ minWidth: 200 }}
            />
          </Stack>
          <Stack direction="row" spacing={2} sx={{ mt: 1.5, flexWrap: "wrap" }}>
            <FormControlLabel control={<Switch checked={reframeEnabled} onChange={e => setReframeEnabled(e.target.checked)} />} label="Auto reframe 9:16" />
            <FormControlLabel control={<Switch checked={audioEnhance} onChange={e => setAudioEnhance(e.target.checked)} />} label="Audio enhance" />
            <FormControlLabel control={<Switch checked={videoEnhance} onChange={e => setVideoEnhance(e.target.checked)} />} label="Video enhance" />
          </Stack>
          {selectedPreset && (
            <Typography variant="caption" sx={{ color: "text.secondary", display: "block", mt: 1 }}>
              {selectedPreset.name}: {selectedPreset.width}×{selectedPreset.height} @ {selectedPreset.fps}fps · CRF {selectedPreset.crf}
            </Typography>
          )}
        </Paper>

        {/* Upload */}
        <Paper elevation={0} sx={{ p: 2, border: 1, borderColor: "divider", borderRadius: 2 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>1. Upload</Typography>
          <Button component="label" variant="outlined" startIcon={<CloudUploadOutlinedIcon />} disabled={busy}>
            {file ? file.name : "Choose video"}
            <input hidden type="file" accept="video/*" onChange={onFile} />
          </Button>
        </Paper>

        {/* Plan preview */}
        <Paper elevation={0} sx={{ p: 2, border: 1, borderColor: "divider", borderRadius: 2 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>Pipeline plan</Typography>
          {plan?.steps ? (
            <Stack direction="row" spacing={0.75} sx={{ flexWrap: "wrap", gap: 0.75, mb: 1 }}>
              {plan.steps.map((s, i) => (
                <Chip key={`${s}-${i}`} label={s} size="small" />
              ))}
            </Stack>
          ) : (
            <Typography variant="caption" color="text.secondary">Loading plan…</Typography>
          )}
          {plan?.notes?.length > 0 && (
            <Box sx={{ mt: 1 }}>
              {plan.notes.slice(0, 6).map((n, i) => (
                <Typography key={i} variant="caption" sx={{ display: "block", color: "text.secondary" }}>• {n}</Typography>
              ))}
            </Box>
          )}
          {plan?.export && (
            <Typography variant="caption" sx={{ display: "block", mt: 1 }}>
              Export: {plan.export.name || plan.export.id} · {plan.export.width}×{plan.export.height}
            </Typography>
          )}
        </Paper>

        <Button
          variant="contained"
          size="large"
          disabled={!file || busy}
          onClick={runFinish}
          startIcon={busy ? <CircularProgress size={18} color="inherit" /> : <MovieFilterOutlinedIcon />}
        >
          {busy ? "Processing…" : "Run finish pipeline"}
        </Button>

        {busy && (
          <Box>
            <LinearProgress variant="determinate" value={progress} sx={{ borderRadius: 1 }} />
            <Typography variant="caption" color="text.secondary">Processing video…</Typography>
          </Box>
        )}

        {/* Review / Export */}
        {result?.success && (
          <Paper elevation={0} sx={{ p: 2, border: 1, borderColor: "success.main", borderRadius: 2 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>3–4. Review & export</Typography>
            <Alert severity="success" sx={{ mb: 1 }}>Ready-to-post file generated.</Alert>
            <Typography variant="body2" sx={{ wordBreak: "break-all" }}>
              Output: {result.output_path}
            </Typography>
            {result.thumbnail_path && (
              <Typography variant="body2" sx={{ wordBreak: "break-all", mt: 0.5 }}>
                Cover: {result.thumbnail_path}
              </Typography>
            )}
            <Divider sx={{ my: 1.5 }} />
            <Typography variant="caption" color="text.secondary">
              Open the Library / generated folder to download. Re-run with different platform presets as needed.
            </Typography>
            <Button sx={{ mt: 1 }} size="small" onClick={() => setActiveStep(3)}>Mark export step</Button>
          </Paper>
        )}
      </Stack>
    </Box>
  )
}

```


---

## Source: `frontend/src/hooks/useCaptionPreview.js`

```javascript
import { useEffect, useState, useMemo } from "react"
import http from "../api/http"

/**
 * Lightweight, deterministic caption preview state from the backend.
 *
 * The backend Phase 2 animation engine evaluates every requested frame and
 * returns a normalized visual-state payload. The frontend only renders it;
 * no spring/bounce/glitch/typewriter/karaoke formulas are duplicated.
 */
export default function useCaptionPreview({ words, presetId, fps = 30, durationMs = 2400, frameStep = 1, enabled = true }) {
  const [frames, setFrames] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const endFrame = useMemo(() => {
    return Math.ceil((durationMs * fps) / 1000)
  }, [durationMs, fps])

  const cacheKey = useMemo(() => {
    return JSON.stringify({ words, presetId, fps, endFrame, frameStep })
  }, [words, presetId, fps, endFrame, frameStep])

  useEffect(() => {
    if (!enabled || !words?.length || !presetId) {
      setFrames(null)
      setError(null)
      return
    }

    let cancelled = false
    const fetchPreview = async () => {
      setLoading(true)
      setError(null)
      try {
        const res = await http.post("/api/captions/preview", {
          words,
          preset_id: presetId,
          fps,
          start_frame: 0,
          end_frame: endFrame,
          frame_step: frameStep,
        })
        if (!cancelled) setFrames(res.data?.frames || null)
      } catch (e) {
        if (!cancelled) setError(e.response?.data?.detail || e.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetchPreview()
    return () => { cancelled = true }
  }, [cacheKey, enabled])

  return { frames, loading, error, endFrame }
}

```


---

## Source: `frontend/src/components/captions/AnimatedCaptionPreview.jsx`

```jsx
import { useEffect, useMemo, useRef, useState } from "react"
import { Box, Paper, Typography, Stack, Chip, CircularProgress, Alert } from "@mui/material"
import useCaptionPreview from "../../hooks/useCaptionPreview"

/**
 * Unicode-safe grapheme cluster extraction.
 *
 * Uses Intl.Segmenter when available; falls back to code-point iteration
 * so we never slice raw UTF-8 bytes.
 */
function getGraphemeClusters(text) {
  if (typeof Intl !== "undefined" && Intl.Segmenter) {
    return Array.from(new Intl.Segmenter("en", { granularity: "grapheme" }).segment(text || "")).map(s => s.segment)
  }
  return Array.from(text || "")
}

export function visibleText(text, revealProgress) {
  const clusters = getGraphemeClusters(text)
  const count = Math.max(0, Math.min(clusters.length, Math.round(clusters.length * revealProgress)))
  return clusters.slice(0, count).join("")
}

function KaraokeWord({ text, highlightProgress, baseColor, highlightColor }) {
  const width = `${Math.max(0, Math.min(1, highlightProgress)) * 100}%`
  return (
    <Box component="span" sx={{ position: "relative", display: "inline-block" }}>
      <Box component="span" sx={{ color: baseColor, opacity: 0.85 }}>{text}</Box>
      <Box
        component="span"
        sx={{
          position: "absolute",
          left: 0,
          top: 0,
          width,
          overflow: "hidden",
          whiteSpace: "nowrap",
          color: highlightColor,
        }}
      >
        {text}
      </Box>
    </Box>
  )
}

function TypewriterWord({ text, revealProgress }) {
  return <>{visibleText(text, revealProgress)}</>
}

function CaptionWord({
  word,
  baseColor,
  highlightColor,
  backgroundHighlight = false,
  backgroundColor = "rgba(0,0,0,0.75)",
  outline = true,
}) {
  const isActive = word.active || word.highlight_progress > 0 || word.opacity > 0.85
  const color = (isActive && word.highlight_progress >= 0) ? (
    word.highlight_progress > 0 ? highlightColor : (word.active ? highlightColor : baseColor)
  ) : baseColor

  const style = useMemo(() => ({
    display: "inline-block",
    opacity: word.opacity,
    transform: `translate(${word.translate_x}px, ${word.translate_y}px) scale(${word.scale}) rotate(${word.rotation}deg)`,
    filter: `blur(${word.blur}px)`,
    color,
    textShadow: outline
      ? `0 0 ${Math.max(word.glow, 0)}px currentColor, 0 2px 0 rgba(0,0,0,0.85), 0 -1px 0 rgba(0,0,0,0.6), 1px 0 0 rgba(0,0,0,0.6), -1px 0 0 rgba(0,0,0,0.6)`
      : `0 0 ${word.glow}px currentColor`,
    letterSpacing: `${word.letter_spacing}px`,
    willChange: "transform, opacity, color",
    transition: "color 80ms linear",
    px: backgroundHighlight && word.active ? 0.7 : 0.15,
    py: backgroundHighlight && word.active ? 0.2 : 0,
    borderRadius: backgroundHighlight && word.active ? 1.5 : 0,
    bgcolor: backgroundHighlight && word.active ? backgroundColor : "transparent",
  }), [word, color, backgroundHighlight, backgroundColor, outline])

  let content
  if (word.reveal_progress > 0 && word.reveal_progress < 1) {
    content = <TypewriterWord text={word.text} revealProgress={word.reveal_progress} />
  } else if (word.highlight_progress > 0) {
    content = <KaraokeWord text={word.text} highlightProgress={word.highlight_progress} baseColor={baseColor} highlightColor={highlightColor} />
  } else {
    content = word.text
  }

  return (
    <Box component="span" sx={{ ...style, mx: 0.55 }}>
      {content}
    </Box>
  )
}

/**
 * AnimatedCaptionPreview
 *
 * Renders a caption segment using deterministic visual states produced by the
 * backend Phase 2 animation engine. It does not contain animation formulas.
 *
 * Props:
 *  - words: array of { text, start_ms, end_ms }
 *  - presetId: one of bounce, explosive, glitch, typewriter, karaoke
 *  - fps: playback frame rate
 *  - durationMs: how long to evaluate (kept short for preset cards)
 *  - frameStep: step between frames (increase to reduce backend payload)
 *  - autoplay: start playback immediately
 *  - loop: restart at end
 *  - width / height: player dimensions
 */
export default function AnimatedCaptionPreview({
  words,
  presetId,
  fps = 30,
  durationMs = 2400,
  frameStep = 1,
  autoplay = true,
  loop = true,
  width = 320,
  height = 560,
  baseColor = "#ffffff",
  highlightColor = "#ffee33",
  backgroundHighlight = false,
  backgroundColor = "rgba(0,0,0,0.75)",
  outline = true,
  onError,
}) {
  const { frames, loading, error, endFrame } = useCaptionPreview({ words, presetId, fps, durationMs, frameStep })
  const [frameIndex, setFrameIndex] = useState(0)
  const [playing, setPlaying] = useState(autoplay)
  const frameCount = frames?.length || 0

  // Playback loop. We drive it from the precomputed frames so it stays in sync
  // with the deterministic backend state.
  useEffect(() => {
    if (!playing || frameCount === 0) return
    const interval = setInterval(() => {
      setFrameIndex(i => {
        const next = i + 1
        if (next >= frameCount) {
          return loop ? 0 : i
        }
        return next
      })
    }, 1000 / fps)
    return () => clearInterval(interval)
  }, [playing, frameCount, fps, loop])

  // Reset when the payload changes.
  useEffect(() => { setFrameIndex(0) }, [frames])

  // Surface errors to parent.
  useEffect(() => { if (error && onError) onError(error) }, [error, onError])

  const currentFrame = frames?.[frameIndex]
  const activeWords = currentFrame?.words || []

  return (
    <Paper
      elevation={0}
      sx={{
        width,
        height,
        bgcolor: "#000",
        borderRadius: 3,
        overflow: "hidden",
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: 1,
        borderColor: "divider",
      }}
      onMouseEnter={() => setPlaying(true)}
      onMouseLeave={() => setPlaying(autoplay)}
    >
      {loading && (
        <Box sx={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <CircularProgress size={28} sx={{ color: "rgba(255,255,255,0.5)" }} />
        </Box>
      )}

      {error && !loading && (
        <Alert severity="warning" sx={{ m: 2, fontSize: "0.75rem" }}>
          {error}
        </Alert>
      )}

      {!error && (
        <Box sx={{ p: 2, textAlign: "center" }}>
          <Typography
            variant="h5"
            sx={{
              color: baseColor,
              fontWeight: 800,
              lineHeight: 1.35,
              textShadow: "0 2px 8px rgba(0,0,0,0.6)",
            }}
          >
            {activeWords.length > 0 ? (
              activeWords.map((word, i) => (
                <CaptionWord
                  key={`${word.word_index}-${i}`}
                  word={word}
                  baseColor={baseColor}
                  highlightColor={highlightColor}
                  backgroundHighlight={backgroundHighlight}
                  backgroundColor={backgroundColor}
                  outline={outline}
                />
              ))
            ) : (
              <Box component="span" sx={{ opacity: 0.4 }}>—</Box>
            )}
          </Typography>
        </Box>
      )}

      {/* Debug / preset badge */}
      <Chip
        label={presetId}
        size="small"
        sx={{
          position: "absolute",
          top: 8,
          right: 8,
          height: 20,
          fontSize: "0.65rem",
          fontWeight: 700,
          bgcolor: "rgba(255,255,255,0.15)",
          color: "#fff",
          border: "1px solid rgba(255,255,255,0.2)",
        }}
      />

      {/* Optional scrub / frame readout */}
      <Stack
        direction="row"
        spacing={0.5}
        sx={{
          position: "absolute",
          bottom: 8,
          left: 8,
          fontSize: "0.65rem",
          color: "rgba(255,255,255,0.5)",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        <Box component="span">{frameIndex}</Box>
        <Box component="span">/</Box>
        <Box component="span">{frameCount || endFrame}</Box>
      </Stack>
    </Paper>
  )
}

```


---

## End of master document

**Repo tip:** `4238626`  
**Full source archive:** `ViralMint-phases-0-10-source.zip`  

You own everything under AGPL-3.0 (same as ViralMint). Keep licenses/attribution when you redistribute.
