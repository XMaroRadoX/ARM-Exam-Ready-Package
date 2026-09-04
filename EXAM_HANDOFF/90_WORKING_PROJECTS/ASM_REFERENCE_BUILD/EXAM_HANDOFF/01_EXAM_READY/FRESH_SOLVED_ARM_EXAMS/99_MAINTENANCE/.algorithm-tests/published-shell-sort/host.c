#include <limits.h>
#include <stddef.h>
#include <stdint.h>
void shell_sort(int *a, size_t n) {
  size_t gap, i;
  if (a == NULL)
    return;
  for (gap = n / 2u; gap != 0u; gap /= 2u)
    for (i = gap; i < n; ++i) {
      int value = a[i];
      size_t j = i;
      while (j >= gap && a[j - gap] > value) {
        a[j] = a[j - gap];
        j -= gap;
      }
      a[j] = value;
    }
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

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

int main(void){return test_main();}
