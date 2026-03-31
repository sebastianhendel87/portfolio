#!/bin/sh
# Always serve THIS folder (the repo root), no matter where you run the script from.
set -e
cd "$(dirname "$0")"
echo "→ Serving: $(pwd)"
echo "→ Open:   http://localhost:8877/"
echo "→ Stop:   Ctrl+C"
exec python3 -m http.server 8877
