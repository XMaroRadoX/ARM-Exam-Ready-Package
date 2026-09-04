#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Recursive DFS with depth contract.
 * Recognition cue: recursive graph traversal bounded depth.
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
uint32_t visit(const uint8_t *a, uint32_t n, uint32_t v, uint8_t *s, uint32_t depth);
uint32_t algorithm_recursive_dfs_with_depth_contract(const uint8_t *a, uint32_t n,
                                                     uint32_t start, uint8_t *s);

static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  return algorithm_recursive_dfs_with_depth_contract(a, 3, 0, s) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[1] = {0}, s[1] = {0};
  return algorithm_recursive_dfs_with_depth_contract(a, 1, 0, s) == 1 &&
         algorithm_recursive_dfs_with_depth_contract(a, 1, 1, s) == 0 &&
         algorithm_recursive_dfs_with_depth_contract(NULL, 1, 0, s) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
