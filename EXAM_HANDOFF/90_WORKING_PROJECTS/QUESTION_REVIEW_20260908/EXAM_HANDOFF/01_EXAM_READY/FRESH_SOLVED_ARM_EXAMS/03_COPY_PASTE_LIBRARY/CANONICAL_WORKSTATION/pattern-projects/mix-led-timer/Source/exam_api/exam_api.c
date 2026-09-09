#include "LPC17xx.h"
#include "exam_api.h"
#include "led.h"
#include "button.h"
#include "timer.h"
#include "systick.h"
#include "RIT.h"
#include "joystick.h"
#include "adc.h"

#define EXAM_LED_COUNT       8u
#define EXAM_BUTTON_COUNT    3u
#define EXAM_TIMER_COUNT     4u
#define EXAM_TIMER_IR_MASK   0x3Fu
#define EXAM_JOYSTICK_MASK   0x1Fu
#define EXAM_SYSTICK_MAX     0x01000000u

extern uint32_t SystemFrequency;

typedef struct {
  uint8_t active;
  uint8_t reported;
  uint32_t stable_ticks;
} exam_debounce_state_t;

static volatile uint32_t exam_event_flags;
static volatile uint32_t exam_button_event_flags;
static volatile uint16_t exam_adc_value;
static volatile uint8_t exam_adc_fresh;
static uint8_t exam_timer_initialized;
static exam_debounce_state_t exam_debounce[EXAM_BUTTON_COUNT];
static uint32_t exam_debounce_required_ticks;
volatile exam_fault_snapshot_t exam_fault_snapshot;
volatile uint8_t exam_fault_snapshot_valid;

static uint8_t exam_button_valid(exam_button_t button)
{
  return (uint8_t)((uint32_t)button < EXAM_BUTTON_COUNT);
}

static uint8_t exam_timer_valid(exam_timer_t timer)
{
  return (uint8_t)((uint32_t)timer < EXAM_TIMER_COUNT);
}

static LPC_TIM_TypeDef *exam_timer_registers(exam_timer_t timer)
{
  switch (timer) {
    case EXAM_TIMER0: return LPC_TIM0;
    case EXAM_TIMER1: return LPC_TIM1;
    case EXAM_TIMER2: return LPC_TIM2;
    case EXAM_TIMER3: return LPC_TIM3;
    default: return 0;
  }
}

static IRQn_Type exam_timer_irq(exam_timer_t timer)
{
  switch (timer) {
    case EXAM_TIMER0: return TIMER0_IRQn;
    case EXAM_TIMER1: return TIMER1_IRQn;
    case EXAM_TIMER2: return TIMER2_IRQn;
    default: return TIMER3_IRQn;
  }
}

static void exam_timer_power_on(exam_timer_t timer)
{
  static const uint8_t power_bits[EXAM_TIMER_COUNT] = { 1u, 2u, 22u, 23u };
  LPC_SC->PCONP |= 1u << power_bits[(uint32_t)timer];
}

static volatile uint32_t *exam_timer_pclk_register(exam_timer_t timer,
                                                    uint8_t *shift)
{
  if (shift == 0) return 0;
  switch (timer) {
    case EXAM_TIMER0: *shift = 2u;  return &LPC_SC->PCLKSEL0;
    case EXAM_TIMER1: *shift = 4u;  return &LPC_SC->PCLKSEL0;
    case EXAM_TIMER2: *shift = 12u; return &LPC_SC->PCLKSEL1;
    case EXAM_TIMER3: *shift = 14u; return &LPC_SC->PCLKSEL1;
    default: return 0;
  }
}

static uint32_t exam_timer_clock_hz(exam_timer_t timer)
{
  volatile uint32_t *selection;
  uint32_t encoding;
  uint32_t divider;
  uint8_t shift;

  selection = exam_timer_pclk_register(timer, &shift);
  if (selection == 0) return 0u;
  encoding = (*selection >> shift) & 3u;
  divider = (encoding == 0u) ? 4u :
            (encoding == 1u) ? 1u :
            (encoding == 2u) ? 2u : 8u;
  return SystemFrequency / divider;
}

static IRQn_Type exam_button_irq(exam_button_t button)
{
  switch (button) {
    case EXAM_BUTTON_INT0: return EINT0_IRQn;
    case EXAM_BUTTON_KEY1: return EINT1_IRQn;
    default: return EINT2_IRQn;
  }
}

