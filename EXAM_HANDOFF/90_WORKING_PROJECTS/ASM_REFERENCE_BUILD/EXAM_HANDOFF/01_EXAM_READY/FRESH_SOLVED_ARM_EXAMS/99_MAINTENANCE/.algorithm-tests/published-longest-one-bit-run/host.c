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

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t longest_one_run(uint32_t value);
int test_main(void) {
  CHECK(longest_one_run(110) == 3);
  CHECK(longest_one_run(0) == 0);
  CHECK(longest_one_run(0xffffffffu) == 32);
  return 0;
}

int main(void){return test_main();}
