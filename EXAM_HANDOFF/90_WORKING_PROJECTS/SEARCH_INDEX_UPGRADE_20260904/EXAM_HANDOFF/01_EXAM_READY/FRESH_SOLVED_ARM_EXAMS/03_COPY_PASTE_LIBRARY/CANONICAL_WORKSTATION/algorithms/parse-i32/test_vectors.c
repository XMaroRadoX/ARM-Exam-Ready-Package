#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int parse_i32(const uint8_t *text, uint32_t length, int32_t *out);
int test_main(void) {
  int32_t v = 99;
  CHECK(parse_i32((const uint8_t *)"123", 3, &v) && v == 123);
  v = 99;
  CHECK(!parse_i32((const uint8_t *)"12x", 3, &v) && v == 99);
  CHECK(!parse_i32((const uint8_t *)"", 0, &v));
  CHECK(parse_i32((const uint8_t *)"-2147483648", 11, &v) && v == INT32_MIN);
  CHECK(!parse_i32((const uint8_t *)"2147483648", 10, &v));
  CHECK(!parse_i32((const uint8_t *)"-", 1, &v));
  return 0;
}
