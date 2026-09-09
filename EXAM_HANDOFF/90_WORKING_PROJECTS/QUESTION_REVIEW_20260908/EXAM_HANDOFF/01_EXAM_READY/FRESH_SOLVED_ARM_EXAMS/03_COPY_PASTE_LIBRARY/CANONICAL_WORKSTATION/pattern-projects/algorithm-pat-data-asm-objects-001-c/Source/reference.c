#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Assembly objects and exported symbols.
 * Recognition cue: define constants initialized reserved aligned exported data.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */

enum { algorithm_algorithm_pat_data_asm_objects_001_c_BUFFER_WORDS = 8 };

const uint32_t algorithm_algorithm_pat_data_asm_objects_001_c_magic = UINT32_C(0x13579BDF);
uint32_t algorithm_algorithm_pat_data_asm_objects_001_c_initialized_words[4] = {1u, 2u, 3u, 4u};
uint32_t
    algorithm_algorithm_pat_data_asm_objects_001_c_workspace[algorithm_algorithm_pat_data_asm_objects_001_c_BUFFER_WORDS];
const uint32_t algorithm_algorithm_pat_data_asm_objects_001_c_masks[4] = {1u, 2u, 4u, 8u};

uint32_t algorithm_algorithm_pat_data_asm_objects_001_c(const uint32_t *values, uint32_t count) {
  uint32_t sum = 0u;

  if ((values == NULL) && (count != 0u)) {
    return 0u;
  }

  while (count != 0u) {
    sum += *values;
    ++values;
    --count;
  }

  return sum;
}

