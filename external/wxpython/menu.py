"""
wxPython Menu — native-looking standalone window.

Install and run:
    pip install wxPython
    python external/wxpython/menu.py
"""

from __future__ import annotations

import wx


class MenuFrame(wx.Frame):
    def __init__(self) -> None:
        super().__init__(parent=None, title="wxPython Menu", size=(440, 560))
        self.SetBackgroundColour(wx.Colour(245, 245, 248))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(245, 245, 248))
        root = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="wxPython Menu")
        title_font = title.GetFont()
        title_font.SetPointSize(18)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(20, 20, 26))

        subtitle = wx.StaticText(panel, label="Native widgets via wxWidgets")
        subtitle.SetForegroundColour(wx.Colour(110, 115, 130))

        root.Add(title, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24)
        root.Add(subtitle, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)
        root.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 24)

        actions_lbl = wx.StaticText(panel, label="Actions")
        actions_lbl.SetForegroundColour(wx.Colour(110, 115, 130))
        root.Add(actions_lbl, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24)

        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        apply_btn = wx.Button(panel, label="Apply")
        apply_btn.SetBackgroundColour(wx.Colour(88, 101, 242))
        apply_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        apply_btn.Bind(wx.EVT_BUTTON, lambda _e: self.log("Apply clicked"))
        reset_btn = wx.Button(panel, label="Reset")
        reset_btn.Bind(wx.EVT_BUTTON, lambda _e: self.log("Reset clicked"))
        btn_row.Add(apply_btn, 1, wx.EXPAND | wx.RIGHT, 8)
        btn_row.Add(reset_btn, 1, wx.EXPAND)
        root.Add(btn_row, 0, wx.EXPAND | wx.ALL, 24)

        self.slider_lbl = wx.StaticText(panel, label="Opacity — 72%")
        self.slider_lbl.SetForegroundColour(wx.Colour(60, 65, 80))
        self.slider = wx.Slider(panel, value=72, minValue=0, maxValue=100)
        self.slider.Bind(wx.EVT_SLIDER, self._on_slider)
        root.Add(self.slider_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        root.Add(self.slider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)

        self.check = wx.CheckBox(panel, label="Remember window size")
        self.check.Bind(wx.EVT_CHECKBOX, lambda _e: self.log(f"Remember size: {self.check.GetValue()}"))
        root.Add(self.check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)

        combo_lbl = wx.StaticText(panel, label="Color scheme")
        combo_lbl.SetForegroundColour(wx.Colour(60, 65, 80))
        self.combo = wx.ComboBox(panel, value="System",
                                 choices=["System", "Light", "Dark"], style=wx.CB_READONLY)
        self.combo.Bind(wx.EVT_COMBOBOX, lambda _e: self.log(f"Scheme: {self.combo.GetValue()}"))
        root.Add(combo_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        root.Add(self.combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)

        self.entry = wx.TextCtrl(panel)
        self.entry.SetHint("Profile name…")
        self.entry.Bind(wx.EVT_TEXT, lambda _e: self.log(f"Profile: {self.entry.GetValue()}"))
        root.Add(self.entry, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)

        self.status = wx.StaticText(panel, label="Ready")
        self.status.SetForegroundColour(wx.Colour(110, 115, 130))
        status_font = self.status.GetFont()
        status_font.SetFamily(wx.FONTFAMILY_TELETYPE)
        self.status.SetFont(status_font)
        root.Add(self.status, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 24)

        panel.SetSizer(root)
        self.Centre()

    def _on_slider(self, _event: wx.CommandEvent) -> None:
        value = self.slider.GetValue()
        self.slider_lbl.SetLabel(f"Opacity — {value}%")
        self.log(f"Opacity: {value}%")

    def log(self, message: str) -> None:
        self.status.SetLabel(message)


def main() -> None:
    app = wx.App()
    MenuFrame().Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
