#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Calculate a square matrix trace
 * Contract: Sum the main diagonal of a contiguous square int32_t matrix. size must be
 * at most 256. A 0x0 matrix has trace zero and may be null. Method:
 * 1. Validate size and pointers.
 * 2. Start at index zero.
 * 3. Advance by size+1 to visit each diagonal cell.
 * 4. Accumulate in 64 bits.
 */
int matrix_trace_i32(const int32_t *matrix, uint32_t size, int64_t *trace_out) {
  if (!trace_out || size > 256 || (!matrix && size))
    return 0;
  int64_t trace = 0;
  for (uint32_t i = 0; i < size; ++i)
    trace += matrix[i * size + i];
  *trace_out = trace;
  return 1;
}
