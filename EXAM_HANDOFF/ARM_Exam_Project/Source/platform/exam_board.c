#include "exam_board.h"
#include <stdarg.h>
#include <string.h>


#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
#define BUTTON_COUNT 3u
#define TIMER_COUNT 4u
#define ADC_CHANNEL_COUNT 8u

/* The course's LPC17xx system file uses the historical CMSIS name. */
extern uint32_t SystemFrequency;

typedef struct {
  volatile uint8_t pending;
  volatile uint8_t confirmed;
  volatile uint16_t ticks;
} button_state_t;

static button_state_t button_state[BUTTON_COUNT];
static button_callback_t button_callback;
static joystick_callback_t joystick_callback;
static volatile uint32_t button_confirm_ticks = CA_BUTTON_CONFIRM_MS / CA_RIT_TICK_MS;
static volatile uint32_t scheduler_tick_count;
static volatile uint32_t joystick_last;
static volatile uint32_t joystick_first;
static volatile uint32_t event_flags;
static timer_callback_t timer_callbacks[TIMER_COUNT];
static uint8_t timer_claimed[TIMER_COUNT];
static uint8_t systick_periodic;
static volatile uint32_t systick_tick_count;
#if !EXAM_OWN_ADC_HANDLER
static adc_sample_t adc_cache[ADC_CHANNEL_COUNT];
static volatile uint32_t adc_cache_generation[ADC_CHANNEL_COUNT];
#endif
static uint32_t adc_actual_clock;
static adc_trigger_t adc_trigger = ADC_TRIGGER_SOFTWARE;
#if !EXAM_OWN_ADC_HANDLER
static uint32_t potentiometer_seen_generation;
static uint8_t potentiometer_initialized;
#endif
static uint8_t dac_initialized;

typedef struct {
  const uint16_t *samples;
  uint32_t count;
  uint32_t index;
  uint8_t timer;
  uint8_t active;
} dac_player_t;
static dac_player_t dac_player;

unsigned char led_value;
unsigned short AD_current;

static LPC_TIM_TypeDef *timer_regs(uint8_t timer)
{
  switch (timer) {
    case 0: return LPC_TIM0;
    case 1: return LPC_TIM1;
    case 2: return LPC_TIM2;
    case 3: return LPC_TIM3;
    default: return 0;
  }
}

static IRQn_Type timer_irqn(uint8_t timer)
{
  switch (timer) {
    case 0: return TIMER0_IRQn;
    case 1: return TIMER1_IRQn;
    case 2: return TIMER2_IRQn;
    default: return TIMER3_IRQn;
  }
}

static void timer_power_on(uint8_t timer)
{
  static const uint8_t bits[TIMER_COUNT] = { 1u, 2u, 22u, 23u };
  LPC_SC->PCONP |= 1u << bits[timer];
}

/* Return the PCLKSEL register and bit position belonging to Timer 0..3.
 * The mapping comes directly from the LPC1768 PCLKSEL0/PCLKSEL1 layout. */
static volatile uint32_t *timer_pclk_select(uint8_t timer, uint8_t *shift)
{
  if (!shift) return 0;
  switch (timer) {
    case 0u: *shift = 2u;  return &LPC_SC->PCLKSEL0;
    case 1u: *shift = 4u;  return &LPC_SC->PCLKSEL0;
    case 2u: *shift = 12u; return &LPC_SC->PCLKSEL1;
    case 3u: *shift = 14u; return &LPC_SC->PCLKSEL1;
    default: return 0;
  }
}

#if !EXAM_OWN_EINT0_HANDLER || !EXAM_OWN_EINT1_HANDLER || !EXAM_OWN_EINT2_HANDLER || (!EXAM_OWN_RIT_HANDLER && (CA_RIT_MODE == RIT_SCHEDULER))
static uint32_t button_gpio_bit(board_button_t button)
{
  return 1u << (10u + (uint32_t)button);
}
#endif

static void button_pin_as_eint(board_button_t button)
{
  uint32_t shift = 20u + 2u * (uint32_t)button;
  LPC_PINCON->PINSEL4 = (LPC_PINCON->PINSEL4 & ~(3u << shift)) | (1u << shift);
}

#if !EXAM_OWN_EINT0_HANDLER || !EXAM_OWN_EINT1_HANDLER || !EXAM_OWN_EINT2_HANDLER
static void button_pin_as_gpio(board_button_t button)
{
  uint32_t shift = 20u + 2u * (uint32_t)button;
  LPC_PINCON->PINSEL4 &= ~(3u << shift);
  LPC_GPIO2->FIODIR &= ~button_gpio_bit(button);
}
#endif

static IRQn_Type button_irqn(board_button_t button)
{
  return (button == BOARD_BUTTON_INT0) ? EINT0_IRQn :
         (button == BOARD_BUTTON_KEY1) ? EINT1_IRQn : EINT2_IRQn;
}

#if !EXAM_OWN_EINT0_HANDLER || !EXAM_OWN_EINT1_HANDLER || !EXAM_OWN_EINT2_HANDLER
static void button_candidate(board_button_t button)
{
  uint32_t bit = 1u << (uint32_t)button;
  NVIC_DisableIRQ(button_irqn(button));
  LPC_SC->EXTINT = bit;
  button_pin_as_gpio(button);
  button_state[button].pending = 1u;
  button_state[button].confirmed = 0u;
  button_state[button].ticks = 0u;
}
#endif

