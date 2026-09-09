#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Shift an array left with a fill value
 * Contract: Shift by amount positions and fill vacated positions. An amount at least
 * count fills the array. Empty input succeeds; null nonempty input fails. Method:
 * 1. Validate storage.
 * 2. Clamp amount to count.
 * 3. Copy in the safe direction.
 * 4. Fill vacated positions.
 */
int array_shift_left(int32_t *values, uint32_t count, uint32_t amount,
                     int32_t fill_value) {
  if (!values && count)
    return 0;
  if (amount > count)
    amount = count;
  for (uint32_t i = 0; i < count - amount; ++i)
    values[i] = values[i + amount];
  for (uint32_t i = count - amount; i < count; ++i)
    values[i] = fill_value;
  return 1;
}
