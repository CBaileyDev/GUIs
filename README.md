# GUIs — Modern Menu Style Showcase

A curated collection of modern GUI menu templates demonstrating different visual styles and implementation approaches. Every template lives in its own folder and implements the same component set so they can be compared side-by-side.

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
│
├── internal/                      # In-process / overlay-style menus
│   ├── overlay-html/index.html    # Fixed overlay panel over a simulated scene
│   ├── game-hud/index.html        # Full-screen game HUD with radar & panel
│   ├── command-palette/index.html # ⌘K-style searchable command modal
│   └── floating-toolbar/index.html# Canvas toolbar + settings popover
│
├── external/                      # Standalone window menus
│   ├── tkinter-menu/menu.py       # Native OS window via Python tkinter/ttk
│   ├── pyqt-menu/menu.py          # PyQt6 dark-themed Qt window
│   └── customtkinter/menu.py      # CustomTkinter — modern rounded tkinter
│
└── styles/                        # Visual style libraries and themes
    ├── imgui-style/main.py        # Dear PyGui — ImGui flat dark aesthetic
    ├── glassmorphism/index.html   # Frosted glass panels, blur backdrop
    ├── neumorphism/index.html     # Soft extruded shadow on light grey
    ├── material/index.html        # Material Design 3 elevated cards
    ├── cyberpunk/index.html       # Neon / scanline dark aesthetic
    ├── brutalism/index.html       # Raw borders, hard shadows, acid yellow
    ├── retro-terminal/index.html  # Green-phosphor CRT terminal
    ├── synthwave/index.html       # Neon pink/cyan grid — 80s future
    ├── claymorphism/index.html    # Soft squishy pastel "clay" shapes
    ├── minimalist/index.html      # Typographic, hairline, near-bare
    ├── nord/index.html            # Arctic north-bluish palette
    ├── dracula/index.html         # Classic dark dev theme
    ├── skeuomorphic/index.html    # Leather, brass, beveled buttons
    ├── paper-sketch/index.html    # Hand-drawn pencil-on-paper look
    ├── vaporwave/index.html       # 90s aesthetic, pastel neon, Japanese serif
    ├── monochrome/index.html      # Pure black-and-white, Swiss grid
    ├── solarized/index.html       # Precision Solarized light palette
    ├── win95/index.html           # Classic Chicago-era Windows chrome
    ├── aqua/index.html            # Glossy early-OSX pinstripe & lozenge
    └── bauhaus/index.html         # Primary colors, geometric shapes
```

## How to Run Each Demo

### HTML/CSS/JS demos (no build step)
Just open the file in any modern browser. For example:

```
open styles/glassmorphism/index.html
open styles/synthwave/index.html
open internal/game-hud/index.html
```

All files under `styles/` (except `imgui-style/`) and all `internal/` templates are plain HTML — no install required.

### Python — Dear PyGui (`styles/imgui-style/`)
```bash
pip install dearpygui
python styles/imgui-style/main.py
```

### Python — tkinter (`external/tkinter-menu/`)
```bash
# tkinter ships with Python on most platforms; ttkthemes is optional
pip install ttkthemes   # optional
python external/tkinter-menu/menu.py
```

### Python — PyQt6 (`external/pyqt-menu/`)
```bash
pip install PyQt6
python external/pyqt-menu/menu.py
```

### Python — CustomTkinter (`external/customtkinter/`)
```bash
pip install customtkinter
python external/customtkinter/menu.py
```

## Adding a New Demo

1. Create a new folder under `internal/`, `external/`, or `styles/<theme-name>/`.
2. Implement the full component template (header, two buttons, slider, checkbox, combo, text input, status output).
3. Keep each demo **self-contained** inside its folder — no shared CSS/JS between templates.
4. Add an entry to the folder tree above with the run command.
