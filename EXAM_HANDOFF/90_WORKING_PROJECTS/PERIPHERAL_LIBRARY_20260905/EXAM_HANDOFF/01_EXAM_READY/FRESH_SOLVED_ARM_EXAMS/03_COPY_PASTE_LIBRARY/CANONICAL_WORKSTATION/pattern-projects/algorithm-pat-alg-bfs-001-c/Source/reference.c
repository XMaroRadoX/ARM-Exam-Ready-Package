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
uint32_t algorithm_algorithm_pat_alg_bfs_001_c(const uint8_t *adj, uint32_t n, uint32_t start,
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

