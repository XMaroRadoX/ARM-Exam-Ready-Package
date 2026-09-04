#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Prime testing and trial factorization.
 * Recognition cue: test prime using divisors through square root.
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

int algorithm_prime_testing_and_trial_factorization(uint32_t value);

uint32_t algorithm_prime_testing_and_trial_factorization_factorize(uint32_t value,
                                                                   uint32_t *factors,
                                                                   uint32_t capacity);

static int pattern_core_vector(void) {
  return algorithm_prime_testing_and_trial_factorization(29) &&
         !algorithm_prime_testing_and_trial_factorization(21) &&
         !algorithm_prime_testing_and_trial_factorization(1);
}
static int pattern_edge_vectors(void) {
  uint32_t f[4] = {0};
  return algorithm_prime_testing_and_trial_factorization(2) &&
         !algorithm_prime_testing_and_trial_factorization(0) &&
         algorithm_prime_testing_and_trial_factorization_factorize(12, f, 4) == 3 &&
         f[0] == 2 && f[1] == 2 && f[2] == 3 &&
         algorithm_prime_testing_and_trial_factorization_factorize(1, f, 4) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
