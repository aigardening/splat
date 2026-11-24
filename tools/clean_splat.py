"""Drop splats further than a radius from a centre point (Polycam builds clumps from the room far from the object).
  python3 tools/clean_splat.py in.ply out.ply --centre x y z --radius r [--hist]
--hist prints the distance histogram first, so the radius can sit in an empty gap."""
import argparse, numpy as np
p = argparse.ArgumentParser(); p.add_argument('src'); p.add_argument('dst')
p.add_argument('--centre', nargs=3, type=float, required=True); p.add_argument('--radius', type=float, required=True)
p.add_argument('--hist', action='store_true'); g = p.parse_args()
f = open(g.src, 'rb').read(); i = f.index(b'end_header\n') + 11; hdr = f[:i].decode('latin1')
n = int(hdr.split('element vertex ')[1].split()[0]); k = hdr.count('property float')
assert k == len([l for l in hdr.splitlines() if l.startswith('property')]), 'only all-float PLYs are handled'
a = np.frombuffer(f[i:i + 4 * n * k], '<f4').reshape(n, k)
r = np.linalg.norm(a[:, :3] - np.array(g.centre, np.float32), axis=1)
if g.hist:
    h, e = np.histogram(r, bins=[0, .5, 1, 1.5, 2, 3, 5, 8, 12, 20, 50, np.inf])
    for c, lo, hi in zip(h, e[:-1], e[1:]): print(f'{lo:6.1f} - {hi:6.1f}  {c}')
b = a[r < g.radius]
open(g.dst, 'wb').write(hdr.replace(f'element vertex {n}', f'element vertex {len(b)}').encode('latin1') + b.astype('<f4').tobytes())
print(n, '->', len(b), 'splats, removed', n - len(b))
