#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int subset_sum(const unsigned short *a, size_t n, size_t target,
               unsigned char *reachable);
int test_main(void) {
  unsigned short a[] = {3, 5};
  unsigned char r[10];
  CHECK(!subset_sum(a, 2, 6, r));
  CHECK(subset_sum(a, 2, 8, r));
  CHECK(subset_sum(a, 0, 0, r));
  return 0;
}
