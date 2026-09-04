#include <limits.h>
#include <stddef.h>
#include <stdint.h>
uint32_t longest_one_run(uint32_t v) {
  uint32_t best = 0, run = 0;
  for (unsigned i = 0; i < 32; i++) {
    run = (v & 1) ? run + 1 : 0;
    if (run > best)
      best = run;
    v >>= 1;
  }
  return best;
}
