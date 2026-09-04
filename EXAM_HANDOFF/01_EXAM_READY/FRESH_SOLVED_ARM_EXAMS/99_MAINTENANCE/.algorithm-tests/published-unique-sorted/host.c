#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t unique_sorted(int32_t *a, uint32_t n) {
  uint32_t k = 0;
  if (a)
    for (uint32_t i = 0; i < n; i++) {
      if (!k || a[i] != a[k - 1])
        a[k++] = a[i];
    }
  return k;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t unique_sorted(int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {1, 1, 2, 3, 3};
  CHECK(unique_sorted(a, 5) == 3 && a[0] == 1 && a[1] == 2 && a[2] == 3);
  CHECK(unique_sorted(0, 0) == 0);
  return 0;
}

int main(void){return test_main();}
