#include <limits.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {
  size_t from, to;
  int weight;
} Edge;
int bellman_ford(const Edge *e, size_t m, size_t n, size_t s, int *d) {
  if (!d || (!e && m) || s >= n || n > 256 || m > UINT32_MAX / 12)
    return 0;
  for (size_t i = 0; i < m; i++)
    if (e[i].from >= n || e[i].to >= n)
      return 0;
  for (size_t i = 0; i < n; i++)
    d[i] = INT_MAX;
  d[s] = 0;
  for (size_t k = 1; k <= n; k++) {
    int changed = 0;
    for (size_t i = 0; i < m; i++)
      if (d[e[i].from] != INT_MAX) {
        int64_t x = (int64_t)d[e[i].from] + e[i].weight;
        if (x < INT_MIN || x >= INT_MAX)
          return 0;
        if (x < d[e[i].to]) {
          if (k == n)
            return 0;
          d[e[i].to] = (int)x;
          changed = 1;
        }
      }
    if (!changed)
      return 1;
  }
  return 1;
}
