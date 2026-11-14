# Configuration reference

## site/config.js

A JavaScript file whose body is strict JSON (so `tools/prepare-album.py` can read it):

```js
window.WALL_CONFIG =
{
  "title": "Our Wall",
  "wallPhoto": { "src": "wall.jpg", "width": 4032, "height": 3024 },
  "frames": [
    { "name": "Left tall", "size": "8x10", "quad": [[0.06,0.30],[0.17,0.30],[0.17,0.60],[0.06,0.60]] },
    { "name": "Top middle", "ratio": 1.5 }
  ],
  "route": [0, 1, 3, 2]
};
```

| Field | Required | Meaning |
|---|---|---|
| `title` | no | browser tab and desktop editor title |
| `wallPhoto` | no | photo of the wall for the desktop mock-up and the starting layout. `src` relative to `site/`; `width`/`height` in pixels (needed to convert normalised corners) |
| `frames[]` | yes | one per frame. Order = frame numbers 1..N shown when aligning; keep it stable once aligned |
| `frames[].name` | no | label in the editor |
| `frames[].size` | no | free-text label, e.g. "8x10 frame" |
| `frames[].ratio` | if no quad | width / height of the visible opening. Portrait 8x10 = 0.8, landscape 6x4 = 1.5 |
| `frames[].quad` | no | inner corners on the wall photo, normalised 0-1, order TL, TR, BR, BL. Without it the frame is placed in a grid |
| `route` | no | order (0-based) in which travelling scenes (Kolam line, drifting photo) visit frames; default is a loop around the wall's centre |

Changing the number or order of frames invalidates saved alignments (the page ignores an alignment with a
different frame count). Re-run `prepare-album.py` after changing frames.

## site/album.js

Written by `tools/prepare-album.py`; don't edit. Each entry:
`{src: "album/p000.jpg?v=<hash>", frame: 0, era: "then"|"now"|"", w, h, b}` where `b` is the byte size
(the page re-downloads a photo whose stored copy has a different size: interrupted downloads heal themselves).
When album.js changes, every browser re-places the album photos on its next start.

## site/alignment.json (optional)

`{"aspect":"16:9","layout":[[[x,y],[x,y],[x,y],[x,y]], ...]}`: one quad per frame in projector coordinates
(0-1). Produced by **Alignment QR** (remote) or **Copy alignment data** (desktop editor, Align tab). Each browser
applies a given alignment.json once (it keeps a fingerprint), so later fine-tuning on the projector isn't
overwritten until you publish a different file.

## Page URL options

Append to the page URL (`…/#play`), or use the short links the deploy script creates (`<code>` + letter):

| Option | Short | Effect |
|---|---|---|
| `#play` | (none) | kiosk mode straight away (the start URL) |
| `#align` | `a` | straight into alignment |
| `?diag=1` | `d` | diagnostics overlay: memory, photos, audio, show timing |
| `?fps=1` | `f` | frame-rate readout |
| `?keys=1` | `k` | shows the key codes the remote sends |
| `?res=1` | `r` | 1-pixel stripe test per frame + the real output resolution |
| `?vector=1` | `v` | no photos, Kolam only (to rule out photo/memory problems) |
| `?anim=1` | `x` | full mode: all scenes with fades (heavier; fine on a computer) |
| `?nw=300` | | frame layout size in px (default 200; see troubleshooting) |
| `?music=live` | | synthesize show music live instead of the files (debugging) |
