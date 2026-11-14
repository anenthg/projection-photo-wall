#!/bin/bash
# Preview the wall on this computer: http://localhost:8000/ (desktop editor) or http://localhost:8000/#play
# Other devices on the same Wi-Fi (e.g. the projector) can open http://<this computer's IP>:8000/#play.
cd "$(dirname "$0")/site" && exec python3 -m http.server "${1:-8000}"
