#include <limits.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {
  size_t u, v;
  unsigned w;
} MstEdge;
static size_t mst_root(size_t *p, size_t x) {
  while (p[x] != x) {
    p[x] = p[p[x]];
    x = p[x];
  }
  return x;
}
unsigned kruskal_mst(const MstEdge *e, size_t m, size_t n, size_t *p) {
  if (!p || !n || n > 256 || (!e && m) || m > UINT32_MAX / 12)
    return UINT_MAX;
  for (size_t i = 0; i < m; i++)
    if (e[i].u >= n || e[i].v >= n || (i && e[i].w < e[i - 1].w))
      return UINT_MAX;
  for (size_t i = 0; i < n; i++)
    p[i] = i;
  size_t used = 0;
  unsigned total = 0;
  for (size_t i = 0; i < m && used + 1 < n; i++) {
    size_t a = mst_root(p, e[i].u), b = mst_root(p, e[i].v);
    if (a != b) {
      if (e[i].w >= UINT_MAX - total)
        return UINT_MAX;
      p[b] = a;
      total += e[i].w;
      used++;
    }
  }
  return used + 1 == n ? total : UINT_MAX;
}
