
#include <stdint.h>
int _fltused=0;
void *memcpy(void*d,const void*s,__SIZE_TYPE__ n){unsigned char*a=d;const unsigned char*b=s;while(n--)*a++=*b++;return d;}
void *memset(void*d,int v,__SIZE_TYPE__ n){unsigned char*a=d;while(n--)*a++=(unsigned char)v;return d;}
#include "exam_api.h"
#define CHECK(x) do {if(!(x))return __LINE__;}while(0)
static uint32_t mock_budget, mock_joy, mock_led, mock_events, mock_buttons;
static uint32_t mock_pending[4]={1,1,1,1}, mock_counter[4], mock_period[4], mock_mode[4],mock_running[4];
static uint32_t mock_rit_running,mock_calls,mock_arg[8],mock_return, mock_adc_fresh,mock_adc_value,mock_dac,mock_dac_calls;
void exam_init(void) {}
void exam_led_write(uint8_t v){mock_led=v;}
uint8_t exam_led_read(void){return (uint8_t)mock_led;}
void exam_led_clear(void){mock_led=0;}
exam_status_t exam_led_on(uint8_t n){if(n<4||n>11)return EXAM_OUT_OF_RANGE;mock_led|=1u<<(11-n);return EXAM_OK;}
exam_status_t exam_led_off(uint8_t n){if(n<4||n>11)return EXAM_OUT_OF_RANGE;mock_led&=~(1u<<(11-n));return EXAM_OK;}
void exam_buttons_init(void){}
void exam_button_ack(exam_button_t b){(void)b;}
exam_status_t exam_debounce_config(uint32_t a,uint32_t b){return a==10&&b==50?EXAM_OK:EXAM_BAD_ARGUMENT;}
exam_status_t exam_debounce_begin(exam_button_t b){mock_arg[7]=b;return EXAM_OK;}
void exam_debounce_tick(void){}
uint32_t exam_button_events_take(void){uint32_t v=mock_buttons;mock_buttons=0;return v;}
exam_status_t exam_timer_config_ticks(exam_timer_t t,uint32_t n,exam_timer_mode_t m){mock_period[t]=n;mock_mode[t]=m;return EXAM_OK;}
exam_status_t exam_timer_config_ms(exam_timer_t t,uint32_t n,exam_timer_mode_t m){return exam_timer_config_ticks(t,n,m);}
void exam_timer_start(exam_timer_t t){mock_running[t]=1;}
void exam_timer_stop(exam_timer_t t){mock_running[t]=0;}
void exam_timer_reset(exam_timer_t t){mock_counter[t]=0;}
uint32_t exam_timer_read(exam_timer_t t){return mock_counter[t];}
uint32_t exam_timer_ack(exam_timer_t t){return mock_pending[t];}
uint8_t exam_timer_is_running(exam_timer_t t){return (uint8_t)mock_running[t];}
exam_status_t exam_rit_config_ms(uint32_t n){return n==10?EXAM_OK:EXAM_BAD_ARGUMENT;}
void exam_rit_start(void){mock_rit_running=1;}
void exam_rit_stop(void){mock_rit_running=0;}
void exam_rit_ack(void){}
void exam_joystick_init(void){}
uint32_t exam_joystick_read(void){return mock_joy;}
uint32_t exam_joystick_pressed_edges(uint32_t old,uint32_t now){return now&~old;}
void exam_adc_init(void){}
void exam_adc_start(void){}
void exam_adc_irq_capture(void){}
uint8_t exam_adc_take(uint16_t *v){if(!mock_adc_fresh)return 0;*v=(uint16_t)mock_adc_value;mock_adc_fresh=0;return 1;}
void exam_dac_init(void){}
exam_status_t exam_dac_write(int32_t v){mock_dac=(uint32_t)v;mock_dac_calls++;return EXAM_OK;}
void exam_events_set(uint32_t v){mock_events|=v;}
uint32_t exam_events_take(uint32_t mask){uint32_t v=mock_events&mask;mock_events&=~mask;return v;}
uint32_t exam_critical_enter(void){return 0;}
void exam_critical_exit(uint32_t saved){(void)saved;}
void NVIC_SetPriority(int irq,uint32_t p){(void)irq;(void)p;}
static void review_step(void);
uint32_t HofstadterConway(uint32_t*a,int n){for(int i=0;i<n;i++)a[i]=100;return 100;}
/* Exam of 18 February 2026, ARM2, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

#define SEQUENCE_LENGTH 1000u
#define SAMPLE_COUNT      45u

extern uint32_t HofstadterConway(uint32_t *values, int dimension);

static uint32_t sequence[SEQUENCE_LENGTH];
static uint32_t sequence_maximum;
static uint32_t sequence_index;
static uint32_t sample_index = SAMPLE_COUNT - 1u;

static const uint16_t SinTable[SAMPLE_COUNT] = {
  410, 467, 523, 576, 627, 673, 714, 749, 778,
  799, 813, 819, 817, 807, 789, 764, 732, 694,
  650, 602, 550, 495, 438, 381, 324, 270, 217,
  169, 125, 87, 55, 30, 12, 2, 0, 6, 20, 41,
  70, 105, 146, 193, 243, 297, 353
};

/* Evaluate the paper's formula in floating point, then cast the result. */
static uint32_t note_threshold(uint32_t value,
                               uint32_t maximum_period,
                               uint32_t minimum_period,
                               uint32_t k)
{
  float range_per_step;
  float threshold;

  range_per_step = (float)(maximum_period - minimum_period) /
                   (float)sequence_maximum;
  threshold = ((float)maximum_period - range_per_step * (float)value) /
              (float)k;

  if (threshold < 1.0f) {
    threshold = 1.0f;
  }

  return (uint32_t)threshold;
}

