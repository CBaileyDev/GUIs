"""
PyQt6 Menu — Standalone window demo for the GUIs showcase.

Install and run:
    pip install PyQt6
    python external/pyqt-menu/menu.py

Shows the standard component template: header, two buttons, slider, checkbox,
combo box, text input and a status output label.
"""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


STYLE = """
QWidget#root {
    background: #1e1f29;
    color: #e8eaf2;
}
QLabel#title {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
}
QLabel#subtitle { color: #9098b0; font-size: 12px; }
QLabel.sectionTitle {
    color: #8a95ff;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}
QLabel.formLabel { color: #c3c9db; font-size: 13px; font-weight: 500; }
QLabel#valueLabel { color: #8a95ff; font-size: 13px; font-weight: 600; }
QLabel#status {
    background: #15161d;
    border: 1px solid #2a2c3a;
    border-radius: 6px;
    padding: 10px 12px;
    color: #9098b0;
    font-family: "Menlo", "Consolas", monospace;
    font-size: 12px;
}
QFrame#divider {
    background: #2a2c3a;
    max-height: 1px; min-height: 1px;
}

QPushButton {
    padding: 10px 14px;
    border-radius: 7px;
    font-weight: 600;
    font-size: 13px;
    border: none;
}
QPushButton#primary {
    background: #6c63ff;
    color: #ffffff;
}
QPushButton#primary:hover { background: #7d75ff; }
QPushButton#primary:pressed { background: #5a51e8; }
QPushButton#secondary {
    background: #2a2c3a;
    color: #e8eaf2;
    border: 1px solid #383b4c;
}
QPushButton#secondary:hover { background: #33364a; }

QSlider::groove:horizontal {
    border: none; height: 4px; background: #2a2c3a; border-radius: 2px;
}
QSlider::sub-page:horizontal { background: #6c63ff; border-radius: 2px; }
QSlider::handle:horizontal {
    background: #ffffff; border: 2px solid #6c63ff;
    width: 14px; height: 14px;
    margin: -6px 0; border-radius: 8px;
}

QCheckBox { color: #e8eaf2; font-size: 14px; padding: 4px 0; spacing: 10px; }
QCheckBox::indicator {
    width: 18px; height: 18px; border-radius: 4px;
    border: 1.5px solid #4a4d63; background: #15161d;
}
QCheckBox::indicator:checked {
    background: #6c63ff; border-color: #6c63ff;
    image: none;
}

QComboBox, QLineEdit {
    padding: 8px 12px; border-radius: 6px;
    background: #15161d; color: #e8eaf2;
    border: 1px solid #2a2c3a; font-size: 13px;
}
QComboBox:focus, QLineEdit:focus { border-color: #6c63ff; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background: #1e1f29; color: #e8eaf2;
    selection-background-color: #6c63ff; border: 1px solid #2a2c3a;
}
QLineEdit::placeholder { color: #5a5f72; }
"""


class MenuWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("root")
        self.setWindowTitle("PyQt6 Menu")
        self.setFixedWidth(420)

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        # Header
        title = QLabel("PyQt6 Menu")
        title.setObjectName("title")
        subtitle = QLabel("Native Qt widgets · dark theme")
        subtitle.setObjectName("subtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        root.addWidget(self._divider())

        # Button row
        actions_lbl = QLabel("ACTIONS")
        actions_lbl.setProperty("class", "sectionTitle")
        actions_lbl.setObjectName("sectionTitle")
        actions_lbl.setStyleSheet(
            "color:#8a95ff;font-size:11px;font-weight:600;letter-spacing:2px;"
        )
        root.addWidget(actions_lbl)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        primary = QPushButton("Apply")
        primary.setObjectName("primary")
        primary.clicked.connect(lambda: self.log("Apply clicked"))
        secondary = QPushButton("Reset")
        secondary.setObjectName("secondary")
        secondary.clicked.connect(lambda: self.log("Reset clicked"))
        btn_row.addWidget(primary)
        btn_row.addWidget(secondary)
        root.addLayout(btn_row)

        # Slider
        slider_head = QHBoxLayout()
        sl_lbl = QLabel("Opacity")
        sl_lbl.setStyleSheet("color:#c3c9db;font-size:13px;font-weight:500;")
        self.value_lbl = QLabel("72%")
        self.value_lbl.setObjectName("valueLabel")
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        slider_head.addWidget(sl_lbl)
        slider_head.addWidget(self.value_lbl)
        root.addLayout(slider_head)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(72)
        slider.valueChanged.connect(self._on_slider)
        root.addWidget(slider)

        # Checkbox
        self.check = QCheckBox("Enable blur backdrop")
        self.check.stateChanged.connect(
            lambda s: self.log(f"Blur enabled: {bool(s)}")
        )
        root.addWidget(self.check)

        # Combo
        combo_lbl = QLabel("Theme preset")
        combo_lbl.setStyleSheet("color:#c3c9db;font-size:13px;font-weight:500;")
        root.addWidget(combo_lbl)
        combo = QComboBox()
        combo.addItems(["Aurora Violet", "Ocean Cyan", "Sunset Rose", "Emerald Mist"])
        combo.currentTextChanged.connect(lambda t: self.log(f"Theme: {t}"))
        root.addWidget(combo)

        # Text input
        entry = QLineEdit()
        entry.setPlaceholderText("Enter overlay title…")
        entry.textChanged.connect(lambda t: self.log(f"Title: {t}"))
        root.addWidget(entry)

        # Status
        self.status = QLabel("status — waiting for input")
        self.status.setObjectName("status")
        self.status.setFont(QFont("Menlo", 10))
        root.addWidget(self.status)

        self.setStyleSheet(STYLE)

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setObjectName("divider")
        line.setFrameShape(QFrame.Shape.HLine)
        return line

    def _on_slider(self, value: int) -> None:
        self.value_lbl.setText(f"{value}%")
        self.log(f"Opacity: {value}%")

    def log(self, message: str) -> None:
        self.status.setText(f"status — {message}")


def main() -> int:
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
