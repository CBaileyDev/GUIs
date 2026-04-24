#!/usr/bin/env python3
"""Render a preview.png for every HTML template using wkhtmltoimage + Pillow.

`internal/*` templates use full-viewport overlays with `overflow: hidden`, so
they have no natural body height. For those we force a viewport height.
Everything else renders at its natural height and gets cropped to MAX_HEIGHT.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
WIDTH = 600
MAX_HEIGHT = 800
VIEWPORT_HEIGHT = 780


def render(html: Path) -> None:
    out = html.parent / "preview.png"
    rel = html.relative_to(ROOT)
    print(f"→ {rel}")

    cmd = [
        "wkhtmltoimage",
        "--quality", "85",
        "--width", str(WIDTH),
        "--enable-local-file-access",
        "--quiet",
    ]
    if rel.parts[0] == "internal":
        cmd += ["--height", str(VIEWPORT_HEIGHT)]
    cmd += [str(html), str(out)]

    subprocess.run(cmd, check=True)

    with Image.open(out) as img:
        img = img.convert("RGB")
        if img.height > MAX_HEIGHT:
            img = img.crop((0, 0, img.width, MAX_HEIGHT))
        img.save(out, "PNG", optimize=True)


def main() -> int:
    templates = [
        f / "index.html"
        for section in ("styles", "internal", "external")
        for f in sorted((ROOT / section).iterdir())
        if (f / "index.html").exists()
    ]
    if not templates:
        print("no templates found", file=sys.stderr)
        return 1
    for html in templates:
        try:
            render(html)
        except subprocess.CalledProcessError as exc:
            print(f"  FAILED: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
