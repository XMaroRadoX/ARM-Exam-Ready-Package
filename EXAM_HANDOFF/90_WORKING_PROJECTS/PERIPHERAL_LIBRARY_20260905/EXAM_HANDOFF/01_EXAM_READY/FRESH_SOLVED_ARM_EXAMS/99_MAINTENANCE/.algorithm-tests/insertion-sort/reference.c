#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
void insertion_sort(int *a, size_t n) {
  size_t i;
  if (a == NULL) return;
  for (i = 1; i < n; ++i) {
    int key = a[i];
    size_t j = i;
    while (j != 0u && a[j - 1u] > key) {
      a[j] = a[j - 1u];
      --j;
    }
    a[j] = key;
  }
}
