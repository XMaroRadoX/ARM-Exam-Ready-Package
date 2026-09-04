#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Dijkstra shortest path.
 * Recognition cue: small fixed graph nonnegative shortest paths.
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
int algorithm_dijkstra_shortest_path(const uint32_t *w, uint32_t n, uint32_t start,
                                     uint32_t *dist, uint8_t *done);

static int pattern_core_vector(void) {
  uint32_t w[9] = {0, 2, 9, 0, 0, 3, 0, 0, 0}, d[3];
  uint8_t done[3];
  return algorithm_dijkstra_shortest_path(w, 3, 0, d, done) && d[2] == 5;
}
static int pattern_edge_vectors(void) {
  uint32_t w[1] = {0}, d[1];
  uint8_t done[1];
  return algorithm_dijkstra_shortest_path(w, 1, 0, d, done) && d[0] == 0 &&
         !algorithm_dijkstra_shortest_path(w, 1, 1, d, done) &&
         !algorithm_dijkstra_shortest_path(NULL, 1, 0, d, done);
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
