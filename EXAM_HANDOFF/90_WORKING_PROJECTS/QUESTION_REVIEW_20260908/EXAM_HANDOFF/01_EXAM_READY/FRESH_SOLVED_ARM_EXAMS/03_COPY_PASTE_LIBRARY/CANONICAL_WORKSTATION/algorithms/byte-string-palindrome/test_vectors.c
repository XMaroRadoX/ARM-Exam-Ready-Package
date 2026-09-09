#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bytes_palindrome(const uint8_t *text, uint32_t length);
int test_main(void) {
  uint8_t a[] = {114, 97, 100, 97, 114}, b[] = {0, 255, 0};
  CHECK(bytes_palindrome(a, 5));
  CHECK(bytes_palindrome(b, 3));
  CHECK(!bytes_palindrome(a, 4));
  CHECK(bytes_palindrome(0, 0));
  return 0;
}