/* Timer A: choose and start the next note when B and C are both stopped. */
void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  uint32_t value;
  uint32_t waveform_threshold;
  uint32_t duration_threshold;

  if ((pending & 1u) == 0u) {
    return;
  }

  if (sequence_index >= SEQUENCE_LENGTH ||
      exam_timer_is_running(EXAM_TIMER1) ||
      exam_timer_is_running(EXAM_TIMER2)) {
    return;
  }

  value = sequence[sequence_index];
  waveform_threshold = note_threshold(value, 5351u, 1062u, 1u);
  duration_threshold = note_threshold(value, 40000000u, 625000u, 5u);

  sequence_index++;
  if (sequence_index == SEQUENCE_LENGTH) {
    (void)exam_timer_stop(EXAM_TIMER0);
  }

  /* Timer B resets on every match and therefore remains periodic. */
  (void)exam_timer_stop(EXAM_TIMER1);
  (void)exam_timer_reset(EXAM_TIMER1);
  (void)exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                                EXAM_TIMER_PERIODIC);

  /* Timer C is a one-shot: interrupt, reset and stop at the match. */
  (void)exam_timer_stop(EXAM_TIMER2);
  (void)exam_timer_reset(EXAM_TIMER2);
  (void)exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                                EXAM_TIMER_ONE_SHOT);

  (void)exam_timer_start(EXAM_TIMER1);
  (void)exam_timer_start(EXAM_TIMER2);
}

/* Timer B: send the next sinusoidal sample to the DAC. */
void TIMER1_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER1);
  if ((pending & 1u) == 0u) {
    return;
  }

  if (!exam_timer_is_running(EXAM_TIMER1)) return;
  sample_index++;
  if (sample_index == SAMPLE_COUNT) {
    sample_index = 0u;
  }

  (void)exam_dac_write(SinTable[sample_index]);
}

/* Timer C: terminate the note by stopping Timer B. */
void TIMER2_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER2);
  if ((pending & 1u) == 0u) {
    return;
  }

  (void)exam_timer_stop(EXAM_TIMER1);
  (void)exam_timer_reset(EXAM_TIMER1);
  (void)exam_timer_stop(EXAM_TIMER2);
  (void)exam_timer_reset(EXAM_TIMER2);
  (void)exam_dac_write(0);
}

int answer_main(void)
{
  exam_init();
  exam_dac_init();
  sequence_maximum = HofstadterConway(sequence, (int)SEQUENCE_LENGTH);
  (void)exam_dac_write(0);

  /* The Combined API derives 50 ms from Timer0's actual peripheral clock. */
  (void)exam_timer_config_ms(EXAM_TIMER0, 50u, EXAM_TIMER_PERIODIC);
  (void)exam_timer_start(EXAM_TIMER0);

  return 0;
}

static void review_step(void){
    /* This paper places the required work in the three timer handlers. */
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
CHECK(mock_period[0]==50);TIMER0_IRQHandler();CHECK(sequence_index==1&&mock_period[1]==1062&&mock_period[2]==125000&&mock_mode[2]==EXAM_TIMER_ONE_SHOT);
TIMER0_IRQHandler();CHECK(sequence_index==1);TIMER1_IRQHandler();CHECK(mock_dac==410);TIMER1_IRQHandler();CHECK(mock_dac==467);
TIMER2_IRQHandler();CHECK(!mock_running[1]&&!mock_running[2]&&mock_dac==0);TIMER1_IRQHandler();CHECK(mock_dac==0);
sequence_index=999;TIMER0_IRQHandler();CHECK(sequence_index==1000&&!mock_running[0]);mock_running[1]=mock_running[2]=0;TIMER0_IRQHandler();CHECK(sequence_index==1000);
return 0;}
