#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t byte_count(const uint8_t *text, uint32_t length, uint8_t key);
int test_main(void) {
  uint8_t a[] = {0, 255, 0, 1};
  CHECK(byte_count(a, 4, 0) == 2);
  CHECK(byte_count(a, 4, 255) == 1);
  CHECK(byte_count(0, 0, 0) == 0);
  return 0;
}
