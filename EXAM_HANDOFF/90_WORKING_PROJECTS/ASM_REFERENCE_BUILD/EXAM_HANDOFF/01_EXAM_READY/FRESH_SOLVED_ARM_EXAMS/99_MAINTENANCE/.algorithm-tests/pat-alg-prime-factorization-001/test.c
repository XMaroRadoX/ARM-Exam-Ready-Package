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

int pat_alg_prime_factorization_001(uint32_t value);

uint32_t pat_alg_prime_factorization_001_factorize(uint32_t value,
                                                   uint32_t *factors,
                                                   uint32_t capacity);



static int pattern_core_vector(void) {
  return pat_alg_prime_factorization_001(29) &&
         !pat_alg_prime_factorization_001(21) &&
         !pat_alg_prime_factorization_001(1);
}
static int pattern_edge_vectors(void) {
  uint32_t f[4] = {0};
  return pat_alg_prime_factorization_001(2) &&
         !pat_alg_prime_factorization_001(0) &&
         pat_alg_prime_factorization_001_factorize(12, f, 4) == 3 &&
         f[0] == 2 && f[1] == 2 && f[2] == 3 &&
         pat_alg_prime_factorization_001_factorize(1, f, 4) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
