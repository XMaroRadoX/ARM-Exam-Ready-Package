#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t arrays_compare_lexicographic(const int32_t *left, uint32_t left_count,
                                     const int32_t *right, uint32_t right_count);
int test_main(void) {
  int32_t a[] = {1, 9}, b[] = {1, 7, 100}, c[] = {1, 9, 0};
  CHECK(arrays_compare_lexicographic(a, 2, b, 3) == 1);
  CHECK(arrays_compare_lexicographic(a, 2, c, 3) == -1);
  CHECK(arrays_compare_lexicographic(a, 2, a, 2) == 0);
  CHECK(arrays_compare_lexicographic(0, 1, a, 2) == 2);
  return 0;
}
