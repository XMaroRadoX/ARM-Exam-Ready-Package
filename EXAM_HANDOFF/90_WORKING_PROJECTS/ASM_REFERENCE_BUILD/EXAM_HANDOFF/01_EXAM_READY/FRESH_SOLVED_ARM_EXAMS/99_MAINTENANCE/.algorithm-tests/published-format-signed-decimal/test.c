#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t format_i32(int32_t value, char *out, uint32_t capacity);
int test_main(void) {
  char s[13] = {0};
  s[12] = 77;
  CHECK(format_i32(INT32_MIN, s, 12) == 11 && s[0] == 45 && s[10] == 56 && s[11] == 0 &&
        s[12] == 77);
  s[0] = 88;
  CHECK(!format_i32(-120, s, 4) && s[0] == 88);
  CHECK(format_i32(0, s, 2) == 1 && s[0] == 48 && s[1] == 0);
  return 0;
}
