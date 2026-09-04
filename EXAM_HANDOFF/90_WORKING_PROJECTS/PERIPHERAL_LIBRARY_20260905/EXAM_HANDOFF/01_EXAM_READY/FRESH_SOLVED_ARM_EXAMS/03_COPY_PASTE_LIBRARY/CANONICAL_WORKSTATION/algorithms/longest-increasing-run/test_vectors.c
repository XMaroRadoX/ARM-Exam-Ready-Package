#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t longest_increasing_run(const int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {1, 2, 2, 3, 4}, b[] = {-1, -1, -1};
  CHECK(longest_increasing_run(a, 5) == 3);
  CHECK(longest_increasing_run(b, 3) == 1);
  CHECK(longest_increasing_run(0, 0) == 0);
  return 0;
}
