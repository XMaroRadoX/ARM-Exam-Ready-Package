#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int64_t maximum_subarray(const int32_t *a, uint32_t n) {
  if (!a || !n)
    return 0;
  int64_t cur = a[0], best = cur;
  for (uint32_t i = 1; i < n; i++) {
    if (cur < 0)
      cur = 0;
    cur += a[i];
    if (cur > best)
      best = cur;
  }
  return best;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int64_t maximum_subarray(const int32_t *a, uint32_t n);
int test_main(void) {
  int32_t a[] = {-2, 3, -1, 4, -8}, b[] = {-9, -2, -7}, c[] = {INT32_MAX, INT32_MAX};
  CHECK(maximum_subarray(a, 5) == 6);
  CHECK(maximum_subarray(b, 3) == -2);
  CHECK(maximum_subarray(c, 2) == 4294967294LL);
  CHECK(maximum_subarray(0, 0) == 0);
  return 0;
}

int main(void){return test_main();}
