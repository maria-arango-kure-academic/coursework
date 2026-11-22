#!/usr/bin/env python3
"""
Tiny anonymous JSON blob store. Stdlib only. No dependencies.

Endpoints:
  POST   /api/blob          → create. Body is JSON. Returns {id, location}.
  GET    /api/blob/<id>     → read.   Returns the stored JSON.
  PUT    /api/blob/<id>     → write.  Body is JSON. Replaces the blob.
  DELETE /api/blob/<id>     → delete. Returns 204.
  GET    /healthz           → 200 OK if alive.

Environment:
  BLOB_DATA_DIR     where blobs are stored on disk. Default /data.
  BLOB_PORT         port to listen on. Default 8088.
  BLOB_ALLOW_ORIGIN CORS Access-Control-Allow-Origin. Default *.
  BLOB_MAX_BYTES    max body size. Default 256000 (256 KB).

Storage shape: each blob is a single JSON file at /data/<id>.json.
IDs are URL-safe random tokens.
"""

import json
import os
import secrets
import sys
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATA_DIR = os.environ.get("BLOB_DATA_DIR", "/data")
ALLOW_ORIGIN = os.environ.get("BLOB_ALLOW_ORIGIN", "*")
PORT = int(os.environ.get("BLOB_PORT", "8088"))
MAX_BYTES = int(os.environ.get("BLOB_MAX_BYTES", "262144"))

ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

os.makedirs(DATA_DIR, exist_ok=True)


def path_for(blob_id):
    if not ID_RE.match(blob_id):
        return None
    return os.path.join(DATA_DIR, blob_id + ".json")


class Handler(BaseHTTPRequestHandler):
    server_version = "BreweryBlob/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOW_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.send_header("Access-Control-Expose-Headers", "Location")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send(self, code, body=None, content_type="application/json", extra_headers=None):
        self.send_response(code)
        self._cors()
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        if body is None:
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if isinstance(body, (dict, list)):
            data = json.dumps(body).encode("utf-8")
            content_type = "application/json"
        elif isinstance(body, bytes):
            data = body
        else:
            data = str(body).encode("utf-8")
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        n = int(self.headers.get("Content-Length", "0") or "0")
        if n <= 0:
            return b""
        if n > MAX_BYTES:
            return None
        return self.rfile.read(n)

    def do_OPTIONS(self):
        self._send(204)

    def do_GET(self):
        if self.path == "/healthz":
            return self._send(200, {"ok": True})
        if not self.path.startswith("/api/blob/"):
            return self._send(404, {"error": "not found"})
        blob_id = self.path.split("/api/blob/", 1)[1].split("?", 1)[0]
        p = path_for(blob_id)
        if not p or not os.path.exists(p):
            return self._send(404, {"error": "not found"})
        with open(p, "rb") as f:
            data = f.read()
        self._send(200, data, content_type="application/json")

    def do_POST(self):
        if self.path != "/api/blob":
            return self._send(404, {"error": "not found"})
        body = self._read_body()
        if body is None:
            return self._send(413, {"error": "payload too large"})
        try:
            json.loads(body or b"null")
        except Exception:
            return self._send(400, {"error": "invalid json"})
        blob_id = secrets.token_urlsafe(9)
        with open(path_for(blob_id), "wb") as f:
            f.write(body or b"null")
        loc = "/api/blob/" + blob_id
        self._send(201, {"id": blob_id, "location": loc}, extra_headers={"Location": loc})

    def do_PUT(self):
        if not self.path.startswith("/api/blob/"):
            return self._send(404, {"error": "not found"})
        blob_id = self.path.split("/api/blob/", 1)[1].split("?", 1)[0]
        p = path_for(blob_id)
        if not p:
            return self._send(400, {"error": "invalid id"})
        body = self._read_body()
        if body is None:
            return self._send(413, {"error": "payload too large"})
        try:
            json.loads(body or b"null")
        except Exception:
            return self._send(400, {"error": "invalid json"})
        with open(p, "wb") as f:
            f.write(body or b"null")
        self._send(200, {"ok": True})

    def do_DELETE(self):
        if not self.path.startswith("/api/blob/"):
            return self._send(404, {"error": "not found"})
        blob_id = self.path.split("/api/blob/", 1)[1].split("?", 1)[0]
        p = path_for(blob_id)
        if p and os.path.exists(p):
            os.remove(p)
        self._send(204)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - - %s\n" % (self.address_string(), fmt % args))


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    sys.stderr.write("brewery-blob listening on 0.0.0.0:%d, data dir %s, allow-origin %s\n" % (PORT, DATA_DIR, ALLOW_ORIGIN))
    sys.stderr.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
