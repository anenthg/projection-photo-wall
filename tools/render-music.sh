#!/bin/bash
# Re-render the show and Kolam music from the scores in site/index.html (SCORES) into site/music/*.m4a.
# Needs Node and macOS afconvert. First run installs the offline Web Audio renderer into tools/node_modules.
# ./render-music.sh renders every score; ./render-music.sh prism grid renders only those.
# After re-rendering, bump the ?v= on SCORES.*.file in index.html, then ./deploy-cloudflare.sh.
set -euo pipefail
cd "$(dirname "$0")"
[ -d node_modules/node-web-audio-api ] || npm install --no-audit --no-fund --no-save node-web-audio-api@1
WAV=../build/music-wav
rm -rf "$WAV"
node render-music.js ../site/index.html "$WAV" "$@"
mkdir -p ../site/music
for f in "$WAV"/*.wav; do
  k=$(basename "$f" .wav)
  afconvert -f m4af -d aac -b 160000 "$f" "../site/music/$k.m4a"
  echo "site/music/$k.m4a  $(afinfo "../site/music/$k.m4a" | sed -n 's/.*estimated duration: \([0-9.]*\).*/\1 s/p')"
done
