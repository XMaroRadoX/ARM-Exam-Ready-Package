#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find the first occurrence of a character
 * Contract: Return a zero-based index, -1 when absent, or -2 for a null input, NUL target, zero capacity, or missing terminator. The complete bound is validated.
 * Method:
 * 1. Scan no farther than capacity.
 * 2. Stop only at NUL.
 * 3. Track the requested matching position.
 * 4. Distinguish not-found from invalid input.
 */
int32_t string_first_occurrence(const uint8_t *text, uint32_t capacity,
                         uint8_t target) {
  if (!text || !target) return -2;
  uint32_t length=0;
  while (length<capacity && text[length]) ++length;
  if (length==capacity) return -2;
  int32_t found=-1;
  for (uint32_t i=0;i<length;++i)
    if (text[i]==target) { return (int32_t)i; }
  return found;
}
