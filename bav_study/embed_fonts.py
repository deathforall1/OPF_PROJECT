#!/usr/bin/env python3
"""Fetch a Google Fonts stylesheet and inline the latin faces as base64 data URIs.

Used to make a self-contained copy of a page before rendering it to PDF with a
headless browser, which otherwise prints in fallback fonts.
"""
import base64
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile
import time

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# only these subsets are worth embedding for an English document
KEEP = ("latin", "latin-ext")


CACHE = pathlib.Path(tempfile.gettempdir()) / "gf-cache"


def fetch(url: str) -> bytes:
    """Download with a small cache and a few retries; the proxy times out
    occasionally and a half-embedded stylesheet is worse than a slow build."""
    CACHE.mkdir(exist_ok=True)
    key = CACHE / hashlib.sha1(url.encode()).hexdigest()
    if key.exists():
        return key.read_bytes()
    last = None
    for attempt in range(4):
        out = subprocess.run(
            ["curl", "-sSL", "--connect-timeout", "20", "--max-time", "120",
             "-A", UA, url], capture_output=True)
        if out.returncode == 0 and out.stdout:
            key.write_bytes(out.stdout)
            return out.stdout
        last = out.returncode
        time.sleep(2 ** attempt)
    raise RuntimeError(f"could not fetch {url} (curl exit {last})")


def inline(css_url: str) -> str:
    css = fetch(css_url).decode("utf-8")
    blocks = []
    # each @font-face is preceded by a /* subset */ comment
    for m in re.finditer(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S):
        subset, block = m.group(1), m.group(2)
        if subset not in KEEP:
            continue
        url_m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not url_m:
            continue
        data = base64.b64encode(fetch(url_m.group(1))).decode("ascii")
        block = block.replace(url_m.group(1),
                              "data:font/woff2;base64," + data)
        blocks.append(block)
    return "\n".join(blocks)


if __name__ == "__main__":
    src, dst, css_url = sys.argv[1], sys.argv[2], sys.argv[3]
    html = open(src, encoding="utf-8").read()
    faces = inline(css_url)
    # drop the network <link>s and splice the embedded faces into the stylesheet
    html = re.sub(r'<link rel="(?:preconnect|stylesheet)"[^>]*>\s*', "", html)
    html = html.replace("<style>", "<style>\n" + faces + "\n", 1)
    # a bare fragment loaded via file:// is decoded as latin-1 without this
    html = '<meta charset="utf-8">\n' + html
    open(dst, "w", encoding="utf-8").write(html)
    print(f"{dst}: {len(faces):,} bytes of embedded font CSS, "
          f"{len(html):,} bytes total")
