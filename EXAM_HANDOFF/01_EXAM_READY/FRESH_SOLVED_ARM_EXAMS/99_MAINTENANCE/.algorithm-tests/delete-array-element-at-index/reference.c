#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Delete an array element at an index
 * Contract: Delete index and return the removed value. Require a nonempty valid array, index<length, and a valid output. Invalid input returns 0 without writes.
 * Method:
 * 1. Validate and save the removed value.
 * 2. Shift later elements left.
 * 3. Decrement length and publish the removed value.
 */
int array_delete_at(int32_t *values, uint32_t *length,
                    uint32_t index, int32_t *removed_out) {
  if (!values || !length || !removed_out || index >= *length) return 0;
  int32_t removed = values[index];
  for (uint32_t i = index + 1; i < *length; ++i) values[i - 1] = values[i];
  --*length;
  *removed_out = removed;
  return 1;
}
