"""Build a mintable folder and zip for one piece:  python3 tools/build.py pieces/trinity
Writes dist/<piece>/index.html (config inlined, title set) next to a copy of the .spz, and dist/<piece>.zip."""
import json, os, re, shutil, sys, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
piece = os.path.abspath(sys.argv[1]); name = os.path.basename(piece.rstrip('/'))
cfg = json.load(open(os.path.join(piece, 'config.json')))
title = cfg.pop('title', name)
html = open(os.path.join(root, 'index.html')).read()
block = 'const CONFIG = ' + json.dumps(cfg, indent=2) + ';\n'
html = re.sub(r'/\*CONFIG\*/.*?/\*END CONFIG\*/', lambda m: '/*CONFIG*/\n' + block + '/*END CONFIG*/', html, flags=re.S)
html = html.replace('<title>splat</title>', f'<title>{title}</title>')
out = os.path.join(root, 'dist', name); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
open(os.path.join(out, 'index.html'), 'w').write(html)
shutil.copy(os.path.join(piece, cfg['file']), out)
z = os.path.join(root, 'dist', name + '.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(os.listdir(out)): zf.write(os.path.join(out, f), f)
print('built', out, 'and', z, round(os.path.getsize(z) / 1e6, 2), 'MB')
