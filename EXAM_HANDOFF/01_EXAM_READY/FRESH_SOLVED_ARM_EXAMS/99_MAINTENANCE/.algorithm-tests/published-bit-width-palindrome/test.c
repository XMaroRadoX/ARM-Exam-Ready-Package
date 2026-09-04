#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bit_palindrome(uint32_t value, uint32_t width);
int test_main(void) {
  CHECK(bit_palindrome(9, 4));
  CHECK(!bit_palindrome(9, 5));
  CHECK(bit_palindrome(123, 0));
  CHECK(bit_palindrome(0x80000001u, 32));
  CHECK(!bit_palindrome(1, 33));
  return 0;
}
