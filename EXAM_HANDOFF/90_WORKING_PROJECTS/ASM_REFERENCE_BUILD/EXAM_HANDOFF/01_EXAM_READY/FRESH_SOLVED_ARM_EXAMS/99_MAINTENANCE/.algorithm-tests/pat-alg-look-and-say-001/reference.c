#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded look-and-say generation.
 * Recognition cue: emit count value pairs with output capacity.
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
uint32_t pat_alg_look_and_say_001(const uint8_t *in, uint32_t n, uint8_t *out,
                                  uint32_t cap) {
  uint32_t i = 0, o = 0;
  if (!in || !out)
    return 0;
  while (i < n) {
    uint8_t v = in[i];
    uint32_t c = 1;
    i++;
    while (i < n && in[i] == v) {
      c++;
      i++;
    }
    if (c > 255u || cap - o < 2u)
      return 0;
    out[o++] = (uint8_t)c;
    out[o++] = v;
  }
  return o;
}

