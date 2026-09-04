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
int pat_alg_dijkstra_001(const uint32_t *w, uint32_t n, uint32_t start,
                         uint32_t *dist, uint8_t *done) {
  uint32_t i, k;
  if (!w || !dist || !done || start >= n || n > 32767u)
    return 0;
  for (i = 0; i < n; i++) {
    dist[i] = 0xffffffffu;
    done[i] = 0;
  }
  dist[start] = 0;
  for (k = 0; k < n; k++) {
    uint32_t u = n, best = 0xffffffffu;
    for (i = 0; i < n; i++)
      if (!done[i] && dist[i] < best) {
        best = dist[i];
        u = i;
      }
    if (u == n)
      break;
    done[u] = 1;
    for (i = 0; i < n; i++)
      if (w[u * n + i] && dist[u] != 0xffffffffu &&
          dist[u] <= 0xffffffffu - w[u * n + i] &&
          dist[u] + w[u * n + i] < dist[i])
        dist[i] = dist[u] + w[u * n + i];
  }
  return 1;
}

