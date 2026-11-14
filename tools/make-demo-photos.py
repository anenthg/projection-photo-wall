#!/usr/bin/env python3
"""Make placeholder photos for trying the pipeline before using real ones.

    python3 tools/make-demo-photos.py /tmp/demo-photos      # then: python3 tools/prepare-album.py /tmp/demo-photos

Writes 18 colourful numbered JPEGs (portrait, landscape and square) into the folder. Needs Pillow.
"""
import colorsys, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is missing: pip install pillow")

out = Path(sys.argv[1] if len(sys.argv) > 1 else "demo-photos")
out.mkdir(parents=True, exist_ok=True)
sizes = [(900, 1200), (1200, 800), (1000, 1000)]
for k in range(18):
    w, h = sizes[k % 3]
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    hue = k / 18
    for y in range(h):
        r, g, b = colorsys.hsv_to_rgb((hue + y / h * 0.15) % 1, 0.65, 0.95 - 0.45 * y / h)
        d.line([(0, y), (w, y)], fill=(int(r * 255), int(g * 255), int(b * 255)))
    for i in range(6):
        cx, cy, r = (i * 137 + k * 59) % w, (i * 211 + k * 97) % h, min(w, h) * (0.08 + 0.04 * (i % 3))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=max(3, w // 200))
    s = min(w, h) // 3
    d.rectangle([w // 2 - s // 2, h // 2 - s // 2, w // 2 + s // 2, h // 2 + s // 2], outline=(255, 255, 255), width=max(4, w // 150))
    d.text((w // 2, h // 2), str(k + 1), fill=(255, 255, 255), anchor="mm", font_size=s // 2)
    im.save(out / f"demo-{k + 1:02d}.jpg", quality=85)
print(f"18 demo photos in {out}")
