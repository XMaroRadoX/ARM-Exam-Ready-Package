#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t string_starts_with(const uint8_t *text, uint32_t text_capacity,
                           const uint8_t *affix, uint32_t affix_capacity);
int test_main(void) {
  uint8_t text[] = "cortex-m3", yes[] = "cortex", no[] = "arm", bad[] = {'x'};
  CHECK(string_starts_with(text, 10, yes, sizeof yes) == 1);
  CHECK(string_starts_with(text, 10, no, sizeof no) == 0);
  CHECK(string_starts_with(text, 10, bad, 1) == -1);
  return 0;
}
