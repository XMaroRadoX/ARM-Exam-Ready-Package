#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bytes_reverse(uint8_t *text, uint32_t length);
int test_main(void) {
  uint8_t a[] = {1, 2, 3, 4, 77};
  CHECK(bytes_reverse(a, 4) && a[0] == 4 && a[3] == 1 && a[4] == 77);
  CHECK(bytes_reverse(0, 0));
  CHECK(!bytes_reverse(0, 1));
  return 0;
}
