#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Shift an array left with a fill value
 * Contract: Shift by amount positions and fill vacated positions. An amount at least
 * count fills the array. Empty input succeeds; null nonempty input fails. Method:
 * 1. Validate storage.
 * 2. Clamp amount to count.
 * 3. Copy in the safe direction.
 * 4. Fill vacated positions.
 */
int array_shift_left(int32_t *values, uint32_t count, uint32_t amount,
                     int32_t fill_value) {
  if (!values && count)
    return 0;
  if (amount > count)
    amount = count;
  for (uint32_t i = 0; i < count - amount; ++i)
    values[i] = values[i + amount];
  for (uint32_t i = count - amount; i < count; ++i)
    values[i] = fill_value;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_shift_left(int32_t *values, uint32_t count, uint32_t amount,
                     int32_t fill_value);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 77};
  CHECK(array_shift_left(a, 4, 2, -1));
  CHECK(a[0] == 3 && a[1] == 4 && a[2] == -1 && a[3] == -1 && a[4] == 77);
  CHECK(array_shift_left(a, 4, 9, 5) && a[0] == 5 && a[3] == 5);
  CHECK(array_shift_left(0, 0, 1, 5));
  CHECK(!array_shift_left(0, 1, 1, 5));
  return 0;
}

int main(void){return test_main();}
