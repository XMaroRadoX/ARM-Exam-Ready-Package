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
uint32_t algorithm_seven_argument_component_merge(uint32_t *label, uint32_t n,
                                                  uint32_t from, uint32_t to,
                                                  uint32_t limit) {
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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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
uint32_t algorithm_seven_argument_component_merge(uint32_t *label, uint32_t n,
                                                  uint32_t from, uint32_t to,
                                                  uint32_t limit);

static int pattern_core_vector(void) {
  uint32_t a[] = {1, 2, 1};
  return algorithm_seven_argument_component_merge(a, 3, 1, 2, 3) == 2 && a[0] == 2 &&
         a[2] == 2;
}
static int pattern_edge_vectors(void) {
  uint32_t a[] = {1, 1};
  return algorithm_seven_argument_component_merge(a, 2, 1, 2, 1) == 0 &&
         algorithm_seven_argument_component_merge(NULL, 0, 1, 2, 0) == 0;
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
