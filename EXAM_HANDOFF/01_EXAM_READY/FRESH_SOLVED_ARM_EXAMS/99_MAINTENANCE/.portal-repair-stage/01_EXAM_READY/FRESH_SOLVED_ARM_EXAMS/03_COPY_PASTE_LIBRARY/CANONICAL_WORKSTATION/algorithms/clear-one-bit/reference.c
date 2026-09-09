#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Clear one bit
 * Contract: Accept bit indexes 0..31. Return 1 and the requested result, or return 0
 * without writing for an invalid index or null output. Method:
 * 1. Validate the index and output.
 * 2. Build or select the requested one-bit mask.
 * 3. Store the exact 32-bit result.
 */
int clear_bit_u32(uint32_t value, uint32_t index, uint32_t *result_out) {
  if (index >= 32 || !result_out)
    return 0;
  *result_out = value & ~(1u << index);
  return 1;
}
