#include "simulated_board.h"
#include <string.h>
void sim_board_reset(sim_board_t *b) { memset(b, 0, sizeof(*b)); }
int sim_timer_config(sim_board_t *b, unsigned id, uint32_t match, uint8_t reset, uint8_t irq) {
  if (id >= SIM_TIMER_COUNT || match == 0u) return -1;
  b->timer[id].match=match; b->timer[id].reset_on_match=reset; b->timer[id].irq_enabled=irq; b->timer[id].running=1u; return 0;
}
void sim_step(sim_board_t *b, uint32_t ticks) {
  unsigned i; b->ticks += ticks;
  for (i=0; i<SIM_TIMER_COUNT; ++i) { sim_timer_t *t=&b->timer[i]; if (!t->running) continue; t->counter += ticks;
    if (t->counter >= t->match) { if (t->irq_enabled) t->irq_pending=1u; if (t->reset_on_match) t->counter %= t->match; }
  }
}
void sim_gpio_input(sim_board_t *b, uint32_t mask, uint8_t pressed) { if (pressed) b->gpio_in |= mask; else b->gpio_in &= ~mask; }
void sim_led_write(sim_board_t *b, uint32_t value) { b->gpio_out=value; }
void sim_adc_set(sim_board_t *b, uint16_t value) { b->adc=(uint16_t)(value & 0x0FFFu); }
int sim_dac_write(sim_board_t *b, uint16_t value) { if (b->dac_count >= 256u || value > 1023u) return -1; b->dac_log[b->dac_count++]=value; return 0; }
