#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Classify an integer as even or odd
 * Contract: Return 0 for even and 1 for odd. Testing the low bit works for positive, zero, and negative two-complement values.
 * Method:
 * 1. Mask bit zero.
 * 2. Return that bit directly.
 */
uint32_t integer_is_odd(int32_t value) {
  return (uint32_t)value & 1u;
}
