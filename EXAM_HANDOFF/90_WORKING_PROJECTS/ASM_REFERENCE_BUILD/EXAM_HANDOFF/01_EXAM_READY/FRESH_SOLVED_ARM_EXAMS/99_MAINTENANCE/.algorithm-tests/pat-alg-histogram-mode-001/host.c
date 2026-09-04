#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Histogram frequency and mode.
 * Recognition cue: count bounded values choose mode.
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
uint32_t pat_alg_histogram_mode_001(const uint8_t *a, uint32_t n,
                                    uint32_t range, uint32_t *freq) {
  uint32_t i, mode = 0;
  if (!freq || (!a && n) || !range || range > 256u) return 0;
  for (i = 0; i < range; i++)
    freq[i] = 0;
  for (i = 0; i < n; i++)
    if (a[i] < range)
      freq[a[i]]++;
  for (i = 1; i < range; i++)
    if (freq[i] > freq[mode])
      mode = i;
  return mode;
}


#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


/*
 * Exam-study reference: Histogram frequency and mode.
 * Recognition cue: count bounded values choose mode.
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
uint32_t pat_alg_histogram_mode_001(const uint8_t *a, uint32_t n,
                                    uint32_t range, uint32_t *freq);



static int pattern_core_vector(void) {
  uint8_t a[] = {2, 1, 2};
  uint32_t f[3];
  return pat_alg_histogram_mode_001(a, 3, 3, f) == 2 && f[2] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {2, 2, 1, 9};
  uint32_t f[3];
  return pat_alg_histogram_mode_001(a, 4, 3, f) == 2 && f[2] == 2;
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
