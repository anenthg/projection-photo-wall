#!/usr/bin/env python3
"""Prepare your photos for the wall: resize, re-encode, assign each to a frame, write site/album.js.

    python3 tools/prepare-album.py ~/Pictures/wall-photos
    python3 tools/prepare-album.py ~/Pictures/wall-photos --max 1280 --quality 65 --per-frame 2

Needs Pillow (pip install pillow). Reads frames from site/config.js. Your originals are never changed.

What it does
  * Every JPEG/PNG/WebP (and HEIC if pillow-heif is installed) under the folder, sorted by path.
  * Fixes rotation from EXIF, strips EXIF (GPS, camera data), resizes so the long edge is at most --max px
    (1280 is plenty: a frame is only ~100-300 projector pixels wide) and saves JPEG at --quality.
  * Writes site/album/p000.jpg, p001.jpg, ... and replaces whatever was there before.
  * Assigns frames: a photo in a sub-folder named frame-3 (1-based, as numbered on the wall in Align) goes to
    that frame; the rest go to the frame whose shape suits them best, sharing evenly. A folder named "then" or
    "now" anywhere in the path tags the photo for the "Then and now" scene (full mode only).
  * Writes site/album.js with each photo's size in bytes (the page uses it to detect incomplete downloads) and
    a content hash in the URL (browsers fetch a photo again only when it really changed).
"""
import argparse, hashlib, io, json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}


def load_config():
    txt = (SITE / "config.js").read_text(encoding="utf-8")
    body = txt[txt.index("=", txt.index("WALL_CONFIG")) + 1:]
    body = body[body.index("{"):body.rindex("}") + 1]
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        sys.exit(f"site/config.js is not strict JSON after 'window.WALL_CONFIG =': {e}")


def frame_ratios(cfg):
    frames = cfg.get("frames") or []
    if not frames:
        sys.exit("site/config.js has no frames")
    wp = cfg.get("wallPhoto") or {}
    W, H = float(wp.get("width") or 1600), float(wp.get("height") or 1000)
    out = []
    for f in frames:
        r = f.get("ratio")
        q = f.get("quad")
        if not r and q and len(q) == 4:
            d = lambda a, b: math.hypot((b[0] - a[0]) * W, (b[1] - a[1]) * H)
            r = (d(q[0], q[1]) + d(q[3], q[2])) / (d(q[0], q[3]) + d(q[1], q[2]))
        out.append(float(r or 0.8))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photos", type=Path, help="folder with your photos (sub-folders allowed)")
    ap.add_argument("--max", type=int, default=1280, help="long edge in px (default 1280)")
    ap.add_argument("--quality", type=int, default=65, help="JPEG quality (default 65)")
    ap.add_argument("--per-frame", type=int, default=0,
                    help="stop after this many photos per frame (default: use every photo)")
    a = ap.parse_args()
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("Pillow is missing: pip install pillow")
    try:
        import pillow_heif  # optional HEIC support
        pillow_heif.register_heif_opener()
    except ImportError:
        pass

    cfg = load_config()
    ratios = frame_ratios(cfg)
    n = len(ratios)
    files = sorted(p for p in a.photos.rglob("*") if p.is_file() and p.suffix.lower() in EXTS
                   and not p.name.startswith("."))
    if not files:
        sys.exit(f"No photos found under {a.photos}")

    out_dir = SITE / "album"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("p*.jpg"):
        old.unlink()

    load = [0] * n
    album, skipped = [], []
    for path in files:
        rel = path.relative_to(a.photos)
        parts = [s.lower() for s in rel.parts[:-1]]
        pinned = next((int(m.group(1)) - 1 for s in parts if (m := re.fullmatch(r"frame-?0*(\d+)", s))), None)
        if pinned is not None and not 0 <= pinned < n:
            skipped.append(f"{rel} (folder frame-{pinned + 1}, but the wall has {n} frames)")
            continue
        era = "then" if "then" in parts else "now" if "now" in parts else ""
        try:
            im = Image.open(path)
            im = ImageOps.exif_transpose(im).convert("RGB")
        except Exception as e:  # unreadable or unsupported (e.g. HEIC without pillow-heif)
            skipped.append(f"{rel} ({e.__class__.__name__}: {e})")
            continue
        im.thumbnail((a.max, a.max), Image.LANCZOS)
        w, h = im.size
        if pinned is None:
            r = w / h
            cands = [i for i in range(n) if not a.per_frame or load[i] < a.per_frame]
            if not cands:
                skipped.append(f"{rel} (every frame already has {a.per_frame})")
                continue
            frame = min(cands, key=lambda i: abs(math.log(r / ratios[i])) + 0.35 * load[i])
        else:
            frame = pinned
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=a.quality, optimize=True, progressive=True)
        data = buf.getvalue()
        name = f"p{len(album):03d}.jpg"
        (out_dir / name).write_bytes(data)
        load[frame] += 1
        album.append({"src": f"album/{name}?v={hashlib.sha1(data).hexdigest()[:8]}", "frame": frame,
                      "era": era, "w": w, "h": h, "b": len(data)})

    js = ("/* Written by tools/prepare-album.py; don't edit by hand. */\nwindow.WALL_ALBUM = "
          + json.dumps(album, separators=(",", ":")) + ";\n")
    (SITE / "album.js").write_text(js, encoding="utf-8")

    total = sum(e["b"] for e in album)
    print(f"{len(album)} photos -> site/album ({total / 1e6:.1f} MB), site/album.js written")
    for i in range(n):
        name = (cfg["frames"][i].get("name") or f"Frame {i + 1}")
        print(f"  frame {i + 1:2d} {name[:28]:28s} ratio {ratios[i]:.2f}: {load[i]} photo(s)")
    if [i for i in range(n) if load[i] == 0]:
        print("  note: some frames got no photo; add photos of that shape or pin some with a frame-N folder")
    if total > 40e6:
        print("  note: over 40 MB; the projector keeps every photo in memory. Fewer photos or --max 1024 help.")
    for s in skipped:
        print("  skipped:", s)


if __name__ == "__main__":
    main()
