#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Move zeros to the end stably
 * Contract: Move every zero after all nonzero values while preserving nonzero order. Empty input succeeds; a null nonempty base fails.
 * Method:
 * 1. Compact nonzero values at a write index.
 * 2. Fill the remaining suffix with zeros.
 * 3. Never read beyond count.
 */
int array_move_zeros_to_end(int32_t *values, uint32_t count) {
  if (!values && count) return 0;
  uint32_t write = 0;
  for (uint32_t read = 0; read < count; ++read)
    if (values[read] != 0) values[write++] = values[read];
  while (write < count) values[write++] = 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_move_zeros_to_end(int32_t *values, uint32_t count);
int test_main(void) {
int32_t a[]={0,4,0,-2,7,77};CHECK(array_move_zeros_to_end(a,5));
CHECK(a[0]==4&&a[1]==-2&&a[2]==7&&a[3]==0&&a[4]==0&&a[5]==77);
CHECK(array_move_zeros_to_end(0,0));CHECK(!array_move_zeros_to_end(0,1));
return 0;
}

int main(void){return test_main();}
