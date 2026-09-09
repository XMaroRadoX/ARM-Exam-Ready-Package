#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Integer array mean
 * Contract: Return the arithmetic mean truncated toward zero. Require 1..INT32_MAX
 * elements and valid pointers. The 64-bit sum prevents intermediate 32-bit overflow;
 * invalid input returns 0 without writing. Method:
 * 1. Accumulate an exact signed 64-bit sum.
 * 2. Divide the signed sum by the positive count.
 * 3. Store the quotient, which always fits int32_t.
 */
int integer_array_mean(const int32_t *values, uint32_t count, int32_t *mean_out) {
  if (!values || !mean_out || count == 0 || count > INT32_MAX)
    return 0;
  int64_t sum = 0;
  for (uint32_t i = 0; i < count; ++i)
    sum += values[i];
  *mean_out = (int32_t)(sum / (int64_t)count);
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int integer_array_mean(const int32_t *values, uint32_t count, int32_t *mean_out);
int test_main(void) {
  int32_t a[] = {-8, 3, 4}, b[] = {INT32_MAX, INT32_MAX}, m = 77;
  CHECK(integer_array_mean(a, 3, &m) && m == 0);
  CHECK(integer_array_mean(b, 2, &m) && m == INT32_MAX);
  m = 77;
  CHECK(!integer_array_mean(a, 0, &m) && m == 77);
  CHECK(!integer_array_mean(0, 3, &m) && m == 77);
  return 0;
}

int main(void){return test_main();}
