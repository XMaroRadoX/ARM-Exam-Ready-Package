#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Compare ASCII strings without case sensitivity
 * Contract: Return -1, 0, or 1 after folding ASCII A-Z to lowercase. Return 2 if either
 * string is null or lacks NUL within its capacity. Non-ASCII bytes compare unchanged.
 * Method:
 * 1. Validate both bounded strings.
 * 2. Fold one pair of ASCII bytes at a time.
 * 3. Return at the first difference or at NUL.
 */
static int length_for_casefold(const uint8_t *s, uint32_t cap) {
  if (!s)
    return 0;
  for (uint32_t i = 0; i < cap; ++i)
    if (!s[i])
      return 1;
  return 0;
}
static uint8_t fold_ascii(uint8_t c) {
  return c >= 'A' && c <= 'Z' ? (uint8_t)(c + 32) : c;
}
int32_t strings_compare_ascii_casefold(const uint8_t *left, uint32_t left_capacity,
                                       const uint8_t *right, uint32_t right_capacity) {
  if (!length_for_casefold(left, left_capacity) ||
      !length_for_casefold(right, right_capacity))
    return 2;
  for (uint32_t i = 0;; ++i) {
    uint8_t a = fold_ascii(left[i]), b = fold_ascii(right[i]);
    if (a < b)
      return -1;
    if (a > b)
      return 1;
    if (!a)
      return 0;
  }
}
