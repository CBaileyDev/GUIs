# GUIs — Modern Menu Style Showcase

A curated collection of modern GUI menu templates demonstrating different visual styles and implementation approaches. Each demo showcases a consistent component template across a variety of style libraries and frameworks.

## Component Template

Every menu in this collection includes:

| Component | Description |
|-----------|-------------|
| **Header / Title** | Styled with a thematic font and accent color |
| **Primary Button** | Main call-to-action, fully styled |
| **Secondary Button** | Alternate action, visually subordinate |
| **Slider** | Continuous value input (e.g. opacity, volume) |
| **Checkbox** | Boolean toggle with label |
| **Combo / Dropdown** | Select from a list of options |
| **Text Input** | Single-line text field |
| **Status / Output** | Feedback area showing current values |

## Folder Layout

```
GUIs/
├── README.md
├── internal/                   # In-process / overlay-style menus
│   └── overlay-html/
│       └── index.html          # Fixed overlay panel over a simulated scene
├── external/                   # Standalone window menus
│   └── tkinter-menu/
│       └── menu.py             # Native OS window via Python tkinter/ttk
└── styles/                     # Visual style libraries and themes
    ├── imgui-style/
    │   └── main.py             # Dear PyGui — ImGui flat dark aesthetic
    ├── glassmorphism/
    │   └── index.html          # Frosted glass panels, blur backdrop
    ├── neumorphism/
    │   └── index.html          # Soft extruded shadow on light grey
    ├── material/
    │   └── index.html          # Material Design 3 elevated cards
    └── cyberpunk/
        └── index.html          # Neon / scanline dark aesthetic
```

## How to Run Each Demo

### HTML/CSS/JS demos (no build step)
Just open the file in any modern browser:
```
styles/glassmorphism/index.html
styles/neumorphism/index.html
styles/material/index.html
styles/cyberpunk/index.html
internal/overlay-html/index.html
```

### Python — Dear PyGui (styles/imgui-style/)
```bash
pip install dearpygui
python styles/imgui-style/main.py
```

### Python — tkinter (external/tkinter-menu/)
```bash
# tkinter ships with Python on most platforms; ttkthemes is optional
pip install ttkthemes   # optional, only needed if using ttkthemes
python external/tkinter-menu/menu.py
```

## Adding a New Demo

1. Choose `internal/`, `external/`, or `styles/<theme-name>/` as the home.
2. Implement the full component template (header, 2 buttons, slider, checkbox, combo, text input).
3. Add a row to the table above with the run command.
