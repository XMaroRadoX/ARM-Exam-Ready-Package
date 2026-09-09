#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Build a decimal digit-frequency table
 * Contract: Clear and fill ten counters for the magnitude digits of value. Zero
 * contributes one zero digit. The unsigned-magnitude conversion handles INT32_MIN. A
 * null table fails. Method:
 * 1. Clear all ten counters.
 * 2. Convert the signed value to an unsigned magnitude.
 * 3. Repeatedly divide by ten and increment the remainder bucket.
 */
int decimal_digit_frequency_i32(int32_t value, uint32_t counts[10]) {
  if (!counts)
    return 0;
  for (uint32_t i = 0; i < 10; ++i)
    counts[i] = 0;
  uint32_t magnitude = value < 0 ? 0u - (uint32_t)value : (uint32_t)value;
  if (magnitude == 0) {
    counts[0] = 1;
    return 1;
  }
  while (magnitude) {
    uint32_t quotient = magnitude / 10u;
    ++counts[magnitude - quotient * 10u];
    magnitude = quotient;
  }
  return 1;
}
