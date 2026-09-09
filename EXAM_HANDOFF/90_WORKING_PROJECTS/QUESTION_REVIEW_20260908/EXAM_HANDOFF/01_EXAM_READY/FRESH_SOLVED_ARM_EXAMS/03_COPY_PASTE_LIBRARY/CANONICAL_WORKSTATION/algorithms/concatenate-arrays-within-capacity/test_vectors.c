#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_concatenate(const int32_t *left, uint32_t left_count, const int32_t *right,
                      uint32_t right_count, int32_t *output, uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2}, b[] = {-3, 4, 5}, o[6] = {0};
  o[5] = 77;
  CHECK(array_concatenate(a, 2, b, 3, o, 5));
  CHECK(o[0] == 1 && o[1] == 2 && o[2] == -3 && o[4] == 5 && o[5] == 77);
  o[0] = 99;
  CHECK(!array_concatenate(a, 2, b, 3, o, 4) && o[0] == 99);
  CHECK(array_concatenate(0, 0, 0, 0, 0, 0));
  return 0;
}
