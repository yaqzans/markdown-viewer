"""Markdown Viewer desktop app: a pywebview window around index.html.

Usage: MarkdownViewer.exe [file.md]
"""
import os
import socket
import sys

import webview

# PyInstaller unpacks bundled files to sys._MEIPASS; in dev they sit next to this script
BASE = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(os.environ.get('LOCALAPPDATA', BASE), 'MarkdownViewer')  # keeps localStorage between runs


def read_md(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return {'name': os.path.basename(path), 'text': f.read()}


class Api:
    def __init__(self, start_path):
        self.start_path = start_path

    def initial_file(self):
        if self.start_path and os.path.isfile(self.start_path):
            return read_md(self.start_path)
        return None

    def open_file(self):
        paths = webview.windows[0].create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=('Markdown (*.md;*.markdown;*.txt)', 'All files (*.*)'))
        return read_md(paths[0]) if paths else None

    def export_pdf(self, suggested_name):
        window = webview.windows[0]
        path = window.create_file_dialog(
            webview.FileDialog.SAVE, save_filename=suggested_name,
            file_types=('PDF (*.pdf)',))
        if not path:
            return None
        path = path if isinstance(path, str) else path[0]
        if not path.lower().endswith('.pdf'):
            path += '.pdf'
        try:
            print_to_pdf(window, path)
        except Exception as e:
            return {'error': str(e)}
        return {'path': path}


def print_to_pdf(window, path):
    """Use WebView2's own PrintToPdf, which applies the page's @media print CSS."""
    from System import Func
    from System.Threading.Tasks import Task

    control = window.native.webview  # the WinForms WebView2 control

    def start():
        settings = control.CoreWebView2.Environment.CreatePrintSettings()
        settings.ShouldPrintBackgrounds = True
        settings.ShouldPrintHeaderAndFooter = False
        settings.MarginTop = settings.MarginBottom = 0.6
        settings.MarginLeft = settings.MarginRight = 0.6
        return control.CoreWebView2.PrintToPdfAsync(path, settings)

    # must start on the UI thread; wait here, on the API worker thread
    task = control.Invoke(Func[Task](start))
    task.Wait()
    if not task.Result:
        raise RuntimeError('WebView2 reported failure writing ' + path)


def free_port(start=42001):
    """First free port from 42001 up. With persistent storage pywebview always
    serves on 42001, and Windows lets a second window share a port that is in
    use, so it would get the first window's page instead of its own."""
    for port in range(start, start + 100):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                pass
    return None


def main():
    start_path = sys.argv[1] if len(sys.argv) > 1 else None
    title = 'Markdown Viewer' + (' - ' + os.path.basename(start_path) if start_path else '')
    webview.create_window(title, os.path.join(BASE, 'index.html'), js_api=Api(start_path),
                          width=1280, height=820, min_size=(600, 400))
    webview.start(gui='edgechromium', private_mode=False, storage_path=DATA, http_port=free_port())


if __name__ == '__main__':
    main()
