#define MODE 0
#define CONTROL_CLOCK 1
#define DEBOUNCE_STEPS 5
#define POLL_BUTTONS 0
#define HAS_LED 0
#define HAS_BUTTONS 1
#define HAS_JOYSTICK 0
#define HAS_TIMER 1
#define HAS_RIT 0
#define HAS_SYSTICK 0
#define HAS_ADC 0
#define HAS_DAC 1
/* Expanded into each complete project by scenario_library.py.
 * One foreground owner changes application state. All times below are 10 ms
 * control steps, except polling-only combinations, which have no time claim.
 */
#include <stdint.h>
#include <string.h>
typedef struct {
  uint32_t ticks, elapsed, value, samples, sum, minimum, maximum;
  uint32_t mean, alarm, running, phase, digit_count, entered, result;
  uint32_t previous_buttons, previous_joy, held, repeat, deadline;
  uint32_t history[8], cursor, filled, output, amplitude, period;
} controller_t;
controller_t app;
void controller_reset(void) {
  memset(&app,0,sizeof(app));
  app.running=MODE==14?0u:1u; app.minimum=4095u; app.amplitude=1023u;
  app.period=50u; app.deadline=300u;
}
/* Inputs are stable active-high masks. A simultaneous reset wins over all
 * other commands. Other simultaneous commands execute INT0, KEY1, then joy.
 * Bounded arithmetic is intentional: display is 8 bits, ADC is 12 bits.
 */
