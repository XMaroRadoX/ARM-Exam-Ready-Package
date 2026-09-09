#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Test whether a string starts with a prefix
 * Contract: Return 1 for a match, 0 for no match, and -1 for invalid or unterminated
 * input. The empty affix matches every valid string. Method:
 * 1. Find both bounded lengths.
 * 2. Reject an affix longer than the text.
 * 3. Compare the required character range.
 */
static int length_for_affix(const uint8_t *s, uint32_t cap, uint32_t *n) {
  if (!s || !n)
    return 0;
  for (uint32_t i = 0; i < cap; ++i)
    if (!s[i]) {
      *n = i;
      return 1;
    }
  return 0;
}
int32_t string_starts_with(const uint8_t *text, uint32_t text_capacity,
                           const uint8_t *affix, uint32_t affix_capacity) {
  uint32_t text_length, affix_length;
  if (!length_for_affix(text, text_capacity, &text_length) ||
      !length_for_affix(affix, affix_capacity, &affix_length))
    return -1;
  if (affix_length > text_length)
    return 0;
  uint32_t start = 0;
  for (uint32_t i = 0; i < affix_length; ++i)
    if (text[start + i] != affix[i])
      return 0;
  return 1;
}
