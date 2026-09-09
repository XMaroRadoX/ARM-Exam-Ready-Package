#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Fill an array with one value
 * Contract: Store fill_value in every element. Empty input succeeds without dereferencing the pointer; a null pointer with nonzero count fails.
 * Method:
 * 1. Validate the base when count is nonzero.
 * 2. Store the same word and advance.
 * 3. Stop after exactly count stores.
 */
int array_fill(int32_t *values, uint32_t count, int32_t fill_value) {
  if (!values && count) return 0;
  for (uint32_t i = 0; i < count; ++i) values[i] = fill_value;
  return 1;
}
