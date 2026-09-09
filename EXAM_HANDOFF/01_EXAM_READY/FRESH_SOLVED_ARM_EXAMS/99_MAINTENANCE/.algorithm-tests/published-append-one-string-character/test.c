#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int string_append_character(uint8_t *text, uint32_t *length, uint32_t capacity,
                            uint8_t character);
int test_main(void) {
  uint8_t a[6] = "ARM";
  uint32_t n = 3;
  CHECK(string_append_character(a, &n, 6, '!'));
  CHECK(n == 4 && a[3] == '!' && a[4] == 0);
  CHECK(!string_append_character(a, &n, 5, '?') && n == 4);
  CHECK(!string_append_character(a, &n, 6, 0) && n == 4);
  return 0;
}
