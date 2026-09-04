#include <limits.h>
#include <stddef.h>
#include <stdint.h>
size_t u32_to_base(unsigned v, unsigned b, char *out, size_t cap) {
  if (!out || b < 2 || b > 16)
    return 0;
  char d[32];
  size_t n = 0;
  do {
    unsigned x = v % b;
    d[n++] = (char)(x < 10 ? 48 + x : 55 + x);
    v /= b;
  } while (v);
  if (cap <= n)
    return 0;
  for (size_t i = 0; i < n; i++)
    out[i] = d[n - 1 - i];
  out[n] = 0;
  return n;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

size_t u32_to_base(unsigned value, unsigned base, char *out, size_t cap);
int test_main(void) {
  char o[34] = {0};
  CHECK(u32_to_base(31, 16, o, 3) == 2 && o[0] == 49 && o[1] == 70 && o[2] == 0);
  o[0] = 88;
  CHECK(!u32_to_base(31, 16, o, 2) && o[0] == 88);
  CHECK(u32_to_base(UINT_MAX, 2, o, 33) == 32);
  return 0;
}

int main(void){return test_main();}
