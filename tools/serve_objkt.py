"""Serve dist/ with objkt's Content-Security-Policy header (tools/objkt_csp.txt, copied from a minted
objkt HTML token), and a test page that frames a piece in a sandboxed iframe on another port:
  python3 tools/serve_objkt.py            then open http://127.0.0.1:8801/?piece=trinity"""
import http.server, os, threading, functools
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSP = open(os.path.join(root, 'tools', 'objkt_csp.txt')).read().strip()
class Piece(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Security-Policy', CSP); self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a): pass
FRAME = b"""<!doctype html><meta charset=utf-8><title>objkt sandbox test</title>
<style>html,body{margin:0;height:100%;background:#1e1f22}iframe{border:0;width:min(90vw,90vh);height:min(90vw,90vh);margin:5vh auto;display:block}</style>
<iframe id=f sandbox="allow-scripts allow-same-origin allow-pointer-lock"></iframe>
<script>const p=new URLSearchParams(location.search).get('piece')||'trinity';document.getElementById('f').src='http://127.0.0.1:8800/'+p+'/?creator=tz1test&viewer=tz1test'</script>"""
class Frame(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(FRAME)
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8800), functools.partial(Piece, directory=os.path.join(root, 'dist')))
threading.Thread(target=srv.serve_forever, daemon=True).start()
print('pieces on http://127.0.0.1:8800/  sandbox test on http://127.0.0.1:8801/?piece=trinity')
http.server.ThreadingHTTPServer(('127.0.0.1', 8801), Frame).serve_forever()
