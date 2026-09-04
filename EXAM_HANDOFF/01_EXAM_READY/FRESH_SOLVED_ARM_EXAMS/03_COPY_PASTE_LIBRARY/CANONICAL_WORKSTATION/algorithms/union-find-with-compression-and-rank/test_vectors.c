#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Union-find with compression and rank.
 * Recognition cue: disjoint set find union.
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
uint32_t find(uint32_t *p, uint32_t x);
int algorithm_union_find_with_compression_and_rank(uint32_t *p, uint8_t *r, uint32_t n,
                                                   uint32_t a, uint32_t b);

static int pattern_core_vector(void) {
  uint32_t p[] = {0, 1, 2};
  uint8_t r[3] = {0};
  return algorithm_union_find_with_compression_and_rank(p, r, 3, 0, 1) &&
         find(p, 0) == find(p, 1);
}
static int pattern_edge_vectors(void) {
  uint32_t p[] = {0, 1};
  uint8_t r[2] = {0};
  return algorithm_union_find_with_compression_and_rank(p, r, 2, 0, 1) &&
         algorithm_union_find_with_compression_and_rank(p, r, 2, 0, 1) &&
         find(p, 0) == find(p, 1) &&
         !algorithm_union_find_with_compression_and_rank(p, r, 2, 0, 2);
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
