#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bytes_palindrome(const uint8_t *s, uint32_t n) {
  if (!s && n)
    return 0;
  for (uint32_t i = 0; i < n / 2; i++)
    if (s[i] != s[n - 1 - i])
      return 0;
  return 1;
}
