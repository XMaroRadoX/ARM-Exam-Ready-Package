#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int string_to_ascii_lowercase(uint8_t *text, uint32_t capacity);
int test_main(void) {
  uint8_t a[] = "Arm-M3", bad[] = {'A', 'B'};
  CHECK(string_to_ascii_lowercase(a, sizeof a));
  CHECK(a[0] == 'a');
  CHECK(a[1] == 'r' && a[4] == 'm');
  CHECK(!string_to_ascii_lowercase(bad, 2) && bad[0] == 'A');
  return 0;
}
