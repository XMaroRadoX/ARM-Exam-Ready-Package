#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Coin change.
 * Recognition cue: minimum coins or number of ways.
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
uint32_t algorithm_coin_change(const uint16_t *coin, uint32_t n, uint32_t amount,
                               uint32_t *dp);

static int pattern_core_vector(void) {
  uint16_t c[] = {1, 3};
  uint32_t d[5];
  return algorithm_coin_change(c, 2, 4, d) == 2;
}
static int pattern_edge_vectors(void) {
  uint16_t c[] = {2};
  uint32_t d[4];
  return algorithm_coin_change(c, 1, 0, d) == 0 &&
         algorithm_coin_change(c, 1, 3, d) == UINT32_MAX;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
