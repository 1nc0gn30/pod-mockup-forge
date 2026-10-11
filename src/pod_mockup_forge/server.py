"""POD Mockup Forge - High-Performance Threaded HTTP Server (Port 8119)
Zero-dependency Python 3.10+ Standard Library HTTP & Static Server
"""

from typing import Optional
import http.server
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any

from .templates import get_all_templates, MOCKUP_TEMPLATES
from .composite_engine import MockupCompositeEngine
from .etsy_specs import EtsyPhotoAuditor


def _default_bind_host() -> str:
    """Bind address: localhost unless explicitly opted in via $ZOTH_BIND_HOST or
    $HOST (IP literal only; zsh sets HOST to the hostname) or --host."""
    import ipaddress, os
    for var in ("ZOTH_BIND_HOST", "HOST"):
        val = os.environ.get(var, "").strip()
        if val == "localhost":
            return "127.0.0.1"
        if val:
            try:
                ipaddress.ip_address(val)
                return val
            except ValueError:
                pass
    return "127.0.0.1"


PORT = int(os.environ.get("MOCKUP_FORGE_PORT", 8119))
START_TIME = time.time()

TELEMETRY = {
    "mockups_rendered": 0,
    "photo_audits_performed": 0,
    "packs_planned": 0
}

PUBLIC_DIR = Path(__file__).resolve().parent.parent.parent / "public"

class MockupForgeHandler(http.server.SimpleHTTPRequestHandler):
    """Zero-dependency HTTP Handler for POD Mockup Forge API and Web UI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({
                "status": "healthy",
                "service": "pod-mockup-forge",
                "version": "1.0.0",
                "port": PORT,
                "uptime_seconds": round(time.time() - START_TIME, 1)
            })
            return

        if path == "/api/stats":
            self._send_json({
                "telemetry": TELEMETRY,
                "uptime_seconds": round(time.time() - START_TIME, 1)
            })
            return

        if path == "/api/templates":
            templates = get_all_templates()
            self._send_json({
                "count": len(templates),
                "templates": templates
            })
            return

        if path == "/api/carousel_plan":
            plan = EtsyPhotoAuditor.generate_listing_pack_plan()
            self._send_json(plan)
            return

        # Fallback to static web assets
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            payload = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception as e:
            self._send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        if path == "/api/render":
            tpl_id = payload.get("template_id", "gildan_18000_flatlay")
            art_url = payload.get("artwork_url", "https://storage.googleapis.com/nullai-assets/designs/flower-wreath.png")
            color = payload.get("color_hex")
            watermark = bool(payload.get("watermark", False))

            spec = MockupCompositeEngine.render_scene_spec(
                template_id=tpl_id,
                artwork_url=art_url,
                color_hex=color,
                watermark=watermark
            )

            TELEMETRY["mockups_rendered"] += 1

            self._send_json({
                "render_spec": spec,
                "status": "success"
            })
            return

        if path == "/api/audit":
            w = int(payload.get("width_px", 2000))
            h = int(payload.get("height_px", 2000))
            mb = float(payload.get("file_size_mb", 3.2))

            audit = EtsyPhotoAuditor.audit_image(w, h, mb)
            TELEMETRY["photo_audits_performed"] += 1

            self._send_json({
                "audit": audit,
                "status": "success"
            })
            return

        self._send_json({"error": f"Endpoint not found: {path}"}, status=404)

def run_server(port: int = PORT, host: Optional[str] = None):
    host = host or _default_bind_host()
    server_address = (host, port)
    httpd = http.server.ThreadingHTTPServer(server_address, MockupForgeHandler)
    print(f"🚀 POD Mockup Forge listening on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down POD Mockup Forge gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    _ap = argparse.ArgumentParser(description="Run the HTTP server and web UI")
    _ap.add_argument("--host", default=None, help="Host interface (default: 127.0.0.1 or $ZOTH_BIND_HOST; use 0.0.0.0 only on trusted networks)")
    _ap.add_argument("--port", type=int, default=PORT)
    _a = _ap.parse_args()
    run_server(port=_a.port, host=_a.host)
