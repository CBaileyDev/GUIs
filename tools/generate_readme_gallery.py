#!/usr/bin/env python3
"""Emit markdown gallery tables for README.md from preview.png files."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STYLES = [
    ("aqua", "Aqua", "Glossy early-OSX pinstripe and lozenge buttons"),
    ("art-deco", "Art Deco", "Gold accents and 1920s symmetry"),
    ("bauhaus", "Bauhaus", "Primary colors and geometric shapes"),
    ("brutalism", "Brutalism", "Hard borders, acid yellow, raw grid"),
    ("claymorphism", "Claymorphism", "Soft inflated pastel clay shapes"),
    ("comic", "Comic", "Halftone dots, bold outlines, KA-POW energy"),
    ("cyberpunk", "Cyberpunk", "Neon scanlines on a dark grid"),
    ("dracula", "Dracula", "Classic purple-and-cyan dev theme"),
    ("gameboy", "Game Boy", "Four-shade green LCD inside a plastic shell"),
    ("glassmorphism", "Glassmorphism", "Frosted glass over a vivid backdrop"),
    ("imgui-style", "Dear ImGui", "Flat immediate-mode dark UI (Python)"),
    ("ios", "iOS", "Grouped lists, switches, and phone chrome"),
    ("linear", "Linear", "Modern dark SaaS dashboard menu"),
    ("material", "Material 3", "Elevated cards and tonal color"),
    ("memphis", "Memphis", "1980s squiggles, confetti, pop colors"),
    ("minimalist", "Minimalist", "Typographic, hairline, near-bare"),
    ("monochrome", "Monochrome", "Pure black-and-white Swiss grid"),
    ("neumorphism", "Neumorphism", "Soft extruded shadows on light grey"),
    ("nord", "Nord", "Arctic north-bluish palette"),
    ("paper-sketch", "Paper Sketch", "Hand-drawn pencil-on-paper look"),
    ("retro-terminal", "Retro Terminal", "Green-phosphor CRT terminal"),
    ("skeuomorphic", "Skeuomorphic", "Leather, brass, and beveled buttons"),
    ("solarized", "Solarized", "Ethan Schoonover's precision light palette"),
    ("steampunk", "Steampunk", "Brass gears, parchment, Victorian chrome"),
    ("swiss", "Swiss", "International Style grid typography"),
    ("synthwave", "Synthwave", "Neon pink/cyan 80s sunset grid"),
    ("tron", "Tron", "Cyan glow grid and derezzed chrome"),
    ("vaporwave", "Vaporwave", "Pastel neon with Japanese serif accents"),
    ("win95", "Windows 95", "Classic Chicago-era window chrome"),
    ("y2k", "Y2K", "Chrome pills, gloss, and bubble glow"),
]

INTERNAL = [
    ("overlay-html", "Overlay Panel", "Fixed settings panel over a simulated scene"),
    ("game-hud", "Game HUD", "Full-screen HUD with stats, minimap, and panel"),
    ("command-palette", "Command Palette", "Searchable ⌘K-style command modal"),
    ("floating-toolbar", "Floating Toolbar", "Canvas toolbar with settings popover"),
    ("sidebar-drawer", "Sidebar Drawer", "Slide-in navigation drawer"),
    ("notification-stack", "Notification Stack", "Toast stack with trigger panel"),
]

EXTERNAL = [
    ("tkinter-menu", "Tkinter", "Standard ttk widgets on a dark palette"),
    ("pyqt-menu", "PyQt6", "Native Qt widgets with dark QSS theme"),
    ("customtkinter", "CustomTkinter", "Rounded modern tkinter widgets"),
    ("wxpython", "wxPython", "Native widgets via wxWidgets"),
]


def cell(folder: str, name: str, desc: str, section: str) -> str:
    rel = f"{section}/{folder}"
    return (
        f'<a href="{rel}/"><img src="{rel}/preview.png" alt="{name}" width="280" /></a><br />'
        f'<strong><a href="{rel}/">{name}</a></strong><br />'
        f"{desc}"
    )


def table(entries: list[tuple[str, str, str]], section: str, cols: int = 3) -> str:
    rows: list[str] = []
    for i in range(0, len(entries), cols):
        chunk = entries[i : i + cols]
        while len(chunk) < cols:
            chunk.append(("", "", ""))
        tds = "".join(
            f"<td align=\"center\" valign=\"top\" width=\"{100 // cols}%\">"
            + (cell(*item, section) if item[0] else "&nbsp;")
            + "</td>"
            for item in chunk
        )
        rows.append(f"<tr>{tds}</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main() -> None:
    print("### Visual styles (`styles/`)\n")
    print(table(STYLES, "styles"))
    print("\n### Overlay patterns (`internal/`)\n")
    print(table(INTERNAL, "internal", cols=2))
    print("\n### Desktop toolkits (`external/`)\n")
    print(table(EXTERNAL, "external", cols=2))


if __name__ == "__main__":
    main()
