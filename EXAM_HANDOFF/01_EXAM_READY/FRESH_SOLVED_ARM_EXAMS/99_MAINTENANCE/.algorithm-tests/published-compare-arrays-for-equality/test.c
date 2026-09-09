#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int arrays_equal(const int32_t *left, const int32_t *right, uint32_t count);
int test_main(void) {
  int32_t a[] = {3, -1, 8}, b[] = {3, -1, 8}, c[] = {3, -1, 7};
  CHECK(arrays_equal(a, b, 3));
  CHECK(!arrays_equal(a, c, 3));
  CHECK(arrays_equal(0, 0, 0));
  CHECK(!arrays_equal(0, b, 3));
  return 0;
}
