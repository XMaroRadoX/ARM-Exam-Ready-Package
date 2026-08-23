#ifndef SIMULATED_BOARD_H
#define SIMULATED_BOARD_H
#include <stdint.h>
#define SIM_TIMER_COUNT 4u
typedef struct { uint32_t counter, match, prescale; uint8_t running, reset_on_match, irq_enabled, irq_pending; } sim_timer_t;
typedef struct { sim_timer_t timer[SIM_TIMER_COUNT]; uint32_t ticks, gpio_in, gpio_out, systick_events; uint16_t adc; uint16_t dac_log[256]; uint16_t dac_count; } sim_board_t;
void sim_board_reset(sim_board_t *b);
int sim_timer_config(sim_board_t *b, unsigned id, uint32_t match, uint8_t reset_on_match, uint8_t irq_enabled);
void sim_step(sim_board_t *b, uint32_t ticks);
void sim_gpio_input(sim_board_t *b, uint32_t mask, uint8_t pressed);
void sim_led_write(sim_board_t *b, uint32_t value);
void sim_adc_set(sim_board_t *b, uint16_t value);
int sim_dac_write(sim_board_t *b, uint16_t value);
#endif
