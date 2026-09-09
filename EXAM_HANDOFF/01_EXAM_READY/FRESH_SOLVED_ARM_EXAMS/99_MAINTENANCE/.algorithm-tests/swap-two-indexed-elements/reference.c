#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Swap two indexed elements
 * Contract: Swap two elements only when both indexes are in range and storage is valid. Equal indexes are a successful no-op. Invalid input returns 0 without writing.
 * Method:
 * 1. Validate the pointer and both indexes.
 * 2. Load both words before storing.
 * 3. Store each word into the other position.
 */
int array_swap_indexes(int32_t *values, uint32_t count,
                       uint32_t first, uint32_t second) {
  if (!values || first >= count || second >= count) return 0;
  int32_t temporary = values[first];
  values[first] = values[second];
  values[second] = temporary;
  return 1;
}