#if !EXAM_OWN_RIT_HANDLER && (CA_RIT_MODE == RIT_SCHEDULER)
static void button_service_10ms(void)
{
  uint32_t i;
  for (i = 0; i < BUTTON_COUNT; ++i) {
    button_state_t *state = &button_state[i];
    uint8_t low;
    if (!state->pending) continue;
    low = (LPC_GPIO2->FIOPIN & button_gpio_bit((board_button_t)i)) == 0u;
    if (!state->confirmed) {
      if (++state->ticks < button_confirm_ticks) continue;
      if (low) {
        state->confirmed = 1u;
        if (button_callback) button_callback((board_button_t)i, BUTTON_EVENT_PRESS);
      } else {
        state->pending = 0u;
        button_pin_as_eint((board_button_t)i);
        NVIC_EnableIRQ(button_irqn((board_button_t)i));
      }
    } else if (!low) {
      state->pending = 0u;
      state->confirmed = 0u;
      if (button_callback) button_callback((board_button_t)i, BUTTON_EVENT_RELEASE);
      button_pin_as_eint((board_button_t)i);
      LPC_SC->EXTINT = 1u << i;
      NVIC_EnableIRQ(button_irqn((board_button_t)i));
    }
  }
}

static void joystick_service_10ms(void)
{
  static uint32_t divider;
  uint32_t current, changed;
  if (++divider < (CA_JOYSTICK_POLL_MS / CA_RIT_TICK_MS)) return;
  divider = 0u;
  current = joystick_read();
  changed = current ^ joystick_last;
  if (joystick_first == 0u && current != 0u) joystick_first = current;
  joystick_last = current;
  if (changed && joystick_callback) joystick_callback(current, changed);
}
#endif

void __attribute__((weak)) exam_user_10ms_hook(void) { }

void board_init(void)
{
  SystemInit();
#if CA_ENABLE_LEDS
  LPC_PINCON->PINSEL4 &= ~0xFFFFu;
  LPC_GPIO2->FIODIR |= 0xFFu;
  LPC_GPIO2->FIOCLR = 0xFFu;
  led_value = 0u;
#endif
  /* Peripherals are opt-in so unused resources remain unclaimed. */
  fault_traps_configure();
}

void board_idle(void)
{
#if CA_IDLE_USE_WFI
  SCB->SCR &= ~(SCB_SCR_SLEEPDEEP_Msk | SCB_SCR_SLEEPONEXIT_Msk);
  __WFI();
#else
  __NOP();
#endif
}

/* Callback helpers require the corresponding built-in IRQ handler. */
static uint8_t timer_has_internal_handler(uint8_t timer)
{
  switch (timer) {
    case 0u: return (uint8_t)!EXAM_OWN_TIMER0_HANDLER;
    case 1u: return (uint8_t)!EXAM_OWN_TIMER1_HANDLER;
    case 2u: return (uint8_t)!EXAM_OWN_TIMER2_HANDLER;
    case 3u: return (uint8_t)!EXAM_OWN_TIMER3_HANDLER;
    default: return 0u;
  }
}

/* SIGNED-INPUT CONVENIENCE FUNCTIONS --------------------------------------
 * Inputs are validated before conversion to the typed driver API. */
board_status_t timer_every_ms(int timer, int milliseconds, timer_callback_t callback)
{
  if (timer < 0 || timer >= (int)TIMER_COUNT || milliseconds <= 0)
    return BOARD_RANGE;
  return timer_start_periodic_interrupt_ms((uint8_t)timer,
                                           (uint32_t)milliseconds, callback);
}

board_status_t timer_every_hz(int timer, int hertz, timer_callback_t callback)
{
  if (timer < 0 || timer >= (int)TIMER_COUNT || hertz <= 0)
    return BOARD_RANGE;
  return timer_start_periodic_interrupt_hz((uint8_t)timer, (uint32_t)hertz,
                                           1u, callback);
}

board_status_t systick_every_ms(int milliseconds)
{
  if (milliseconds <= 0) return BOARD_RANGE;
  return systick_start_periodic_ms((uint32_t)milliseconds);
}

board_status_t potentiometer_start(void)
{
#if EXAM_OWN_ADC_HANDLER
  return BOARD_BUSY;
#else
  board_status_t status;
  if (!potentiometer_initialized) {
    status = adc_init(5u, SystemFrequency / 4u);
    if (status != BOARD_OK) return status;
    potentiometer_initialized = 1u;
  }
  status = adc_configure_trigger(ADC_TRIGGER_SOFTWARE, 0u);
  if (status != BOARD_OK) return status;
  potentiometer_seen_generation = adc_cache_generation[5];
  return adc_start_conversion();
#endif
}

board_status_t potentiometer_read(int *value)
{
  if (!value) return BOARD_INVALID;
#if EXAM_OWN_ADC_HANDLER
  return BOARD_BUSY;
#else
  if (adc_cache_generation[5] == potentiometer_seen_generation)
    return BOARD_NOT_READY;
  *value = (int)adc_cache[5].value;
  potentiometer_seen_generation = adc_cache_generation[5];
  (void)adc_start_conversion(); /* Automatically request the next reading. */
  return BOARD_OK;
#endif
}

