#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int quickselect(int *a, size_t n, size_t k, int *out) {
  size_t lo = 0u, hi;
  if (a == NULL || out == NULL || k >= n)
    return 0;
  hi = n - 1u;
  for (;;) {
    size_t i, j = lo;
    int p = a[hi];
    for (i = lo; i < hi; ++i)
      if (a[i] < p) {
        int t = a[i];
        a[i] = a[j];
        a[j++] = t;
      }
    a[hi] = a[j];
    a[j] = p;
    if (j == k) {
      *out = a[j];
      return 1;
    }
    if (k < j)
      hi = j - 1u;
    else
      lo = j + 1u;
  }
}
