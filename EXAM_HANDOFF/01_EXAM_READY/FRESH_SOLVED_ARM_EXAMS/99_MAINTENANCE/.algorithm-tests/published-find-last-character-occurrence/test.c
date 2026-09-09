#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t string_last_occurrence(const uint8_t *text, uint32_t capacity, uint8_t target);
int test_main(void) {
  uint8_t a[] = "BANANA", bad[] = {'A', 'A'};
  CHECK(string_last_occurrence(a, 7, 'A') == 5);
  CHECK(string_last_occurrence(a, 7, 'Z') == -1);
  CHECK(string_last_occurrence(bad, 2, 'A') == -2);
  CHECK(string_last_occurrence(a, 7, 0) == -2);
  return 0;
}
