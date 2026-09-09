#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bounded_word_length(const uint32_t *a, uint32_t capacity, uint32_t sentinel,
                        uint32_t *length) {
  if (!a || !length)
    return 0;
  for (uint32_t i = 0; i < capacity; i++)
    if (a[i] == sentinel) {
      *length = i;
      return 1;
    }
  return 0;
}
