# Markdown Viewer

A small offline Windows app for reading and editing Markdown files. Editor on the left, live preview on the right.

## Download

**[Download MarkdownViewer.exe](https://github.com/yaqzans/markdown-viewer/releases/latest/download/MarkdownViewer.exe)** (about 14 MB, one file)

Double-click it. Nothing to install, no internet needed. It uses the Edge WebView2 engine that comes with Windows 10 and 11.

Windows SmartScreen may warn the first time because the exe is not signed. Click **More info**, then **Run anyway**.

## Features

- Editor with line numbers and markdown syntax colouring
- Live preview with GitHub-style rendering: tables, task lists, code blocks with syntax colours
- **Open** a `.md` file, drag one onto the window, or use **Open with > MarkdownViewer.exe** in Explorer
- **Export PDF** saves a real `.pdf` file: preview only, always light theme, full length
- **Copy** the markdown, **Reset** to the sample
- **Sync scroll** works both ways: scrolling either pane moves the other
- Draggable divider between the panes, **Hide editor** for a full-width preview
- **Dark mode**
- Remembers your last text, dark mode and divider position

## Build from source

```
py -3.11 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pyinstaller --noconfirm --onefile --windowed --name MarkdownViewer --add-data "index.html;." --add-data "vendor;vendor" app.py
```

The exe lands in `dist\`. `index.html` also works on its own in a browser (Export PDF then uses the print dialog).

Bundled libraries in `vendor/`: marked 12.0.2, DOMPurify 3.1.6, highlight.js 11.9.0, CodeMirror 5.65.16.
