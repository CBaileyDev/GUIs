# pip install dearpygui
import dearpygui.dearpygui as dpg


def log(msg):
    dpg.set_value("output", msg)


def on_apply():
    log("Apply clicked")


def on_reset():
    dpg.set_value("opacity_slider", 0.5)
    dpg.set_value("blur_checkbox", False)
    dpg.set_value("theme_combo", "Dark")
    dpg.set_value("title_input", "")
    log("Reset to defaults")


def on_slider(_sender, value):
    log(f"Opacity: {value:.0%}")


def on_checkbox(_sender, value):
    log(f"Toolbar visible: {value}")


def on_combo(_sender, value):
    log(f"Theme: {value}")


def on_input(_sender, value):
    log(f"Title: {value}")


dpg.create_context()

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20, 20, 20, 255))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 20, 20, 240))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 80, 80, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (41, 41, 41, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 60, 60, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 70, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (20, 20, 20, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41, 74, 122, 255))
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (66, 150, 250, 255))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (66, 150, 250, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (66, 150, 250, 102))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (66, 150, 250, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (15, 135, 250, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 4)

dpg.bind_theme(global_theme)

with dpg.window(label="ImGui Menu", tag="main_window", width=420, height=400):
    dpg.add_text("Dear ImGui aesthetic")
    dpg.add_separator()

    dpg.add_button(label="Apply", width=180, callback=on_apply)
    dpg.add_same_line(spacing=10)
    dpg.add_button(label="Reset", width=180, callback=on_reset)

    dpg.add_separator()

    dpg.add_slider_float(
        label="Opacity",
        tag="opacity_slider",
        default_value=0.5,
        min_value=0.0,
        max_value=1.0,
        width=370,
        callback=on_slider,
    )

    dpg.add_checkbox(label="Show toolbar", tag="blur_checkbox", callback=on_checkbox)

    dpg.add_combo(
        label="Theme",
        tag="theme_combo",
        items=["Dark", "Light", "Classic", "High Contrast"],
        default_value="Dark",
        width=240,
        callback=on_combo,
    )

    dpg.add_input_text(
        label="Title",
        tag="title_input",
        hint="Window title…",
        width=240,
        callback=on_input,
    )

    dpg.add_separator()
    dpg.add_text("Ready", tag="output", color=(150, 150, 150, 255))

dpg.create_viewport(title="Dear ImGui Style", width=460, height=440)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
