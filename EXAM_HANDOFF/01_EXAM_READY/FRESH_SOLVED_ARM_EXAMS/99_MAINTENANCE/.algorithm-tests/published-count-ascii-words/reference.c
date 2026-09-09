#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Count ASCII words
 * Contract: Count maximal runs of non-whitespace bytes. ASCII space, tab, line feed,
 * vertical tab, form feed, and carriage return are separators. Return -1 for null or
 * unterminated input. Method:
 * 1. Validate NUL within capacity.
 * 2. Track whether the scan is inside a word.
 * 3. Increment only when a non-space byte begins a new word.
 */
static int ascii_space(uint8_t c) { return c == ' ' || (c >= '\t' && c <= '\r'); }
int32_t string_count_ascii_words(const uint8_t *text, uint32_t capacity) {
  if (!text)
    return -1;
  uint32_t length = 0;
  while (length < capacity && text[length])
    ++length;
  if (length == capacity || length > INT32_MAX)
    return -1;
  uint32_t words = 0;
  int inside = 0;
  for (uint32_t i = 0; i < length; ++i) {
    int space = ascii_space(text[i]);
    if (!space && !inside)
      ++words;
    inside = !space;
  }
  return (int32_t)words;
}
