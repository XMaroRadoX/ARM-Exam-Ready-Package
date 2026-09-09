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
