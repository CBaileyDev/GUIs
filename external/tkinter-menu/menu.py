# pip install tk  (tkinter ships with Python on most platforms; no extra install needed)
# Optional dark theme enhancement: pip install ttkthemes
import tkinter as tk
from tkinter import ttk

try:
    from ttkthemes import ThemedTk
    USE_THEMED = True
except ImportError:
    USE_THEMED = False


BG       = "#1e1e2e"
BG2      = "#2a2a3e"
FG       = "#cdd6f4"
FG_DIM   = "#6c7086"
ACCENT   = "#89b4fa"
ACCENT2  = "#cba6f7"
SUCCESS  = "#a6e3a1"
BORDER   = "#313244"
FONT     = ("Segoe UI", 10)
FONT_H1  = ("Segoe UI", 16, "bold")
FONT_SM  = ("Segoe UI", 9)
MONO     = ("Consolas", 10)


class DarkMenu(tk.Tk if not USE_THEMED else object):
    def __init__(self):
        if USE_THEMED:
            self.root = ThemedTk(theme="equilux")
        else:
            self.root = tk.Tk()
            self.root.configure(bg=BG)

        root = self.root
        root.title("Tkinter Dark Menu — GUI Showcase")
        root.geometry("440x540")
        root.resizable(True, True)
        root.minsize(380, 480)

        self._apply_styles()
        self._build_ui(root)

    def _apply_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(".",
            background=BG,
            foreground=FG,
            font=FONT,
            troughcolor=BG2,
            borderwidth=0,
            focuscolor=ACCENT,
            selectforeground=BG,
            selectbackground=ACCENT,
        )
        style.configure("TFrame",   background=BG)
        style.configure("Card.TFrame", background=BG2, relief="flat")
        style.configure("TLabel",   background=BG,  foreground=FG,     font=FONT)
        style.configure("Dim.TLabel", background=BG, foreground=FG_DIM, font=FONT_SM)
        style.configure("H1.TLabel", background=BG, foreground=ACCENT,  font=FONT_H1)
        style.configure("Sub.TLabel", background=BG, foreground=FG_DIM, font=("Segoe UI", 9))

        style.configure("Primary.TButton",
            background=ACCENT, foreground=BG,
            font=("Segoe UI", 10, "bold"),
            padding=(16, 8),
            relief="flat",
        )
        style.map("Primary.TButton",
            background=[("active", ACCENT2), ("pressed", ACCENT2)],
            foreground=[("active", BG)],
        )
        style.configure("Secondary.TButton",
            background=BG2, foreground=FG,
            font=FONT,
            padding=(16, 8),
            relief="flat",
        )
        style.map("Secondary.TButton",
            background=[("active", BORDER), ("pressed", BORDER)],
        )
        style.configure("TScale",
            background=BG,
            troughcolor=BG2,
            sliderthickness=18,
            sliderrelief="flat",
        )
        style.map("TScale", background=[("active", ACCENT)])

        style.configure("TCheckbutton",
            background=BG,
            foreground=FG,
            indicatorcolor=BG2,
            indicatordiameter=16,
        )
        style.map("TCheckbutton",
            indicatorcolor=[("selected", ACCENT), ("active", BG2)],
            background=[("active", BG)],
        )
        style.configure("TCombobox",
            fieldbackground=BG2,
            background=BG2,
            foreground=FG,
            arrowcolor=ACCENT,
            selectforeground=FG,
            selectbackground=BG2,
            padding=(8, 6),
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", BG2)],
            selectbackground=[("readonly", BG2)],
            selectforeground=[("readonly", FG)],
        )
        style.configure("TEntry",
            fieldbackground=BG2,
            foreground=FG,
            insertcolor=ACCENT,
            padding=(8, 6),
        )
        style.configure("Horizontal.TScale",
            background=BG,
            troughcolor=BORDER,
            sliderlength=20,
        )

    def _build_ui(self, root):
        outer = ttk.Frame(root, padding=24)
        outer.pack(fill="both", expand=True)

        # Header
        ttk.Label(outer, text="STYLE SHOWCASE", style="Sub.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Tkinter Dark Menu", style="H1.TLabel").pack(anchor="w")

        sep = tk.Frame(outer, height=1, bg=BORDER)
        sep.pack(fill="x", pady=(12, 16))

        # Buttons
        btn_row = ttk.Frame(outer)
        btn_row.pack(fill="x", pady=(0, 16))
        ttk.Button(btn_row, text="Apply", style="Primary.TButton",
                   command=self._on_apply).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Reset", style="Secondary.TButton",
                   command=self._on_reset).pack(side="left")

        sep2 = tk.Frame(outer, height=1, bg=BORDER)
        sep2.pack(fill="x", pady=(0, 16))

        # Slider
        self.slider_var = tk.DoubleVar(value=65)
        slider_frame = ttk.Frame(outer)
        slider_frame.pack(fill="x", pady=(0, 14))
        lbl_row = ttk.Frame(slider_frame)
        lbl_row.pack(fill="x", pady=(0, 6))
        ttk.Label(lbl_row, text="Opacity").pack(side="left")
        self.slider_lbl = ttk.Label(lbl_row, text="65%", foreground=ACCENT, background=BG)
        self.slider_lbl.pack(side="right")
        ttk.Scale(
            slider_frame,
            from_=0, to=100,
            variable=self.slider_var,
            orient="horizontal",
            command=self._on_slider,
        ).pack(fill="x")

        # Checkbox
        self.check_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(outer, text="Enable blur effect",
                        variable=self.check_var,
                        command=self._on_check).pack(anchor="w", pady=(0, 14))

        # Combo
        combo_frame = ttk.Frame(outer)
        combo_frame.pack(fill="x", pady=(0, 14))
        ttk.Label(combo_frame, text="Theme preset", style="Dim.TLabel").pack(anchor="w", pady=(0, 4))
        self.combo_var = tk.StringVar(value="Catppuccin Mocha")
        combo = ttk.Combobox(combo_frame,
                             textvariable=self.combo_var,
                             values=["Catppuccin Mocha", "Tokyo Night", "Dracula", "Nord", "Gruvbox"],
                             state="readonly")
        combo.pack(fill="x")
        combo.bind("<<ComboboxSelected>>", self._on_combo)
        # Fix dropdown colors
        root.option_add("*TCombobox*Listbox.background", BG2)
        root.option_add("*TCombobox*Listbox.foreground", FG)
        root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        root.option_add("*TCombobox*Listbox.selectForeground", BG)

        # Text entry
        entry_frame = ttk.Frame(outer)
        entry_frame.pack(fill="x", pady=(0, 16))
        ttk.Label(entry_frame, text="Overlay title", style="Dim.TLabel").pack(anchor="w", pady=(0, 4))
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        entry.pack(fill="x")
        self.entry_var.trace_add("write", self._on_entry)

        sep3 = tk.Frame(outer, height=1, bg=BORDER)
        sep3.pack(fill="x", pady=(0, 12))

        # Output
        self.output_var = tk.StringVar(value="status — waiting for input")
        out_frame = tk.Frame(outer, bg=BG2, padx=12, pady=8)
        out_frame.pack(fill="x")
        tk.Label(out_frame, textvariable=self.output_var,
                 bg=BG2, fg=FG_DIM, font=MONO, anchor="w").pack(fill="x")

    def _log(self, msg):
        self.output_var.set(f"status — {msg}")

    def _on_apply(self):
        self._log("Apply clicked")

    def _on_reset(self):
        self.slider_var.set(65)
        self.slider_lbl.config(text="65%")
        self.check_var.set(False)
        self.combo_var.set("Catppuccin Mocha")
        self.entry_var.set("")
        self._log("Reset to defaults")

    def _on_slider(self, val):
        pct = int(float(val))
        self.slider_lbl.config(text=f"{pct}%")
        self._log(f"Opacity: {pct}%")

    def _on_check(self):
        self._log(f"Blur enabled: {self.check_var.get()}")

    def _on_combo(self, _event=None):
        self._log(f"Theme: {self.combo_var.get()}")

    def _on_entry(self, *_):
        val = self.entry_var.get()
        if val:
            self._log(f"Title: {val}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DarkMenu()
    app.run()
