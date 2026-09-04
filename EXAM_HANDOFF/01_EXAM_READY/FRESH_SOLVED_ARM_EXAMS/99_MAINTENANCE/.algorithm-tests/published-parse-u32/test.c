#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int parse_u32(const uint8_t *text, uint32_t length, uint32_t *out);
int test_main(void) {
  uint32_t v = 99;
  CHECK(parse_u32((const uint8_t *)"123", 3, &v) && v == 123);
  v = 99;
  CHECK(!parse_u32((const uint8_t *)"12x", 3, &v) && v == 99);
  CHECK(!parse_u32((const uint8_t *)"", 0, &v));
  CHECK(parse_u32((const uint8_t *)"4294967295", 10, &v) && v == UINT32_MAX);
  CHECK(!parse_u32((const uint8_t *)"4294967296", 10, &v));
  return 0;
}
