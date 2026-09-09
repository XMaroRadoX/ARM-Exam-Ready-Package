#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Partition even values before odd values stably
 * Contract: Move even values before odd values while preserving order within both groups. The in-place insertion method uses no scratch buffer.
 * Method:
 * 1. Scan left to right.
 * 2. Save an even value that follows odds.
 * 3. Shift the odd block right.
 * 4. Insert the saved even value.
 */
int array_stable_even_first(int32_t *values, uint32_t count) {
  if (!values && count) return 0;
  for (uint32_t i = 1; i < count; ++i) {
    if ((values[i] & 1) == 0) {
      int32_t even = values[i];
      uint32_t j = i;
      while (j && (values[j - 1] & 1)) {
        values[j] = values[j - 1];
        --j;
      }
      values[j] = even;
    }
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_stable_even_first(int32_t *values, uint32_t count);
int test_main(void) {
int32_t a[]={3,2,5,4,1,77};CHECK(array_stable_even_first(a,5));
CHECK(a[0]==2&&a[1]==4&&a[2]==3&&a[3]==5&&a[4]==1&&a[5]==77);
CHECK(array_stable_even_first(0,0));CHECK(!array_stable_even_first(0,1));
return 0;
}

int main(void){return test_main();}
