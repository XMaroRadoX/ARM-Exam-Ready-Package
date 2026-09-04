#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int prime_sieve(uint8_t *flags, uint32_t limit, uint32_t capacity);
int test_main(void) {
  uint8_t f[12] = {0};
  f[11] = 77;
  CHECK(prime_sieve(f, 10, 11) && f[2] && f[3] && f[5] && f[7] && !f[0] && !f[1] &&
        !f[4] && !f[9] && f[11] == 77);
  CHECK(!prime_sieve(f, 10, 10));
  return 0;
}