static uint32_t exam_button_gpio_mask(exam_button_t button)
{
  return 1u << (10u + (uint32_t)button);
}

static uint32_t exam_button_pin_shift(exam_button_t button)
{
  return 20u + 2u * (uint32_t)button;
}

static void exam_button_pin_as_gpio(exam_button_t button)
{
  uint32_t shift = exam_button_pin_shift(button);
  LPC_PINCON->PINSEL4 &= ~(3u << shift);
  LPC_GPIO2->FIODIR &= ~exam_button_gpio_mask(button);
}

static void exam_button_pin_as_eint(exam_button_t button)
{
  uint32_t shift = exam_button_pin_shift(button);
  LPC_PINCON->PINSEL4 = (LPC_PINCON->PINSEL4 & ~(3u << shift)) |
                        (1u << shift);
}

static void exam_debounce_restore_button(exam_button_t button)
{
  exam_debounce_state_t *state = &exam_debounce[(uint32_t)button];

  if (state->active) {
    IRQn_Type irq = exam_button_irq(button);
    exam_button_pin_as_eint(button);
    LPC_SC->EXTINT = 1u << (uint32_t)button;
    NVIC_ClearPendingIRQ(irq);
    NVIC_EnableIRQ(irq);
  }

  state->active = 0u;
  state->reported = 0u;
  state->stable_ticks = 0u;
}

uint8_t exam_button_is_pressed(exam_button_t button)
{
  if (!exam_button_valid(button)) return 0u;
  return (uint8_t)((LPC_GPIO2->FIOPIN & exam_button_gpio_mask(button)) == 0u);
}

uint32_t exam_critical_enter(void)
{
  uint32_t previous = __get_PRIMASK();
  __disable_irq();
  __DMB();
  return previous;
}

void exam_critical_exit(uint32_t saved_primask)
{
  __DMB();
  __set_PRIMASK(saved_primask);
}

void exam_events_set(uint32_t bits)
{
  uint32_t key = exam_critical_enter();
  exam_event_flags |= bits;
  exam_critical_exit(key);
}

uint32_t exam_events_take(uint32_t mask)
{
  uint32_t result;
  uint32_t key = exam_critical_enter();
  result = exam_event_flags & mask;
  exam_event_flags &= ~mask;
  exam_critical_exit(key);
  return result;
}

void exam_faults_configure(uint8_t enable_configurable_faults,
                           uint8_t trap_divide_by_zero,
                           uint8_t trap_unaligned)
{
  const uint32_t configurable_mask = SCB_SHCSR_USGFAULTENA_Msk |
                                     SCB_SHCSR_BUSFAULTENA_Msk |
                                     SCB_SHCSR_MEMFAULTENA_Msk;

  if (enable_configurable_faults != 0u) SCB->SHCSR |= configurable_mask;
  else SCB->SHCSR &= ~configurable_mask;

  if (trap_divide_by_zero != 0u) SCB->CCR |= SCB_CCR_DIV_0_TRP_Msk;
  else SCB->CCR &= ~SCB_CCR_DIV_0_TRP_Msk;

  if (trap_unaligned != 0u) SCB->CCR |= SCB_CCR_UNALIGN_TRP_Msk;
  else SCB->CCR &= ~SCB_CCR_UNALIGN_TRP_Msk;

  __DSB();
  __ISB();
}

void exam_fault_snapshot_clear(void)
{
  uint32_t key = exam_critical_enter();
  exam_fault_snapshot_valid = 0u;
  exam_critical_exit(key);
}

void __attribute__((noreturn))
exam_fault_capture_from_exception(exam_exception_frame_t *frame,
                                  uint32_t exc_return)
{
  exam_fault_snapshot.exception_number =
      SCB->ICSR & SCB_ICSR_VECTACTIVE_Msk;
  exam_fault_snapshot.exc_return = exc_return;
  exam_fault_snapshot.frame.r0 = frame->r0;
  exam_fault_snapshot.frame.r1 = frame->r1;
  exam_fault_snapshot.frame.r2 = frame->r2;
  exam_fault_snapshot.frame.r3 = frame->r3;
  exam_fault_snapshot.frame.r12 = frame->r12;
  exam_fault_snapshot.frame.lr = frame->lr;
  exam_fault_snapshot.frame.pc = frame->pc;
  exam_fault_snapshot.frame.xpsr = frame->xpsr;
  exam_fault_snapshot.cfsr = SCB->CFSR;
  exam_fault_snapshot.hfsr = SCB->HFSR;
  exam_fault_snapshot.dfsr = SCB->DFSR;
  exam_fault_snapshot.afsr = SCB->AFSR;
  exam_fault_snapshot.bfar = SCB->BFAR;
  exam_fault_snapshot.mmfar = SCB->MMFAR;
  __DSB();
  exam_fault_snapshot_valid = 1u;
  __DSB();

  for (;;) {
    __NOP();
  }
}

