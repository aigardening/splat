// ply_to_spz with a chosen SPZ version (3 = gzip, widest viewer support; 4 = zstd).
// Build: clang++ -std=c++17 -O2 -I<spz>/src <spz>/src/cc/*.cc ply_to_spz_v.cpp -lz -lzstd
#include <iostream>
#include <cstdlib>
#include "cc/load-spz.h"
int main(int argc, char *argv[]) {
  if (argc < 3) { std::cerr << "usage: ply_to_spz_v in.ply out.spz [version]\n"; return 1; }
  spz::UnpackOptions u; spz::GaussianCloud g = spz::loadSplatFromPly(argv[1], u);
  spz::PackOptions p; if (argc > 3) p.version = std::atoi(argv[3]);
  std::cout << "points " << g.numPoints << " shDegree " << g.shDegree << " version " << p.version << "\n";
  return spz::saveSpz(g, p, argv[2]) ? 0 : 2;
}
