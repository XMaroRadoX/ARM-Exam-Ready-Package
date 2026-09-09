#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t divisor_count(uint32_t n);
int test_main(void) {
  CHECK(divisor_count(0) == 0);
  CHECK(divisor_count(1) == 1);
  CHECK(divisor_count(36) == 9);
  CHECK(divisor_count(13) == 2);
  return 0;
}
