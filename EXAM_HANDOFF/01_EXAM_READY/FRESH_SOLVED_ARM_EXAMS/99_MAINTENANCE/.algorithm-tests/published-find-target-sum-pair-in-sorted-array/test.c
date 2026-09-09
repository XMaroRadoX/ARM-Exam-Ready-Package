#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_pair_sum_sorted(const int32_t *values, uint32_t count, int32_t target,
                          uint32_t *first_out, uint32_t *second_out);
int test_main(void) {
  int32_t a[] = {1, 2, 4, 7, 9};
  uint32_t i = 99, j = 99;
  CHECK(array_pair_sum_sorted(a, 5, 11, &i, &j) && i == 1 && j == 4);
  i = 99;
  j = 99;
  CHECK(!array_pair_sum_sorted(a, 5, 99, &i, &j) && i == 99 && j == 99);
  CHECK(!array_pair_sum_sorted(a, 5, 10, &i, &i));
  return 0;
}
