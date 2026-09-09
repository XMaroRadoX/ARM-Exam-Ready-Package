#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find bounded string length
 * Contract: Find NUL within capacity and return its index through length_out. A null pointer, zero capacity, or missing terminator returns 0 without changing the output.
 * Method:
 * 1. Validate both pointers.
 * 2. Scan at most capacity bytes.
 * 3. Stop at NUL and publish its index only then.
 */
int string_length_bounded(const uint8_t *text, uint32_t capacity,
                          uint32_t *length_out) {
  if (!text || !length_out) return 0;
  for (uint32_t i = 0; i < capacity; ++i) {
    if (text[i] == 0) {
      *length_out = i;
      return 1;
    }
  }
  return 0;
}
