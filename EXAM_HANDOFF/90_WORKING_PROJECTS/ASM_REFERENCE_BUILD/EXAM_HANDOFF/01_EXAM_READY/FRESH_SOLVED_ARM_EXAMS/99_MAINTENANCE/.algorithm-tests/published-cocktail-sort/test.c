#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
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