void __attribute__((weak))
exam_svc_dispatch(uint8_t service_number, exam_exception_frame_t *frame)
{
  (void)service_number;
  (void)frame;
}

void exam_svc_capture_from_exception(exam_exception_frame_t *frame)
{
  const uint8_t service_number =
      ((const uint8_t *)(uintptr_t)frame->pc)[-2];
  exam_svc_dispatch(service_number, frame);
}

#if EXAM_ENABLE_FAULT_HANDLERS
#define EXAM_FAULT_WRAPPER(name) \
  __attribute__((naked)) void name(void) { \
    __asm volatile( \
      "tst lr, #4\n" \
      "ite eq\n" \
      "mrseq r0, msp\n" \
      "mrsne r0, psp\n" \
      "mov r1, lr\n" \
      "b exam_fault_capture_from_exception\n"); \
  }

EXAM_FAULT_WRAPPER(HardFault_Handler)
EXAM_FAULT_WRAPPER(MemManage_Handler)
EXAM_FAULT_WRAPPER(BusFault_Handler)
EXAM_FAULT_WRAPPER(UsageFault_Handler)
#endif

#if EXAM_ENABLE_SVC_HANDLER
__attribute__((naked)) void SVC_Handler(void)
{
  __asm volatile(
    "tst lr, #4\n"
    "ite eq\n"
    "mrseq r0, msp\n"
    "mrsne r0, psp\n"
    "b exam_svc_capture_from_exception\n");
}
#endif

void exam_init(void)
{
  uint32_t index;
  uint32_t key;

  SystemInit();
  LED_init();

  key = exam_critical_enter();
  exam_event_flags = 0u;
  exam_button_event_flags = 0u;
  exam_adc_value = 0u;
  exam_adc_fresh = 0u;
  exam_timer_initialized = 0u;
  exam_fault_snapshot_valid = 0u;
  exam_debounce_required_ticks = 0u;
  for (index = 0u; index < EXAM_BUTTON_COUNT; ++index) {
    exam_debounce[index].active = 0u;
    exam_debounce[index].reported = 0u;
    exam_debounce[index].stable_ticks = 0u;
  }
  exam_critical_exit(key);
}

exam_status_t exam_led_on(uint8_t board_label)
{
  uint32_t key;
  uint8_t index;
  if (board_label < 4u || board_label > 11u) return EXAM_OUT_OF_RANGE;
  index = (uint8_t)(11u - board_label);
  key = exam_critical_enter();
  LED_On(index);
  exam_critical_exit(key);
  return EXAM_OK;
}

exam_status_t exam_led_off(uint8_t board_label)
{
  uint32_t key;
  uint8_t index;
  if (board_label < 4u || board_label > 11u) return EXAM_OUT_OF_RANGE;
  index = (uint8_t)(11u - board_label);
  key = exam_critical_enter();
  LED_Off(index);
  exam_critical_exit(key);
  return EXAM_OK;
}

exam_status_t exam_led_toggle(uint8_t board_label)
{
  uint32_t key;
  uint8_t index;
  if (board_label < 4u || board_label > 11u) return EXAM_OUT_OF_RANGE;
  index = (uint8_t)(11u - board_label);
  key = exam_critical_enter();
  if ((led_value & (1u << index)) != 0u) LED_Off(index);
  else LED_On(index);
  exam_critical_exit(key);
  return EXAM_OK;
}

exam_status_t exam_led_one_hot(uint8_t board_label)
{
  uint32_t key;
  uint8_t index;
  if (board_label < 4u || board_label > 11u) return EXAM_OUT_OF_RANGE;
  index = (uint8_t)(11u - board_label);
  key = exam_critical_enter();
  LED_Out(1u << index);
  exam_critical_exit(key);
  return EXAM_OK;
}