board_status_t speaker_write(int value)
{
  board_status_t status;
  if (value < 0 || value > 1023) return BOARD_RANGE;
  status = dac_init();
  if (status != BOARD_OK) return status;
  return dac_write((uint16_t)value);
}

board_status_t speaker_write_percent(int percent)
{
  board_status_t status;
  if (percent < 0 || percent > 100) return BOARD_RANGE;
  status = dac_init();
  if (status != BOARD_OK) return status;
  return dac_write((uint16_t)((percent * 1023 + 50) / 100));
}

int int0_pressed(void) { return (int)button_is_pressed(BOARD_BUTTON_INT0); }
int key1_pressed(void) { return (int)button_is_pressed(BOARD_BUTTON_KEY1); }
int key2_pressed(void) { return (int)button_is_pressed(BOARD_BUTTON_KEY2); }
int joystick_up_pressed(void) { return (int)joystick_is_pressed(JOYSTICK_UP); }
int joystick_down_pressed(void) { return (int)joystick_is_pressed(JOYSTICK_DOWN); }
int joystick_left_pressed(void) { return (int)joystick_is_pressed(JOYSTICK_LEFT); }
int joystick_right_pressed(void) { return (int)joystick_is_pressed(JOYSTICK_RIGHT); }
int joystick_button_pressed(void) { return (int)joystick_is_pressed(JOYSTICK_SELECT); }

board_status_t led_write_number(uint8_t led_number, uint8_t on)
{
#if CA_ENABLE_LEDS
  uint8_t port_bit;
  if (led_number >= 4u && led_number <= 11u) port_bit = (uint8_t)(11u - led_number);
  else return BOARD_RANGE;
  if (on) LPC_GPIO2->FIOSET = 1u << port_bit;
  else LPC_GPIO2->FIOCLR = 1u << port_bit;
  led_value = (unsigned char)(LPC_GPIO2->FIOPIN & 0xFFu);
  return BOARD_OK;
#else
  (void)led_number; (void)on; return BOARD_NOT_ENABLED;
#endif
}

/* Beginner shortcuts.  Keep led_write_number() as the single implementation
 * so old code and new code always use exactly the same LED numbering. */
board_status_t led_on(uint8_t led_number) { return led_write_number(led_number, 1u); }
board_status_t led_off(uint8_t led_number) { return led_write_number(led_number, 0u); }
void led_all_off(void) { (void)led_write_mask(0u); }

board_status_t led_write_mask(uint8_t mask)
{
#if CA_ENABLE_LEDS
  LPC_GPIO2->FIOCLR = 0xFFu;
  LPC_GPIO2->FIOSET = mask;
  led_value = mask;
  return BOARD_OK;
#else
  (void)mask; return BOARD_NOT_ENABLED;
#endif
}

board_status_t led_toggle(uint8_t led_number)
{
  uint8_t bit;
  if (led_number >= 4u && led_number <= 11u) bit = (uint8_t)(11u - led_number);
  else return BOARD_RANGE;
  return led_write_number(led_number, (uint8_t)((LPC_GPIO2->FIOPIN & (1u << bit)) == 0u));
}

uint8_t led_read_mask(void) { return (uint8_t)(LPC_GPIO2->FIOPIN & 0xFFu); }
void led_write8(uint8_t value) { (void)led_write_mask(value); }

void buttons_init(button_callback_t callback)
{
  uint32_t i;
  button_callback = callback;
  for (i = 0; i < BUTTON_COUNT; ++i) {
    button_state[i].pending = button_state[i].confirmed = 0u;
    button_state[i].ticks = 0u;
    button_pin_as_eint((board_button_t)i);
    NVIC_ClearPendingIRQ(button_irqn((board_button_t)i));
    NVIC_EnableIRQ(button_irqn((board_button_t)i));
  }
  LPC_SC->EXTMODE |= 0x7u;
  LPC_SC->EXTPOLAR &= ~0x7u;
  LPC_SC->EXTINT = 0x7u;
}

board_status_t button_irq_start(board_button_t button)
{
  uint32_t bit;
  if ((uint32_t)button >= BUTTON_COUNT) return BOARD_RANGE;
  bit = 1u << (uint32_t)button;
  button_pin_as_eint(button);
  LPC_SC->EXTMODE |= bit;
  LPC_SC->EXTPOLAR &= ~bit;
  LPC_SC->EXTINT = bit;
  NVIC_ClearPendingIRQ(button_irqn(button));
  NVIC_EnableIRQ(button_irqn(button));
  return BOARD_OK;
}

void buttons_set_confirmation_ms(uint32_t milliseconds)
{
  if (milliseconds >= CA_RIT_TICK_MS && milliseconds % CA_RIT_TICK_MS == 0u)
    button_confirm_ticks = milliseconds / CA_RIT_TICK_MS;
}

uint32_t buttons_pressed_mask(void)
{
  return (~LPC_GPIO2->FIOPIN >> 10) & 0x7u;
}

uint8_t button_is_pressed(board_button_t button)
{
  if ((uint32_t)button >= BUTTON_COUNT) return 0u;
  return (uint8_t)((buttons_pressed_mask() & (1u << (uint32_t)button)) != 0u);
}

