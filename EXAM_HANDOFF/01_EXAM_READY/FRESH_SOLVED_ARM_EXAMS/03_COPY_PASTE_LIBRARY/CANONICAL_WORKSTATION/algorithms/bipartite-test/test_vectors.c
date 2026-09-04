#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int graph_is_bipartite(const uint8_t *a, size_t n, int8_t *color, size_t *queue);
int test_main(void) {
  uint8_t a[] = {0, 1, 0, 1, 0, 1, 0, 1, 0};
  int8_t c[3];
  size_t q[3];
  CHECK(graph_is_bipartite(a, 3, c, q) && c[0] != c[1] && c[1] != c[2]);
  a[2] = a[6] = 1;
  CHECK(!graph_is_bipartite(a, 3, c, q));
  uint8_t self[] = {1};
  CHECK(!graph_is_bipartite(self, 1, c, q));
  return 0;
}
