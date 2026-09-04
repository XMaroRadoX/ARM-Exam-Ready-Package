#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
void cocktail_sort(int *a, size_t n) {
  size_t lo = 0u, hi = n;
  int changed = 1;
  if (a == NULL) return;
  while (changed && hi > lo + 1u) {
    size_t i;
    changed = 0;
    for (i = lo + 1u; i < hi; ++i) if (a[i - 1u] > a[i]) { int t=a[i-1u]; a[i-1u]=a[i]; a[i]=t; changed=1; }
    if (!changed) break;
    --hi; changed = 0;
    for (i = hi - 1u; i > lo; --i) if (a[i - 1u] > a[i]) { int t=a[i-1u]; a[i-1u]=a[i]; a[i]=t; changed=1; }
    ++lo;
  }
}
