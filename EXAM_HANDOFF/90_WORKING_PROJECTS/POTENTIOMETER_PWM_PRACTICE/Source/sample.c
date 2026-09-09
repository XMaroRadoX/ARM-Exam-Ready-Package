#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t SystemFrequency;

#define PWM_PERIOD_TICKS 1000u

/* Watch these in the debugger while turning the potentiometer. */
volatile uint16_t knob_value;
volatile uint32_t pwm_on_ticks;

static void led11_pwm_init(void)
{
  LPC_SC->PCONP |= 1u << 6; /* Power PWM1. */
  LPC_SC->PCLKSEL0 = (LPC_SC->PCLKSEL0 & ~(3u << 12)) |
                     (1u << 12); /* PWM clock = processor clock. */
  LPC_PWM1->TCR = 1u << 1; /* Hold the counter in reset. */
  LPC_PWM1->CTCR = 0u;     /* Count clock ticks. */
  LPC_PWM1->PR = (SystemFrequency / 1000000u) - 1u;
  LPC_PWM1->MCR = 1u << 1; /* Reset at MR0; no PWM interrupt. */
  LPC_PWM1->MR0 = PWM_PERIOD_TICKS;
  LPC_PWM1->MR1 = 0u;      /* Initially off. */
  LPC_PWM1->LER = (1u << 0) | (1u << 1);
  LPC_PWM1->PCR = 1u << 9; /* Enable single-edge PWM1.1. */
  LPC_PINCON->PINSEL4 = (LPC_PINCON->PINSEL4 & ~3u) | 1u;
  /* P2.0 / LED11 now belongs to PWM1.1. */
  LPC_PWM1->TCR = (1u << 0) | (1u << 3);
}

int main(void)
{
  uint16_t sample;

  exam_init();
  led11_pwm_init();
  exam_adc_init();
  exam_adc_start();

  while (1) {
    if (exam_adc_take(&sample) != 0u) {
      knob_value = sample;
      pwm_on_ticks = ((uint32_t)sample * PWM_PERIOD_TICKS) / 4095u;
      LPC_PWM1->MR1 = pwm_on_ticks;
      LPC_PWM1->LER = 1u << 1; /* Apply MR1 at a PWM cycle boundary. */
      exam_adc_start();       /* Request the next reading. */
    }
    /* Poll for completed samples; no sleep/check race in this exercise. */
  }
}