void joystick_init(joystick_callback_t callback)
{
  const uint32_t mask = 0x1Fu << 25;
  LPC_PINCON->PINSEL3 &= ~((3u << 18) | (3u << 20) | (3u << 22) | (3u << 24) | (3u << 26));
  LPC_PINCON->PINMODE3 &= ~((3u << 18) | (3u << 20) | (3u << 22) | (3u << 24) | (3u << 26));
  LPC_GPIO1->FIODIR &= ~mask;
  joystick_callback = callback;
  joystick_last = joystick_read();
  joystick_first = 0u;
}

uint32_t joystick_read(void)
{
  uint32_t pins = (~LPC_GPIO1->FIOPIN >> 25) & 0x1Fu;
  uint32_t result = 0u;
  if (pins & (1u << 0)) result |= JOYSTICK_SELECT;
  if (pins & (1u << 1)) result |= JOYSTICK_DOWN;
  if (pins & (1u << 2)) result |= JOYSTICK_LEFT;
  if (pins & (1u << 3)) result |= JOYSTICK_RIGHT;
  if (pins & (1u << 4)) result |= JOYSTICK_UP;
  return result;
}

uint8_t joystick_is_pressed(uint32_t direction)
{
  if (direction == 0u || (direction & ~0x1Fu) != 0u) return 0u;
  return (uint8_t)((joystick_read() & direction) == direction);
}

uint32_t joystick_first_movement(void) { return joystick_first; }
void joystick_reset_first_movement(void) { joystick_first = 0u; }

board_status_t timer_set_clock_divider(uint8_t timer, uint8_t divider)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  volatile uint32_t *selection;
  uint32_t encoding;
  uint8_t shift;

  /* LPC1768 encodes /4, /1, /2 and /8 as 0, 1, 2 and 3. */
  switch (divider) {
    case 1u: encoding = 1u; break;
    case 2u: encoding = 2u; break;
    case 4u: encoding = 0u; break;
    case 8u: encoding = 3u; break;
    default: return BOARD_RANGE;
  }

  selection = timer_pclk_select(timer, &shift);
  if (!t || !selection) return BOARD_RANGE;
  timer_power_on(timer);
  if (t->TCR & 1u) return BOARD_BUSY; /* Do not change speed mid-period. */
  *selection = (*selection & ~(3u << shift)) | (encoding << shift);
  return BOARD_OK;
}

uint32_t timer_peripheral_clock_hz(uint8_t timer)
{
  volatile uint32_t *selection;
  uint32_t encoding;
  uint32_t divider;
  uint8_t shift;

  selection = timer_pclk_select(timer, &shift);
  if (!selection) return 0u;
  encoding = (*selection >> shift) & 3u;
  /* Encoding: 0=/4, 1=/1, 2=/2, 3=/8. */
  divider = (encoding == 0u) ? 4u :
            (encoding == 1u) ? 1u :
            (encoding == 2u) ? 2u : 8u;
  return SystemFrequency / divider;
}

board_status_t timer_set_prescaler(uint8_t timer, uint32_t prescaler)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  if (!t) return BOARD_RANGE;
  timer_power_on(timer);
  t->PR = prescaler;
  return BOARD_OK;
}

uint32_t timer_counter_clock_hz(uint8_t timer)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t peripheral_clock;
  uint64_t divisor;

  if (!t || (t->CTCR & 3u) != TIMER_MODE_TIMER) return 0u;
  peripheral_clock = timer_peripheral_clock_hz(timer);
  divisor = (uint64_t)t->PR + 1u;
  return (uint32_t)((uint64_t)peripheral_clock / divisor);
}

board_status_t timer_calculate_match_for_frequency(uint8_t timer, uint32_t frequency_hz,
                                                   uint32_t events_per_cycle, uint32_t *match_value)
{
  uint32_t counter_clock;
  uint64_t events_per_second;
  uint64_t ticks;

  if (!match_value || frequency_hz == 0u || events_per_cycle == 0u) return BOARD_INVALID;
  counter_clock = timer_counter_clock_hz(timer);
  if (counter_clock == 0u) return BOARD_RANGE;

  events_per_second = (uint64_t)frequency_hz * events_per_cycle;
  if (events_per_second > counter_clock) return BOARD_RANGE;

  /* Round to the nearest whole timer tick for the closest possible rate. */
  ticks = ((uint64_t)counter_clock + events_per_second / 2u) / events_per_second;
  if (ticks == 0u || ticks > 0xFFFFFFFFu) return BOARD_RANGE;
  *match_value = (uint32_t)ticks;
  return BOARD_OK;
}

board_status_t timer_configure_frequency(uint8_t timer, uint8_t match, uint32_t frequency_hz,
                                         uint32_t events_per_cycle, uint32_t actions)
{
  uint32_t match_value;
  board_status_t status = timer_calculate_match_for_frequency(
      timer, frequency_hz, events_per_cycle, &match_value);
  if (status != BOARD_OK) return status;
  return timer_configure_match(timer, match, match_value, actions);
}

uint8_t timer_match_occurred(uint32_t pending_flags, uint8_t match)
{
  if (match > 3u) return 0u;
  return (uint8_t)((pending_flags & (1u << match)) != 0u);
}

uint8_t timer_capture_occurred(uint32_t pending_flags, uint8_t capture)
{
  if (capture > 1u) return 0u;
  return (uint8_t)((pending_flags & (1u << (4u + capture))) != 0u);
}

