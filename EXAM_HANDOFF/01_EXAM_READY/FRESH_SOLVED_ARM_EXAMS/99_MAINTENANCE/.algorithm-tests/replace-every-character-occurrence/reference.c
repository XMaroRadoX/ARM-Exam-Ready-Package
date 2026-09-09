#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Replace every occurrence of a character
 * Contract: Replace every old_character before NUL and return the replacement count. Both characters must be non-NUL. Invalid or unterminated input returns UINT32_MAX without modifying text.
 * Method:
 * 1. Validate the bounded length first.
 * 2. Scan exactly the characters before NUL.
 * 3. Replace matches and count them.
 */
uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
                                  uint8_t old_character,
                                  uint8_t new_character) {
  if (!text || !old_character || !new_character) return UINT32_MAX;
  uint32_t length=0;
  while (length<capacity && text[length]) ++length;
  if (length==capacity) return UINT32_MAX;
  uint32_t replaced=0;
  for (uint32_t i=0;i<length;++i)
    if (text[i]==old_character) { text[i]=new_character; ++replaced; }
  return replaced;
}
