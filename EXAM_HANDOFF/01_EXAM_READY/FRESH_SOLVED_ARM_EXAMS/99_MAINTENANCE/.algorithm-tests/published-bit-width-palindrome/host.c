#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bit_palindrome(uint32_t v, uint32_t w) {
  if (w > 32)
    return 0;
  uint32_t r = 0, x = v;
  for (uint32_t i = 0; i < w; i++) {
    r = (r << 1) | (x & 1);
    x >>= 1;
  }
  uint32_t m = w == 32 ? UINT32_MAX : w ? ((1u << w) - 1) : 0;
  return r == (v & m);
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int bit_palindrome(uint32_t value, uint32_t width);
int test_main(void) {
  CHECK(bit_palindrome(9, 4));
  CHECK(!bit_palindrome(9, 5));
  CHECK(bit_palindrome(123, 0));
  CHECK(bit_palindrome(0x80000001u, 32));
  CHECK(!bit_palindrome(1, 33));
  return 0;
}

int main(void){return test_main();}
