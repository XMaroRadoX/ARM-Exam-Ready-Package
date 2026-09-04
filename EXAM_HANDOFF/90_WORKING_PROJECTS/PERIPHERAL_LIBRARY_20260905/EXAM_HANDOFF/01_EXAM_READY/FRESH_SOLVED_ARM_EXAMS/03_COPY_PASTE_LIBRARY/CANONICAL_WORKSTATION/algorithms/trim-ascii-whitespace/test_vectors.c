#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t trim_ascii(uint8_t *text, uint32_t length);
int test_main(void) {
  uint8_t s[] = {32, 9, 65, 66, 32, 10}, a[] = {9, 32, 13};
  CHECK(trim_ascii(s, 6) == 2 && s[0] == 65 && s[1] == 66);
  CHECK(trim_ascii(a, 3) == 0);
  CHECK(trim_ascii(0, 0) == 0);
  return 0;
}
