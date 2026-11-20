# Kozy Art Proxy: the ESP32 display asks this for album art over plain, local
# HTTP. This (on the Pi) fetches Home Assistant's own media-player art image
# (which works for any source — albums, radio, DJ mixes, Sonos) and resizes it
# to a small 200x200 JPEG the memory-tight ESP32 can decode. Keeps TLS/internet
# and big images off the display.
#
#   GET /cover?u=<http Home-Assistant media_player_proxy url>  ->  200x200 JPEG
#
# Only urls on the local Home Assistant host are allowed (not an open proxy).
import io
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image

PORT = 8099
ALLOWED_HOST = "192.168.4.200"      # Home Assistant
SIZE = 200


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if not (parsed.path == "/" or parsed.path.startswith("/cover")):
            self.send_error(404)
            return
        u = (urllib.parse.parse_qs(parsed.query).get("u") or [""])[0]
        if urllib.parse.urlparse(u).hostname != ALLOWED_HOST:
            self.send_error(400, "only local Home Assistant urls allowed")
            return
        try:
            raw = urllib.request.urlopen(u, timeout=10).read()
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img.thumbnail((SIZE, SIZE), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=85)
            data = buf.getvalue()
        except Exception as e:                       # noqa: BLE001
            self.send_error(502, "art fetch/resize failed: %s" % e)
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print("Kozy Art Proxy on :%d (resize to %dpx)" % (PORT, SIZE), flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
