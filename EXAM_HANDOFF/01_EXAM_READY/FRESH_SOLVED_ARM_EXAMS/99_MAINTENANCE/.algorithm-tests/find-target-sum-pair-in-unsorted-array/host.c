#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Find a target-sum pair in a unsorted array
 * Contract: Find two distinct indexes whose exact 64-bit sum equals target. Output pointers must be valid and distinct; failure writes nothing.
 * Method:
 * 1. Enumerate first indexes from low to high.
 * 2. Enumerate each later second index.
 * 3. Return the lexicographically first matching pair.
 */
int array_pair_sum_unsorted(const int32_t *values, uint32_t count,
                    int32_t target, uint32_t *first_out,
                    uint32_t *second_out) {
  if (!values || !first_out || !second_out || first_out == second_out) return 0;
  for (uint32_t first = 0; first < count; ++first)
    for (uint32_t second = first + 1; second < count; ++second)
      if ((int64_t)values[first] + values[second] == target) {
        *first_out = first; *second_out = second; return 1;
      }
  return 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_pair_sum_unsorted(const int32_t *values, uint32_t count, int32_t target,
                    uint32_t *first_out, uint32_t *second_out);
int test_main(void) {
int32_t a[]={8,3,5,2};uint32_t i=99,j=99;
CHECK(array_pair_sum_unsorted(a,4,10,&i,&j)&&i==0&&j==3);
i=99;j=99;CHECK(!array_pair_sum_unsorted(a,4,99,&i,&j)&&i==99&&j==99);
CHECK(!array_pair_sum_unsorted(a,4,10,&i,&i));
return 0;
}

int main(void){return test_main();}
