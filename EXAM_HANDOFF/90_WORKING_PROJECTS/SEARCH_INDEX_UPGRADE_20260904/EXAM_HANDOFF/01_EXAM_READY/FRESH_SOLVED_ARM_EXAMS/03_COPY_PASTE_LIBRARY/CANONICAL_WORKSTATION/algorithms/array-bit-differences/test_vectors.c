#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint64_t array_bit_differences(const uint32_t *a, const uint32_t *b, uint32_t n);
int test_main(void) {
  uint32_t a[] = {0, 0xffffffffu}, b[] = {0xffffffffu, 0};
  CHECK(array_bit_differences(a, b, 2) == 64);
  CHECK(array_bit_differences(0, 0, 0) == 0);
  return 0;
}
