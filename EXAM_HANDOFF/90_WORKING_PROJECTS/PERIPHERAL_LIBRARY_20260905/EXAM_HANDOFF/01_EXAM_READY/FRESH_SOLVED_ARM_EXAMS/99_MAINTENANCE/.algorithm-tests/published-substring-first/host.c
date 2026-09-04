#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t substring_first(const uint8_t *s, uint32_t n, const uint8_t *p, uint32_t m) {
  if (n > INT32_MAX || (!s && n) || (!p && m))
    return -1;
  if (!m)
    return 0;
  if (m > n)
    return -1;
  uint32_t k = 0;
  (void)k;
  for (uint32_t i = 0; i <= n - m; i++) {
    uint32_t j = 0;
    while (j < m && s[i + j] == p[j])
      j++;
    if (j == m) {
      return (int32_t)i;
    }
  }
  return -1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int32_t substring_first(const uint8_t *text, uint32_t length, const uint8_t *pattern,
                        uint32_t pattern_length);
int test_main(void) {
  uint8_t s[] = {97, 97, 97, 97}, p[] = {97, 97}, z[] = {98};
  CHECK(substring_first(s, 4, p, 2) == 0);
  CHECK(substring_first(s, 4, z, 1) == -1);
  CHECK(substring_first(s, 4, 0, 0) == 0);
  CHECK(substring_first(0, 0, p, 2) == -1);
  return 0;
}

int main(void){return test_main();}