board_status_t timer_start_periodic_interrupt_hz(uint8_t timer, uint32_t frequency_hz,
                                                 uint32_t events_per_cycle,
                                                 timer_callback_t callback)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  board_status_t status;

  if (!t) return BOARD_RANGE;
  if (!callback) return BOARD_INVALID;
  if (!timer_has_internal_handler(timer)) return BOARD_BUSY;
  if (t->TCR & 1u) return BOARD_BUSY;

  /* This helper owns MR0. Clock-divider and prescaler settings are retained. */
  status = timer_configure_frequency(timer, 0u, frequency_hz, events_per_cycle,
                                     TIMER_ACTION_INTERRUPT | TIMER_ACTION_RESET);
  if (status != BOARD_OK) return status;
  status = timer_set_callback(timer, callback);
  if (status != BOARD_OK) return status;

  (void)timer_reset(timer);
  t->IR = 0x3Fu; /* Clear stale match/capture flags before the first period. */
  return timer_start(timer);
}

board_status_t timer_start_periodic_interrupt_ms(uint8_t timer, uint32_t period_ms,
                                                 timer_callback_t callback)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t counter_clock;
  uint64_t ticks;
  board_status_t status;

  if (!t) return BOARD_RANGE;
  if (!callback || period_ms == 0u) return BOARD_INVALID;
  if (!timer_has_internal_handler(timer)) return BOARD_BUSY;
  if (t->TCR & 1u) return BOARD_BUSY;
  counter_clock = timer_counter_clock_hz(timer);
  if (counter_clock == 0u) return BOARD_RANGE;

  /* Round milliseconds to the nearest whole tick.  A 64-bit intermediate
   * prevents overflow when the counter clock is 100 MHz. */
  ticks = ((uint64_t)counter_clock * period_ms + 500u) / 1000u;
  if (ticks == 0u || ticks > 0xFFFFFFFFu) return BOARD_RANGE;
  status = timer_configure_match(timer, 0u, (uint32_t)ticks,
                                 TIMER_ACTION_INTERRUPT | TIMER_ACTION_RESET);
  if (status != BOARD_OK) return status;
  status = timer_set_callback(timer, callback);
  if (status != BOARD_OK) return status;
  (void)timer_reset(timer);
  t->IR = 0x3Fu;
  return timer_start(timer);
}

board_status_t timer_configure_match(uint8_t timer, uint8_t match, uint32_t value, uint32_t actions)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t shift;
  volatile uint32_t *mr;
  if (!t || match > 3u || (actions & ~7u)) return BOARD_RANGE;
  timer_power_on(timer);
  mr = &t->MR0;
  mr[match] = value;
  shift = 3u * match;
  t->MCR = (t->MCR & ~(7u << shift)) | ((actions & 7u) << shift);
  if (actions & TIMER_ACTION_INTERRUPT) {
    NVIC_ClearPendingIRQ(timer_irqn(timer));
    NVIC_EnableIRQ(timer_irqn(timer));
  }
  return BOARD_OK;
}

board_status_t timer_configure_capture(uint8_t timer, uint8_t capture, timer_capture_edge_t edge, uint8_t interrupt_enable)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t shift;
  if (!t || capture > 1u || edge < CAPTURE_RISING || edge > CAPTURE_BOTH) return BOARD_RANGE;
  timer_power_on(timer);
  shift = capture * 3u;
  t->CCR = (t->CCR & ~(7u << shift)) | (((uint32_t)edge | (interrupt_enable ? 4u : 0u)) << shift);
  if (interrupt_enable) NVIC_EnableIRQ(timer_irqn(timer));
  return BOARD_OK;
}

board_status_t timer_read_capture(uint8_t timer, uint8_t capture, uint32_t *value)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  if (!t || capture > 1u || !value) return BOARD_INVALID;
  *value = capture ? t->CR1 : t->CR0;
  return BOARD_OK;
}

board_status_t timer_set_counter_mode(uint8_t timer, timer_counter_mode_t mode, uint8_t capture_input)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  if (!t || mode > TIMER_MODE_COUNTER_BOTH || capture_input > 1u) return BOARD_RANGE;
  timer_power_on(timer);
  t->CTCR = (uint32_t)mode | ((uint32_t)capture_input << 2);
  return BOARD_OK;
}

board_status_t timer_configure_external_match(uint8_t timer, uint8_t match, timer_external_match_t action, uint8_t initial_state)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t shift;
  if (!t || match > 3u || action > EXT_MATCH_TOGGLE) return BOARD_RANGE;
  timer_power_on(timer);
  shift = 4u + match * 2u;
  t->EMR = (t->EMR & ~((3u << shift) | (1u << match))) |
           ((uint32_t)action << shift) | (initial_state ? (1u << match) : 0u);
  return BOARD_OK;
}

