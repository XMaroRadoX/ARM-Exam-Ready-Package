#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Flood fill and maze propagation.
 * Recognition cue: fill connected grid cells.
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
uint32_t pat_alg_flood_fill_001(uint8_t *g, uint32_t rows, uint32_t cols,
                                uint32_t start, uint8_t oldv, uint8_t newv,
                                uint32_t *q) {
  uint32_t h = 0, t = 0, c = 0;
  if (!cols || rows > UINT32_MAX / cols) return 0;
  uint32_t n = rows * cols;
  if (!g || !q || start >= n || oldv == newv || g[start] != oldv)
    return 0;
  g[start] = newv;
  q[t++] = start;
  while (h < t) {
    uint32_t p = q[h++], r = p / cols, x = p % cols;
    c++;
    if (r && g[p - cols] == oldv) {
      g[p - cols] = newv;
      q[t++] = p - cols;
    }
    if (r + 1 < rows && g[p + cols] == oldv) {
      g[p + cols] = newv;
      q[t++] = p + cols;
    }
    if (x && g[p - 1] == oldv) {
      g[p - 1] = newv;
      q[t++] = p - 1;
    }
    if (x + 1 < cols && g[p + 1] == oldv) {
      g[p + 1] = newv;
      q[t++] = p + 1;
    }
  }
  return c;
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  uint8_t g[] = {1, 1, 0, 1};
  uint32_t q[4];
  return pat_alg_flood_fill_001(g, 2, 2, 0, 1, 2, q) == 3 && g[3] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t g[] = {1};
  uint32_t q[1];
  return pat_alg_flood_fill_001(g, 1, 1, 0, 1, 2, q) == 1 && g[0] == 2 &&
         pat_alg_flood_fill_001(g, 1, 1, 0, 2, 2, q) == 0 &&
         pat_alg_flood_fill_001(NULL, 1, 1, 0, 1, 2, q) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int main(void) { return pattern_test_suite(); }
#endif
