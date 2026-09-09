#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Produce adjacent differences
 * Contract: Write values[i+1]-values[i] as signed 64-bit results. Output length is
 * count-1 for nonempty input and zero for empty input. Validate all inputs before
 * writing. Method:
 * 1. Compute the required output count.
 * 2. Load neighboring values.
 * 3. Widen before subtracting.
 * 4. Store each 64-bit difference.
 */
int array_adjacent_differences(const int32_t *values, uint32_t count, int64_t *output,
                               uint32_t capacity) {
  uint32_t needed = count ? count - 1 : 0;
  if (capacity < needed || (!values && count) || (!output && needed))
    return 0;
  for (uint32_t i = 0; i < needed; ++i)
    output[i] = (int64_t)values[i + 1] - values[i];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_adjacent_differences(const int32_t *values, uint32_t count, int64_t *output,
                               uint32_t capacity);
int test_main(void) {
  int32_t a[] = {INT32_MIN, 0, INT32_MAX};
  int64_t o[3] = {0};
  o[2] = 77;
  CHECK(array_adjacent_differences(a, 3, o, 2));
  CHECK(o[0] == 2147483648LL && o[1] == 2147483647LL && o[2] == 77);
  CHECK(array_adjacent_differences(0, 0, 0, 0));
  o[0] = 99;
  CHECK(!array_adjacent_differences(a, 3, o, 1) && o[0] == 99);
  return 0;
}

int main(void){return test_main();}
