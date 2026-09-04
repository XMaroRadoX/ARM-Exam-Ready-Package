#include <limits.h>
#include <stddef.h>
#include <stdint.h>
void insertion_sort(int *a, size_t n) {
  size_t i;
  if (a == NULL)
    return;
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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

void insertion_sort(int *a, size_t n);
int test_main(void) {
  int a[] = {3, 1, 2, INT_MIN, INT_MAX, 2};
  insertion_sort(a, 6);
  CHECK(a[0] == INT_MIN && a[1] == 1 && a[2] == 2 && a[3] == 2 && a[4] == 3 &&
        a[5] == INT_MAX);
  insertion_sort(0, 0);
  return 0;
}

int main(void){return test_main();}
