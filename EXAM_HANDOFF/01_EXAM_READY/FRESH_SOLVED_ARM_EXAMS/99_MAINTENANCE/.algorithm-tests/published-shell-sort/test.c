#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
void shell_sort(int *a, size_t n);
int test_main(void) {
  int a[] = {9, 3, 7, 1, -5, INT_MAX, INT_MIN};
  shell_sort(a, 7);
  for (int i = 1; i < 7; i++)
    CHECK(a[i - 1] <= a[i]);
  CHECK(a[0] == INT_MIN && a[6] == INT_MAX);
  shell_sort(0, 0);
  return 0;
}
