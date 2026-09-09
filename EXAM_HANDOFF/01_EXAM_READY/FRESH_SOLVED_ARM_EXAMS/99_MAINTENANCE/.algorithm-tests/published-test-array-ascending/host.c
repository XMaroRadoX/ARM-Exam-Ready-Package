#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Test whether an array is ascending
 * Contract: Return 1 when every adjacent pair is in nondecreasing signed order. Empty
 * and one-element arrays are ascending; a null pointer is valid only for count zero.
 * Method:
 * 1. Start with the second element.
 * 2. Compare it with its predecessor.
 * 3. Reject the first decrease.
 */
int array_is_ascending(const int32_t *values, uint32_t count) {
  if (count == 0)
    return 1;
  if (!values)
    return 0;
  for (uint32_t i = 1; i < count; ++i)
    if (values[i] < values[i - 1])
      return 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_is_ascending(const int32_t *values, uint32_t count);
int test_main(void) {
  int32_t a[] = {-3, -3, 4, 9}, b[] = {-3, 4, 2};
  CHECK(array_is_ascending(a, 4));
  CHECK(!array_is_ascending(b, 3));
  CHECK(array_is_ascending(0, 0));
  CHECK(!array_is_ascending(0, 1));
  return 0;
}

int main(void){return test_main();}
