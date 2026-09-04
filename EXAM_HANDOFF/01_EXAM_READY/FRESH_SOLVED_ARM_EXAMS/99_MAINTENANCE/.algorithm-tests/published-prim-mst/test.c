#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
unsigned prim_mst(const unsigned *w, size_t n, size_t start, unsigned *best,
                  unsigned char *used);
int test_main(void) {
  unsigned w[] = {0, 2, 9, 2, 0, 3, 9, 3, 0}, b[3];
  unsigned char u[3];
  CHECK(prim_mst(w, 3, 0, b, u) == 5);
  unsigned d[] = {0, 0, 0, 0};
  CHECK(prim_mst(d, 2, 0, b, u) == UINT_MAX);
  CHECK(prim_mst(d, 1, 0, b, u) == 0);
  unsigned big[] = {0, UINT_MAX - 1, 0, UINT_MAX - 1, 0, 2, 0, 2, 0};
  CHECK(prim_mst(big, 3, 0, b, u) == UINT_MAX);
  return 0;
}
