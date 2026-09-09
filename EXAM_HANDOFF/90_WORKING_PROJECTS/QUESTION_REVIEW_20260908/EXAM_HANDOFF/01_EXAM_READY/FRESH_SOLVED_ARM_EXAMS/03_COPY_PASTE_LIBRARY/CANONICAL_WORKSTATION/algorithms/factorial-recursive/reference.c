#include <limits.h>
#include <stddef.h>
#include <stdint.h>
static uint32_t fact_step(uint32_t n) { return n ? n * fact_step(n - 1) : 1; }
int factorial_recursive(uint32_t n, uint32_t *out) {
  if (!out || n > 12)
    return 0;
  *out = fact_step(n);
  return 1;
}
