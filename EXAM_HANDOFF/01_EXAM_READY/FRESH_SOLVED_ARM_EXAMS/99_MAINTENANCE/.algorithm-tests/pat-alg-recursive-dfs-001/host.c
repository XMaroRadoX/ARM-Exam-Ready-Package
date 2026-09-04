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
uint32_t visit(const uint8_t *a, uint32_t n, uint32_t v, uint8_t *s,
               uint32_t depth) {
  uint32_t w, c = 1;
  if (!a || !s || v >= n || !depth || depth > n || s[v])
    return 0;
  s[v] = 1;
  for (w = 0; w < n; w++)
    if (a[v * n + w] && !s[w])
      c += visit(a, n, w, s, depth + 1);
  return c;
}
uint32_t pat_alg_recursive_dfs_001(const uint8_t *a, uint32_t n, uint32_t start,
                                   uint8_t *s) {
  return (!a || !s || start >= n || n > 256u) ? 0 : visit(a, n, start, s, 1);
}


#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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
uint32_t visit(const uint8_t *a, uint32_t n, uint32_t v, uint8_t *s,
               uint32_t depth);
uint32_t pat_alg_recursive_dfs_001(const uint8_t *a, uint32_t n, uint32_t start,
                                   uint8_t *s);



static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  return pat_alg_recursive_dfs_001(a, 3, 0, s) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[1] = {0}, s[1] = {0};
  return pat_alg_recursive_dfs_001(a, 1, 0, s) == 1 &&
         pat_alg_recursive_dfs_001(a, 1, 1, s) == 0 &&
         pat_alg_recursive_dfs_001(NULL, 1, 0, s) == 0;
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
