# Projection Photo Wall

Turn a wall of empty picture frames into a living photo wall: a small projector warps a separate photo stream
into each frame, changes one frame at a time with a slow zoom, draws a glowing Kolam line across the wall
between photos, and on demand plays one-minute sound-and-light shows with original music. Everything runs in
one web page, aligned with a TV remote, on an Android projector in a kiosk browser.

**With an AI coding agent:** point it at this repo and say *"Set up my photo wall following AGENTS.md"*. The
playbook walks it (and you) through photos, frame layout, publishing, the projector and alignment, with a check
at every step.

## What you need

- Picture frames on a wall, glass removed (any number, any mix of sizes).
- An Android projector (or a projector plus an Android TV box / Fire TV stick) that can sit 1 to 2 m from the
  wall. Tested on a 720p/1080p portable Android 13 projector; see [docs/hardware.md](docs/hardware.md).
- Your photos, a computer with Python 3 (and Node 18+ for publishing).
- Optional: a free Cloudflare account for hosting ([docs/hosting.md](docs/hosting.md) has a local-only option).

## Quick start

```bash
python3 -m pip install pillow
# 1. Describe your frames: edit site/config.js (or click corners on a wall photo: tools/mark-frames.html)
# 2. Prepare photos (resize, strip location data, assign to frames):
python3 tools/prepare-album.py ~/Pictures/wall-photos
# 3. Preview:
./serve.sh                     # http://localhost:8000/  (and /#play)
# 4. Publish (unlisted URL) and put the short link in Fully Kiosk Browser on the projector:
./deploy-cloudflare.sh
```

Then align each frame with the remote: any arrow opens the menu, **Align frames**
([docs/alignment.md](docs/alignment.md)).

## On the wall

| Remote menu | What it does |
|---|---|
| Kolam now | the Kolam scene with its own music (the automatic one every 2 minutes is silent) |
| Light show | all five shows back to back, ~5 min |
| Skyfire, Laser tide, Prism, Neon grid, Phoenix | one show each, ~1 min with music |
| Sound test | a chime and the audio status |
| Align frames | per-frame alignment; its menu has Alignment QR to back up the alignment |

OK or Back stops a show. Photos change one frame at a time, each frame once a minute.

## Repo layout

| Path | What it is |
|---|---|
| `site/index.html` | the whole app (editor, kiosk mode, scenes, shows, audio) |
| `site/config.js` | your frames (names, shapes, optional corners on a wall photo) |
| `site/album.js`, `site/album/` | your photos, written by `tools/prepare-album.py` (git-ignored) |
| `site/alignment.json` | optional default alignment (from Alignment QR) |
| `site/music/` | pre-rendered show music (original, made from the scores in index.html) |
| `tools/prepare-album.py` | resize, strip EXIF, assign photos to frames, write album.js |
| `tools/mark-frames.html` | click frame corners on a wall photo, get config.js entries |
| `tools/make-demo-photos.py` | placeholder photos for a dry run |
| `tools/render-music.sh` | re-render the music after editing a score |
| `deploy-cloudflare.sh`, `serve.sh` | publish to Cloudflare Pages / preview locally |
| `docs/` | hardware, configuration, hosting, projector, alignment, customizing, troubleshooting |

## Privacy

Photos stay out of git. When published, they sit on a public-but-unlisted site: a long random path, no index,
no search engines, no referrer. That is obscurity, not access control; anyone with the full URL can see them.
`docs/hosting.md` explains the trade-off and a local-network alternative where nothing leaves your home.

## License

MIT, including the music in `site/music/` (original compositions generated from the scores in `index.html`).