void controller_step(uint32_t buttons,uint32_t joy,uint32_t valid,uint32_t adc) {
  uint32_t press=buttons & ~app.previous_buttons;
  uint32_t edges=joy & ~app.previous_joy;
  uint32_t released=app.previous_buttons & ~buttons;
  app.previous_buttons=buttons; app.previous_joy=joy;
  ++app.ticks;
  if (press & 4u) {
    controller_reset(); app.previous_buttons=buttons; app.previous_joy=joy;
    return;
  }
  if (adc>4095u) adc=4095u;
  if (valid) {
    ++app.samples;
    if (adc<app.minimum) app.minimum=adc;
    if (adc>app.maximum) app.maximum=adc;
    app.sum-=app.history[app.cursor]; app.history[app.cursor]=adc; app.sum+=adc;
    app.cursor=(app.cursor+1u)&7u;
    if (app.filled<8u) ++app.filled;
    app.mean=app.sum/app.filled;
    app.amplitude=adc>>2;
  }
#if MODE == 1 /* press counter */
  if (press&1u) app.value=(app.value+1u)&255u;
  if (press&2u) app.value=(app.value-1u)&255u;
#elif MODE == 2 /* ordered binary input */
  if (app.digit_count<32u && (press&2u)) { app.entered<<=1; ++app.digit_count; }
  if (app.digit_count<32u && (edges&16u)) { app.entered=(app.entered<<1)|1u; ++app.digit_count; }
  if (press&1u) { app.result=app.entered; app.value=app.result; }
#elif MODE == 3 /* toggle, release, and one long-press action */
  if (press&1u) app.value^=1u;
  if (released&1u) app.value^=2u;
  if (buttons&1u) { if (app.held<100u) ++app.held; if(app.held==100u) {app.value^=4u; ++app.held;} }
  else app.held=0u;
#elif MODE == 4 /* stopwatch with pause */
  if (press&1u) app.running^=1u;
  if (app.running) ++app.elapsed;
  app.value=app.elapsed/100u;
#elif MODE == 5 /* countdown */
  if (press&1u) app.running^=1u;
  if (app.running && app.deadline) --app.deadline;
  app.alarm=(app.deadline==0u); app.value=(app.deadline+99u)/100u;
#elif MODE == 6 /* reaction: arm, wait, react */
  if (press&1u) {app.phase=1u;app.elapsed=0u;app.result=0u;}
  if (app.phase==1u) { if (press&2u) {app.phase=4u;app.result=0xFFu;} else if (++app.elapsed>=100u) {app.phase=2u;app.elapsed=0u;} }
  else if(app.phase==2u) { if(press&2u) {app.result=app.elapsed;app.phase=3u;} else ++app.elapsed; }
  app.value=(app.phase==2u)?0xFFu:app.result;
#elif MODE == 7 /* bounded movement with hold repeat */
  if (joy) ++app.repeat; else app.repeat=0u;
  if ((edges&8u) || ((joy&8u)&&app.repeat>=50u&&app.repeat%10u==0u)) {if(app.value<7u)++app.value;}
  if ((edges&4u) || ((joy&4u)&&app.repeat>=50u&&app.repeat%10u==0u)) {if(app.value) --app.value;}
#elif MODE == 8 /* four-command code entry */
  if(edges&8u) {app.entered=((app.entered<<2)|1u)&255u; if(app.digit_count<4u)++app.digit_count;}
  if(edges&4u) {app.entered=((app.entered<<2)|2u)&255u; if(app.digit_count<4u)++app.digit_count;}
  if(edges&1u) {app.result=(app.digit_count==4u&&app.entered==0x66u);app.value=app.result?0xFFu:0u;app.digit_count=0u;app.entered=0u;}
#elif MODE == 9 /* ADC scaling */
  if(valid) app.value=(adc*100u+2047u)/4095u;
#elif MODE == 10 /* ADC hysteresis */
  if(valid) {if(adc>=3000u) app.alarm=1u;else if(adc<=2000u) app.alarm=0u;}
  app.value=app.alarm?255u:0u;
#elif MODE == 11 /* moving mean */
  if(valid) app.value=app.mean>>4;
#elif MODE == 12 /* captured sample */
  if((press&1u) && app.filled) {app.result=app.history[(app.cursor+7u)&7u];app.value=app.result>>4;}
#elif MODE == 13 /* potentiometer sets bounded interval */
  if(valid) app.period=5u+(adc*95u)/4095u;
  if(++app.elapsed>=app.period) {app.elapsed=0u;app.value^=255u;}
#elif MODE == 14 /* finite waveform burst, busy trigger ignored */
  if((press&1u) && !app.phase) {app.phase=1u;app.elapsed=0u;}
  if(app.phase && ++app.elapsed>=20u) {app.phase=0u;app.elapsed=0u;}
  app.running=app.phase;app.value=app.phase?255u:0u;
#elif MODE == 15 /* waveform pause and restart */
  if(press&1u) app.running^=1u;
  if(edges&8u) {app.phase=(app.phase+1u)%3u;}
  app.value=app.phase;
#elif MODE == 16 /* note sequencer: note, gap, next note */
  if(++app.elapsed==20u) app.running=0u;
  if(app.elapsed>=30u) {app.elapsed=0u;app.running=1u;app.phase=(app.phase+1u)%3u;}
  app.period=1u+app.phase; app.value=app.phase;
#elif MODE == 17 /* min/max selection */
  if(press&1u) app.phase^=1u;
  if(app.samples) app.value=(app.phase?app.maximum:app.minimum)>>4;
#else /* composed monitor: every selected input has an independent role */
  if(press&1u) app.running^=1u;
  if(press&2u) app.phase=(app.phase+1u)%3u;
  if(edges&8u) app.value=(app.value+1u)&255u;
  if(edges&4u) app.value=(app.value-1u)&255u;
  if(edges&1u) app.phase=(app.phase+1u)%3u;
  if(valid && app.running) app.value=adc>>4;
  /* Even the small combinations have an observable job: button-only inputs
   * select three display levels, clocked monitors advance while running, and
   * a joystick controls a static DAC level when no sample timer is selected. */
  if(!HAS_ADC && !HAS_JOYSTICK && (press&2u)) app.value=app.phase*85u;
  if(!HAS_ADC && !HAS_JOYSTICK && CONTROL_CLOCK && app.running && app.ticks%50u==0u) app.value=(app.value+1u)&255u;
  if(HAS_DAC && !HAS_ADC) {
    if(HAS_JOYSTICK || !HAS_TIMER) app.amplitude=app.value*1023u/255u;
    else if(HAS_BUTTONS) app.amplitude=(3u-app.phase)*341u;
  }
#endif
  app.output=app.value&255u;
}

