# Agent playbook: set up a projection photo wall

You are helping someone project their photos into the picture frames hanging on their wall. Follow the phases
in order. Each phase ends with a **check**; don't move on until it passes. Ask the person only what the
"Ask" lines list; decide everything else yourself from this file and `docs/`.

What they end up with: a web page (`site/`) hosted as an unlisted website, opened full-screen by a kiosk browser
on an Android projector. The page warps one photo stream into each frame (each frame aligned with the remote),
changes photos once a minute with a slow zoom, plays a Kolam line-drawing scene every 2 minutes, and has
on-demand light shows with music from the remote's menu.

## Ground rules

- **Privacy first.** The photos are personal. Never upload them anywhere except the person's own Cloudflare Pages
  project (Phase 5), never commit them (`site/album/` and `site/album.js` are git-ignored), and never paste
  their URLs into public places. `.cloudflare-site` holds the secret URL path: never commit, print in public
  logs, or share it.
- **One source of truth:** `site/index.html` is the whole app. Configure it through `site/config.js` (frames)
  and `site/album.js` (photos, generated). Don't fork the page per wall.
- **Keep the page CSP-clean:** scripts only from `'self'`, cdnjs.cloudflare.com, cdn.jsdelivr.net or unpkg.com;
  fonts from Google Fonts. No other network calls.
- **Small, verified steps.** Run each command, read its output, and fix problems before going on. Tell the
  person before anything that changes their projector or publishes something.
- **After alignment, nobody touches the projector's keystone, zoom, focus-by-zoom or position.** Any change
  moves the picture and the frames must be re-aligned.

## Phase 0: gather inputs

Ask (one message):

1. A folder of photos (JPEG/PNG/HEIC), roughly 2 to 4 per frame. Optional sub-folders `frame-3` (pin to frame 3)
   and `then`/`now` (tags for the "Then and now" scene).
2. A straight-on photo of the wall with the empty frames (phone photo, whole wall in view, frames' glass
   removed). Optional but recommended: it gives a good starting layout and a desktop mock-up.
3. How many frames, and for each roughly its shape (portrait/landscape/square, or the print size like 8x10).
   Not needed if you get the wall photo.
4. The projector or player: brand/model and Android version. It must run Android (projector, TV box, Fire TV
   stick). **On Android, recommend Fully Kiosk Browser** (the tested kiosk app; don't substitute another
   browser or kiosk app unless the person insists). See `docs/hardware.md` if they don't have a device yet.
5. Cloudflare (required, there is no other hosting option): "The page and photos will be on a public but
   unlisted website (Cloudflare Pages, free), under a long random URL that is never linked or indexed. Anyone
   with the full URL could see the photos. OK?" If yes, ask them to create a free Cloudflare account and verify
   its email, following the README section **Cloudflare account (required)**; creating the account and
   logging in are the person's job, never yours. If they won't use Cloudflare, stop: this setup doesn't
   support other hosting.

**Check:** you have photos, a frame list (or wall photo), an Android device, an explicit yes to Cloudflare
hosting, and the person confirms their Cloudflare account exists and its email is verified.

## Phase 1: tools

```bash
python3 --version          # 3.8+
python3 -m pip install pillow        # for tools/prepare-album.py (add pillow-heif for HEIC)
node --version             # 18+, only for publishing (wrangler) and re-rendering music
```

If `pip install` is blocked (externally managed Python), use a venv: `python3 -m venv .venv && .venv/bin/pip
install pillow`, then run the tools with `.venv/bin/python`.

