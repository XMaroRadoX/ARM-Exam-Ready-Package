#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int string_delete_character(uint8_t *text, uint32_t *length, uint32_t index,
                            uint8_t *removed_out);
int test_main(void) {
  uint8_t a[6] = "AXRM", removed = 0;
  uint32_t n = 4;
  CHECK(string_delete_character(a, &n, 1, &removed) && removed == 'X' && n == 3);
  CHECK(a[0] == 'A' && a[1] == 'R' && a[2] == 'M' && a[3] == 0);
  removed = 9;
  CHECK(!string_delete_character(a, &n, 3, &removed) && removed == 9);
  return 0;
}
