"""
CustomTkinter Menu — Modern-looking tkinter-based window.

Install and run:
    pip install customtkinter
    python external/customtkinter/menu.py
"""

from __future__ import annotations

import customtkinter as ctk


class MenuApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("CustomTkinter Menu")
        self.geometry("440x600")
        self.configure(fg_color="#0e1220")

        card = ctk.CTkFrame(self, fg_color="#161b2e", corner_radius=16)
        card.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            card,
            text="CustomTkinter Menu",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        ).pack(anchor="w", padx=22, pady=(20, 0))

        ctk.CTkLabel(
            card,
            text="Modern rounded tkinter widgets",
            font=ctk.CTkFont(size=12),
            text_color="#8a93b3",
        ).pack(anchor="w", padx=22, pady=(0, 14))

        ctk.CTkFrame(card, fg_color="#252b45", height=1).pack(fill="x", padx=22)

        # Buttons
        self._section_label(card, "ACTIONS")
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=22, pady=(0, 14))

        ctk.CTkButton(
            btn_row, text="Apply", fg_color="#5b6cff", hover_color="#6d7dff",
            corner_radius=8, height=38, command=lambda: self.log("Apply clicked"),
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(
            btn_row, text="Reset", fg_color="#252b45", hover_color="#2d3352",
            text_color="#e3e7f5", border_width=1, border_color="#383f5c",
            corner_radius=8, height=38, command=lambda: self.log("Reset clicked"),
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        # Slider
        slider_head = ctk.CTkFrame(card, fg_color="transparent")
        slider_head.pack(fill="x", padx=22, pady=(6, 4))
        ctk.CTkLabel(
            slider_head, text="Opacity",
            font=ctk.CTkFont(size=13), text_color="#c3c9db",
        ).pack(side="left")
        self.slider_value = ctk.CTkLabel(
            slider_head, text="72%",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#5b6cff",
        )
        self.slider_value.pack(side="right")

        self.slider = ctk.CTkSlider(
            card, from_=0, to=100, number_of_steps=100,
            progress_color="#5b6cff", button_color="#ffffff",
            button_hover_color="#e0e4ff", command=self._on_slider,
        )
        self.slider.set(72)
        self.slider.pack(fill="x", padx=22, pady=(0, 14))

        # Checkbox
        self.check_var = ctk.IntVar(value=0)
        ctk.CTkCheckBox(
            card, text="Enable blur backdrop",
            variable=self.check_var, fg_color="#5b6cff",
            hover_color="#6d7dff", corner_radius=4,
            font=ctk.CTkFont(size=13),
            command=lambda: self.log(f"Blur enabled: {bool(self.check_var.get())}"),
        ).pack(anchor="w", padx=22, pady=(0, 14))

        # Dropdown
        self._section_label(card, "THEME PRESET")
        self.combo = ctk.CTkComboBox(
            card, values=["Aurora Violet", "Ocean Cyan", "Sunset Rose", "Emerald Mist"],
            fg_color="#0f1324", border_color="#383f5c", button_color="#5b6cff",
            button_hover_color="#6d7dff", dropdown_fg_color="#161b2e",
            command=lambda v: self.log(f"Theme: {v}"),
        )
        self.combo.set("Aurora Violet")
        self.combo.pack(fill="x", padx=22, pady=(0, 14))

        # Entry
        self.entry = ctk.CTkEntry(
            card, placeholder_text="Enter overlay title…",
            fg_color="#0f1324", border_color="#383f5c", corner_radius=8, height=36,
        )
        self.entry.pack(fill="x", padx=22, pady=(0, 14))
        self.entry.bind("<KeyRelease>", lambda _e: self.log(f"Title: {self.entry.get()}"))

        # Status
        self.status = ctk.CTkLabel(
            card, text="status — waiting for input",
            font=ctk.CTkFont(size=12, family="Menlo"),
            fg_color="#0b0f1e", text_color="#8a93b3",
            corner_radius=8, anchor="w", justify="left",
            padx=12, pady=10,
        )
        self.status.pack(fill="x", padx=22, pady=(6, 20))

    def _section_label(self, parent, text: str) -> None:
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#8a93b3",
        ).pack(anchor="w", padx=22, pady=(10, 6))

    def _on_slider(self, value: float) -> None:
        pct = int(value)
        self.slider_value.configure(text=f"{pct}%")
        self.log(f"Opacity: {pct}%")

    def log(self, message: str) -> None:
        self.status.configure(text=f"status — {message}")


if __name__ == "__main__":
    MenuApp().mainloop()
