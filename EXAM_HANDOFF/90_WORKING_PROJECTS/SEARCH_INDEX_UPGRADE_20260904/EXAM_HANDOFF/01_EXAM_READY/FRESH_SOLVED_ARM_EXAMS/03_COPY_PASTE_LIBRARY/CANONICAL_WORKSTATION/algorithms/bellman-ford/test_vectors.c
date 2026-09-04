#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {
  size_t from, to;
  int weight;
} Edge;
int bellman_ford(const Edge *edges, size_t m, size_t n, size_t start, int *distance);
int test_main(void) {
  Edge e[] = {{0, 1, 4}, {1, 2, -2}, {0, 2, 9}};
  int d[3];
  CHECK(bellman_ford(e, 3, 3, 0, d) && d[0] == 0 && d[1] == 4 && d[2] == 2);
  e[2].from = 9;
  CHECK(!bellman_ford(e, 3, 3, 0, d));
  Edge cyc[] = {{0, 1, 1}, {1, 0, -2}};
  CHECK(!bellman_ford(cyc, 2, 2, 0, d));
  CHECK(bellman_ford(0, 0, 3, 0, d) && d[1] == INT_MAX);
  return 0;
}
