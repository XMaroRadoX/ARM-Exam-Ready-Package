#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int32_t recursive_binary_search(const int32_t *a, uint32_t n, int32_t key) {
  if (!a || !n || n > INT32_MAX)
    return -1;
  uint32_t m = n / 2;
  if (a[m] == key)
    return (int32_t)m;
  if (key < a[m])
    return recursive_binary_search(a, m, key);
  int32_t p = recursive_binary_search(a + m + 1, n - m - 1, key);
  return p < 0 ? -1 : (int32_t)(m + 1) + (int32_t)p;
}
