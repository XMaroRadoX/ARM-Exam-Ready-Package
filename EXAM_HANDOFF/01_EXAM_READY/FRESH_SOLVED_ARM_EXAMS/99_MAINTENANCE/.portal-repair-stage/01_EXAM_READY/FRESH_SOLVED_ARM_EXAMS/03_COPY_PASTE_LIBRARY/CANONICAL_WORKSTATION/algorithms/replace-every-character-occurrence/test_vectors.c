#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
                                  uint8_t old_character, uint8_t new_character);
int test_main(void) {
  uint8_t a[] = "BANANA", bad[] = {'A', 'A'};
  CHECK(string_replace_character(a, 7, 'A', 'X') == 3);
  CHECK(a[0] == 'B' && a[1] == 'X' && a[5] == 'X' && a[6] == 0);
  CHECK(string_replace_character(bad, 2, 'A', 'X') == UINT32_MAX && bad[0] == 'A');
  CHECK(string_replace_character(a, 7, 0, 'X') == UINT32_MAX);
  return 0;
}
