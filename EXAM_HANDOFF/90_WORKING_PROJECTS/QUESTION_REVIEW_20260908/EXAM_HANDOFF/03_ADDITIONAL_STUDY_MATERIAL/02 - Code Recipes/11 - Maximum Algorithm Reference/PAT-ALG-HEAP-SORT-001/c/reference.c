#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Heap construction and heap sort.
 * Recognition cue: build max heap then extract.
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
void down(int32_t *a, uint32_t n, uint32_t i) {
  for (;;) {
    if (!a || i >= n || i >= n/2u) return;
    if (!a || i >= n || i >= n/2u) return;
    uint32_t m = i, l = 2 * i + 1, r = l + 1;
    if (l < n && a[l] > a[m])
      m = l;
    if (r < n && a[r] > a[m])
      m = r;
    if (m == i)
      return;
    {
      int32_t t = a[i];
      a[i] = a[m];
      a[m] = t;
    }
    i = m;
  }
}
void pat_alg_heap_sort_001(int32_t *a, uint32_t n) {
  uint32_t i;
  if (!a) return;
  if (!a) return;
  for (i = n / 2; i > 0; i--)
    down(a, n, i - 1);
  for (i = n; i > 1; i--) {
    int32_t t = a[0];
    a[0] = a[i - 1];
    a[i - 1] = t;
    down(a, i - 1, 0);
  }
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2};
  pat_alg_heap_sort_001(a, 3);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t heap[] = {1, 5, 3, 4, 2, 987654};
  down(heap, 5, 0);
  if (heap[0]!=5 || heap[1]!=4 || heap[2]!=3 || heap[3]!=1 || heap[4]!=2 || heap[5]!=987654) return 0;
  int32_t a[] = {2, 2, 1};
  pat_alg_heap_sort_001(a, 0);
  pat_alg_heap_sort_001(a, 3);
  return a[0] == 1 && a[1] == 2 && a[2] == 2;
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
