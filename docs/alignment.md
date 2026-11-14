# Aligning the frames

Every frame is an independent quad: the page warps its photo so the four corners land exactly on the frame's
opening, whatever the angle. Do this after the projector is in its final position with keystone and zoom set.

## With the remote (on the projector)

1. Any arrow → menu → **Align frames**. Each frame shows a numbered calibration grid; frame 1 is highlighted.
2. **Whole frame:** arrows move it 1 px; hold the arrow to move 10 px at a time. Get it roughly in place.
3. **Corners:** press OK: the top-left corner is highlighted; arrows move just that corner. OK again moves to
   top-right, bottom-right, bottom-left.
4. After the 4th corner, OK opens the Align menu: **Next frame**, **Previous frame**, **This frame again**,
   **Alignment QR**, **Done: back to Play**.
5. Repeat for each frame. Aim for the grid's edge to sit just inside the opening (light on the black frame
   border is more visible than a hair of unlit mat).

Everything is saved in the projector's browser as you go.

## Back it up as the default

Menu (in Align) → **Alignment QR** → scan with a phone camera → save the text exactly as `site/alignment.json`
→ `./deploy-cloudflare.sh`. A reset browser, a new projector, or a desktop preview then starts from that
alignment. Each browser applies a given alignment.json once, so later remote tweaks are kept.

## With a mouse (desktop editor)

Open the page without `#play` on a computer connected to the projector as a second screen: **Project on
wall**, **Align** tab, drag the corner handles. **Copy alignment data** gives the same JSON as the QR.

## Tips

- Start with the frames that are farthest apart; mistakes in keystone show up there first.
- If every frame is off in the same way, the projector moved: re-align (or restore alignment.json if you can
  put it back exactly).
- **Reset alignment** (desktop editor) returns to the layout from config.js.