**Check:** `python3 -c "import PIL"` (or the venv's python) succeeds.

## Phase 2: describe the wall (`site/config.js`)

Edit the JSON in `site/config.js` (strict JSON after `window.WALL_CONFIG =`; field reference in
`docs/configuration.md`).

- **With a wall photo (preferred):** open `tools/mark-frames.html` in a browser (double-click the file; it
  works offline), open the wall photo, and click each frame's four inner corners in the order top-left,
  top-right, bottom-right, bottom-left. Copy the output's `wallPhoto` and `frames` into `config.js` and copy the
  photo to `site/wall.jpg` (or the name shown). If you can't drive a browser, estimate the corners yourself by
  looking at the photo (normalised 0-1 coordinates, same corner order) and confirm visually in Phase 4.
- **Without a wall photo:** list the frames with `name` and `ratio` (width/height of the visible opening:
  8x10 portrait = 0.8, 6x4 landscape = 1.5, square = 1). The page lays them out in a grid; real alignment
  happens on the wall in Phase 7.
- Number frames left to right, top to bottom; the person will see these numbers when aligning.
- Set `title` (shown in the browser tab and desktop editor).

**Check:** `python3 tools/prepare-album.py --check` prints "config.js OK" and the frame list (it needs no
photos and changes nothing).

## Phase 3: prepare the photos

```bash
python3 tools/prepare-album.py /path/to/their/photos
```

It fixes rotation, strips EXIF (location!), resizes to 1280 px JPEG q65, assigns each photo to the frame whose
shape fits best (or its `frame-N` folder), and writes `site/album/` + `site/album.js`. Read its summary:

- every frame should get at least one photo; if not, ask for more photos of that shape or pin some;
- total size ideally under ~30 MB (the projector holds all photos in memory). Use `--max 1024` or fewer photos
  if it's bigger;
- "skipped" lines: usually HEIC without `pillow-heif` (`pip install pillow-heif`) or unreadable files.

Don't hand-edit `album.js`; re-run the tool after any photo change.

**Check:** the summary shows every frame with photos and no unexpected skips.

## Phase 4: preview locally

```bash
./serve.sh          # http://localhost:8000/
```

Open `http://localhost:8000/` in a desktop browser (or drive one): the **On the wall** tab shows the wall photo
(if any) with photos inside each frame. Then open `http://localhost:8000/#play`: a progress bar, then all
frames filled; press an arrow key for the menu, try **Kolam now** and **Prism**.

**Check:** frames sit on the frames in the mock-up (if a wall photo was used), every frame shows a photo, the
menu works, no errors in the browser console. Fix `config.js` corners now if the mock-up is off.

## Phase 5: publish

Cloudflare Pages (required; the account from Phase 0):

```bash
./deploy-cloudflare.sh
```

The first run creates `.cloudflare-site` (project name, secret path, short code) and opens `wrangler login` if
needed: tell the person a Cloudflare tab will ask whether Wrangler may make changes to their account, and that
they select **Allow** while signed in to the right account. Logging in is the person's job. It prints three URLs: give the person the **short link** (typed on the
projector) and the **desktop editor** URL. Re-run it after any change; the URLs never change.

Nothing has to be enabled in the Cloudflare dashboard: the script publishes to the production branch, and a
production `*.pages.dev` address is public by default. Make sure the person hasn't put Cloudflare Access (Zero
Trust) in front of it, or the projector will hit a login screen. Problems: `docs/hosting.md#troubleshooting`.

**Check:** the short link opens the wall with no login screen from a phone on mobile data (Wi-Fi off), in a
private tab: photos load, no 404. A brand-new address can take a few minutes to start resolving.

## Phase 6: the projector

Recommended app on an Android projector: **Fully Kiosk Browser** (fully-kiosk.com, also on Google Play).
Walk the person through `docs/projector-kiosk.md` (install Fully Kiosk Browser, start URL = short link, the
settings list). The person does the clicking on the device; you explain one step at a time. Key settings:
start URL, **Autoplay videos ON** (allows sound), keep screen on, start on boot, hardware acceleration on.

**Check:** the wall appears full-screen on the projector, photos load (progress bar finishes), and the menu
opens with any arrow on the remote.

## Phase 7: align on the wall

Physical prep first (`docs/hardware.md`): glass out of the frames, projector placed so its picture covers all
frames, keystone/zoom set once and then left alone.

Then on the remote: arrow → menu → **Align frames**. Per frame: arrows move the whole frame (hold for big
steps), OK steps through its 4 corners (arrows move the highlighted corner), one more OK opens the menu with
**Next frame / Previous frame / This frame again / Alignment QR / Done**. Details: `docs/alignment.md`.

Alignment is saved in the projector's browser. Back it up: menu → **Alignment QR** → person scans it with a
phone and sends you the text → save it as `site/alignment.json` → `./deploy-cloudflare.sh`. Any browser that
opens the page then starts from that alignment.

**Check:** every photo fills its frame opening with no light spilling onto the black frame or wall.

## Phase 8: final checks

On the projector, from the remote menu:

- **Sound test** plays a chime (if silent: projector volume, Fully "Autoplay videos", see troubleshooting).
- **Light show** plays all five shows with music (~5 min); OK or Back stops it.
- Leave it 5 minutes: photos change one frame at a time (each frame once a minute), Kolam every 2 minutes.
- Power-cycle the projector: the wall should come back by itself (Fully "Start on boot").

If anything misbehaves, open the short link with `d` appended (diagnostics overlay) and use
`docs/troubleshooting.md`.

## Changing things later

| Change | Do |
|---|---|
| Photos | update the folder, re-run `tools/prepare-album.py`, then `./deploy-cloudflare.sh` |
| Frames added/removed | edit `config.js`, re-run `prepare-album.py`, deploy, re-align new frames |
| Default alignment | Alignment QR -> `site/alignment.json` -> deploy |
| Music or shows | `docs/customizing.md` (scores in `index.html`, `tools/render-music.sh`) |
| Timings (photo interval, Kolam gap) | `docs/customizing.md` |
