#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int array_copy_overlap(int32_t *destination, uint32_t capacity, const int32_t *source,
                       uint32_t count);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 9}, b[] = {7, 8, 9};
  CHECK(array_copy_overlap(a + 1, 4, a, 4) && a[0] == 1 && a[1] == 1 && a[4] == 4);
  CHECK(array_copy_overlap(b, 3, b, 3) && b[2] == 9);
  CHECK(!array_copy_overlap(b, 2, a, 3));
  CHECK(array_copy_overlap(0, 0, 0, 0));
  return 0;
}
