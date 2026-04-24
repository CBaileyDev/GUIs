#!/usr/bin/env python3
"""Draw preview.png placeholders for the Python-only templates.

These are mockups — a real screenshot would require running a display server
with the actual GUI toolkit. The generated image matches the app's typical
chrome (title bar, colors, typography) so the main README gallery stays
visually consistent.
"""

from __future__ import annotations

from pathlib import Path

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


def draw_chrome(d: ImageDraw.ImageDraw, title: str, bg: str, fg: str, dots_style: str = "mac") -> None:
    d.rectangle((0, 0, W, 32), fill=bg)
    if dots_style == "mac":
        for i, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
            d.ellipse((14 + i * 20, 10, 26 + i * 20, 22), fill=color)
    else:  # windows
        d.rectangle((W - 90, 0, W - 60, 32), fill=bg, outline=fg)
        d.rectangle((W - 60, 0, W - 30, 32), fill=bg, outline=fg)
        d.rectangle((W - 30, 0, W, 32), fill="#e81123")
    d.text((W / 2, 16), title, fill=fg, font=pick_font(12), anchor="mm")


def draw_slider(d, y: int, label: str, value: int, fg: str, track: str, thumb: str, font) -> None:
    d.text((32, y), label, fill=fg, font=font)
    tw = pick_font(12).getlength(f"{value}%")
    d.text((W - 32 - tw, y), f"{value}%", fill=thumb, font=pick_font(12))
    d.rounded_rectangle((32, y + 26, W - 32, y + 30), radius=2, fill=track)
    cx = 32 + (W - 64) * value / 100
    d.rounded_rectangle((32, y + 26, cx, y + 30), radius=2, fill=thumb)
    d.ellipse((cx - 8, y + 20, cx + 8, y + 36), fill=thumb, outline="white", width=2)


def draw_check(d, x: int, y: int, checked: bool, fg: str, accent: str, label: str, font) -> None:
    d.rounded_rectangle((x, y, x + 18, y + 18), radius=4, fill=accent if checked else "#222", outline=fg, width=1)
    if checked:
        d.line([(x + 4, y + 9), (x + 8, y + 13), (x + 14, y + 5)], fill="white", width=2)
    d.text((x + 30, y + 2), label, fill=fg, font=font)


def draw_btn(d, box, text, bg, fg, font, outline=None) -> None:
    d.rounded_rectangle(box, radius=8, fill=bg, outline=outline, width=1 if outline else 0)
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), text, fill=fg, font=font, anchor="mm")


