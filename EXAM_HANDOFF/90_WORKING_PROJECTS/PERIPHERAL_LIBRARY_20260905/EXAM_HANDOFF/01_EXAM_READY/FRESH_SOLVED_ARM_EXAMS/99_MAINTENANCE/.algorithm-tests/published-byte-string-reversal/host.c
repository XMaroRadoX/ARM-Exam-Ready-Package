#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int bytes_reverse(uint8_t *s, uint32_t n) {
  if (!s && n)
    return 0;
  for (uint32_t i = 0; i < n / 2; i++) {
    uint8_t t = s[i];
    s[i] = s[n - 1 - i];
    s[n - 1 - i] = t;
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int bytes_reverse(uint8_t *text, uint32_t length);
int test_main(void) {
  uint8_t a[] = {1, 2, 3, 4, 77};
  CHECK(bytes_reverse(a, 4) && a[0] == 4 && a[3] == 1 && a[4] == 77);
  CHECK(bytes_reverse(0, 0));
  CHECK(!bytes_reverse(0, 1));
  return 0;
}

int main(void){return test_main();}
