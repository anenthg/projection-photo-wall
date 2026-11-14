#!/bin/bash
# Publish site/ to Cloudflare Pages as a public-but-unlisted site.
#
#   ./deploy-cloudflare.sh            build + deploy, prints the wall's URLs
#   ./deploy-cloudflare.sh --dry-run  build the upload folder only (build/cloudflare), no upload
#
# Needs Node (npx) and a Cloudflare account; the first run opens a browser for `wrangler login` if needed.
#
# "Unlisted": the wall lives under a long random path, kept in .cloudflare-site (git-ignored; never commit or
# share it). The site root and every other path return 404, search engines are told not to index anything,
# and no Referer is sent. Anyone who has the full URL can still see the photos: it is obscurity, not a login.
# The short link (/<code>, 6 letters) exists only to make typing on a TV remote bearable; it is guessable with
# enough tries, so delete the _redirects lines below if that matters to you.
set -euo pipefail
cd "$(dirname "$0")"

CONF=.cloudflare-site
if [ ! -f "$CONF" ]; then
  # First run: pick a project name and secret path once; reuse them forever after so the URL is stable.
  printf 'PROJECT=photowall-%s\nWALLPATH=%s\n' "$(openssl rand -hex 3)" "$(openssl rand -hex 16)" > "$CONF"
  chmod 600 "$CONF"
fi
# shellcheck disable=SC1090
source "$CONF"
if [ -z "${SHORT:-}" ]; then
  # 6 chars, lowercase, no look-alikes (0/o, 1/l/i). '|| true': tr dies of SIGPIPE when head closes the pipe.
  SHORT=$( (LC_ALL=C tr -dc 'abcdefghjkmnpqrstuvwxyz23456789' < /dev/urandom || true) | head -c 6)
  [ ${#SHORT} -eq 6 ] || { echo "Could not generate a short code" >&2; exit 1; }
  printf 'SHORT=%s\n' "$SHORT" >> "$CONF"
fi

[ -s site/album.js ] || { echo "site/album.js is missing: run tools/prepare-album.py first" >&2; exit 1; }

OUT=build/cloudflare
rm -rf "$OUT"; mkdir -p "$OUT/$WALLPATH"
# Everything in site/ (page, config.js, album.js, album/, music/, optional alignment.json and wall photo).
rsync -a --exclude '.*' site/ "$OUT/$WALLPATH/"

# Root and unknown paths: plain 404 (a top-level 404.html also stops Pages treating the site as an SPA).
printf '<!doctype html><meta charset="utf-8"><title>Not found</title><p>Not found.</p>\n' > "$OUT/404.html"
printf 'User-agent: *\nDisallow: /\n' > "$OUT/robots.txt"
# Short links (type these on the projector): /<code> the wall, /<code>a straight into Align,
# /<code>d diagnostics overlay, /<code>f frame rate, /<code>k key log, /<code>r resolution test,
# /<code>v Kolam only (no photos), /<code>x full mode (all scenes, fades).
{
  printf '/%s /%s/#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sa /%s/#align 302\n' "$SHORT" "$WALLPATH"
  printf '/%sd /%s/?diag=1#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sf /%s/?fps=1#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sk /%s/?keys=1#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sr /%s/?res=1#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sv /%s/?vector=1#play 302\n' "$SHORT" "$WALLPATH"
  printf '/%sx /%s/?anim=1#play 302\n' "$SHORT" "$WALLPATH"
} > "$OUT/_redirects"

# Inline script/style; scripts only from cdnjs/jsdelivr/unpkg; fonts from Google Fonts; photos are blobs.
cat > "$OUT/_headers" <<'EOF'
/*
  X-Robots-Tag: noindex, nofollow, noarchive, noimageindex
  Referrer-Policy: no-referrer
  X-Content-Type-Options: nosniff
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; media-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'
/*/alignment.json
  Cache-Control: no-store
/*/config.js
  Cache-Control: no-cache
/*/album.js
  Cache-Control: no-cache
EOF

echo "Upload folder: $OUT ($(du -sh "$OUT" | cut -f1))"
[ "${1:-}" = "--dry-run" ] && exit 0

WR="npx -y wrangler@4.158.0"
$WR whoami >/dev/null 2>&1 || $WR login
# --force (create only): wrangler 4.15x otherwise hands new projects to "Pages on Workers", whose
# auto-detection fails on this folder layout. Classic Pages honours _headers, _redirects and 404.html.
$WR pages project list 2>/dev/null | grep -q "$PROJECT" || $WR pages project create "$PROJECT" --production-branch main --force
$WR pages deploy "$OUT" --project-name "$PROJECT" --branch main --commit-dirty=true

echo
echo "Short link (type on the projector): $PROJECT.pages.dev/$SHORT    (align: $PROJECT.pages.dev/${SHORT}a)"
echo "Wall (kiosk start URL):             https://$PROJECT.pages.dev/$WALLPATH/#play"
echo "Desktop editor (mock-up, Align):    https://$PROJECT.pages.dev/$WALLPATH/"
