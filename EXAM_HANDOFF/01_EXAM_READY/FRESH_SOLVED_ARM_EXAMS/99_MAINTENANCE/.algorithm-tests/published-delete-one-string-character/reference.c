#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Delete one character at an index
 * Contract: Delete index, return the removed byte, and preserve NUL termination.
 * Require index<length and text[length] to be NUL. Invalid input writes nothing.
 * Method:
 * 1. Validate and save the selected byte.
 * 2. Shift all later bytes including NUL left.
 * 3. Decrement length and publish the removed byte.
 */
int string_delete_character(uint8_t *text, uint32_t *length, uint32_t index,
                            uint8_t *removed_out) {
  if (!text || !length || !removed_out || index >= *length || text[*length] != 0)
    return 0;
  uint8_t removed = text[index];
  for (uint32_t i = index; i < *length; ++i)
    text[i] = text[i + 1];
  --*length;
  *removed_out = removed;
  return 1;
}
