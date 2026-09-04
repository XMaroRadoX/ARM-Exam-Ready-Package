#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t longest_equal_run(const int32_t *a, uint32_t n) {
  if (!a || !n)
    return 0;
  uint32_t r = 1, b = 1;
  for (uint32_t i = 1; i < n; i++) {
    r = a[i] == a[i - 1] ? r + 1 : 1;
    if (r > b)
      b = r;
  }
  return b;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t longest_equal_run(const int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {1, 2, 2, 3, 4}, b[] = {-1, -1, -1};
  CHECK(longest_equal_run(a, 5) == 2);
  CHECK(longest_equal_run(b, 3) == 3);
  CHECK(longest_equal_run(0, 0) == 0);
  return 0;
}

int main(void){return test_main();}
