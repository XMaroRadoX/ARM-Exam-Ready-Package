#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Run-length encoding.
 * Recognition cue: compress consecutive equal values including final run.
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
uint32_t algorithm_run_length_final_run_handling(const uint8_t *in, uint32_t n,
                                                 uint8_t *value, uint8_t *run,
                                                 uint32_t cap) {
  uint32_t i = 0, o = 0;
  if (!in || !value || !run)
    return 0;
  while (i < n) {
    uint8_t v = in[i], c = 1;
    i++;
    while (i < n && in[i] == v && c < 255u) {
      c++;
      i++;
    }
    if (o >= cap)
      return 0;
    value[o] = v;
    run[o] = c;
    o++;
  }
  return o;
}
