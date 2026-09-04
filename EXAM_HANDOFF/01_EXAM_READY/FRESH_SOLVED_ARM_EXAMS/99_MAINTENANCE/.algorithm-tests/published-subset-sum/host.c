#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int subset_sum(const unsigned short *a, size_t n, size_t target, unsigned char *r) {
  if (!a || !r || target == SIZE_MAX)
    return 0;
  for (size_t s = 0; s <= target; s++)
    r[s] = 0;
  r[0] = 1;
  for (size_t i = 0; i < n; i++)
    if (a[i])
      for (size_t s = target + 1; s > a[i];) {
        --s;
        if (r[s - a[i]])
          r[s] = 1;
      }
  return r[target] != 0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int subset_sum(const unsigned short *a, size_t n, size_t target,
               unsigned char *reachable);
int test_main(void) {
  unsigned short a[] = {3, 5};
  unsigned char r[10];
  CHECK(!subset_sum(a, 2, 6, r));
  CHECK(subset_sum(a, 2, 8, r));
  CHECK(subset_sum(a, 0, 0, r));
  return 0;
}

int main(void){return test_main();}
