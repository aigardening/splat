"""Headless check of a built piece inside the objkt sandbox test page (tools/serve_objkt.py must be running).
  python3 tools/shoot.py trinity out.png [size] [wait_s] [--still]   (--still holds the opening view: use it for the cover)
Prints console errors and CSP violations; exits 1 if the piece did not render."""
import sys, time
from playwright.sync_api import sync_playwright
args = [a for a in sys.argv if a != '--still']
piece, out = args[1], args[2]
size = int(args[3]) if len(args) > 3 else 800; wait = float(args[4]) if len(args) > 4 else 3
msgs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': size, 'height': size})
    pg.on('console', lambda m: msgs.append(f'{m.type}: {m.text}'))
    pg.on('pageerror', lambda e: msgs.append(f'pageerror: {e}'))
    pg.goto(f'http://127.0.0.1:8800/{piece}/?creator=tz1test&viewer=tz1test' + ('&still' if '--still' in sys.argv else ''))
    t0 = time.time(); ok = False
    while time.time() - t0 < 180:
        st = pg.evaluate("[document.body.dataset.ready, document.body.dataset.error]")
        if st[0] or st[1]: ok = bool(st[0]); break
        time.sleep(1)
    print('ready' if ok else 'NOT READY', round(time.time() - t0, 1), 's', st)
    time.sleep(wait)
    import base64
    url = pg.evaluate("document.getElementById('c').toDataURL('image/png')")
    open(out, 'wb').write(base64.b64decode(url.split(',')[1]))
    b.close()
for m in msgs: print(m)
sys.exit(0 if ok else 1)
