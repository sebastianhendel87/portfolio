#!/usr/bin/env python3
"""Serve the repo root for local preview.

Uses ThreadingHTTPServer so many concurrent requests (video range seeks, images) do not
block each other. A single-thread server queues everything: leaving a video-heavy page
can look like navigation is broken.

HTML is sent with no-cache so edits show on refresh. Images, fonts, and video use a
short max-age so navigating between pages does not re-download large files every time
(unlike no-store on everything, which makes the site feel very slow).
"""
from __future__ import annotations

import errno
import http.server
import os
import posixpath
import sys
import urllib.parse

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FIRST_PORT = 8877
PORT_TRIES = 30

# Your five Dune clips live here on this Mac (not in Google Drive / not in the repo).
DUNE_CLIPS_DIR = os.path.expanduser(
    "~/Documents/Portfolio/SH Website - Cursor/Dune"
)

_DUNE_CLIP_NAMES = frozenset(
    {
        "dune-01.mp4",
        "dune-02.mp4",
        "dune-03.mp4",
        "dune-04.mov",
        "dune-05.mov",
    }
)

# Tonscan assets live here on this Mac (not in Google Drive / not in the repo).
# We search both the base folder and the "Tonscan hero" subfolder so you can keep
# your original file organization.
_TONSCAN_ASSET_DIRS = (
    os.path.expanduser("~/Documents/Portfolio/Tonscan/Tonscan hero"),
    os.path.expanduser("~/Documents/Portfolio/Tonscan"),
)


class DevHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".mov": "video/quicktime",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        path = self.path.split("?", 1)[0].lower()
        is_html = path.endswith(".html") or path in ("/", "")
        if is_html:
            self.send_header("Cache-Control", "no-cache, must-revalidate")
        else:
            # Dev-only: reuse images/fonts/video for a few minutes between navigations.
            self.send_header("Cache-Control", "public, max-age=300")
        super().end_headers()

    def translate_path(self, path: str) -> str:
        path = path.split("?", 1)[0].split("#", 1)[0]
        path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        parts = [p for p in path.split("/") if p]
        if len(parts) == 2 and parts[0] == "dune" and parts[1] in _DUNE_CLIP_NAMES:
            alt = os.path.join(DUNE_CLIPS_DIR, parts[1])
            if os.path.isfile(alt):
                return os.path.abspath(alt)
        if len(parts) == 2 and parts[0] == "tonscan":
            requested = parts[1]
            for base in _TONSCAN_ASSET_DIRS:
                alt = os.path.join(base, requested)
                if os.path.isfile(alt):
                    return os.path.abspath(alt)
        return super().translate_path(path)


class DevThreadingHTTPServer(http.server.ThreadingHTTPServer):
    """Same as ThreadingHTTPServer but SO_REUSEADDR so restarts are painless."""

    allow_reuse_address = True


if __name__ == "__main__":
    start = int(os.environ.get("PORT", str(DEFAULT_FIRST_PORT)))
    httpd = None
    port_used = None
    for port in range(start, start + PORT_TRIES):
        try:
            httpd = DevThreadingHTTPServer(("", port), DevHandler)
            port_used = port
            break
        except OSError as e:
            if e.errno != errno.EADDRINUSE:
                raise
    if httpd is None:
        print(
            f"Could not use ports {start}-{start + PORT_TRIES - 1} (all busy).",
            file=sys.stderr,
        )
        print("Quit the other preview, or run: PORT=9000 python3 serve.py", file=sys.stderr)
        sys.exit(1)

    port_file = os.path.join(DIRECTORY, ".preview-port.txt")
    try:
        with open(port_file, "w", encoding="utf-8") as f:
            f.write(str(port_used))
    except OSError:
        pass

    with httpd:
        print("")
        print("  Dune clips (1–5) load from:")
        print(f"    {DUNE_CLIPS_DIR}")
        print("")
        print("  Open in Chrome (use this exact port):")
        print(f"    http://localhost:{port_used}/")
        print(f"    http://localhost:{port_used}/dune.html")
        print("")
        print(f"  (Puerto guardado en: {port_file})")
        print("")
        print(f"  Site root: {DIRECTORY}")
        print("  Stop: Ctrl+C")
        print("")
        httpd.serve_forever()
