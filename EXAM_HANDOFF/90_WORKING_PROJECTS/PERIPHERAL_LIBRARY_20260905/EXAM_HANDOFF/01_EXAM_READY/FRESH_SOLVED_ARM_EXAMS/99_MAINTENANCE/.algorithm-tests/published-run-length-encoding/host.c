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
uint32_t algorithm_run_length_encoding(const uint8_t *in, uint32_t n, uint8_t *value,
                                       uint8_t *run, uint32_t cap) {
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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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
uint32_t algorithm_run_length_encoding(const uint8_t *in, uint32_t n, uint8_t *value,
                                       uint8_t *run, uint32_t cap);

static int pattern_core_vector(void) {
  uint8_t a[] = {1, 1, 2}, v[3] = {0}, r[3] = {0};
  return algorithm_run_length_encoding(a, 3, v, r, 3) == 2 && v[0] == 1 && r[0] == 2 &&
         v[1] == 2 && r[1] == 1;
}
static int pattern_edge_vectors(void) {
  uint8_t v[2], r[2], a[] = {9};
  return algorithm_run_length_encoding(a, 0, v, r, 2) == 0 &&
         algorithm_run_length_encoding(a, 1, v, r, 2) == 1 && v[0] == 9 && r[0] == 1 &&
         algorithm_run_length_encoding(a, 1, v, r, 0) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

int main(void){return test_main();}
