#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
size_t topological_sort(const uint8_t *a, size_t n, size_t *degree, size_t *queue,
                        size_t *out);
int test_main(void) {
  uint8_t a[] = {0, 1, 0, 0, 0, 1, 0, 0, 0};
  size_t d[3], q[3], o[3];
  CHECK(topological_sort(a, 3, d, q, o) == 3 && o[0] == 0 && o[2] == 2);
  a[6] = 1;
  CHECK(topological_sort(a, 3, d, q, o) == 0);
  return 0;
}
