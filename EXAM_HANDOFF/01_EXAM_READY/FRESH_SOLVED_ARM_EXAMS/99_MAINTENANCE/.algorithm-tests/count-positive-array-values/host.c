#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Count positive array values
 * Contract: Count matching signed words. A null pointer returns zero; the routine never writes memory.
 * Method:
 * 1. Start the count at zero.
 * 2. Test each element against the requested condition.
 * 3. Increment exactly once for each match.
 */
uint32_t count_array_positive(const int32_t *values, uint32_t count) {
  uint32_t matches = 0;
  if (!values) return 0;
  for (uint32_t i = 0; i < count; ++i)
    if (values[i] > 0) ++matches;
  return matches;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t count_array_positive(const int32_t *values, uint32_t count);
int test_main(void) {
int32_t a[]={-2,0,5,-7,0};
CHECK(count_array_positive(a,4)==1);
CHECK(count_array_positive(0,4)==0);
CHECK(count_array_positive(a,0)==0);
return 0;
}

int main(void){return test_main();}
