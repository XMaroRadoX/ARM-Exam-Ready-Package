#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Breadth-first search.
 * Recognition cue: graph traversal explicit queue.
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
uint32_t algorithm_breadth_first_search(const uint8_t *adj, uint32_t n, uint32_t start,
                                        uint8_t *seen, uint32_t *q) {
  uint32_t h = 0, t = 0, c = 0;
  if (!adj || !seen || !q || start >= n || n > 65535u)
    return 0;
  seen[start] = 1;
  q[t++] = start;
  while (h < t) {
    uint32_t v = q[h++], w;
    c++;
    for (w = 0; w < n; w++)
      if (adj[v * n + w] && !seen[w]) {
        seen[w] = 1;
        q[t++] = w;
      }
  }
  return c;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


/*
 * Exam-study reference: Breadth-first search.
 * Recognition cue: graph traversal explicit queue.
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
uint32_t algorithm_breadth_first_search(const uint8_t *adj, uint32_t n, uint32_t start,
                                        uint8_t *seen, uint32_t *q);

static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  uint32_t q[3];
  return algorithm_breadth_first_search(a, 3, 0, s, q) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t a[1] = {0}, s[1] = {0};
  uint32_t q[1];
  return algorithm_breadth_first_search(a, 1, 0, s, q) == 1 &&
         algorithm_breadth_first_search(a, 1, 1, s, q) == 0 &&
         algorithm_breadth_first_search(NULL, 1, 0, s, q) == 0;
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
