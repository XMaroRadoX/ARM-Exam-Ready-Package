#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp) {
  if (!n)
    return 1;
  if (!a || !tmp || a == tmp)
    return 0;
  size_t count[256];
  for (unsigned shift = 0; shift < 32; shift += 8) {
    for (size_t b = 0; b < 256; b++)
      count[b] = 0;
    for (size_t i = 0; i < n; i++)
      count[(a[i] >> shift) & 255]++;
    size_t sum = 0;
    for (size_t b = 0; b < 256; b++) {
      size_t c = count[b];
      count[b] = sum;
      sum += c;
    }
    for (size_t i = 0; i < n; i++) {
      unsigned b = (a[i] >> shift) & 255;
      tmp[count[b]++] = a[i];
    }
    for (size_t i = 0; i < n; i++)
      a[i] = tmp[i];
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp);
int test_main(void) {
  uint32_t a[] = {256, 1, UINT32_MAX, 0, 1}, t[5];
  CHECK(radix_sort_u32(a, 5, t) && a[0] == 0 && a[1] == 1 && a[2] == 1 && a[3] == 256 &&
        a[4] == UINT32_MAX);
  CHECK(radix_sort_u32(0, 0, 0));
  CHECK(!radix_sort_u32(a, 5, a));
  return 0;
}

int main(void){return test_main();}
