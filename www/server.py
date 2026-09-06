#!/usr/bin/env python3
"""Serves index.html with {{placeholders}} filled in. No JavaScript needed."""

import mimetypes
import os
import shutil
import socket
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BOARD_NAMES = {
    "Arduino SA,Imola": "Arduino UNO Q",
}

PORT = 8000
HERE = Path(__file__).parent


def read(path, default=""):
    try:
        return Path(path).read_text(errors="replace").strip("\x00 \t\n")
    except OSError:
        return default


def values():
    """Every {{name}} you can use in index.html is a key in this dict."""
    u = os.uname()
    disk = shutil.disk_usage("/")
    uptime = int(float(read("/proc/uptime", "0").split()[0] or 0))

    memory = {}
    for line in read("/proc/meminfo").splitlines():
        key, sep, value = line.partition(":")
        if sep and value.split():
            memory[key] = int(value.split()[0]) * 1024

    warmest = 0
    for zone in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
        raw = read(zone)
        if raw.lstrip("-").isdigit():
            warmest = max(warmest, int(raw) / 1000)

    return {
        "hostname": u.nodename,
        "kernel": u.release,
        "arch": u.machine,
        "built": u.version,
        "os": next((l.split("=", 1)[1].strip('"')
                    for l in read("/etc/os-release").splitlines()
                    if l.startswith("PRETTY_NAME=")), "Linux"),
        "board": read("/sys/firmware/devicetree/base/model", "unknown"),
        "board_name": BOARD_NAMES.get(
            read("/sys/firmware/devicetree/base/model", ""), "Unknown board"),
        "soc": (read("/sys/firmware/devicetree/base/compatible", "")
                .replace("\x00", " ").split() or ["unknown"])[-1],
        "cores": str(os.cpu_count()),
        "uptime": f"{uptime // 86400}d {uptime % 86400 // 3600}h {uptime % 3600 // 60}m",
        "load": f"{os.getloadavg()[0]:.2f}",
        "memory_used": f"{(memory.get('MemTotal', 0) - memory.get('MemAvailable', 0)) / 2**20:.0f} MB",
        "memory_total": f"{memory.get('MemTotal', 0) / 2**20:.0f} MB",
        "disk_free": f"{disk.free / 2**30:.1f} GB",
        "temperature": f"{warmest:.1f}" if warmest else "n/a",
        "time": time.strftime("%H:%M:%S"),
    }


def build_page():
    html = (HERE / "index.html").read_text()
    for name, value in values().items():
        html = html.replace("{{" + name + "}}", str(value))
    return html

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def send(self, body, kind, status=200):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html"):
            try:
                self.send(build_page().encode(), "text/html; charset=utf-8")
            except OSError as problem:
                self.send(f"Cannot read index.html: {problem}\n".encode(),
                          "text/plain", 500)
            return

        wanted = (HERE / path.lstrip("/"))
        try:
            wanted = wanted.resolve(strict=True)
            wanted.relative_to(HERE.resolve())
            if wanted.suffix == ".py":
                raise ValueError("not yours to read")
            body = wanted.read_bytes()
        except (OSError, ValueError):
            self.send(b"Not found\n", "text/plain", 404)
            return

        kind = mimetypes.guess_type(wanted.name)[0] or "application/octet-stream"
        self.send(body, kind)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s  %s\n" % (time.strftime("%H:%M:%S"), fmt % args))


if __name__ == "__main__":
    print(f"serving on http://{socket.gethostname()}.local:{PORT}/   (ctrl-c to stop)")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
