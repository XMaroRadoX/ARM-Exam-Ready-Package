#include <limits.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {
  uint8_t stable, candidate;
  uint16_t ticks;
} Debounce;
int debounce_update(Debounce *s, uint8_t sample, uint16_t required, uint8_t *changed) {
  if (s == 0 || changed == 0 || required == 0u)
    return 0;
  *changed = 0u;
  if (sample != s->candidate) {
    s->candidate = sample;
    s->ticks = 1u;
  } else if (s->ticks < required)
    ++s->ticks;
  if (s->ticks == required && s->stable != s->candidate) {
    s->stable = s->candidate;
    *changed = 1u;
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

typedef struct {
  uint8_t stable, candidate;
  uint16_t ticks;
} Debounce;
int debounce_update(Debounce *s, uint8_t sample, uint16_t required, uint8_t *changed);
int test_main(void) {
  Debounce s = {0, 0, 0};
  uint8_t c = 9;
  CHECK(debounce_update(&s, 1, 2, &c) && !c);
  CHECK(debounce_update(&s, 0, 2, &c) && !c);
  CHECK(debounce_update(&s, 1, 2, &c) && !c);
  CHECK(debounce_update(&s, 1, 2, &c) && c && s.stable == 1);
  CHECK(debounce_update(&s, 0, 1, &c) && c && !s.stable);
  return 0;
}

int main(void){return test_main();}
