#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_pair_sum_unsorted(const int32_t *values, uint32_t count, int32_t target,
                            uint32_t *first_out, uint32_t *second_out);
int test_main(void) {
  int32_t a[] = {8, 3, 5, 2};
  uint32_t i = 99, j = 99;
  CHECK(array_pair_sum_unsorted(a, 4, 10, &i, &j) && i == 0 && j == 3);
  i = 99;
  j = 99;
  CHECK(!array_pair_sum_unsorted(a, 4, 99, &i, &j) && i == 99 && j == 99);
  CHECK(!array_pair_sum_unsorted(a, 4, 10, &i, &i));
  return 0;
}
