# Customizing

All behaviour lives in `site/index.html`. Search for the names below.

## Timing

| What | Where | Default |
|---|---|---|
| Seconds per photo (per frame; frames are staggered) | `interval:60` in the `S={...}` defaults; the desktop editor slider overrides it per browser | 60 (minimum 60: slower devices need ~10-15 s to decode and show a photo) |
| Kolam every N seconds | `LITE_EVERY=120` | 120 |
| Slow zoom on photos | `kb:true` in `S` defaults | on |

## Modes

- **Lite (default, projector):** instant photo cuts with slow zoom, Kolam between photos, light shows on demand.
- **Full (`?anim=1`):** cross-fades and seven ambient scenes (photo panorama, drifting photo, then-and-now,
  lantern, fireflies, Kolam, dawn flight). Heavier: good on a computer, often too much for a projector.
- **Vector only (`?vector=1`):** no photos at all.

## Light shows and music

- Scenes: `SCENE.skyfire`, `laser`, `prism`, `grid`, `phoenix` (each `show:1`). Order of **Light show**:
  `SHOW_KEYS`; order in the menu: `SHOW_MENU`.
- Music: `SCORES.<name>`: a step sequencer (`bpm`, `steps`, `at(step, time, X)`) using the synth voices in
  `AUD.api` (kick, snare, clap, hat, bass, pluck, lead, pad, bell, flute, veena, tanpura, ...). `X.cue(...)`
  emits visual cues that the scene receives in sync with the music.
- The projector plays **pre-rendered files** (`site/music/*.m4a`), because synthesizing a busy score live while
  drawing a show is too much for a projector CPU (the music stutters and dies after a few seconds). After
  editing a score:

  ```bash
  tools/render-music.sh prism          # or no argument for all; needs Node + macOS afconvert
  ```

  then bump `?v=` on that `SCORES.<name>.file` line and deploy. On Linux, replace the `afconvert` line with
  `ffmpeg -i in.wav -c:a aac -b:a 160k out.m4a`.
- `SCORES.kolam` plays only when **Kolam now** is chosen from the menu; `level:.7` renders it softer.

## Look

- Frame layout size `NW` (default 200 px): see troubleshooting before changing it.
- Captions: set per photo in the desktop editor ("Caption for the selected photo"); toggle with Show captions.
- Brightness / contrast / edge trim: desktop editor, Projector section (saved per browser).
