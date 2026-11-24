"""Build a mintable folder and zip for one piece:  python3 tools/build.py pieces/trinity
Writes dist/<piece>/index.html (config inlined, title set) next to a copy of the .spz or .glb, and dist/<piece>.zip.
config.json "viewer": "glb" uses glb.html and copies vendor/three into the piece."""
import json, os, re, shutil, sys, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
piece = os.path.abspath(sys.argv[1]); name = os.path.basename(piece.rstrip('/'))
cfg = json.load(open(os.path.join(piece, 'config.json')))
title = cfg.pop('title', name)
viewer = cfg.pop('viewer', 'splat')
html = open(os.path.join(root, 'glb.html' if viewer == 'glb' else 'index.html')).read()
block = 'const CONFIG = ' + json.dumps(cfg, indent=2) + ';\n'
html = re.sub(r'/\*CONFIG\*/.*?/\*END CONFIG\*/', lambda m: '/*CONFIG*/\n' + block + '/*END CONFIG*/', html, flags=re.S)
html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, count=1)
out = os.path.join(root, 'dist', name); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
open(os.path.join(out, 'index.html'), 'w').write(html)
shutil.copy(os.path.join(piece, cfg['file']), out)
if viewer == 'glb':                                   # three.js travels with the piece
    shutil.copytree(os.path.join(root, 'vendor', 'three'), os.path.join(out, 'three'))
z = os.path.join(root, 'dist', name + '.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for d, _, fs in sorted(os.walk(out)):
        for f in sorted(fs): zf.write(os.path.join(d, f), os.path.relpath(os.path.join(d, f), out))
print('built', out, 'and', z, round(os.path.getsize(z) / 1e6, 2), 'MB')
