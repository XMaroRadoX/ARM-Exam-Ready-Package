#include <limits.h>
#include <stddef.h>
#include <stdint.h>
void cocktail_sort(int *a, size_t n) {
  size_t lo = 0u, hi = n;
  int changed = 1;
  if (a == NULL)
    return;
  while (changed && hi > lo + 1u) {
    size_t i;
    changed = 0;
    for (i = lo + 1u; i < hi; ++i)
      if (a[i - 1u] > a[i]) {
        int t = a[i - 1u];
        a[i - 1u] = a[i];
        a[i] = t;
        changed = 1;
      }
    if (!changed)
      break;
    --hi;
    changed = 0;
    for (i = hi - 1u; i > lo; --i)
      if (a[i - 1u] > a[i]) {
        int t = a[i - 1u];
        a[i - 1u] = a[i];
        a[i] = t;
        changed = 1;
      }
    ++lo;
  }
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

void cocktail_sort(int *a, size_t n);
int test_main(void) {
  int a[] = {3, 2, 1, INT_MIN, INT_MAX, 2};
  cocktail_sort(a, 6);
  for (int i = 1; i < 6; i++)
    CHECK(a[i - 1] <= a[i]);
  CHECK(a[0] == INT_MIN && a[5] == INT_MAX);
  cocktail_sort(0, 0);
  return 0;
}

int main(void){return test_main();}
