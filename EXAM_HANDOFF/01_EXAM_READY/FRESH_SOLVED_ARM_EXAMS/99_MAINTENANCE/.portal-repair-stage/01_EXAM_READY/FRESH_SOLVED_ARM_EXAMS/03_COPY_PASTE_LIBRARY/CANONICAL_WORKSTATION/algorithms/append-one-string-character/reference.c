#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Append one character
 * Contract: Append one non-NUL byte and preserve NUL termination. Require text[length]
 * to be NUL and space for the character plus the new terminator. Invalid input writes
 * nothing. Method:
 * 1. Validate storage, length, character, and current NUL.
 * 2. Write the character over the old NUL.
 * 3. Write a new NUL and increment length.
 */
int string_append_character(uint8_t *text, uint32_t *length, uint32_t capacity,
                            uint8_t character) {
  if (!text || !length || character == 0 || *length >= capacity || text[*length] != 0 ||
      capacity - *length < 2)
    return 0;
  text[*length] = character;
  text[*length + 1] = 0;
  ++*length;
  return 1;
}