board_status_t timer_start(uint8_t timer) { LPC_TIM_TypeDef *t = timer_regs(timer); if (!t) return BOARD_RANGE; t->TCR = 1u; return BOARD_OK; }
board_status_t timer_stop(uint8_t timer) { LPC_TIM_TypeDef *t = timer_regs(timer); if (!t) return BOARD_RANGE; t->TCR = 0u; return BOARD_OK; }
board_status_t timer_reset(uint8_t timer) { LPC_TIM_TypeDef *t = timer_regs(timer); if (!t) return BOARD_RANGE; t->TCR = 2u; t->TCR = 0u; return BOARD_OK; }
board_status_t timer_set_callback(uint8_t timer, timer_callback_t callback) { if (timer >= TIMER_COUNT) return BOARD_RANGE; if (!timer_has_internal_handler(timer) || timer_claimed[timer]) return BOARD_BUSY; timer_callbacks[timer] = callback; return BOARD_OK; }
uint32_t timer_read_counter(uint8_t timer) { LPC_TIM_TypeDef *t = timer_regs(timer); return t ? t->TC : 0u; }

#if !EXAM_OWN_TIMER0_HANDLER || !EXAM_OWN_TIMER1_HANDLER || !EXAM_OWN_TIMER2_HANDLER || !EXAM_OWN_TIMER3_HANDLER
static void timer_irq(uint8_t timer)
{
  LPC_TIM_TypeDef *t = timer_regs(timer);
  uint32_t pending = t->IR & 0x3Fu;
  t->IR = pending; /* LPC1768 timer flags are write-one-to-clear. */
  if (dac_player.active && dac_player.timer == timer && (pending & 1u)) {
    (void)dac_write(dac_player.samples[dac_player.index++]);
    if (dac_player.index >= dac_player.count) { dac_player.active = 0u; timer_claimed[timer] = 0u; (void)timer_stop(timer); dac_silence(); }
  }
  if (timer_callbacks[timer]) timer_callbacks[timer](timer, pending);
}

#if !EXAM_OWN_TIMER0_HANDLER
void TIMER0_IRQHandler(void) { timer_irq(0u); }
#endif
#if !EXAM_OWN_TIMER1_HANDLER
void TIMER1_IRQHandler(void) { timer_irq(1u); }
#endif
#if !EXAM_OWN_TIMER2_HANDLER
void TIMER2_IRQHandler(void) { timer_irq(2u); }
#endif
#if !EXAM_OWN_TIMER3_HANDLER
void TIMER3_IRQHandler(void) { timer_irq(3u); }
#endif
#endif

board_status_t rit_scheduler_start(void)
{
#if (CA_RIT_MODE == RIT_SCHEDULER) && !EXAM_OWN_RIT_HANDLER
  LPC_SC->PCONP |= 1u << 16;
  LPC_SC->PCLKSEL1 = (LPC_SC->PCLKSEL1 & ~(3u << 26)) | (1u << 26);
  LPC_RIT->RICOMPVAL = SystemFrequency / (1000u / CA_RIT_TICK_MS);
  LPC_RIT->RIMASK = 0u;
  LPC_RIT->RICOUNTER = 0u;
  LPC_RIT->RICTRL = (1u << 1) | (1u << 2) | (1u << 3);
  NVIC_ClearPendingIRQ(RIT_IRQn);
  NVIC_EnableIRQ(RIT_IRQn);
  return BOARD_OK;
#else
  return BOARD_BUSY;
#endif
}
void rit_scheduler_stop(void) { LPC_RIT->RICTRL &= ~(1u << 3); }
uint32_t rit_scheduler_ticks(void) { return scheduler_tick_count; }

board_status_t rit_raw_configure(uint32_t compare, uint32_t mask, uint8_t clear_on_match)
{
#if CA_RIT_MODE == RIT_RAW
  LPC_SC->PCONP |= 1u << 16;
  LPC_RIT->RICOMPVAL = compare; LPC_RIT->RIMASK = mask; LPC_RIT->RICOUNTER = 0u;
  LPC_RIT->RICTRL = (1u << 2) | (clear_on_match ? (1u << 1) : 0u);
  NVIC_EnableIRQ(RIT_IRQn);
  return BOARD_OK;
#else
  (void)compare; (void)mask; (void)clear_on_match; return BOARD_BUSY;
#endif
}
board_status_t rit_raw_start(void) { if (CA_RIT_MODE != RIT_RAW) return BOARD_BUSY; LPC_RIT->RICTRL |= 1u << 3; return BOARD_OK; }
void rit_raw_stop(void) { LPC_RIT->RICTRL &= ~(1u << 3); }
uint32_t rit_raw_read(void) { return LPC_RIT->RICOUNTER; }

#if !EXAM_OWN_RIT_HANDLER
void RIT_IRQHandler(void)
{
  LPC_RIT->RICTRL |= 1u; /* W1C interrupt flag. */
#if CA_RIT_MODE == RIT_SCHEDULER
  ++scheduler_tick_count;
  button_service_10ms();
  joystick_service_10ms();
  exam_user_10ms_hook();
#endif
}
#endif

