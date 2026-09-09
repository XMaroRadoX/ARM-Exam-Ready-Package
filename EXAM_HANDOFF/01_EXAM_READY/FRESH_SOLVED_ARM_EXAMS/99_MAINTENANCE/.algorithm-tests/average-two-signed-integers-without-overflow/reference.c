#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Average two signed integers without overflow
 * Contract: Return (left+right)/2 with C signed-division semantics: truncate toward zero. The addition is formed as a signed 64-bit value, so opposite and extreme inputs cannot overflow.
 * Method:
 * 1. Form the two-word signed sum.
 * 2. If a negative sum is odd, add one before shifting.
 * 3. Arithmetic-shift the 64-bit sum right once.
 */
int32_t average_two_i32(int32_t left, int32_t right) {
  return (int32_t)(((int64_t)left + right) / 2);
}
