#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Insert one character at an index
 * Contract: Insert one non-NUL byte before index, where index may equal length. Require
 * a valid current terminator and one spare byte. Invalid input writes nothing. Method:
 * 1. Validate all conditions.
 * 2. Shift the suffix including NUL one byte right.
 * 3. Store the character and increment length.
 */
int string_insert_character(uint8_t *text, uint32_t *length, uint32_t capacity,
                            uint32_t index, uint8_t character) {
  if (!text || !length || character == 0 || index > *length || *length >= capacity ||
      text[*length] != 0 || capacity - *length < 2)
    return 0;
  for (uint32_t i = *length + 1; i > index; --i)
    text[i] = text[i - 1];
  text[index] = character;
  ++*length;
  return 1;
}
