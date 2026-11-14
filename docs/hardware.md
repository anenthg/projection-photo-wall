# Hardware and physical setup

## Projector

- **Android is the easy path.** The page runs in Fully Kiosk Browser, an Android app, which is the
  recommended way to run the wall on an Android projector (docs/projector-kiosk.md). A projector with Android
  built in, or any projector plus an Android TV box / Fire TV stick on HDMI, works. iOS/Apple TV can't run it.
- **Brightness:** in a dimmed room 200 to 500 ANSI lumens is plenty: only the frame openings are lit.
- **Resolution:** many budget "1080p" Android projectors render apps at 1280x720 and upscale. That's fine: a
  frame only gets ~100 to 300 projector pixels across anyway. Use the page's resolution test (`?res=1`, short
  link + `r`) to see what you actually get. If the projector offers a 1080p output setting, use it.
- **Throw:** the picture must cover all frames with ~10% margin. Picture width = distance / throw ratio
  (typical 1.2, short-throw 0.5). Example: frames spanning 1.3 m need ~1.5 m of picture: ~1.8 m away at 1.2.
  Closer = more pixels per frame = sharper photos, as long as the picture still covers every frame.
- **Mounting:** shelf, tripod or ceiling mount; it must not move later. Straight-on is best, but keystone
  correction is fine because every frame is warped individually anyway.

## Frames

- **Remove glass/acrylic** and peel protective film. Glass reflects the beam back as glare.
- Matte white or light mats and backing take light best; brown/dark backing cards dull every colour.
- Black frame borders are ideal: light that spills over the edge is barely visible.
- Any number of frames, any mix of sizes and orientations; tilted frames are fine (each is a free quad).

## Room

- Projected black is not black: the wall glows faintly. Dim the room for the best effect.
- The projector's fan and speaker: sound plays from the projector (or the TV box's HDMI audio).

## Order of work

1. Hang frames, remove glass.
2. Place the projector, set focus, keystone and zoom so the picture covers everything.
3. **Never touch keystone, zoom or position again**, then align each frame (docs/alignment.md).