board_status_t systick_configure(uint32_t reload, uint8_t periodic, uint8_t interrupt_enable)
{
  uint32_t source = SysTick->CTRL & SysTick_CTRL_CLKSOURCE_Msk;
  if (reload == 0u || reload > 0x00FFFFFFu) return BOARD_RANGE;
  SysTick->CTRL = 0u;
  SysTick->LOAD = reload - 1u;
  SysTick->VAL = 0u;
  systick_periodic = periodic ? 1u : 0u;
  SysTick->CTRL = source | (interrupt_enable ? SysTick_CTRL_TICKINT_Msk : 0u) | SysTick_CTRL_ENABLE_Msk;
  return BOARD_OK;
}
board_status_t systick_start_periodic_ms(uint32_t period_ms)
{
  uint64_t reload;
  if (period_ms == 0u) return BOARD_INVALID;
  reload = ((uint64_t)SystemFrequency * period_ms + 500u) / 1000u;
  if (reload == 0u || reload > 0x00FFFFFFu) return BOARD_RANGE;
  (void)systick_set_clock_source(1u);
  return systick_configure((uint32_t)reload, 1u, 1u);
}
board_status_t systick_set_clock_source(uint8_t processor_clock) { uint32_t enabled = SysTick->CTRL & SysTick_CTRL_ENABLE_Msk; SysTick->CTRL &= ~SysTick_CTRL_ENABLE_Msk; if (processor_clock) SysTick->CTRL |= SysTick_CTRL_CLKSOURCE_Msk; else SysTick->CTRL &= ~SysTick_CTRL_CLKSOURCE_Msk; SysTick->CTRL |= enabled; return BOARD_OK; }
uint32_t systick_calibration_value(void) { return SysTick->CALIB & SysTick_CALIB_TENMS_Msk; }
uint8_t systick_has_precise_calibration(void) { return (uint8_t)((SysTick->CALIB & SysTick_CALIB_NOREF_Msk) == 0u && (SysTick->CALIB & SysTick_CALIB_SKEW_Msk) == 0u); }
uint32_t systick_ticks(void) { return systick_tick_count; }
#if !EXAM_OWN_SYSTICK_HANDLER
void SysTick_Handler(void) { ++systick_tick_count; if (!systick_periodic) SysTick->CTRL &= ~SysTick_CTRL_ENABLE_Msk; }
#endif

board_status_t adc_init(uint8_t channel, uint32_t peripheral_clock_hz)
{
  uint32_t divider;
  if (channel >= ADC_CHANNEL_COUNT || peripheral_clock_hz == 0u) return BOARD_RANGE;
  LPC_SC->PCONP |= 1u << 12;
  divider = (peripheral_clock_hz + CA_ADC_MAX_CLOCK_HZ - 1u) / CA_ADC_MAX_CLOCK_HZ;
  if (divider == 0u) divider = 1u;
  if (divider > 256u) return BOARD_RANGE;
  adc_actual_clock = peripheral_clock_hz / divider;
  if (channel == 5u) LPC_PINCON->PINSEL3 = (LPC_PINCON->PINSEL3 & ~(3u << 30)) | (3u << 30);
  LPC_ADC->ADCR = (1u << channel) | ((divider - 1u) << 8) | (1u << 21);
  LPC_ADC->ADINTEN = 1u << 8;
  NVIC_ClearPendingIRQ(ADC_IRQn);
  NVIC_EnableIRQ(ADC_IRQn);
  return BOARD_OK;
}

board_status_t adc_configure_trigger(adc_trigger_t trigger, uint8_t falling_edge)
{
  if (trigger != ADC_TRIGGER_SOFTWARE && (trigger < ADC_TRIGGER_P2_10 || trigger > ADC_TRIGGER_MAT1_1)) return BOARD_RANGE;
  adc_trigger = trigger;
  LPC_ADC->ADCR = (LPC_ADC->ADCR & ~((7u << 24) | (1u << 27))) |
                  ((uint32_t)trigger << 24) | (falling_edge ? (1u << 27) : 0u);
  return BOARD_OK;
}

board_status_t adc_start_conversion(void)
{
  if (adc_trigger != ADC_TRIGGER_SOFTWARE) return BOARD_BUSY;
  LPC_ADC->ADCR = (LPC_ADC->ADCR & ~(7u << 24)) | (1u << 24);
  return BOARD_OK;
}

board_status_t adc_start_burst(uint32_t channel_mask)
{
  if ((channel_mask & 0xFFu) == 0u || (channel_mask & ~0xFFu)) return BOARD_RANGE;
  LPC_ADC->ADCR = (LPC_ADC->ADCR & ~((0xFFu) | (7u << 24))) | channel_mask | (1u << 16);
  return BOARD_OK;
}
void adc_stop_burst(void) { LPC_ADC->ADCR &= ~(1u << 16); }

#if !EXAM_OWN_ADC_HANDLER
static void adc_cache_raw(uint32_t raw)
{
  uint8_t channel = (uint8_t)((raw >> 24) & 7u);
  adc_cache[channel].raw = raw;
  adc_cache[channel].value = (uint16_t)((raw >> 4) & 0x0FFFu);
  adc_cache[channel].channel = channel;
  adc_cache[channel].done = (uint8_t)((raw >> 31) & 1u);
  adc_cache[channel].overrun = (uint8_t)((raw >> 30) & 1u);
  ++adc_cache_generation[channel];
  if (channel == 5u) AD_current = adc_cache[channel].value;
}

void ADC_IRQHandler(void)
{
  uint32_t raw = LPC_ADC->ADGDR; /* Exactly one hardware read per conversion. */
  adc_cache_raw(raw);
}
#endif

