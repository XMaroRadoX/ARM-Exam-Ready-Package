#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Multiply a matrix by a scalar with overflow detection
 * Contract: Multiply every cell by scalar in signed int32_t. Require dimensions at most
 * 256, enough disjoint output, and no overflow. A full preflight prevents partial
 * writes. Method:
 * 1. Validate dimensions and storage.
 * 2. Use a signed 64-bit product to preflight each cell.
 * 3. Repeat and store after every product is known safe.
 */
int matrix_scalar_multiply_i32(const int32_t *matrix, uint32_t rows, uint32_t columns,
                               int32_t scalar, int32_t *output, uint32_t capacity) {
  if (rows > 256 || columns > 256)
    return 0;
  uint32_t count = rows * columns;
  if (capacity < count || ((!matrix || !output) && count))
    return 0;
  for (uint32_t i = 0; i < count; ++i) {
    int64_t wide = (int64_t)matrix[i] * scalar;
    if (wide < INT32_MIN || wide > INT32_MAX)
      return 0;
  }
  for (uint32_t i = 0; i < count; ++i)
    output[i] = matrix[i] * scalar;
  return 1;
}
