#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Compare two arrays for equality
 * Contract: Return 1 when all count signed words are equal. Empty arrays are equal even with null pointers. A null pointer with a nonzero count returns 0.
 * Method:
 * 1. Accept count zero immediately.
 * 2. Validate both bases.
 * 3. Stop on the first unequal pair.
 */
int arrays_equal(const int32_t *left, const int32_t *right,
                 uint32_t count) {
  if (count == 0) return 1;
  if (!left || !right) return 0;
  for (uint32_t i = 0; i < count; ++i)
    if (left[i] != right[i]) return 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int arrays_equal(const int32_t *left, const int32_t *right, uint32_t count);
int test_main(void) {
int32_t a[]={3,-1,8},b[]={3,-1,8},c[]={3,-1,7};
CHECK(arrays_equal(a,b,3));CHECK(!arrays_equal(a,c,3));
CHECK(arrays_equal(0,0,0));CHECK(!arrays_equal(0,b,3));
return 0;
}

int main(void){return test_main();}
