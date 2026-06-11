#!/usr/bin/env python3
"""Render preview.png for every HTML template using Playwright."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
INTERNAL_VIEWPORT = {"width": 1200, "height": 780}
DEFAULT_VIEWPORT = {"width": 1200, "height": 800}


def discover_templates() -> list[tuple[str, Path]]:
    templates: list[tuple[str, Path]] = []
    for section in ("styles", "internal"):
        base = ROOT / section
        if not base.is_dir():
            continue
        for folder in sorted(base.iterdir()):
            html = folder / "index.html"
            if html.is_file():
                templates.append((section, html))
    return templates


def render(page, html: Path, section: str, out: Path) -> None:
    url = html.as_uri()
    page.goto(url, wait_until="networkidle", timeout=30_000)
    page.wait_for_timeout(400)

    if section == "internal":
        page.screenshot(path=str(out), full_page=False)
        return

    card = page.query_selector(".card, .window, .card-wrap, body > .container")
    box = card.bounding_box() if card else None
    if box:
        height = min(max(box["y"] + box["height"] + 40, 600), 1600)
        page.set_viewport_size({"width": 1200, "height": int(height)})
        page.goto(url, wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(400)

    page.screenshot(path=str(out), full_page=False)


def main() -> int:
    templates = discover_templates()
    if not templates:
        print("no templates found", file=sys.stderr)
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for section, html in templates:
                rel = html.relative_to(ROOT)
                out = html.parent / "preview.png"
                print(f"→ {rel}")
                context = browser.new_context(
                    viewport=INTERNAL_VIEWPORT if section == "internal" else DEFAULT_VIEWPORT,
                    device_scale_factor=1,
                )
                page = context.new_page()
                try:
                    render(page, html, section, out)
                except Exception as exc:
                    print(f"  FAILED: {exc}", file=sys.stderr)
                finally:
                    context.close()
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