void exam_led_write(uint8_t value)
{
  uint32_t key = exam_critical_enter();
  LED_Out(value);
  exam_critical_exit(key);
}

uint8_t exam_led_read(void)
{
  uint8_t value;
  uint32_t key = exam_critical_enter();
  value = led_value;
  exam_critical_exit(key);
  return value;
}

void exam_led_clear(void)
{
  exam_led_write(0u);
}

void exam_buttons_init(void)
{
  uint32_t index;
  uint32_t key = exam_critical_enter();
  LPC_SC->EXTINT = 0x7u;
  NVIC_ClearPendingIRQ(EINT0_IRQn);
  NVIC_ClearPendingIRQ(EINT1_IRQn);
  NVIC_ClearPendingIRQ(EINT2_IRQn);
  BUTTON_init();
  LPC_SC->EXTINT = 0x7u;
  for (index = 0u; index < EXAM_BUTTON_COUNT; ++index) {
    exam_debounce[index].active = 0u;
    exam_debounce[index].reported = 0u;
    exam_debounce[index].stable_ticks = 0u;
  }
  exam_button_event_flags = 0u;
  exam_critical_exit(key);
}

void exam_button_ack(exam_button_t button)
{
  if (!exam_button_valid(button)) return;
  LPC_SC->EXTINT = 1u << (uint32_t)button;
}

exam_status_t exam_debounce_config(uint32_t sample_period_ms,
                                   uint32_t confirmation_ms)
{
  uint64_t required;
  uint32_t index;
  uint32_t key;

  if (sample_period_ms == 0u || confirmation_ms == 0u)
    return EXAM_BAD_ARGUMENT;
  required = ((uint64_t)confirmation_ms + sample_period_ms - 1u) /
             sample_period_ms;
  if (required == 0u || required > 0xFFFFFFFFu)
    return EXAM_OUT_OF_RANGE;

  key = exam_critical_enter();
  exam_debounce_required_ticks = (uint32_t)required;
  exam_button_event_flags = 0u;
  for (index = 0u; index < EXAM_BUTTON_COUNT; ++index) {
    exam_debounce_restore_button((exam_button_t)index);
  }
  exam_critical_exit(key);
  return EXAM_OK;
}

exam_status_t exam_debounce_begin(exam_button_t button)
{
  IRQn_Type irq;
  uint32_t key;

  if (!exam_button_valid(button)) return EXAM_BAD_ARGUMENT;
  if (exam_debounce_required_ticks == 0u) {
    exam_button_ack(button);
    return EXAM_NOT_READY;
  }

  irq = exam_button_irq(button);
  key = exam_critical_enter();
  NVIC_DisableIRQ(irq);
  exam_button_pin_as_gpio(button);
  exam_button_ack(button);
  if (!exam_debounce[(uint32_t)button].active) {
    exam_debounce[(uint32_t)button].active = 1u;
    exam_debounce[(uint32_t)button].reported = 0u;
    exam_debounce[(uint32_t)button].stable_ticks = 0u;
  }
  exam_critical_exit(key);
  return EXAM_OK;
}

void exam_debounce_tick(void)
{
  uint32_t index;
  uint32_t key = exam_critical_enter();

  for (index = 0u; index < EXAM_BUTTON_COUNT; ++index) {
    exam_button_t button = (exam_button_t)index;
    exam_debounce_state_t *state = &exam_debounce[index];
    IRQn_Type irq;

    if (!state->active) continue;

    if (exam_button_is_pressed(button)) {
      if (state->stable_ticks < exam_debounce_required_ticks)
        ++state->stable_ticks;
      if (state->stable_ticks >= exam_debounce_required_ticks &&
          !state->reported) {
        exam_button_event_flags |= 1u << index;
        state->reported = 1u;
      }
    } else {
      irq = exam_button_irq(button);
      state->active = 0u;
      state->reported = 0u;
      state->stable_ticks = 0u;
      exam_button_pin_as_eint(button);
      LPC_SC->EXTINT = 1u << index;
      NVIC_ClearPendingIRQ(irq);
      NVIC_EnableIRQ(irq);
    }
  }

  exam_critical_exit(key);
}

