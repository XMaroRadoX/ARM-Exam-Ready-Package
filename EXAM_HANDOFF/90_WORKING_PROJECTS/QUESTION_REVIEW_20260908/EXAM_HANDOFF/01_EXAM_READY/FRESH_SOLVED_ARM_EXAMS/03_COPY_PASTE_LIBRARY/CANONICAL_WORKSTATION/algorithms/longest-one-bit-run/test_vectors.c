#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t longest_one_run(uint32_t value);
int test_main(void) {
  CHECK(longest_one_run(110) == 3);
  CHECK(longest_one_run(0) == 0);
  CHECK(longest_one_run(0xffffffffu) == 32);
  return 0;
}
