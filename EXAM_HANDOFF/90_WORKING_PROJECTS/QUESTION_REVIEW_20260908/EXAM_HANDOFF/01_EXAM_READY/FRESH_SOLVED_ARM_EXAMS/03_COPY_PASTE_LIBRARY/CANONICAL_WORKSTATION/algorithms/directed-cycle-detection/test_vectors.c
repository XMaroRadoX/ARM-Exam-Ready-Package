#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int directed_cycle(const uint8_t *a, size_t n, uint8_t *state);
int test_main(void) {
  uint8_t a[] = {0, 1, 0, 0, 0, 1, 0, 0, 0}, s[3];
  CHECK(!directed_cycle(a, 3, s));
  a[6] = 1;
  CHECK(directed_cycle(a, 3, s));
  uint8_t self[] = {1};
  CHECK(directed_cycle(self, 1, s));
  return 0;
}
