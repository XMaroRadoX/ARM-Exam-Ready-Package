#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int second_smallest(const int32_t *a, uint32_t n, int32_t *out) {
  if (!a || !out || !n)
    return 0;
  int32_t best = a[0], second = 0;
  int have = 0;
  for (uint32_t i = 1; i < n; i++) {
    int32_t x = a[i];
    if (x < best) {
      second = best;
      best = x;
      have = 1;
    } else if (x != best && (!have || x < second)) {
      second = x;
      have = 1;
    }
  }
  if (have)
    *out = second;
  return have;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int second_smallest(const int32_t *a, uint32_t n, int32_t *out);
int test_main(void) {
  int32_t a[] = {4, 9, 9, 2}, e[] = {INT32_MIN, INT32_MAX}, v = 77;
  CHECK(second_smallest(a, 4, &v) && v == 4);
  CHECK(second_smallest(e, 2, &v) && v == INT32_MAX);
  v = 77;
  CHECK(!second_smallest(a, 1, &v) && v == 77);
  CHECK(!second_smallest(0, 0, &v));
  return 0;
}

int main(void){return test_main();}
