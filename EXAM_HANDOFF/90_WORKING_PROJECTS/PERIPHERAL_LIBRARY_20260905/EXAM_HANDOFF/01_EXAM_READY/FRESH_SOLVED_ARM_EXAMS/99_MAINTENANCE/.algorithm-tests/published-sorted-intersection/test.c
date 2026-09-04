#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t sorted_intersection(const int32_t *a, uint32_t n, const int32_t *b, uint32_t m,
                             int32_t *out, uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2, 2}, b[] = {2, 3}, o[6] = {0};
  o[5] = 77;
  CHECK(sorted_intersection(a, 3, b, 2, o, 5) == 1 && o[0] == 2 && o[5] == 77);
  CHECK(sorted_intersection(a, 3, b, 2, o, 4) == UINT32_MAX);
  CHECK(sorted_intersection(0, 0, 0, 0, 0, 0) == 0);
  return 0;
}
