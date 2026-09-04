#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int floyd_warshall(int *d, size_t n, int inf) {
  if (!d || n > 256 || inf <= 0)
    return 0;
  for (size_t k = 0; k < n; k++)
    for (size_t i = 0; i < n; i++)
      for (size_t j = 0; j < n; j++)
        if (d[i * n + k] != inf && d[k * n + j] != inf) {
          int64_t x = (int64_t)d[i * n + k] + d[k * n + j];
          if (x < INT_MIN || x > INT_MAX)
            return 0;
          if (x < d[i * n + j])
            d[i * n + j] = (int)x;
        }
  for (size_t i = 0; i < n; i++)
    if (d[i * n + i] < 0)
      return 0;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int floyd_warshall(int *distance, size_t n, int infinity);
int test_main(void) {
  int d[] = {0, 4, 9, 999, 0, -2, 999, 999, 0};
  CHECK(floyd_warshall(d, 3, 999) && d[2] == 2 && d[3] == 999);
  int cyc[] = {0, -1, -1, 0};
  CHECK(!floyd_warshall(cyc, 2, 999));
  int big[] = {0, INT_MAX - 1, INT_MAX - 1, 0};
  CHECK(!floyd_warshall(big, 2, INT_MAX));
  return 0;
}

int main(void){return test_main();}
