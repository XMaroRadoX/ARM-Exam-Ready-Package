#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int floyd_warshall(int *distance, size_t n, int infinity);
int test_main(void) {
  int d[] = {0, 4, 9, 999, 0, -2, 999, 999, 0};
  CHECK(floyd_warshall(d, 3, 999) && d[2] == 2 && d[3] == 999);
  int cyc[] = {0, -1, -1, 0};
  CHECK(!floyd_warshall(cyc, 2, 999));
  int big[] = {0, INT_MAX - 1, INT_MAX - 1, 0};
  CHECK(!floyd_warshall(big, 2, INT_MAX));
  return 0;
}