uint32_t exam_button_events_take(void)
{
  uint32_t result;
  uint32_t key = exam_critical_enter();
  result = exam_button_event_flags;
  exam_button_event_flags = 0u;
  exam_critical_exit(key);
  return result;
}

static uint8_t exam_timer_ready(exam_timer_t timer)
{
  static const uint8_t power_bits[EXAM_TIMER_COUNT] = {1u, 2u, 22u, 23u};
  return (uint8_t)((exam_timer_initialized & (1u << (uint32_t)timer)) &&
      (LPC_SC->PCONP & (1u << power_bits[(uint32_t)timer])) &&
      !(exam_timer_registers(timer)->TCR & 3u));
}

exam_status_t exam_timer_config_match(exam_timer_t timer, uint8_t match,
                                      uint32_t ticks, uint32_t actions)
{
  LPC_TIM_TypeDef *registers;
  uint32_t shift;
  uint32_t saved;
  if (!exam_timer_valid(timer) || match > 3u || (actions & ~7u))
    return EXAM_BAD_ARGUMENT;
  if (!ticks) return EXAM_OUT_OF_RANGE;
  saved = exam_critical_enter();
  if (!exam_timer_ready(timer)) {
    exam_critical_exit(saved);
    return EXAM_NOT_READY;
  }
  registers = exam_timer_registers(timer);
  shift = 3u * match;
  switch (match) {
    case 0u: registers->MR0 = ticks; break;
    case 1u: registers->MR1 = ticks; break;
    case 2u: registers->MR2 = ticks; break;
    default: registers->MR3 = ticks; break;
  }
  registers->MCR = (registers->MCR & ~(7u << shift)) | (actions << shift);
  registers->IR = 1u << match;
  if (actions & EXAM_MATCH_INTERRUPT) NVIC_EnableIRQ(exam_timer_irq(timer));
  exam_critical_exit(saved);
  return EXAM_OK;
}

exam_status_t exam_timer_set_prescaler(exam_timer_t timer, uint32_t prescaler)
{
  uint32_t saved;
  LPC_TIM_TypeDef *registers;
  if (!exam_timer_valid(timer)) return EXAM_BAD_ARGUMENT;
  saved = exam_critical_enter();
  if (!exam_timer_ready(timer)) {
    exam_critical_exit(saved);
    return EXAM_NOT_READY;
  }
  registers = exam_timer_registers(timer);
  registers->PR = prescaler;
  registers->PC = 0u;
  exam_critical_exit(saved);
  return EXAM_OK;
}

exam_status_t exam_timer_set_clock_divider(exam_timer_t timer, uint8_t divider)
{
  uint8_t shift;
  uint32_t encoding, saved;
  volatile uint32_t *selection;
  if (!exam_timer_valid(timer)) return EXAM_BAD_ARGUMENT;
  switch (divider) {
    case 1u: encoding = 1u; break;
    case 2u: encoding = 2u; break;
    case 4u: encoding = 0u; break;
    case 8u: encoding = 3u; break;
    default: return EXAM_BAD_ARGUMENT;
  }
  saved = exam_critical_enter();
  if (!exam_timer_ready(timer)) {
    exam_critical_exit(saved);
    return EXAM_NOT_READY;
  }
  selection = exam_timer_pclk_register(timer, &shift);
  *selection = (*selection & ~(3u << shift)) | (encoding << shift);
  exam_critical_exit(saved);
  return EXAM_OK;
}

uint8_t exam_timer_match_happened(uint32_t flags, uint8_t match)
{
  return (uint8_t)(match < 4u && (flags & (1u << match)) != 0u);
}

uint8_t exam_timer_capture_happened(uint32_t flags, uint8_t capture)
{
  return (uint8_t)(capture < 2u && (flags & (1u << (4u + capture))) != 0u);
}

uint32_t exam_joystick_released_edges(uint32_t previous, uint32_t current)
{
  return previous & ~current & EXAM_JOYSTICK_MASK;
}

