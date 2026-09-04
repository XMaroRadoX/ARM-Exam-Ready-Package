#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
void insertion_sort(int *a, size_t n);
int test_main(void) {
  int a[] = {3, 1, 2, INT_MIN, INT_MAX, 2};
  insertion_sort(a, 6);
  CHECK(a[0] == INT_MIN && a[1] == 1 && a[2] == 2 && a[3] == 2 && a[4] == 3 &&
        a[5] == INT_MAX);
  insertion_sort(0, 0);
  return 0;
}
