#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int majority_element(const int32_t *a, uint32_t n, int32_t *out) {
  if (!a || !n || !out)
    return 0;
  int32_t v = 0;
  uint32_t votes = 0, c = 0;
  for (uint32_t i = 0; i < n; i++) {
    if (!votes) {
      v = a[i];
      votes = 1;
    } else if (v == a[i])
      votes++;
    else
      votes--;
  }
  for (uint32_t i = 0; i < n; i++)
    c += a[i] == v;
  if (c <= n / 2)
    return 0;
  *out = v;
  return 1;
}
