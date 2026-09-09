#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Insert an array element at an index
 * Contract: Insert before index, where index may equal the old length. Require
 * length<capacity, index<=length, and valid storage. Invalid input returns 0 without
 * changing the array or length. Method:
 * 1. Validate every condition before writing.
 * 2. Shift the suffix right from the end.
 * 3. Store the new value and increment length.
 */
int array_insert_at(int32_t *values, uint32_t *length, uint32_t capacity,
                    uint32_t index, int32_t value) {
  if (!values || !length || *length >= capacity || index > *length)
    return 0;
  for (uint32_t i = *length; i > index; --i)
    values[i] = values[i - 1];
  values[index] = value;
  ++*length;
  return 1;
}
