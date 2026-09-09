#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Concatenate two arrays within capacity
 * Contract: Write left followed by right. Reject count overflow, insufficient capacity,
 * or invalid nonempty pointers before writing. The output must not overlap either
 * input. Empty inputs are allowed. Method:
 * 1. Validate the total count and pointers.
 * 2. Copy the left array.
 * 3. Continue with the right array.
 */
int array_concatenate(const int32_t *left, uint32_t left_count, const int32_t *right,
                      uint32_t right_count, int32_t *output, uint32_t capacity) {
  if (left_count > UINT32_MAX - right_count)
    return 0;
  uint32_t total = left_count + right_count;
  if (capacity < total || (!left && left_count) || (!right && right_count) ||
      (!output && total))
    return 0;
  for (uint32_t i = 0; i < left_count; ++i)
    output[i] = left[i];
  for (uint32_t i = 0; i < right_count; ++i)
    output[left_count + i] = right[i];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_concatenate(const int32_t *left, uint32_t left_count, const int32_t *right,
                      uint32_t right_count, int32_t *output, uint32_t capacity);
int test_main(void) {
  int32_t a[] = {1, 2}, b[] = {-3, 4, 5}, o[6] = {0};
  o[5] = 77;
  CHECK(array_concatenate(a, 2, b, 3, o, 5));
  CHECK(o[0] == 1 && o[1] == 2 && o[2] == -3 && o[4] == 5 && o[5] == 77);
  o[0] = 99;
  CHECK(!array_concatenate(a, 2, b, 3, o, 4) && o[0] == 99);
  CHECK(array_concatenate(0, 0, 0, 0, 0, 0));
  return 0;
}

int main(void){return test_main();}
