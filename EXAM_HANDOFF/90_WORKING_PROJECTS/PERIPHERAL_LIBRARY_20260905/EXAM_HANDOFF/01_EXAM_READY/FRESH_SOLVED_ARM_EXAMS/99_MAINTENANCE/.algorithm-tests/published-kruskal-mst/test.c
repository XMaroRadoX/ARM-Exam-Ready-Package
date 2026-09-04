#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {
  size_t u, v;
  unsigned w;
} MstEdge;
unsigned kruskal_mst(const MstEdge *edges, size_t m, size_t n, size_t *parent);
int test_main(void) {
  MstEdge e[] = {{0, 1, 2}, {1, 2, 3}, {0, 2, 9}};
  size_t p[3];
  CHECK(kruskal_mst(e, 3, 3, p) == 5);
  e[2].v = 3;
  CHECK(kruskal_mst(e, 3, 3, p) == UINT_MAX);
  CHECK(kruskal_mst(0, 0, 1, p) == 0);
  CHECK(kruskal_mst(0, 0, 2, p) == UINT_MAX);
  return 0;
}
