#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int astar_grid(const unsigned char *w, size_t rows, size_t cols, size_t start,
               size_t goal, unsigned *g, unsigned char *c) {
  if (!w || !g || !c || !rows || !cols || rows > 256 || cols > 256)
    return 0;
  size_t n = rows * cols;
  if (start >= n || goal >= n || w[start] || w[goal])
    return 0;
  for (size_t i = 0; i < n; i++) {
    g[i] = UINT_MAX;
    c[i] = 0;
  }
  g[start] = 0;
  for (;;) {
    size_t v = n;
    unsigned best = UINT_MAX;
    for (size_t i = 0; i < n; i++)
      if (!c[i] && g[i] != UINT_MAX) {
        size_t r = i / cols, x = i % cols, gr = goal / cols, gx = goal % cols;
        unsigned h =
            (unsigned)((r > gr ? r - gr : gr - r) + (x > gx ? x - gx : gx - x));
        if (g[i] + h < best) {
          best = g[i] + h;
          v = i;
        }
      }
    if (v == n)
      return 0;
    if (v == goal)
      return 1;
    c[v] = 1;
    size_t next[4], count = 0;
    if (v >= cols)
      next[count++] = v - cols;
    if (v + cols < n)
      next[count++] = v + cols;
    if (v % cols)
      next[count++] = v - 1;
    if (v % cols + 1 < cols)
      next[count++] = v + 1;
    for (size_t j = 0; j < count; j++) {
      size_t x = next[j];
      if (!w[x] && !c[x] && g[v] + 1 < g[x])
        g[x] = g[v] + 1;
    }
  }
}
