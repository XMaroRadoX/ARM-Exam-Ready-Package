#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Component-label merge.
 * Recognition cue: Kruskal component replacement and stacked arguments.
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
uint32_t algorithm_component_label_merge(uint32_t *label, uint32_t n, uint32_t from,
                                         uint32_t to, uint32_t limit) {
  uint32_t i, c = 0;
  if (!label || n > limit)
    return 0;
  for (i = 0; i < n; i++)
    if (label[i] == from) {
      label[i] = to;
      c++;
    }
  return c;
}