exam_status_t exam_timer_config_ticks(exam_timer_t timer, uint32_t ticks,
                                      exam_timer_mode_t mode)
{
  LPC_TIM_TypeDef *registers;
  IRQn_Type irq;
  uint32_t actions;

  if (!exam_timer_valid(timer)) return EXAM_BAD_ARGUMENT;
  if (ticks == 0u) return EXAM_OUT_OF_RANGE;
  if (mode != EXAM_TIMER_PERIODIC && mode != EXAM_TIMER_ONE_SHOT &&
      mode != EXAM_TIMER_MODULO_NO_IRQ) return EXAM_BAD_ARGUMENT;

  registers = exam_timer_registers(timer);
  irq = exam_timer_irq(timer);
  actions = (mode == EXAM_TIMER_PERIODIC) ? 3u :
            (mode == EXAM_TIMER_ONE_SHOT) ? 7u : 2u;

  exam_timer_power_on(timer);
  registers->TCR = 0u;
  registers->TCR = 2u;
  registers->CTCR = 0u;
  registers->PR = 0u;
  registers->PC = 0u;
  registers->TC = 0u;
  registers->IR = EXAM_TIMER_IR_MASK;
  registers->MR0 = ticks;
  registers->MCR = (registers->MCR & ~7u) | actions;
  registers->TCR = 0u;
  NVIC_ClearPendingIRQ(irq);

  exam_timer_initialized |= (uint8_t)(1u << (uint32_t)timer);
  if (mode != EXAM_TIMER_MODULO_NO_IRQ) {
    NVIC_SetPriority(irq, (uint32_t)timer);
    NVIC_EnableIRQ(irq);
  }
  return EXAM_OK;
}

exam_status_t exam_timer_config_ms(exam_timer_t timer, uint32_t milliseconds,
                                   exam_timer_mode_t mode)
{
  uint32_t clock;
  uint64_t ticks;
  if (!exam_timer_valid(timer)) return EXAM_BAD_ARGUMENT;
  if (milliseconds == 0u) return EXAM_OUT_OF_RANGE;
  clock = exam_timer_clock_hz(timer);
  if (clock == 0u) return EXAM_NOT_READY;
  ticks = ((uint64_t)clock * milliseconds + 500u) / 1000u;
  if (ticks == 0u || ticks > 0xFFFFFFFFu) return EXAM_OUT_OF_RANGE;
  return exam_timer_config_ticks(timer, (uint32_t)ticks, mode);
}

exam_status_t exam_timer_config_hz(exam_timer_t timer, uint32_t hertz,
                                   exam_timer_mode_t mode)
{
  uint32_t clock;
  uint64_t ticks;
  if (!exam_timer_valid(timer)) return EXAM_BAD_ARGUMENT;
  if (hertz == 0u) return EXAM_OUT_OF_RANGE;
  clock = exam_timer_clock_hz(timer);
  if (clock == 0u) return EXAM_NOT_READY;
  if (hertz > clock) return EXAM_OUT_OF_RANGE;
  ticks = ((uint64_t)clock + hertz / 2u) / hertz;
  if (ticks == 0u || ticks > 0xFFFFFFFFu) return EXAM_OUT_OF_RANGE;
  return exam_timer_config_ticks(timer, (uint32_t)ticks, mode);
}

void exam_timer_start(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  if (registers != 0) registers->TCR = 1u;
}

void exam_timer_stop(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  if (registers != 0) registers->TCR = 0u;
}

void exam_timer_reset(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  if (registers == 0) return;
  registers->TCR = 2u;
  registers->TCR = 0u;
}

uint32_t exam_timer_read(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  return (registers == 0) ? 0u : registers->TC;
}

uint32_t exam_timer_ack(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  uint32_t pending;
  if (registers == 0) return 0u;
  pending = registers->IR & EXAM_TIMER_IR_MASK;
  registers->IR = pending;
  return pending;
}

uint8_t exam_timer_is_running(exam_timer_t timer)
{
  LPC_TIM_TypeDef *registers = exam_timer_registers(timer);
  return (registers == 0) ? 0u : (uint8_t)(registers->TCR & 1u);
}

exam_status_t exam_systick_config_ticks(uint32_t ticks)
{
  if (ticks == 0u || ticks > EXAM_SYSTICK_MAX)
    return EXAM_OUT_OF_RANGE;
  SysTick->CTRL = 0u;
  SysTick->LOAD = ticks - 1u;
  SysTick->VAL = 0u;
  SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk |
                  SysTick_CTRL_TICKINT_Msk |
                  SysTick_CTRL_ENABLE_Msk;
  return EXAM_OK;
}

