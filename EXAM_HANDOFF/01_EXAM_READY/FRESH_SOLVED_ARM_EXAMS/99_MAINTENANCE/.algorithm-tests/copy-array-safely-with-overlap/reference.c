#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Copy an array safely with overlap
 * Contract: Copy count words with memmove semantics. Require capacity>=count and valid nonempty pointers. Exact aliasing succeeds. Direction is chosen before writing so overlapping slices are preserved.
 * Method:
 * 1. Validate capacity and pointers.
 * 2. Copy forward when safe.
 * 3. Copy backward when destination begins inside the source range.
 */
int array_copy_overlap(int32_t *destination, uint32_t capacity,
                       const int32_t *source, uint32_t count) {
  if (capacity < count || ((!destination || !source) && count)) return 0;
  if (count == 0 || destination == source) return 1;
  uintptr_t d = (uintptr_t)destination, s = (uintptr_t)source;
  if (d < s || d - s >= (uintptr_t)count * sizeof(*source)) {
    for (uint32_t i = 0; i < count; ++i) destination[i] = source[i];
  } else {
    for (uint32_t i = count; i != 0; --i) destination[i - 1] = source[i - 1];
  }
  return 1;
}
