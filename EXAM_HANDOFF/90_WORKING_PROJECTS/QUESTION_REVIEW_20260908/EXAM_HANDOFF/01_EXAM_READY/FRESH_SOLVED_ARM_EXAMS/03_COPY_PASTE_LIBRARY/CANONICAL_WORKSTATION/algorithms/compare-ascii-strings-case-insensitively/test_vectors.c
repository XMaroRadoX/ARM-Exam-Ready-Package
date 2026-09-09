#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t strings_compare_ascii_casefold(const uint8_t *left, uint32_t left_capacity,
                                       const uint8_t *right, uint32_t right_capacity);
int test_main(void) {
  uint8_t a[] = "Arm", b[] = "aRM", c[] = "abd", bad[] = {'x'};
  CHECK(strings_compare_ascii_casefold(a, 4, b, 4) == 0);
  CHECK(strings_compare_ascii_casefold(a, 4, c, 4) == 1);
  CHECK(strings_compare_ascii_casefold(bad, 1, b, 4) == 2);
  return 0;
}
