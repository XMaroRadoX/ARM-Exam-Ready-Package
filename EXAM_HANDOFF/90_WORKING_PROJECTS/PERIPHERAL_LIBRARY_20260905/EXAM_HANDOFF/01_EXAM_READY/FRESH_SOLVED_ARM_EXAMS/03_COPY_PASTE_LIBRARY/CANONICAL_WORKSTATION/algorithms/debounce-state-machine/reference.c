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