board_status_t adc_read_channel(uint8_t channel, adc_sample_t *sample)
{
  if (channel >= ADC_CHANNEL_COUNT || !sample) return BOARD_INVALID;
#if EXAM_OWN_ADC_HANDLER
  return BOARD_BUSY;
#else
  if (!adc_cache_generation[channel]) return BOARD_NOT_READY;
  *sample = adc_cache[channel];
  return BOARD_OK;
#endif
}
board_status_t adc_read_value(uint8_t channel, uint16_t *value)
{
  adc_sample_t sample;
  board_status_t status;
  if (!value) return BOARD_INVALID;
  status = adc_read_channel(channel, &sample);
  if (status != BOARD_OK) return status;
  *value = sample.value;
  return BOARD_OK;
}
uint32_t adc_clock_hz(void) { return adc_actual_clock; }

board_status_t dac_init(void)
{
#if CA_ENABLE_DAC
  if (dac_initialized) return BOARD_OK;
  LPC_PINCON->PINSEL1 = (LPC_PINCON->PINSEL1 & ~(3u << 20)) | (2u << 20);
#ifdef SIMULATOR
  LPC_GPIO0->FIODIR |= 1u << 26;
#endif
  dac_silence();
  dac_initialized = 1u;
  return BOARD_OK;
#else
  return BOARD_NOT_ENABLED;
#endif
}
board_status_t dac_write(uint16_t value) { if (value > 1023u) return BOARD_RANGE; LPC_DAC->DACR = (uint32_t)value << 6; return BOARD_OK; }
void dac_silence(void) { LPC_DAC->DACR = 0u; }
board_status_t dac_validate_update_rate(uint32_t update_hz) { return (update_hz && update_hz <= CA_DAC_MAX_UPDATE_HZ) ? BOARD_OK : BOARD_RANGE; }

board_status_t dac_play_samples(const uint16_t *samples, uint32_t count, uint32_t update_hz, uint8_t timer)
{
  uint32_t ticks;
  board_status_t status;
  if (!samples || !count || timer >= TIMER_COUNT) return BOARD_INVALID;
  if (!timer_has_internal_handler(timer)) return BOARD_BUSY;
  status = dac_init();
  if (status != BOARD_OK) return status;
  if (dac_validate_update_rate(update_hz) != BOARD_OK) return BOARD_RANGE;
  if (timer_claimed[timer]) return BOARD_BUSY;
  timer_claimed[timer] = 1u;
  dac_player.samples = samples; dac_player.count = count; dac_player.index = 0u; dac_player.timer = timer; dac_player.active = 1u;
  ticks = (SystemFrequency / 4u) / update_hz;
  (void)timer_set_prescaler(timer, 0u);
  (void)timer_configure_match(timer, 0u, ticks, TIMER_ACTION_INTERRUPT | TIMER_ACTION_RESET);
  return timer_start(timer);
}

uint32_t critical_enter(void) { uint32_t previous = __get_PRIMASK(); __disable_irq(); __DMB(); return previous; }
void critical_exit(uint32_t previous_primask) { __DMB(); __set_PRIMASK(previous_primask); }
void event_flags_set(uint32_t flags) { uint32_t key = critical_enter(); event_flags |= flags; critical_exit(key); }
uint32_t event_flags_take(uint32_t mask) { uint32_t key = critical_enter(); uint32_t result = event_flags & mask; event_flags &= ~mask; critical_exit(key); return result; }

void *board_direct_register(const char *name)
{
  if (!name) return 0;
  if (!strcmp(name, "GPIO1")) return LPC_GPIO1;
  if (!strcmp(name, "GPIO2")) return LPC_GPIO2;
  if (!strcmp(name, "TIMER0")) return LPC_TIM0;
  if (!strcmp(name, "TIMER1")) return LPC_TIM1;
  if (!strcmp(name, "TIMER2")) return LPC_TIM2;
  if (!strcmp(name, "TIMER3")) return LPC_TIM3;
  if (!strcmp(name, "RIT")) return LPC_RIT;
  if (!strcmp(name, "ADC")) return LPC_ADC;
  if (!strcmp(name, "DAC")) return LPC_DAC;
  return 0;
}

#if !EXAM_OWN_EINT0_HANDLER
void EINT0_IRQHandler(void) { button_candidate(BOARD_BUTTON_INT0); }
#endif
#if !EXAM_OWN_EINT1_HANDLER
void EINT1_IRQHandler(void) { button_candidate(BOARD_BUTTON_KEY1); }
#endif
#if !EXAM_OWN_EINT2_HANDLER
void EINT2_IRQHandler(void) { button_candidate(BOARD_BUTTON_KEY2); }
#endif

uint32_t board_self_test_run(void)
{
  uint32_t failed = 0u;
#if CA_ENABLE_LEDS
  uint8_t saved = led_read_mask();
  if (led_write_mask(0xA5u) != BOARD_OK || led_read_mask() != 0xA5u) failed |= SELF_TEST_LED_API;
  (void)led_write_mask(saved);
#endif
  if (joystick_read() & ~0x1Fu) failed |= SELF_TEST_JOYSTICK_IDLE;
  if (adc_clock_hz() > CA_ADC_MAX_CLOCK_HZ) failed |= SELF_TEST_ADC_CLOCK;
  if (systick_configure(0x01000001u, 1u, 1u) != BOARD_RANGE) failed |= SELF_TEST_SYSTICK_RANGE;
  if (dac_validate_update_rate(CA_DAC_MAX_UPDATE_HZ + 1u) != BOARD_RANGE) failed |= SELF_TEST_DAC_RANGE;
  return failed;
}
