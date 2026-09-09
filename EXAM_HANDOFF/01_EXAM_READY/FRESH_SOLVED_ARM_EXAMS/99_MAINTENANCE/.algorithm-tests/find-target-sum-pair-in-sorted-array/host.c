#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find a target-sum pair in a sorted array
 * Contract: Input must be ascending. Find two distinct indexes whose exact 64-bit sum equals target. Output pointers must be valid and distinct; failure writes nothing.
 * Method:
 * 1. Start at both ends.
 * 2. Compare the widened sum with target.
 * 3. Move the left or right index until a pair is found.
 */
int array_pair_sum_sorted(const int32_t *values, uint32_t count,
                    int32_t target, uint32_t *first_out,
                    uint32_t *second_out) {
  if (!values || !first_out || !second_out || first_out == second_out) return 0;
  uint32_t first = 0, second = count - 1;
  while (first < second) {
    int64_t sum = (int64_t)values[first] + values[second];
    if (sum == target) { *first_out = first; *second_out = second; return 1; }
    if (sum < target) ++first; else --second;
  }
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_pair_sum_sorted(const int32_t *values, uint32_t count, int32_t target,
                    uint32_t *first_out, uint32_t *second_out);
int test_main(void) {
int32_t a[]={1,2,4,7,9};uint32_t i=99,j=99;
CHECK(array_pair_sum_sorted(a,5,11,&i,&j)&&i==1&&j==4);
i=99;j=99;CHECK(!array_pair_sum_sorted(a,5,99,&i,&j)&&i==99&&j==99);
CHECK(!array_pair_sum_sorted(a,5,10,&i,&i));
return 0;
}

int main(void){return test_main();}
