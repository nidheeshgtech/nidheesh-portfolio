"""Preview dist/ like Cloudflare Pages: clean URLs (/work/ai71), 404.html, and the rules in _headers.
  python3 tools/serve_dist.py   ->  http://localhost:8790"""
import os, http.server, socketserver, fnmatch
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
PORT = int(os.environ.get('PORT', 8790))

def load_headers():
    rules, cur = [], None
    for line in open(os.path.join(ROOT, '_headers')):
        if not line.strip():
            continue
        if not line.startswith(' '):
            cur = (line.strip(), {}); rules.append(cur)
        else:
            k, v = line.strip().split(':', 1); cur[1][k.strip()] = v.strip()
    return rules
RULES = load_headers()

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def send_head(self):
        path = self.path.split('?')[0].split('#')[0]
        if path.endswith('.html') and path != '/404.html':
            self.send_response(308); self.send_header('Location', path[:-5].replace('/index', '/') or '/'); self.end_headers(); return None
        fs = os.path.join(ROOT, path.lstrip('/'))
        if not os.path.splitext(path)[1] and path != '/' and os.path.isfile(fs + '.html'):
            self.path = path + '.html'
        elif not os.path.exists(fs):
            self.path = '/404.html'; self._404 = True
        return super().send_head()
    def send_response(self, code, message=None):
        if getattr(self, '_404', False) and code == 200: code = 404
        super().send_response(code, message)
    def end_headers(self):
        path = self.path.split('?')[0]
        for pat, hs in RULES:
            if fnmatch.fnmatch(path, pat) or path == pat:
                for k, v in hs.items(): self.send_header(k, v)
        super().end_headers()
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), H) as s:
    print(f'serving dist/ on http://localhost:{PORT}')
    s.serve_forever()
