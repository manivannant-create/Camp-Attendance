"""Local dashboard server with a built-in proxy (no CORS issues, no pip installs).

Run:   python server.py
Open:  http://localhost:8000
"""
import os
import re
import urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode

API = "https://lepweknn8k.execute-api.ap-south-1.amazonaws.com/api/msmsbms/bmsCampTeacherAttendanceget"
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teacher_attendance_dashboard.html")
PORT = int(os.environ.get("PORT", 8000))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            with open(PAGE, "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if url.path == "/health":
            return self._send(200, b"bms-proxy-ok", "text/plain")
        if url.path == "/proxy":
            q = parse_qs(url.query)
            camp = q.get("campId", [""])[0]
            date = q.get("attendanceDate", [""])[0]
            # Only forward well-formed values, so this can't be used as an open proxy
            if not (re.fullmatch(r"\d{1,6}", camp) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)):
                return self._send(400, b'{"error":"bad campId or attendanceDate"}', "application/json")
            target = API + "?" + urlencode({"campId": camp, "attendanceDate": date})
            try:
                with urllib.request.urlopen(target, timeout=30) as r:
                    return self._send(200, r.read(), "application/json; charset=utf-8")
            except Exception as e:
                return self._send(502, ('{"error":"%s"}' % str(e).replace('"', "'")).encode(), "application/json")
        self._send(404, b"Not found", "text/plain")

    def log_message(self, fmt, *args):
        pass  # keep the console quiet


if __name__ == "__main__":
    print(f"Dashboard running on port {PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
