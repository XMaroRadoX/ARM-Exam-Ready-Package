#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint64_t divisor_sum(uint32_t n);
int test_main(void) {
  CHECK(divisor_sum(0) == 0);
  CHECK(divisor_sum(1) == 1);
  CHECK(divisor_sum(12) == 28);
  CHECK(divisor_sum(36) == 91);
  return 0;
}
