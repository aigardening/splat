# splats

A small, self-contained Gaussian splat viewer for minting splats as interactive HTML pieces on
[objkt](https://objkt.com), plus the pieces themselves.

`index.html` is the whole viewer: WebGL2, no libraries, nothing fetched except the `.spz` file next
to it. It reads Niantic [SPZ](https://github.com/nianticlabs/spz) files (versions 2 and 3, gzip),
sorts the splats back to front in a blob worker, and evaluates view-dependent colour (spherical
harmonics up to degree 3). The piece opens on a set view and turns slowly; drag to orbit, scroll or
pinch to zoom, and the turn eases back in when you let go.

## Pieces

| Piece | Splats | Size | Source |
|---|---|---|---|
| `pieces/trinity` | 408,635 | 8.4 MB | Polycam capture, 142 photos; one stray clump from the room removed |

Each piece folder holds the `.spz`, a `config.json` (opening view, spin, background) and `cover.jpg`.

## Build and test

```bash
python3 tools/build.py pieces/trinity          # dist/trinity/ and dist/trinity.zip (the file to mint)
python3 tools/serve_objkt.py                   # serves dist/ under objkt's Content-Security-Policy
open "http://127.0.0.1:8801/?piece=trinity"    # the piece in a sandboxed iframe, as on objkt
python3 tools/shoot.py trinity shot.png 1200 1 --still    # headless render; --still holds the opening view
```

`tools/objkt_csp.txt` is the Content-Security-Policy taken from a minted objkt HTML token.

## From a Polycam capture to a piece

1. Export the splat from Polycam as **Splat PLY**.
2. `python3 tools/clean_splat.py in.ply clean.ply --centre x y z --radius r --hist` removes far-off clumps; pick the radius in an empty gap of the histogram.
3. Convert with Niantic's library: build `tools/ply_to_spz_v.cpp` against [nianticlabs/spz](https://github.com/nianticlabs/spz)
   (`clang++ -std=c++17 -O2 -Ispz/src spz/src/cc/*.cc tools/ply_to_spz_v.cpp -lz -lzstd`), then
   `./ply_to_spz_v clean.ply piece.spz 3`. Version 3 is gzip, which browsers decode natively.
4. Make `pieces/<name>/config.json` (copy Trinity's; Polycam files need `"flipY": true`), build, test, render the cover.
