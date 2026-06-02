#!/usr/bin/env python3
# servidorlogslmstudio.py - Servidor web para logs de LM Studio
# Sirve la carpeta donde se ejecuta y todas sus subcarpetas
# Dependencias: solo Python stdlib

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = int(os.environ.get("LM_LOG_PORT", 1235))

class LogDirHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "Directory not found")
            return None

        entries.sort()
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        rel_path = os.path.relpath(path, self.directory)
        if rel_path == ".":
            rel_path = ""

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html><head><title>LM Studio Logs - {rel_path or "Root"}</title>
<style>
body {{ font-family: monospace; background: #1a1a2e; color: #e0e0e0; margin: 20px; }}
h1 {{ color: #00d4ff; font-size: 1.2em; }}
a {{ color: #00d4ff; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.dir {{ color: #6bcb77; }}
.file {{ color: #e0e0e0; }}
.log {{ color: #ffd93d; }}
.error {{ color: #ff6b6b; }}
table {{ border-collapse: collapse; width: 100%; }}
td {{ padding: 4px 8px; border-bottom: 1px solid #333; }}
td:first-child {{ width: 120px; color: #888; font-size: 0.85em; }}
td:nth-child(2) {{ width: 80px; text-align: right; color: #888; font-size: 0.85em; }}
.meta {{ color: #666; font-size: 0.8em; margin-top: 15px; }}
.back {{ margin-bottom: 10px; }}
</style>
<meta http-equiv="refresh" content="60">
</head><body>
<h1>LM Studio Logs{': /' + rel_path if rel_path else ''}</h1>
<div class="back"><a href="/">Volver al inicio</a></div>
<table>
"""

        if rel_path:
            parent = os.path.dirname(rel_path)
            html += f'<tr><td class="dir"><a href="/{parent if parent else "."}">../</a></td><td></td><td></td></tr>'

        for d in dirs:
            full = os.path.join(path, d)
            size = ""
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M")
            html += f'<tr><td class="dir"><a href="/{os.path.join(rel_path, d)}">{d}/</a></td><td>{size}</td><td>{mtime}</td></tr>'

        for f in files:
            full = os.path.join(path, f)
            size = self.format_size(os.path.getsize(full))
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M")
            css_class = "log" if f.endswith(".log") else "file"
            if "error" in f.lower():
                css_class = "error"
            html += f'<tr><td class="{css_class}"><a href="/{os.path.join(rel_path, f)}">{f}</a></td><td>{size}</td><td>{mtime}</td></tr>'

        html += f"""</table>
<p class="meta">Directorio: {self.directory} | Actualizado: {now} | Auto-refresh: 60s</p>
</body></html>"""
        return html.encode("utf-8")

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write(f"[{timestamp}] {args[0]}\n")

if __name__ == "__main__":
    serve_dir = os.getcwd()
    server = HTTPServer(("0.0.0.0", PORT), LogDirHandler)
    server.directory = serve_dir
    print(f"=== LM Studio Log Server ===")
    print(f"Directorio: {serve_dir}")
    print(f"URL: http://scacnet.cacsa.eu:{PORT}")
    print(f"Auto-refresh: 60s")
    print("")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        server.shutdown()