def tkinter_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#ededed")
    d = ImageDraw.Draw(img)
    draw_chrome(d, "tkinter Menu", "#dcdcdc", "#222")
    d.rectangle((0, 32, W, H), fill="#ededed")
    d.text((32, 56), "tkinter Menu", fill="#111", font=pick_font(22, bold=True))
    d.text((32, 90), "Native Python Tk widgets", fill="#555", font=pick_font(13))
    d.line((32, 124, W - 32, 124), fill="#c4c4c4", width=1)
    draw_btn(d, (32, 150, 290, 192), "Apply", "#0078d7", "white", pick_font(14, bold=True))
    draw_btn(d, (310, 150, W - 32, 192), "Reset", "#f3f3f3", "#111", pick_font(14, bold=True), outline="#b8b8b8")
    draw_slider(d, 220, "Opacity", 72, "#222", "#c4c4c4", "#0078d7", pick_font(13))
    draw_check(d, 32, 290, True, "#222", "#0078d7", "Enable blur backdrop", pick_font(13))
    d.text((32, 330), "Theme preset", fill="#555", font=pick_font(12))
    d.rounded_rectangle((32, 352, W - 32, 390), radius=3, fill="white", outline="#b8b8b8", width=1)
    d.text((44, 370), "Aurora Violet", fill="#222", font=pick_font(13), anchor="lm")
    d.polygon([(W - 52, 364), (W - 40, 364), (W - 46, 372)], fill="#555")
    d.rounded_rectangle((32, 406, W - 32, 444), radius=3, fill="white", outline="#b8b8b8", width=1)
    d.text((44, 425), "Enter overlay title…", fill="#999", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((32, 470, W - 32, 510), radius=3, fill="#f6f6f6", outline="#d4d4d4", width=1)
    d.text((44, 490), "status — waiting for input", fill="#555", font=pick_mono(12), anchor="lm")
    img.save(out, "PNG", optimize=True)


def pyqt_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#1e1f29")
    d = ImageDraw.Draw(img)
    draw_chrome(d, "PyQt6 Menu", "#14151c", "#e8eaf2")
    d.rectangle((0, 32, W, H), fill="#1e1f29")
    d.text((32, 56), "PyQt6 Menu", fill="white", font=pick_font(22, bold=True))
    d.text((32, 90), "Native Qt widgets · dark theme", fill="#9098b0", font=pick_font(13))
    d.line((32, 124, W - 32, 124), fill="#2a2c3a", width=1)
    d.text((32, 140), "ACTIONS", fill="#8a95ff", font=pick_font(11, bold=True))
    draw_btn(d, (32, 162, 290, 204), "Apply", "#6c63ff", "white", pick_font(14, bold=True))
    draw_btn(d, (310, 162, W - 32, 204), "Reset", "#2a2c3a", "#e8eaf2", pick_font(14, bold=True), outline="#383b4c")
    draw_slider(d, 230, "Opacity", 72, "#c3c9db", "#2a2c3a", "#6c63ff", pick_font(13))
    draw_check(d, 32, 300, True, "#e8eaf2", "#6c63ff", "Enable blur backdrop", pick_font(13))
    d.text((32, 340), "Theme preset", fill="#c3c9db", font=pick_font(12))
    d.rounded_rectangle((32, 360, W - 32, 398), radius=6, fill="#15161d", outline="#2a2c3a", width=1)
    d.text((44, 379), "Aurora Violet", fill="#e8eaf2", font=pick_font(13), anchor="lm")
    d.polygon([(W - 52, 374), (W - 40, 374), (W - 46, 382)], fill="#9098b0")
    d.rounded_rectangle((32, 414, W - 32, 452), radius=6, fill="#15161d", outline="#2a2c3a", width=1)
    d.text((44, 433), "Enter overlay title…", fill="#5a5f72", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((32, 478, W - 32, 520), radius=6, fill="#15161d", outline="#2a2c3a", width=1)
    d.text((44, 498), "status — waiting for input", fill="#9098b0", font=pick_mono(12), anchor="lm")
    img.save(out, "PNG", optimize=True)


def customtkinter_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#0e1220")
    d = ImageDraw.Draw(img)
    draw_chrome(d, "CustomTkinter Menu", "#0a0e1a", "#e3e7f5")
    d.rectangle((0, 32, W, H), fill="#0e1220")
    d.rounded_rectangle((18, 50, W - 18, H - 18), radius=16, fill="#161b2e")
    d.text((40, 72), "CustomTkinter Menu", fill="white", font=pick_font(22, bold=True))
    d.text((40, 106), "Modern rounded tkinter widgets", fill="#8a93b3", font=pick_font(13))
    d.line((40, 140, W - 40, 140), fill="#252b45", width=1)
    d.text((40, 156), "ACTIONS", fill="#8a93b3", font=pick_font(11, bold=True))
    draw_btn(d, (40, 178, 290, 216), "Apply", "#5b6cff", "white", pick_font(14, bold=True))
    draw_btn(d, (310, 178, W - 40, 216), "Reset", "#252b45", "#e3e7f5", pick_font(14, bold=True), outline="#383f5c")
    draw_slider(d, 244, "Opacity", 72, "#c3c9db", "#252b45", "#5b6cff", pick_font(13))
    draw_check(d, 40, 314, False, "#e3e7f5", "#5b6cff", "Enable blur backdrop", pick_font(13))
    d.text((40, 350), "THEME PRESET", fill="#8a93b3", font=pick_font(11, bold=True))
    d.rounded_rectangle((40, 374, W - 40, 412), radius=8, fill="#0f1324", outline="#383f5c", width=1)
    d.text((52, 393), "Aurora Violet", fill="#e3e7f5", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((W - 80, 374, W - 40, 412), radius=8, fill="#5b6cff")
    d.polygon([(W - 68, 388), (W - 52, 388), (W - 60, 398)], fill="white")
    d.rounded_rectangle((40, 426, W - 40, 464), radius=8, fill="#0f1324", outline="#383f5c", width=1)
    d.text((52, 445), "Enter overlay title…", fill="#5a5f72", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((40, 488, W - 40, 530), radius=8, fill="#0b0f1e")
    d.text((52, 508), "status — waiting for input", fill="#8a93b3", font=pick_mono(12), anchor="lm")
    img.save(out, "PNG", optimize=True)


def wxpython_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#f5f5f8")
    d = ImageDraw.Draw(img)
    draw_chrome(d, "wxPython Menu", "#e9e9ed", "#222")
    d.rectangle((0, 32, W, H), fill="#f5f5f8")
    d.text((32, 56), "wxPython Menu", fill="#141e", font=pick_font(22, bold=True))
    d.text((32, 90), "Native widgets via wxWidgets on your OS", fill="#6e7382", font=pick_font(13))
    d.line((32, 124, W - 32, 124), fill="#cacad2", width=1)
    d.text((32, 140), "ACTIONS", fill="#6e7382", font=pick_font(11, bold=True))
    draw_btn(d, (32, 162, 290, 200), "Apply", "#5865f2", "white", pick_font(14, bold=True))
    draw_btn(d, (310, 162, W - 32, 200), "Reset", "white", "#333", pick_font(14, bold=True), outline="#c5c7cc")
    draw_slider(d, 226, "Opacity — 72%", 72, "#3c4150", "#d1d3da", "#5865f2", pick_font(13))
    draw_check(d, 32, 296, True, "#333", "#5865f2", "Enable blur backdrop", pick_font(13))
    d.text((32, 336), "Theme preset", fill="#3c4150", font=pick_font(12))
    d.rounded_rectangle((32, 356, W - 32, 394), radius=4, fill="white", outline="#c5c7cc", width=1)
    d.text((44, 375), "Aurora Violet", fill="#222", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((32, 410, W - 32, 448), radius=4, fill="white", outline="#c5c7cc", width=1)
    d.text((44, 429), "Enter overlay title…", fill="#888", font=pick_font(13), anchor="lm")
    d.rounded_rectangle((32, 472, W - 32, 514), radius=4, fill="#f0f0f4", outline="#d9d9de", width=1)
    d.text((44, 493), "status — waiting for input", fill="#6e7382", font=pick_mono(12), anchor="lm")
    img.save(out, "PNG", optimize=True)


def imgui_mock(out: Path) -> None:
    img = Image.new("RGB", (W, H), "#1d1d26")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 30), fill="#232330")
    d.text((14, 15), "Dear PyGui · ImGui Menu", fill="#dcdce0", font=pick_font(12), anchor="lm")
    d.rectangle((0, 30, W, H), fill="#1d1d26")
    d.text((22, 50), "Dear PyGui Menu", fill="white", font=pick_font(22, bold=True))
    d.text((22, 82), "Flat immediate-mode dark ImGui aesthetic", fill="#9090a0", font=pick_font(12))
    d.line((22, 112, W - 22, 112), fill="#333344", width=1)
    d.text((22, 124), "ACTIONS", fill="#e7b53c", font=pick_mono(10))
    draw_btn(d, (22, 144, 285, 178), "Apply", "#4a8cf0", "white", pick_font(13, bold=True))
    draw_btn(d, (300, 144, W - 22, 178), "Reset", "#3a3a4a", "#dcdce0", pick_font(13, bold=True))
    d.text((22, 200), f"Opacity", fill="#dcdce0", font=pick_font(12))
    d.text((W - 22, 200), "72%", fill="#e7b53c", font=pick_mono(12), anchor="rt")
    d.rectangle((22, 222, W - 22, 238), fill="#0f0f18", outline="#333344", width=1)
    d.rectangle((22, 222, 22 + (W - 44) * 0.72, 238), fill="#4a8cf0")
    d.rectangle((22, 258, W - 22, 282), fill="#2a2a36")
    d.rectangle((22, 258, 40, 282), fill="#4a8cf0")
    d.line([(27, 270), (32, 275), (36, 264)], fill="white", width=2)
    d.text((52, 270), "Enable blur backdrop", fill="#dcdce0", font=pick_font(12), anchor="lm")
    d.text((22, 302), "Theme preset", fill="#dcdce0", font=pick_font(12))
    d.rectangle((22, 322, W - 22, 346), fill="#0f0f18", outline="#333344", width=1)
    d.text((34, 334), "Aurora Violet", fill="#dcdce0", font=pick_font(12), anchor="lm")
    d.polygon([(W - 42, 330), (W - 30, 330), (W - 36, 340)], fill="#9090a0")
    d.rectangle((22, 364, W - 22, 388), fill="#0f0f18", outline="#333344", width=1)
    d.text((34, 376), "Enter overlay title…", fill="#60606c", font=pick_font(12), anchor="lm")
    d.rectangle((22, 410, W - 22, 446), fill="#0f0f18", outline="#333344", width=1)
    d.text((34, 428), "status — waiting for input", fill="#9090a0", font=pick_mono(11), anchor="lm")
    img.save(out, "PNG", optimize=True)


TARGETS = {
    "external/tkinter-menu": tkinter_mock,
    "external/pyqt-menu": pyqt_mock,
    "external/customtkinter": customtkinter_mock,
    "external/wxpython": wxpython_mock,
    "styles/imgui-style": imgui_mock,
}


def main() -> int:
    for rel, fn in TARGETS.items():
        folder = ROOT / rel
        folder.mkdir(exist_ok=True)
        out = folder / "preview.png"
        print(f"→ {rel}/preview.png")
        fn(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
