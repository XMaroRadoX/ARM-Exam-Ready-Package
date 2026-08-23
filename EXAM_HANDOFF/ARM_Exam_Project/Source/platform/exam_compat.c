#include "exam_compat.h"

extern uint32_t SystemFrequency;

void LED_init(void)
{
  LPC_PINCON->PINSEL4 &= ~0xFFFFu;
  LPC_GPIO2->FIODIR |= 0xFFu;
  LPC_GPIO2->FIOCLR = 0xFFu;
  led_value = 0u;
}
void LED_deinit(void) { LPC_GPIO2->FIODIR &= ~0xFFu; }
void LED_On(unsigned int n) { if (n < 8u) { LPC_GPIO2->FIOSET = 1u << n; led_value = (unsigned char)(LPC_GPIO2->FIOPIN & 0xFFu); } }
void LED_Off(unsigned int n) { if (n < 8u) { LPC_GPIO2->FIOCLR = 1u << n; led_value = (unsigned char)(LPC_GPIO2->FIOPIN & 0xFFu); } }
void LED_Out(unsigned int value) { led_write8((uint8_t)value); }
void BUTTON_init(void) { buttons_init(0); }
uint32_t init_timer(uint8_t timer, uint32_t interval)
{
  if (timer > 3u) return 0u;
  return timer_configure_match(timer, 0u, interval,
      TIMER_ACTION_INTERRUPT | TIMER_ACTION_RESET) == BOARD_OK;
}
void enable_timer(uint8_t timer) { (void)timer_start(timer); }
void disable_timer(uint8_t timer) { (void)timer_stop(timer); }
void reset_timer(uint8_t timer) { (void)timer_reset(timer); }
uint32_t init_RIT(uint32_t interval)
{
#if CA_RIT_MODE == RIT_RAW
  return rit_raw_configure(interval, 0u, 1u) == BOARD_OK ? 0u : 1u;
#else
  (void)interval;
  return rit_scheduler_start() == BOARD_OK ? 0u : 1u;
#endif
}
void enable_RIT(void)
{
#if CA_RIT_MODE == RIT_RAW
  (void)rit_raw_start();
#else
  (void)rit_scheduler_start();
#endif
}
void disable_RIT(void) { rit_raw_stop(); }
void reset_RIT(void) { LPC_RIT->RICOUNTER = 0u; }
void ADC_init(void) { (void)adc_init(5u, SystemFrequency / 4u); }
void ADC_start_conversion(void) { (void)adc_start_conversion(); }
