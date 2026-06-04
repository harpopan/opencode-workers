#!/usr/bin/env python3
# servidorlogslmstudio.py - Servidor web para logs de LM Studio
# Version: 3.1
# Sirve la carpeta donde se ejecuta y todas sus subcarpetas
# Dependencias: solo Python stdlib

import io
import os
import sys
import socket
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = int(os.environ.get("LM_LOG_PORT", 1235))

class LogDirHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

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
            href = parent.replace(os.sep, "/") if parent else "/"
            html += f'<tr><td class="dir"><a href="{href}">../</a></td><td></td><td></td></tr>'

        for d in dirs:
            full = os.path.join(path, d)
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M")
            href = os.path.join(rel_path, d).replace(os.sep, "/")
            html += f'<tr><td class="dir"><a href="/{href}">{d}/</a></td><td></td><td>{mtime}</td></tr>'

        for f in files:
            full = os.path.join(path, f)
            size = self.format_size(os.path.getsize(full))
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M")
            css_class = "log" if f.endswith(".log") else "file"
            if "error" in f.lower():
                css_class = "error"
            href = os.path.join(rel_path, f).replace(os.sep, "/")
            html += f'<tr><td class="{css_class}"><a href="/{href}">{f}</a></td><td>{size}</td><td>{mtime}</td></tr>'

        html += f"""</table>
<p class="meta">Directorio: {self.directory} | Actualizado: {now} | Auto-refresh: 60s</p>
</body></html>"""
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write(f"[{timestamp}] {args[0]}\n")

def get_local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        ips.append(socket.gethostbyname(hostname))
        for info in socket.getaddrinfo(hostname, None):
            addr = info[4][0]
            if addr not in ips and not addr.startswith("127."):
                ips.append(addr)
    except Exception:
        pass
    return ips

if __name__ == "__main__":
    serve_dir = os.getcwd()
    handler = partial(LogDirHandler, directory=serve_dir)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), handler)

    print(f"=== LM Studio Log Server ===")
    print(f"Directorio: {serve_dir}")
    print(f"")
    print(f"URLs de acceso:")
    ips = get_local_ips()
    for ip in ips:
        print(f"  http://{ip}:{PORT}")
    print(f"")
    print(f"Auto-refresh: 60s | CORS habilitado")
    print(f"Presiona Ctrl+C para detener.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        server.shutdown()