#ifndef SCENARIO_TEST
#include "exam_api.h"
#include "LPC17xx.h"
/* Interrupts publish immutable snapshots. The foreground consumer owns app.
 * The bounded queue drops NEW input when full and reports the loss. It never
 * overwrites an older command or pretends event bits preserve multiplicity.
 */
typedef struct {uint32_t buttons,joy,valid,adc;} input_t;
static volatile input_t queue[32];
static volatile uint32_t head,tail;
volatile uint32_t lost_inputs,raw_edges,supervisor_ticks,output_ticks;
static uint32_t stable_buttons,stable_joy;
static uint8_t button_count[3],joy_count[5];
static volatile uint32_t audio_amplitude=1023u,audio_enabled=1u,audio_shape,audio_divider=1u;
static uint32_t audio_index,audio_delay;
static void require(exam_status_t status) {if(status!=EXAM_OK) {for(;;){}}}
static uint32_t stable_mask(uint32_t raw,uint32_t previous,uint8_t *count,uint32_t width) {
  uint32_t i;
  for(i=0u;i<width;++i) {
    uint32_t bit=1u<<i;
    if((raw&bit)==(previous&bit)) count[i]=0u;
    else if(++count[i]>=DEBOUNCE_STEPS) {previous^=bit;count[i]=0u;}
  }
  return previous;
}
static void capture_inputs(void) {
  uint32_t b=0u,j=0u,next,valid=0u;uint16_t sample=0u;
#if HAS_BUTTONS
  b=(uint32_t)exam_button_is_pressed(EXAM_BUTTON_INT0) |
    ((uint32_t)exam_button_is_pressed(EXAM_BUTTON_KEY1)<<1) |
    ((uint32_t)exam_button_is_pressed(EXAM_BUTTON_KEY2)<<2);
  stable_buttons=stable_mask(b,stable_buttons,button_count,3u); b=stable_buttons;
#endif
#if HAS_JOYSTICK
  j=exam_joystick_read();stable_joy=stable_mask(j,stable_joy,joy_count,5u);j=stable_joy;
#endif
#if HAS_ADC
  valid=exam_adc_take(&sample);
  if(valid) exam_adc_start();
#endif
  next=(head+1u)&31u;
  if(next==tail) {++lost_inputs;return;}
  queue[head].buttons=b;queue[head].joy=j;queue[head].valid=valid;queue[head].adc=sample;
  __DMB(); head=next;
}
#if HAS_BUTTONS
void EINT0_IRQHandler(void) {exam_button_ack(EXAM_BUTTON_INT0);++raw_edges;}
void EINT1_IRQHandler(void) {exam_button_ack(EXAM_BUTTON_KEY1);++raw_edges;}
void EINT2_IRQHandler(void) {exam_button_ack(EXAM_BUTTON_KEY2);++raw_edges;}
#endif
#if HAS_ADC
void ADC_IRQHandler(void) {exam_adc_irq_capture();}
#endif
static void stream_sample(void) {
#if HAS_DAC
  static const uint16_t sine[8]={512u,874u,1023u,874u,512u,150u,0u,150u};
  uint32_t sample;
  if(!audio_enabled) {audio_index=0u;audio_delay=0u;(void)exam_dac_write(0);return;}
  if(++audio_delay<audio_divider)return;
  audio_delay=0u;
  sample=audio_shape==1u?(audio_index<4u?1023u:0u):audio_shape==2u?audio_index*146u:sine[audio_index];
  (void)exam_dac_write((int32_t)(sample*audio_amplitude/1023u));
  audio_index=(audio_index+1u)&7u;
#endif
}
#if HAS_TIMER
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if(exam_timer_match_happened(flags,0u)) {
    ++output_ticks;
#if CONTROL_CLOCK == 1
    capture_inputs();
#endif
  }
}
#if HAS_DAC
void TIMER1_IRQHandler(void) {uint32_t f=exam_timer_ack(EXAM_TIMER1);if(exam_timer_match_happened(f,0u))stream_sample();}
#endif
#endif
#if HAS_RIT
void RIT_IRQHandler(void) {exam_rit_ack();
#if CONTROL_CLOCK == 2
  capture_inputs();
#else
  ++output_ticks;
#endif
}
#endif
#if HAS_SYSTICK
void SysTick_Handler(void) {
#if CONTROL_CLOCK == 3
  capture_inputs();
#else
  ++supervisor_ticks;
#endif
}
#endif
int main(void) {
  exam_init();controller_reset();audio_enabled=app.running;
#if HAS_BUTTONS
  exam_buttons_init();
  NVIC_SetPriority(EINT0_IRQn,3u);NVIC_SetPriority(EINT1_IRQn,3u);NVIC_SetPriority(EINT2_IRQn,3u);
#if POLL_BUTTONS
  NVIC_DisableIRQ(EINT0_IRQn);NVIC_DisableIRQ(EINT1_IRQn);NVIC_DisableIRQ(EINT2_IRQn);
#endif
#endif
#if HAS_JOYSTICK
  exam_joystick_init();
#endif
#if HAS_ADC
  exam_adc_init();NVIC_SetPriority(ADC_IRQn,2u);exam_adc_start();
#endif
#if HAS_DAC
  exam_dac_init();(void)exam_dac_write(0);
#endif
#if HAS_TIMER
  require(exam_timer_config_ms(EXAM_TIMER0,10u,EXAM_TIMER_PERIODIC));
  NVIC_SetPriority(TIMER0_IRQn,2u);exam_timer_start(EXAM_TIMER0);
#if HAS_DAC
  require(exam_timer_config_hz(EXAM_TIMER1,8000u,EXAM_TIMER_PERIODIC));
  NVIC_SetPriority(TIMER1_IRQn,1u);exam_timer_start(EXAM_TIMER1);
#endif
#endif
#if HAS_RIT
  require(exam_rit_config_ms(10u));NVIC_SetPriority(RIT_IRQn,2u);exam_rit_start();
#endif
#if HAS_SYSTICK
  require(exam_systick_config_ms(CONTROL_CLOCK==3?10u:100u));NVIC_SetPriority(SysTick_IRQn,2u);
#endif
  for(;;) {
    input_t input;uint32_t saved;
#if CONTROL_CLOCK == 0
    capture_inputs();
#endif
    saved=exam_critical_enter();
    if(tail==head) {exam_critical_exit(saved);continue;}
    input.buttons=queue[tail].buttons;input.joy=queue[tail].joy;input.valid=queue[tail].valid;input.adc=queue[tail].adc;
    tail=(tail+1u)&31u;exam_critical_exit(saved);
    controller_step(input.buttons,input.joy,input.valid,input.adc);
    saved=exam_critical_enter();
    audio_amplitude=app.amplitude;audio_enabled=app.running;audio_shape=app.phase%3u;
    audio_divider=MODE==16?app.period:1u;
    exam_critical_exit(saved);
#if HAS_LED
    exam_led_write((uint8_t)app.output);
#endif
#if HAS_DAC && !HAS_TIMER
    /* No sample-clock timer: this is a static control voltage, not audio. */
    (void)exam_dac_write(app.running?(int32_t)app.amplitude:0);
#endif
  }
}
#endif
