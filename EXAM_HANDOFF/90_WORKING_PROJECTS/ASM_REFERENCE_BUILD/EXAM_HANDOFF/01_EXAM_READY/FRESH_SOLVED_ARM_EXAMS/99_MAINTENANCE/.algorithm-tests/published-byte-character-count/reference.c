#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t byte_count(const uint8_t *s, uint32_t n, uint8_t key) {
  uint32_t c = 0;
  if (s)
    for (uint32_t i = 0; i < n; i++)
      c += s[i] == key;
  return c;
}
