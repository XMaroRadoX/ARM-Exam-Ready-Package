#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Add two matrices with overflow detection
 * Contract: Perform elementwise signed int32_t arithmetic. Require dimensions at most
 * 256, enough disjoint output storage, and no cell overflow. A complete preflight
 * guarantees failure performs no writes. Method:
 * 1. Validate dimensions, capacity, and pointers.
 * 2. Preflight every cell using widened arithmetic.
 * 3. Repeat the scan and store only after all cells are safe.
 */
int matrix_add_i32(const int32_t *left, const int32_t *right, uint32_t rows,
                   uint32_t columns, int32_t *output, uint32_t capacity) {
  if (rows > 256 || columns > 256)
    return 0;
  uint32_t count = rows * columns;
  if (capacity < count || ((!left || !right || !output) && count))
    return 0;
  for (uint32_t i = 0; i < count; ++i) {
    int64_t wide = (int64_t)left[i] + right[i];
    if (wide < INT32_MIN || wide > INT32_MAX)
      return 0;
  }
  for (uint32_t i = 0; i < count; ++i)
    output[i] = left[i] + right[i];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_add_i32(const int32_t *left, const int32_t *right, uint32_t rows,
                   uint32_t columns, int32_t *output, uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4}, b[] = {5, 6, 7, 8}, o[5] = {0};
  o[4] = 77;
  CHECK(matrix_add_i32(a, b, 2, 2, o, 4));
  CHECK(o[0] == 6 && o[3] == 12 && o[4] == 77);
  int32_t x[] = {INT32_MAX}, y[] = {1};
  o[0] = 99;
  CHECK(!matrix_add_i32(x, y, 1, 1, o, 1) && o[0] == 99);
  CHECK(!matrix_add_i32(a, b, 2, 2, o, 3));
  return 0;
}

int main(void){return test_main();}
