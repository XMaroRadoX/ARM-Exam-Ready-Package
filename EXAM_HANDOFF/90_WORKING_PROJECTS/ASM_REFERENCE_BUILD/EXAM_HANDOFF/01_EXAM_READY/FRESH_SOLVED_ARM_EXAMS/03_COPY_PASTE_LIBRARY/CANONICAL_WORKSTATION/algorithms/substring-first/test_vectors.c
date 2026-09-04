#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t substring_first(const uint8_t *text, uint32_t length, const uint8_t *pattern,
                        uint32_t pattern_length);
int test_main(void) {
  uint8_t s[] = {97, 97, 97, 97}, p[] = {97, 97}, z[] = {98};
  CHECK(substring_first(s, 4, p, 2) == 0);
  CHECK(substring_first(s, 4, z, 1) == -1);
  CHECK(substring_first(s, 4, 0, 0) == 0);
  CHECK(substring_first(0, 0, p, 2) == -1);
  return 0;
}
