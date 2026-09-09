#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t integer_is_odd(int32_t value);
int test_main(void) {
  CHECK(integer_is_odd(0) == 0);
  CHECK(integer_is_odd(7) == 1);
  CHECK(integer_is_odd(-7) == 1);
  CHECK(integer_is_odd(-8) == 0);
  return 0;
}
