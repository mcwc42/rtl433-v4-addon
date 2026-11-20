# Kozy Art Proxy: the ESP32 display asks this for album art over plain, local
# HTTP; this (on the Pi, which has reliable internet + TLS) fetches the real
# cover and relays the bytes. Keeps TLS/internet off the memory-tight ESP32.
#
#   GET /cover?u=<https Apple-CDN url>  ->  the JPEG (relayed)
#
# Only https URLs on Apple's CDN are allowed (not an open proxy).
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8099
ALLOWED_SUFFIXES = (".mzstatic.com",)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if not (parsed.path == "/" or parsed.path.startswith("/cover")):
            self.send_error(404)
            return
        u = (urllib.parse.parse_qs(parsed.query).get("u") or [""])[0]
        host = (urllib.parse.urlparse(u).hostname or "")
        if not u.startswith("https://") or not any(host.endswith(s) for s in ALLOWED_SUFFIXES):
            self.send_error(400, "only https Apple-CDN urls allowed")
            return
        try:
            with urllib.request.urlopen(u, timeout=8) as r:
                data = r.read()
        except Exception as e:                       # noqa: BLE001
            self.send_error(502, "fetch failed: %s" % e)
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print("Kozy Art Proxy on :%d" % PORT, flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
