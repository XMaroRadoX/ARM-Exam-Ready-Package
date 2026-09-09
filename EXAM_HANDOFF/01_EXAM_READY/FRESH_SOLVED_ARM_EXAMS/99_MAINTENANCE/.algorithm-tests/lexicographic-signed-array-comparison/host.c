#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Lexicographically compare two signed arrays
 * Contract: Return -1, 0, or 1 using signed element order, then shorter-prefix order. A null pointer is valid only with a zero count; invalid input returns 2.
 * Method:
 * 1. Compare corresponding values up to the shorter count.
 * 2. Return at the first unequal signed pair.
 * 3. If the common prefix matches, compare lengths.
 */
int32_t arrays_compare_lexicographic(const int32_t *left,
                                     uint32_t left_count,
                                     const int32_t *right,
                                     uint32_t right_count) {
  if ((!left && left_count) || (!right && right_count)) return 2;
  uint32_t n = left_count < right_count ? left_count : right_count;
  for (uint32_t i = 0; i < n; ++i) {
    if (left[i] < right[i]) return -1;
    if (left[i] > right[i]) return 1;
  }
  return left_count < right_count ? -1 : left_count > right_count ? 1 : 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int32_t arrays_compare_lexicographic(const int32_t *left, uint32_t left_count,
                                     const int32_t *right, uint32_t right_count);
int test_main(void) {
int32_t a[]={1,9},b[]={1,7,100},c[]={1,9,0};
CHECK(arrays_compare_lexicographic(a,2,b,3)==1);
CHECK(arrays_compare_lexicographic(a,2,c,3)==-1);
CHECK(arrays_compare_lexicographic(a,2,a,2)==0);
CHECK(arrays_compare_lexicographic(0,1,a,2)==2);
return 0;
}

int main(void){return test_main();}
