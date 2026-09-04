#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
void shell_sort(int *a, size_t n) {
  size_t gap, i;
  if (a == NULL) return;
  for (gap = n / 2u; gap != 0u; gap /= 2u)
    for (i = gap; i < n; ++i) {
      int value = a[i]; size_t j = i;
      while (j >= gap && a[j-gap] > value) { a[j] = a[j-gap]; j -= gap; }
      a[j] = value;
    }
}
