#include <limits.h>
#include <stddef.h>
#include <stdint.h>
size_t upper_bound_i32(const int *a, size_t n, int key) {
  size_t lo = 0u, hi = n;
  if (a == NULL)
    return 0u;
  while (lo < hi) {
    size_t m = lo + (hi - lo) / 2u;
    if (a[m] <= key)
      lo = m + 1u;
    else
      hi = m;
  }
  return lo;
}
