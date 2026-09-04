#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int parse_i32(const uint8_t *s, uint32_t n, int32_t *out) {
  if (!s || !out || !n)
    return 0;
  int neg = 0;
  if (n && (s[0] == 45 || s[0] == 43)) {
    neg = s[0] == 45;
    s++;
    n--;
  }
  if (!n)
    return 0;
  uint32_t v = 0;
  for (uint32_t i = 0; i < n; i++) {
    if (s[i] < 48 || s[i] > 57)
      return 0;
    uint32_t d = s[i] - 48;
    if (v > 429496729u || (v == 429496729u && d > 5))
      return 0;
    v = v * 10 + d;
  }
  if (v > (neg ? 2147483648u : 2147483647u))
    return 0;
  *out = neg ? (int32_t)(-(int64_t)v) : (int32_t)v;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

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

int main(void){return test_main();}
