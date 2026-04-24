#!/usr/bin/env python3
"""
Injects a modernization CSS block into each styles/*/index.html.

The block is placed just before the closing </style> tag of the first style
block, so it cascades after the original rules. Each style gets tokens and
polish that match its theme (dark/light, accent color, color-scheme).

Re-runnable: the block is wrapped in /* @@MODERNIZED-v1 @@ */ markers so
subsequent runs replace the existing injection rather than duplicating it.
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "styles"

START = "/* @@MODERNIZED-v1-start @@ */"
END = "/* @@MODERNIZED-v1-end @@ */"

# Per-style modernization profile.
# accent   — focus ring + accent-color
# scheme   — light | dark | light dark
# bg_tint  — optional subtle conic/radial overlay for visual depth
# hero     — additional CSS to layer on top for per-theme polish
PROFILES: dict[str, dict] = {
    "aqua": {
        "accent": "#0a84ff", "scheme": "light",
        "hero": """
            html { color-scheme: light; }
            body { background:
                radial-gradient(1000px 500px at 50% -10%, rgba(150,200,255,0.55), transparent 60%),
                linear-gradient(180deg, #eaf3ff 0%, #cfe1f5 100%) !important; }
            .card { border-radius: 18px !important;
                box-shadow: 0 30px 60px -20px rgba(8,40,80,0.35),
                            0 2px 0 rgba(255,255,255,0.8) inset,
                            0 0 0 1px rgba(40,80,140,0.08) !important; }
        """,
    },
    "art-deco": {
        "accent": "#d4a944", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(800px 500px at 50% 0%, rgba(212,169,68,0.18), transparent 65%),
                linear-gradient(180deg, #14110b 0%, #0a0806 100%) !important; }
            .card { border-radius: 4px !important; }
        """,
    },
    "bauhaus": {
        "accent": "#1e88e5", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(600px 400px at 85% 15%, rgba(253,216,53,0.35), transparent 60%),
                radial-gradient(700px 500px at 10% 90%, rgba(30,136,229,0.18), transparent 60%),
                #f2ecdc !important; }
        """,
    },
    "brutalism": {
        "accent": "#0000ff", "scheme": "light",
        "hero": """
            body { background-image:
                linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px) !important;
                background-size: 24px 24px, 24px 24px !important;
                background-color: #ffff33 !important; }
        """,
    },
    "claymorphism": {
        "accent": "#8a5cf5", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(900px 600px at 20% 10%, #e5e2ff 0%, transparent 60%),
                radial-gradient(700px 500px at 90% 90%, #ffd6ee 0%, transparent 55%),
                linear-gradient(135deg, #f1ecff 0%, #fde8f3 100%) !important; }
        """,
    },
    "comic": {"accent": "#1d7bff", "scheme": "light", "hero": ""},
    "cyberpunk": {
        "accent": "#ff00ff", "scheme": "dark",
        "hero": """
            body::after { content: ''; position: fixed; inset: 0;
                background: radial-gradient(1000px 500px at 50% 0%, rgba(255,0,255,0.12), transparent 60%);
                pointer-events: none; z-index: 0; }
        """,
    },
    "dracula": {
        "accent": "#bd93f9", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 20% 0%, rgba(189,147,249,0.12), transparent 60%),
                radial-gradient(700px 400px at 100% 100%, rgba(139,233,253,0.08), transparent 60%),
                #282a36 !important; }
        """,
    },
    "gameboy": {"accent": "#0f380f", "scheme": "light", "hero": ""},
    "glassmorphism": {
        "accent": "#a78bfa", "scheme": "dark",
        "hero": """
            body { background:
                conic-gradient(from 180deg at 30% 30%, #7b2ff7 0deg, #00c6fb 140deg, #f857a6 260deg, #7b2ff7 360deg) !important;
                background-attachment: fixed !important; }
            body::before { width: 520px !important; height: 520px !important; filter: blur(110px) !important; opacity: 0.45 !important; }
            body::after  { width: 480px !important; height: 480px !important; filter: blur(110px) !important; opacity: 0.45 !important; }
            .card { border-radius: 28px !important; }
        """,
    },
    "ios": {
        "accent": "#007aff", "scheme": "light",
        "hero": """
            body { background: linear-gradient(180deg, #f2f2f7 0%, #e8eaf0 100%) !important; }
        """,
    },
    "linear": {
        "accent": "#7885ff", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(1200px 600px at 50% -200px, rgba(94,106,210,0.35), transparent 60%),
                radial-gradient(700px 500px at 100% 100%, rgba(120,133,255,0.10), transparent 60%),
                #08090a !important; }
            .card { border-radius: 16px !important; }
        """,
    },
    "material": {
        "accent": "#6750a4", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(900px 600px at 20% 0%, rgba(103,80,164,0.08), transparent 60%),
                var(--md-surface, #fef7ff) !important; }
        """,
    },
    "memphis": {"accent": "#ff2fa0", "scheme": "light", "hero": ""},
    "minimalist": {
        "accent": "#111", "scheme": "light",
        "hero": """
            body { background: #fafafa !important; }
            .card { box-shadow: 0 1px 0 rgba(0,0,0,0.04), 0 40px 80px -60px rgba(0,0,0,0.12) !important; }
            h1 { letter-spacing: -0.9px !important; }
        """,
    },
    "monochrome": {"accent": "#000", "scheme": "light", "hero": ""},
    "neumorphism": {
        "accent": "#6c63ff", "scheme": "light",
        "hero": """
            body { background: linear-gradient(145deg, #eef1f6 0%, #e3e8ee 100%) !important; }
        """,
    },
    "nord": {
        "accent": "#88c0d0", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 50% 0%, rgba(136,192,208,0.10), transparent 60%),
                #2e3440 !important; }
        """,
    },
    "paper-sketch": {"accent": "#5a3c2e", "scheme": "light", "hero": ""},
    "retro-terminal": {
        "accent": "#33ff66", "scheme": "dark",
        "hero": """
            body::before { content:''; position: fixed; inset:0; pointer-events:none; z-index: 1;
                background: repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0 1px, transparent 1px 3px); }
            body::after { content:''; position: fixed; inset:0; pointer-events:none; z-index:1;
                box-shadow: inset 0 0 180px rgba(0,0,0,0.85); }
        """,
    },
    "skeuomorphic": {
        "accent": "#b07a3a", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 50% 0%, rgba(200,160,100,0.18), transparent 60%),
                linear-gradient(180deg, #3a2817 0%, #241509 100%) !important; }
        """,
    },
    "solarized": {
        "accent": "#268bd2", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 10% 0%, rgba(38,139,210,0.10), transparent 60%),
                #fdf6e3 !important; }
        """,
    },
    "steampunk": {
        "accent": "#c9962a", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(800px 500px at 50% 0%, rgba(201,150,42,0.20), transparent 60%),
                linear-gradient(180deg, #2a1c0e 0%, #181008 100%) !important; }
        """,
    },
    "swiss": {"accent": "#d7261e", "scheme": "light", "hero": ""},
    "synthwave": {
        "accent": "#ff2bd0", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 50% 0%, rgba(255,43,208,0.18), transparent 60%),
                radial-gradient(800px 500px at 100% 100%, rgba(0,234,255,0.12), transparent 60%),
                #0a0320 !important; }
        """,
    },
    "tron": {
        "accent": "#4fd1ff", "scheme": "dark",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 50% 0%, rgba(79,209,255,0.18), transparent 60%),
                #000814 !important; }
        """,
    },
    "vaporwave": {"accent": "#ff77c8", "scheme": "dark", "hero": ""},
    "win95": {"accent": "#0a246a", "scheme": "light", "hero": ""},
    "y2k": {
        "accent": "#2e8bff", "scheme": "light",
        "hero": """
            body { background:
                radial-gradient(900px 500px at 20% 0%, rgba(46,139,255,0.18), transparent 60%),
                radial-gradient(700px 500px at 90% 100%, rgba(255,124,223,0.16), transparent 60%),
                linear-gradient(180deg, #e8edf7 0%, #c8d2e6 100%) !important; }
        """,
    },
}


def build_block(name: str, profile: dict) -> str:
    accent = profile.get("accent", "currentColor")
    scheme = profile.get("scheme", "light dark")
    hero = (profile.get("hero") or "").strip()
    return f"""
{START}
html {{ color-scheme: {scheme}; }}
body {{
    min-height: 100dvh;
    accent-color: {accent};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    font-synthesis: none;
}}
:focus-visible {{
    outline: 2px solid {accent};
    outline-offset: 2px;
    border-radius: 6px;
}}
a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible,
textarea:focus-visible, [role="switch"]:focus-visible, [tabindex]:focus-visible {{
    outline: 2px solid {accent};
    outline-offset: 2px;
}}
::selection {{ background: color-mix(in srgb, {accent} 30%, transparent); color: inherit; }}
img {{ image-rendering: auto; }}
html {{ scroll-behavior: smooth; }}
@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
        scroll-behavior: auto !important;
    }}
}}
{hero}
{END}
""".strip() + "\n"


def apply(path: Path) -> bool:
    name = path.parent.name
    profile = PROFILES.get(name)
    if profile is None:
        return False
    text = path.read_text(encoding="utf-8")
    block = build_block(name, profile)

    # Remove any previous injection with the same marker.
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
    text = pattern.sub("", text)

    # Inject just before the FIRST </style>.
    idx = text.find("</style>")
    if idx < 0:
        return False
    new_text = text[:idx] + "\n" + block + text[idx:]
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for folder in sorted(STYLES.iterdir()):
        html = folder / "index.html"
        if not html.exists():
            continue
        if apply(html):
            changed.append(folder.name)
    print(f"Updated {len(changed)} files:")
    for c in changed:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
