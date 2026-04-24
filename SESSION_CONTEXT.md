# Session handoff — GUIs showcase (pictures + per-template READMEs)

Copy this file into the next session so it can continue where this one left off.

## Where we are

- **Repo**: `cbaileydev/guis` (`/home/user/GUIs`)
- **Branch**: `claude/organize-templates-1qayq`
- **Draft PR**: https://github.com/CBaileyDev/GUIs/pull/1
- **Last pushed commit**: `b10d6fe feat: add 13 more menu templates (27 → 40 total)`

## Running user request

> "make the read me have pictures showing each and then each template should
> have their own in depth readme"

## What's already done (uncommitted, on disk)

1. **`preview.png` generated for all 40 templates** (35 via wkhtmltoimage on
   the HTML files + 5 Pillow-drawn mockups for the Python-only templates).
   Paths: `<section>/<folder>/preview.png`.
2. **Two generator scripts at the repo root** (also uncommitted):
   - `render_previews.py` — renders HTML templates via `wkhtmltoimage`, crops
     to `MAX_HEIGHT = 800`. Internal overlays get `--height 780` because they
     use `overflow: hidden` + fixed positioning and have no natural page
     height.
   - `render_python_previews.py` — draws mockup PNGs with Pillow for the five
     Python-only templates (`external/tkinter-menu`, `external/pyqt-menu`,
     `external/customtkinter`, `external/wxpython`, `styles/imgui-style`).
3. **One HTML tweak** to make the preview capture work: in
   `internal/sidebar-drawer/index.html` the drawer now starts with the `.open`
   class on the `.backdrop` and `.drawer` elements (so wkhtmltoimage captures
   it visible), and the `requestAnimationFrame(open_drawer)` line was removed.
   Status: modified but uncommitted.

`git status --short` at handoff time:

```
 M internal/sidebar-drawer/index.html
?? render_previews.py
?? render_python_previews.py
?? styles/<every>/preview.png        (29 files)
?? internal/<every>/preview.png      (6 files)
?? external/<every>/preview.png      (4 files)
?? styles/imgui-style/preview.png    (1 file)
```

That's **40 preview PNGs** + 2 scripts + 1 HTML edit.

## What still needs to be done

1. **Per-template README.md for all 40 templates.** Each lives alongside its
   source in its own folder (e.g. `styles/glassmorphism/README.md`).
   Target contents, roughly 80–180 words each:
   - Title + the rendered `preview.png` at the top.
   - One-sentence tagline.
   - "Design notes" — palette, typography, signature effects (e.g. blur,
     hard shadow offset, CRT scanline mask), any visual quirks.
   - "Components" — list of the standard component set implemented in this
     template (header, two buttons, slider, checkbox, dropdown, text input,
     status output). Note any extras (e.g. glassmorphism has a big button
     showcase, modal, toast stack; win95 adds a title bar + menu bar; game-hud
     adds a radar + player bars).
   - "Run" — the exact command to open/run it.
   - Optional: browser-support caveats (e.g. `backdrop-filter` needed for
     glassmorphism; conic-gradient for game-hud radar).
2. **Rewrite the root `README.md`** as a gallery. Suggested layout: markdown
   tables with 2 or 3 columns of thumbnails + template names, one table per
   section (`styles/`, `internal/`, `external/`). Each thumbnail links to the
   template's folder so the per-template README comes up on GitHub. Keep the
   existing "Component Template" table and the run-instructions, but move them
   below the gallery.
3. **Commit + push.** Probably two commits:
   - `chore: add preview.png for every template + render scripts`
   - `docs: gallery README and per-template READMEs`
   Push to `claude/organize-templates-1qayq` (PR #1 is the draft to update).

## Suggested approach for the per-template READMEs

Don't hand-write 40 files. Write a single `scripts/gen_readmes.py` that has a
dict of per-template metadata (palette, fonts, signature effects, extras) and
renders each README from a Jinja-free f-string template. Keeps every README
consistent, and lets you bulk-regenerate later. The standard component list
and run command are shared — only the tagline + design notes + extras vary.

Data you can pull directly from the HTML to seed the script:
- `<title>` → display name
- Google Fonts `<link>` → typography section
- CSS `:root` vars or the first `.card { background: ... }` → palette

## Tooling notes

- **wkhtmltoimage 0.12.6** is available at `/usr/bin/wkhtmltoimage`. Uses
  older QtWebKit. Known limitations we hit: no `backdrop-filter`, imperfect
  `conic-gradient` support, does not wait for JS `setTimeout` or transitions
  before snapping. Mitigations: internal overlays get a forced viewport via
  `--height`, and the sidebar-drawer is started `open` in the markup.
- **Playwright** is installed but **chromium download is blocked** by the
  sandbox (`403 Host not in allowlist` on cdn.playwright.dev). Don't retry;
  wkhtmltoimage is fine for static previews.
- **Pillow** is installed for post-processing (cropping) and for the Python
  mockups.
- **apt** works in a limited way — `wkhtmltopdf` was installed via apt (that's
  where wkhtmltoimage comes from).

## Repo layout reminder (40 templates)

```
styles/   (30)   aqua, art-deco, bauhaus, brutalism, claymorphism, comic,
                 cyberpunk, dracula, gameboy, glassmorphism, imgui-style,
                 ios, linear, material, memphis, minimalist, monochrome,
                 neumorphism, nord, paper-sketch, retro-terminal,
                 skeuomorphic, solarized, steampunk, swiss, synthwave,
                 tron, vaporwave, win95, y2k
internal/ ( 6)   command-palette, floating-toolbar, game-hud,
                 notification-stack, overlay-html, sidebar-drawer
external/ ( 4)   customtkinter, pyqt-menu, tkinter-menu, wxpython
```

Every HTML template implements: header, primary + secondary buttons, slider,
checkbox, dropdown, text input, status/output — consistent across the gallery.

## PR watch

The session was subscribed to PR #1 activity
(`mcp__github__subscribe_pr_activity`). CodeRabbit skipped review because the
PR is a draft; it will kick in on "Ready for review" or a
`@coderabbitai review` comment. No unresolved review threads, no CI failures
to address.

## Suggested next actions, in order

1. `git add -A` the preview PNGs, scripts, and the sidebar-drawer edit; commit
   as `chore: add preview.png for every template + render scripts`.
2. Write `scripts/gen_readmes.py` with a dict of per-template metadata; run it
   to produce all 40 `README.md` files.
3. Rewrite root `README.md` with a thumbnail gallery.
4. Commit `docs: gallery README and per-template READMEs` and push to
   `claude/organize-templates-1qayq`.
5. Don't mark the PR ready for review — user hasn't asked.
