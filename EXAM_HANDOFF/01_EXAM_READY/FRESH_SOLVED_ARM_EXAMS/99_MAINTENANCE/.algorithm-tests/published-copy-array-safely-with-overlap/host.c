#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Copy an array safely with overlap
 * Contract: Copy count words with memmove semantics. Require capacity>=count and valid
 * nonempty pointers. Exact aliasing succeeds. Direction is chosen before writing so
 * overlapping slices are preserved. Method:
 * 1. Validate capacity and pointers.
 * 2. Copy forward when safe.
 * 3. Copy backward when destination begins inside the source range.
 */
int array_copy_overlap(int32_t *destination, uint32_t capacity, const int32_t *source,
                       uint32_t count) {
  if (capacity < count || ((!destination || !source) && count))
    return 0;
  if (count == 0 || destination == source)
    return 1;
  uintptr_t d = (uintptr_t)destination, s = (uintptr_t)source;
  if (d < s || d - s >= (uintptr_t)count * sizeof(*source)) {
    for (uint32_t i = 0; i < count; ++i)
      destination[i] = source[i];
  } else {
    for (uint32_t i = count; i != 0; --i)
      destination[i - 1] = source[i - 1];
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int array_copy_overlap(int32_t *destination, uint32_t capacity, const int32_t *source,
                       uint32_t count);
int test_main(void) {
  int32_t a[] = {1, 2, 3, 4, 9}, b[] = {7, 8, 9};
  CHECK(array_copy_overlap(a + 1, 4, a, 4) && a[0] == 1 && a[1] == 1 && a[4] == 4);
  CHECK(array_copy_overlap(b, 3, b, 3) && b[2] == 9);
  CHECK(!array_copy_overlap(b, 2, a, 3));
  CHECK(array_copy_overlap(0, 0, 0, 0));
  return 0;
}

int main(void){return test_main();}
