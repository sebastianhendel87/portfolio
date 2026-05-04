#!/bin/sh
set -e
cd "$(dirname "$0")"
# 8888 avoids fighting leftover `next dev` processes that often sit on 9999.
export PORT="${PORT:-8888}"
exec python3 serve.py
