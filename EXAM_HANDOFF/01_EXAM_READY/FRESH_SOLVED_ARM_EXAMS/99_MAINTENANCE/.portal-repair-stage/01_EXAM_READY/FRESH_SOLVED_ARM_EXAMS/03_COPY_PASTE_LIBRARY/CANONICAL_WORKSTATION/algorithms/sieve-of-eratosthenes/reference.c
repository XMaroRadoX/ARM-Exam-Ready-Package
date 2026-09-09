#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int prime_sieve(uint8_t *f, uint32_t n, uint32_t cap) {
  if (!f || n > 65535 || cap <= n)
    return 0;
  for (uint32_t i = 0; i <= n; i++)
    f[i] = i >= 2;
  for (uint32_t p = 2; p <= n / p; p++)
    if (f[p])
      for (uint32_t j = p * p; j <= n; j += p)
        f[j] = 0;
  return 1;
}
