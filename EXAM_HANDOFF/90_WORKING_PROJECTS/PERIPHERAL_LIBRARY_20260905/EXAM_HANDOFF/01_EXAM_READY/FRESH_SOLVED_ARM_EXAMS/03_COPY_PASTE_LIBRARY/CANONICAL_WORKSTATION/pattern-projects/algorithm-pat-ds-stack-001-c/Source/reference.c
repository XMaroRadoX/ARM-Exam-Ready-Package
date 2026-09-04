#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Array-backed stack.
 * Recognition cue: bounded LIFO push pop.
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
int algorithm_algorithm_pat_ds_stack_001_c(int32_t *a, uint32_t cap, uint32_t *top, int push,
                     int32_t *value) {
  if (!a || !top || !value || *top > cap)
    return 0;
  if (push) {
    if (*top >= cap)
      return 0;
    a[(*top)++] = *value;
  } else {
    if (!*top)
      return 0;
    *value = a[--*top];
  }
  return 1;
}

