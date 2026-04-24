# pip install dearpygui
import dearpygui.dearpygui as dpg

STATUS = ["waiting for input"]


def log(msg):
    STATUS[0] = msg
    dpg.set_value("output", f"status — {msg}")


def on_apply():
    log("Apply clicked")


def on_reset():
    dpg.set_value("opacity_slider", 0.5)
    dpg.set_value("blur_checkbox", False)
    dpg.set_value("theme_combo", "Dark")
    dpg.set_value("title_input", "")
    log("Reset to defaults")


def on_slider(sender, value):
    log(f"Opacity: {value:.0%}")


def on_checkbox(sender, value):
    log(f"Blur enabled: {value}")


def on_combo(sender, value):
    log(f"Theme: {value}")


def on_input(sender, value):
    log(f"Title: {value}")


dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font_file(
        # Falls back gracefully if not found — DPG ships a built-in font
        "C:/Windows/Fonts/consola.ttf" if False else "",
        14,
    ) if False else None

# ImGui-style dark theme
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,       (15,  15,  15,  255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg,        (20,  20,  20,  255))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg,        (20,  20,  20,  240))
        dpg.add_theme_color(dpg.mvThemeCol_Border,         (80,  80,  80,  255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,        (41,  41,  41,  255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60,  60,  60,  255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,  (70,  70,  70,  255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg,        (20,  20,  20,  255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,  (41,  74, 122,  255))
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,      (36,  36,  36,  255))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,    (5,   5,   5,   135))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,  (79,  79,  79,  255))
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,      (66, 150, 250,  255))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab,     (66, 150, 250,  255))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive,(117,138,204, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button,         (66, 150, 250,  102))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  (66, 150, 250,  255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   (15, 135, 250,  255))
        dpg.add_theme_color(dpg.mvThemeCol_Header,         (66, 150, 250,   79))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,  (66, 150, 250,  204))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,   (66, 150, 250,  255))
        dpg.add_theme_color(dpg.mvThemeCol_Text,           (255,255,255,  255))
        dpg.add_theme_color(dpg.mvThemeCol_TextDisabled,   (128,128,128,  255))
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding,  4)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,   3)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,    3)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding,   4)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,     8, 6)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding,    6, 4)

dpg.bind_theme(global_theme)

with dpg.window(
    label="ImGui-Style Menu — GUI Showcase",
    tag="main_window",
    width=420,
    height=400,
    no_resize=False,
    no_move=False,
):
    dpg.add_text("STYLE SHOWCASE", color=(128, 128, 128, 255))
    dpg.add_text("Dear ImGui Aesthetic", color=(66, 150, 250, 255))
    dpg.add_separator()
    dpg.add_spacer(height=4)

    # Buttons
    dpg.add_button(label="Apply", width=180, callback=on_apply)
    dpg.add_same_line(spacing=10)
    dpg.add_button(label="Reset", width=180, callback=on_reset)

    dpg.add_spacer(height=6)
    dpg.add_separator()
    dpg.add_spacer(height=6)

    # Slider
    dpg.add_slider_float(
        label="Opacity",
        tag="opacity_slider",
        default_value=0.5,
        min_value=0.0,
        max_value=1.0,
        width=370,
        callback=on_slider,
    )

    dpg.add_spacer(height=4)

    # Checkbox
    dpg.add_checkbox(
        label="Enable blur",
        tag="blur_checkbox",
        callback=on_checkbox,
    )

    dpg.add_spacer(height=6)

    # Combo / dropdown
    dpg.add_combo(
        label="Theme",
        tag="theme_combo",
        items=["Dark", "Light", "Classic", "High Contrast"],
        default_value="Dark",
        width=240,
        callback=on_combo,
    )

    dpg.add_spacer(height=6)

    # Text input
    dpg.add_input_text(
        label="Title",
        tag="title_input",
        hint="Enter overlay title...",
        width=240,
        callback=on_input,
    )

    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=4)

    # Output
    dpg.add_text("status — waiting for input", tag="output", color=(150, 150, 150, 255))

dpg.create_viewport(
    title="Dear ImGui Style — GUI Showcase",
    width=460,
    height=440,
    resizable=True,
)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
