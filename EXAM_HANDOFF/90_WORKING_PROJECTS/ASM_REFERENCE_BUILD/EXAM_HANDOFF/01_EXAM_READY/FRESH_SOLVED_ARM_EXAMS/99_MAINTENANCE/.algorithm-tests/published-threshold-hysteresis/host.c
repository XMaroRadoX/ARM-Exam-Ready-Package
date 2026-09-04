#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int hysteresis_update(uint16_t sample, uint16_t low, uint16_t high, uint8_t *state) {
  if (state == 0 || low >= high)
    return 0;
  if (*state == 0u && sample >= high)
    *state = 1u;
  else if (*state != 0u && sample <= low)
    *state = 0u;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int hysteresis_update(uint16_t sample, uint16_t low, uint16_t high, uint8_t *state);
int test_main(void) {
  uint8_t s = 0;
  CHECK(hysteresis_update(21, 10, 20, &s) && s == 1);
  CHECK(hysteresis_update(15, 10, 20, &s) && s == 1);
  CHECK(hysteresis_update(9, 10, 20, &s) && s == 0);
  CHECK(!hysteresis_update(1, 20, 10, &s));
  return 0;
}

int main(void){return test_main();}
