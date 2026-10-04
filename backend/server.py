#!/usr/bin/env python3
"""Tiny REST backend for the CN project.
Run:  python3 server.py A 3001   (Mac 3, Backend A)
      python3 server.py B 3002   (Mac 4, Backend B)
"""
import datetime, hashlib, json, socket, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BACKEND_ID = sys.argv[1] if len(sys.argv) > 1 else "A"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
HOST = socket.gethostname()

# /api/info is IDENTICAL on both backends, so its ETag matches no matter
# which backend answers -> conditional requests (304) work behind the LB.
INFO_BODY = json.dumps({
    "project": "Private Network Service Platform",
    "topics": ["DNS", "TCP", "TLS", "HTTP", "Load balancing", "Caching"],
    "version": 1,
}, indent=2).encode()
INFO_ETAG = '"' + hashlib.sha1(INFO_BODY).hexdigest()[:16] + '"'


class Handler(BaseHTTPRequestHandler):
    server_version = "TeamBackend/1.0"

    def reply(self, code, body=b"", ctype="application/json", headers=None):
        self.send_response(code)
        self.send_header("X-Backend", BACKEND_ID)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        if code != 304:
            self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if code != 304 and self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            html = (f"<h1>Backend {BACKEND_ID} is running</h1>"
                    f"<p>Host {HOST}, port {PORT}</p>"
                    "<p><a href='/api/status'>/api/status</a> | "
                    "<a href='/api/info'>/api/info</a></p>")
            self.reply(200, html.encode(), "text/html", {"Cache-Control": "no-store"})
        elif path == "/api/status":
            data = {"backend": BACKEND_ID, "status": "ok", "host": HOST,
                    "port": PORT,
                    "time": datetime.datetime.now().isoformat(timespec="seconds")}
            self.reply(200, json.dumps(data).encode(), headers={"Cache-Control": "no-store"})
        elif path == "/api/info":
            cache = {"Cache-Control": "public, max-age=60", "ETag": INFO_ETAG}
            if self.headers.get("If-None-Match") == INFO_ETAG:
                self.reply(304, headers=cache)          # client copy still valid
            else:
                self.reply(200, INFO_BODY, headers=cache)
        else:
            self.reply(404, json.dumps({"error": "not found", "backend": BACKEND_ID}).encode())

    def do_HEAD(self):
        self.do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)   # 0.0.0.0 = reachable from the LAN
    print(f"Backend {BACKEND_ID} listening on 0.0.0.0:{PORT}  (Ctrl+C to stop)")
    server.serve_forever()
