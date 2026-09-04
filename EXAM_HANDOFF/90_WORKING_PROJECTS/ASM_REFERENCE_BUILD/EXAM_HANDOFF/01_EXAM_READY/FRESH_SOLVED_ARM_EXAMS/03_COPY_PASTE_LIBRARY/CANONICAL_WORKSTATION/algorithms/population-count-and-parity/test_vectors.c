#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Population count and parity.
 * Recognition cue: count set bits parity.
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

uint32_t algorithm_population_count_and_parity(uint32_t value);

uint32_t algorithm_population_count_and_parity_parity(uint32_t value);

static int pattern_core_vector(void) {
  return algorithm_population_count_and_parity(0xf0f0u) == 8;
}
static int pattern_edge_vectors(void) {
  return algorithm_population_count_and_parity(0) == 0 &&
         algorithm_population_count_and_parity(UINT32_MAX) == 32 &&
         algorithm_population_count_and_parity_parity(7) == 1 &&
         algorithm_population_count_and_parity_parity(3) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