exam_status_t exam_systick_config_ms(uint32_t milliseconds)
{
  uint64_t ticks;
  if (milliseconds == 0u) return EXAM_OUT_OF_RANGE;
  ticks = ((uint64_t)SystemFrequency * milliseconds + 500u) / 1000u;
  if (ticks == 0u || ticks > EXAM_SYSTICK_MAX)
    return EXAM_OUT_OF_RANGE;
  return exam_systick_config_ticks((uint32_t)ticks);
}

void exam_systick_stop(void)
{
  SysTick->CTRL = 0u;
}

exam_status_t exam_rit_config_ticks(uint32_t ticks)
{
  if (ticks == 0u) return EXAM_OUT_OF_RANGE;
  (void)init_RIT(ticks);
  return EXAM_OK;
}

exam_status_t exam_rit_config_ms(uint32_t milliseconds)
{
  uint64_t ticks;
  if (milliseconds == 0u) return EXAM_OUT_OF_RANGE;
  ticks = ((uint64_t)SystemFrequency * milliseconds + 500u) / 1000u;
  if (ticks == 0u || ticks > 0xFFFFFFFFu) return EXAM_OUT_OF_RANGE;
  return exam_rit_config_ticks((uint32_t)ticks);
}

void exam_rit_start(void) { enable_RIT(); }
void exam_rit_stop(void) { disable_RIT(); }
void exam_rit_reset(void) { reset_RIT(); }
void exam_rit_ack(void) { LPC_RIT->RICTRL |= 1u; }

void exam_joystick_init(void)
{
  uint32_t pin_mask = 0x1Fu << 25;
  uint32_t mode_mask = (3u << 18) | (3u << 20) | (3u << 22) |
                       (3u << 24) | (3u << 26);
  joystick_init();
  LPC_PINCON->PINSEL3 &= ~mode_mask;
  LPC_PINCON->PINMODE3 &= ~mode_mask;
  LPC_GPIO1->FIODIR &= ~pin_mask;
  /* A masked FIOPIN input reads as zero, which looks pressed after inversion. */
  LPC_GPIO1->FIOMASK &= ~pin_mask;
}

uint32_t exam_joystick_read(void)
{
  return (~LPC_GPIO1->FIOPIN >> 25) & EXAM_JOYSTICK_MASK;
}

uint32_t exam_joystick_pressed_edges(uint32_t previous, uint32_t current)
{
  previous &= EXAM_JOYSTICK_MASK;
  current &= EXAM_JOYSTICK_MASK;
  return current & ~previous;
}

void exam_adc_init(void)
{
  uint32_t key = exam_critical_enter();
  exam_adc_value = 0u;
  exam_adc_fresh = 0u;
  exam_critical_exit(key);
  ADC_init();
}

void exam_adc_start(void)
{
  ADC_start_conversion();
}

void exam_adc_irq_capture(void)
{
  uint32_t raw = LPC_ADC->ADGDR;
  if ((raw & (1u << 31)) == 0u) return;
  exam_adc_value = (uint16_t)((raw >> 4) & 0x0FFFu);
  exam_adc_fresh = 1u;
}

uint8_t exam_adc_take(uint16_t *result)
{
  uint8_t fresh;
  uint32_t key;
  if (result == 0) return 0u;
  key = exam_critical_enter();
  fresh = exam_adc_fresh;
  if (fresh) {
    *result = exam_adc_value;
    exam_adc_fresh = 0u;
  }
  exam_critical_exit(key);
  return fresh;
}

void exam_adc_show_high8(uint16_t result)
{
  exam_led_write((uint8_t)((result & 0x0FFFu) >> 4));
}

void exam_dac_init(void)
{
  LPC_PINCON->PINSEL1 = (LPC_PINCON->PINSEL1 & ~(3u << 20)) |
                        (2u << 20);
  LPC_GPIO0->FIODIR |= 1u << 26;
  /* Deterministic zero output, BIAS = 0 for the fast waveform/audio mode. */
  LPC_DAC->DACR = 0u;
}

exam_status_t exam_dac_write(int32_t sample)
{
  if (sample < 0 || sample > 1023) return EXAM_OUT_OF_RANGE;
  LPC_DAC->DACR = (LPC_DAC->DACR & (1u << 16)) |
                  ((uint32_t)sample << 6);
  return EXAM_OK;
}
