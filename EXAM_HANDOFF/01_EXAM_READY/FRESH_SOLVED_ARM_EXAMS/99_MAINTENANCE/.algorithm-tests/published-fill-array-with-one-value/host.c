#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Fill an array with one value
 * Contract: Store fill_value in every element. Empty input succeeds without
 * dereferencing the pointer; a null pointer with nonzero count fails. Method:
 * 1. Validate the base when count is nonzero.
 * 2. Store the same word and advance.
 * 3. Stop after exactly count stores.
 */
int array_fill(int32_t *values, uint32_t count, int32_t fill_value) {
  if (!values && count)
    return 0;
  for (uint32_t i = 0; i < count; ++i)
    values[i] = fill_value;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_fill(int32_t *values, uint32_t count, int32_t fill_value);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 77};
  CHECK(array_fill(a, 4, -3));
  CHECK(a[0] == -3 && a[3] == -3 && a[4] == 77);
  CHECK(array_fill(0, 0, 9));
  CHECK(!array_fill(0, 1, 9));
  return 0;
}

int main(void){return test_main();}
