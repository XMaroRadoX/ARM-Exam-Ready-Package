#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int astar_grid(const unsigned char *wall, size_t rows, size_t cols, size_t start,
               size_t goal, unsigned *g, unsigned char *closed);
int test_main(void) {
  unsigned char w[6] = {0}, c[6];
  unsigned g[6];
  CHECK(astar_grid(w, 2, 3, 0, 5, g, c) && g[5] == 3);
  w[1] = w[4] = 1;
  CHECK(!astar_grid(w, 2, 3, 0, 5, g, c));
  w[1] = w[4] = 0;
  w[0] = 1;
  CHECK(!astar_grid(w, 2, 3, 0, 0, g, c));
  w[0] = 0;
  CHECK(astar_grid(w, 2, 3, 0, 0, g, c) && g[0] == 0);
  CHECK(!astar_grid(w, 0, 3, 0, 0, g, c));
  return 0;
}
