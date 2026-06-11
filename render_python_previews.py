#!/usr/bin/env python3
"""Draw preview.png placeholders for Python-only templates."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 600, 640


def pick_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def pick_mono(size: int) -> ImageFont.ImageFont:
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_chrome(d: ImageDraw.ImageDraw, title: str, bg: str, fg: str) -> None:
    d.rectangle((0, 0, W, 32), fill=bg)
    for i, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse((14 + i * 20, 10, 26 + i * 20, 22), fill=color)
    d.text((W / 2, 16), title, fill=fg, font=pick_font(12), anchor="mm")


def draw_menu_mock(
    out: Path,
    *,
    title: str,
    subtitle: str,
    chrome_bg: str,
    chrome_fg: str,
    body_bg: str,
    card_bg: str | None,
    title_fg: str,
    sub_fg: str,
    line_fg: str,
    primary_bg: str,
    secondary_bg: str,
    secondary_fg: str,
    secondary_outline: str | None,
    label_fg: str,
    accent: str,
    field_bg: str,
    field_outline: str,
    field_fg: str,
    placeholder: str,
    combo_value: str,
    check_label: str,
    check_on: bool,
    status_fg: str,
    status_text: str = "Ready",
    card_inset: int = 0,
) -> None:
    img = Image.new("RGB", (W, H), body_bg)
    d = ImageDraw.Draw(img)
    draw_chrome(d, title, chrome_bg, chrome_fg)

    top = 32 + card_inset
    left = 18 + card_inset
    right = W - 18 - card_inset
    if card_bg:
        d.rounded_rectangle((18, 50, W - 18, H - 18), radius=16, fill=card_bg)

    x = left + 14
    d.text((x, top + 24), title, fill=title_fg, font=pick_font(22, bold=True))
    d.text((x, top + 58), subtitle, fill=sub_fg, font=pick_font(13))
    d.line((x, top + 92, right - 14, top + 92), fill=line_fg, width=1)

    y = top + 118
    d.text((x, y), "Actions", fill=sub_fg, font=pick_font(11, bold=True))
    draw_btn = lambda box, text, bg, fg, outline=None: (
        d.rounded_rectangle(box, radius=8, fill=bg, outline=outline, width=1 if outline else 0),
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), text, fill=fg, font=pick_font(14, bold=True), anchor="mm"),
    )
    draw_btn((x, y + 22, x + 250, y + 64), "Apply", primary_bg, "white")
    draw_btn((x + 268, y + 22, right - 14, y + 64), "Reset", secondary_bg, secondary_fg, secondary_outline)

    y += 100
    d.text((x, y), "Opacity", fill=label_fg, font=pick_font(13))
    d.text((right - 14, y), "72%", fill=accent, font=pick_font(12), anchor="rt")
    d.rounded_rectangle((x, y + 26, right - 14, y + 30), radius=2, fill=line_fg)
    cx = x + (right - 14 - x) * 0.72
    d.rounded_rectangle((x, y + 26, cx, y + 30), radius=2, fill=accent)
    d.ellipse((cx - 8, y + 20, cx + 8, y + 36), fill=accent, outline="white", width=2)

    y += 70
    d.rounded_rectangle((x, y, x + 18, y + 18), radius=4,
                        fill=accent if check_on else field_bg, outline=label_fg, width=1)
    if check_on:
        d.line([(x + 4, y + 9), (x + 8, y + 13), (x + 14, y + 5)], fill="white", width=2)
    d.text((x + 30, y + 2), check_label, fill=label_fg, font=pick_font(13))

    y += 40
    d.text((x, y), "Theme" if "ImGui" not in title else "Style", fill=label_fg, font=pick_font(12))
    d.rounded_rectangle((x, y + 22, right - 14, y + 60), radius=6, fill=field_bg, outline=field_outline, width=1)
    d.text((x + 12, y + 41), combo_value, fill=field_fg, font=pick_font(13), anchor="lm")

    y += 80
    d.rounded_rectangle((x, y, right - 14, y + 38), radius=6, fill=field_bg, outline=field_outline, width=1)
    d.text((x + 12, y + 19), placeholder, fill=sub_fg, font=pick_font(13), anchor="lm")

    y += 56
    d.rounded_rectangle((x, y, right - 14, y + 40), radius=6, fill=field_bg if not card_bg else "#0b0f1e")
    d.text((x + 12, y + 20), status_text, fill=status_fg, font=pick_mono(12), anchor="lm")

    img.save(out, "PNG", optimize=True)


def imgui_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#1d1d26")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 30), fill="#232330")
    d.text((14, 15), "Dear ImGui Style", fill="#dcdce0", font=pick_font(12), anchor="lm")
    d.rectangle((0, 30, W, H), fill="#1d1d26")
    d.text((22, 50), "Dear ImGui aesthetic", fill="#9090a0", font=pick_font(12))
    d.line((22, 72, W - 22, 72), fill="#333344", width=1)
    d.rounded_rectangle((22, 88, 285, 122), radius=3, fill="#4a8cf0")
    d.text((153, 105), "Apply", fill="white", font=pick_font(13, bold=True), anchor="mm")
    d.rounded_rectangle((300, 88, W - 22, 122), radius=3, fill="#3a3a4a")
    d.text((361, 105), "Reset", fill="#dcdce0", font=pick_font(13, bold=True), anchor="mm")
    d.text((22, 144), "Opacity", fill="#dcdce0", font=pick_font(12))
    d.text((W - 22, 144), "50%", fill="#4a8cf0", font=pick_mono(12), anchor="rt")
    d.rectangle((22, 166, W - 22, 182), fill="#0f0f18", outline="#333344", width=1)
    d.rectangle((22, 166, 22 + (W - 44) * 0.5, 182), fill="#4a8cf0")
    d.text((22, 200), "Show toolbar", fill="#dcdce0", font=pick_font(12))
    d.text((22, 232), "Theme", fill="#dcdce0", font=pick_font(12))
    d.rectangle((22, 252, W - 22, 276), fill="#0f0f18", outline="#333344", width=1)
    d.text((34, 264), "Dark", fill="#dcdce0", font=pick_font(12), anchor="lm")
    d.rectangle((22, 294, W - 22, 318), fill="#0f0f18", outline="#333344", width=1)
    d.text((34, 306), "Window title…", fill="#60606c", font=pick_font(12), anchor="lm")
    d.text((22, 340), "Ready", fill="#9090a0", font=pick_mono(11))
    img.save(out, "PNG", optimize=True)


THEMES: dict[str, Callable[[Path], None]] = {
    "external/tkinter-menu": lambda out: draw_menu_mock(
        out, title="Tkinter Menu", subtitle="Standard ttk widgets on a dark palette",
        chrome_bg="#dcdcdc", chrome_fg="#222", body_bg="#1e1e2e", card_bg=None,
        title_fg="#89b4fa", sub_fg="#6c7086", line_fg="#313244",
        primary_bg="#89b4fa", secondary_bg="#2a2a3e", secondary_fg="#cdd6f4", secondary_outline=None,
        label_fg="#cdd6f4", accent="#89b4fa", field_bg="#2a2a3e", field_outline="#313244",
        field_fg="#cdd6f4", placeholder="Config key…", combo_value="Catppuccin Mocha",
        check_label="Bold headers", check_on=False, status_fg="#6c7086",
    ),
    "external/pyqt-menu": lambda out: draw_menu_mock(
        out, title="PyQt6 Menu", subtitle="Native Qt widgets · dark theme",
        chrome_bg="#14151c", chrome_fg="#e8eaf2", body_bg="#1e1f29", card_bg=None,
        title_fg="#ffffff", sub_fg="#9098b0", line_fg="#2a2c3a",
        primary_bg="#6c63ff", secondary_bg="#2a2c3a", secondary_fg="#e8eaf2", secondary_outline="#383b4c",
        label_fg="#c3c9db", accent="#8a95ff", field_bg="#15161d", field_outline="#2a2c3a",
        field_fg="#e8eaf2", placeholder="Window title…", combo_value="Fusion",
        check_label="Show toolbar", check_on=False, status_fg="#9098b0",
    ),
    "external/customtkinter": lambda out: draw_menu_mock(
        out, title="CustomTkinter Menu", subtitle="Rounded widgets on a dark card",
        chrome_bg="#0a0e1a", chrome_fg="#e3e7f5", body_bg="#0e1220", card_bg="#161b2e",
        title_fg="#ffffff", sub_fg="#8a93b3", line_fg="#252b45",
        primary_bg="#5b6cff", secondary_bg="#252b45", secondary_fg="#e3e7f5", secondary_outline="#383f5c",
        label_fg="#c3c9db", accent="#5b6cff", field_bg="#0f1324", field_outline="#383f5c",
        field_fg="#e3e7f5", placeholder="Profile name…", combo_value="Dark",
        check_label="High DPI scaling", check_on=False, status_fg="#8a93b3", card_inset=18,
    ),
    "external/wxpython": lambda out: draw_menu_mock(
        out, title="wxPython Menu", subtitle="Native widgets via wxWidgets",
        chrome_bg="#e9e9ed", chrome_fg="#222", body_bg="#f5f5f8", card_bg=None,
        title_fg="#14141a", sub_fg="#6e7382", line_fg="#cacad2",
        primary_bg="#5865f2", secondary_bg="#ffffff", secondary_fg="#333333", secondary_outline="#c5c7cc",
        label_fg="#3c4150", accent="#5865f2", field_bg="#ffffff", field_outline="#c5c7cc",
        field_fg="#222222", placeholder="Profile name…", combo_value="System",
        check_label="Remember window size", check_on=False, status_fg="#6e7382",
    ),
    "styles/imgui-style": imgui_mock,
}


def main() -> int:
    for rel, fn in THEMES.items():
        folder = ROOT / rel
        folder.mkdir(exist_ok=True)
        out = folder / "preview.png"
        print(f"→ {rel}/preview.png")
        fn(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
