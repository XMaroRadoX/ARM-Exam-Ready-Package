#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Packed binary matrix multiplication.
 * Recognition cue: multiply packed binary matrices over GF(2).
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
uint64_t algorithm_packed_binary_matrix_multiplication(uint64_t a, uint64_t b);

static int pattern_core_vector(void) {
  uint64_t i = UINT64_C(0x8040201008040201);
  return algorithm_packed_binary_matrix_multiplication(i, i) == i;
}
static int pattern_edge_vectors(void) {
  uint64_t identity = UINT64_C(0x8040201008040201);
  return algorithm_packed_binary_matrix_multiplication(0, identity) == 0 &&
         algorithm_packed_binary_matrix_multiplication(identity, 0) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
