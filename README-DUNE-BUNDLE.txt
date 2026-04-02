DUNE LAYOUT BUNDLE
==================

What’s inside
-------------
- dune.html              — main case study (use this as the “live” version)
- dune-v2.html, dune-v3.html, dune-v4.html — alternate layouts
- dune-layout-archive.html — index with links to all of the above
- serve.py / serve.sh — local preview server (serves this folder)
- dune/ — hero video, stills, and any clips stored in the repo
- favicon.svg

How to preview
--------------
1. Unzip this folder anywhere on your Mac.
2. Open Terminal, go into the unzipped folder:
     cd path/to/this/folder
3. Run:
     python3 serve.py
4. In Chrome open the URL shown (e.g. http://localhost:8877/dune.html).

Five motion clips (dune-01 … dune-05)
--------------------------------------
serve.py loads these from:
  Documents / Portfolio / SH Website - Cursor / Dune
on your Mac, with the filenames expected by the HTML (see serve.py).

If you move the bundle to another computer, copy those five files into that
folder or adjust serve.py to match your paths.

Fonts
-----
If headings look wrong, copy the Monument Grotesk .woff2 files from your full
portfolio project into a fonts/ folder next to these HTML files (same paths as
in the main site).
