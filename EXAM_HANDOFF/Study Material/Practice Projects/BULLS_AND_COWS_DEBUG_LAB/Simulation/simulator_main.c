#include "simulated_board.h"
#include <assert.h>
int main(void) { sim_board_t b; sim_board_reset(&b);
  assert(sim_timer_config(&b,0u,10u,1u,1u)==0); sim_step(&b,25u); assert(b.timer[0].counter==5u && b.timer[0].irq_pending);
  sim_gpio_input(&b,4u,1u); assert((b.gpio_in&4u)!=0u); sim_gpio_input(&b,4u,0u); assert((b.gpio_in&4u)==0u);
  sim_adc_set(&b,4095u); assert(b.adc==4095u); assert(sim_dac_write(&b,1023u)==0 && b.dac_log[0]==1023u);
  sim_led_write(&b,0xA5u); assert(b.gpio_out==0xA5u); return 0; }
