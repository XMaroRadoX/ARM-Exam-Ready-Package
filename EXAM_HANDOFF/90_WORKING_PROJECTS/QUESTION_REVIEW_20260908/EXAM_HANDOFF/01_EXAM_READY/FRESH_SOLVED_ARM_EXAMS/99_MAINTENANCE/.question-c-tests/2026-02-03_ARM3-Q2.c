
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
void Recaman(uint32_t*a,uint8_t n){mock_calls++;mock_arg[0]=n;uint32_t v[4]={0,1,3,6};for(int i=0;i<n;i++)a[i]=i<4?v[i]:(uint32_t)i;}
/* Exam of 3 February 2026: debounced KEY2 and two-second playback. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

#define EVENT_SEQUENCE_STEP (1u << 0)
extern void Recaman(uint32_t *area, uint8_t length);

/* All sequence/display state belongs to the foreground. */
static uint32_t sequence[255];
static uint8_t latest_value;
static uint8_t have_sample;
static uint8_t sequence_length;
static uint8_t sequence_active;
static uint32_t display_index;

void EINT2_IRQHandler(void)
{
  (void)exam_debounce_begin(EXAM_BUTTON_KEY2);
}

void RIT_IRQHandler(void)
{
  exam_rit_ack();
  exam_debounce_tick();
}

void ADC_IRQHandler(void) { exam_adc_irq_capture(); }

void TIMER0_IRQHandler(void)
{
  if ((exam_timer_ack(EXAM_TIMER0) & 1u) != 0u)
    exam_events_set(EVENT_SEQUENCE_STEP);
}

static void begin_sequence(void)
{
  exam_timer_stop(EXAM_TIMER0);
  exam_timer_reset(EXAM_TIMER0);
  (void)exam_events_take(EVENT_SEQUENCE_STEP);
  sequence_active = 0u;
  sequence_length = latest_value;
  display_index = 0u;
  if (sequence_length == 0u) {
    exam_led_clear();
    return;
  }
  Recaman(sequence, sequence_length);
  exam_led_write((uint8_t)sequence[0]);
  display_index = 1u;
  if (sequence_length > 1u &&
      exam_timer_config_ms(EXAM_TIMER0, 2000u, EXAM_TIMER_PERIODIC) == EXAM_OK) {
    sequence_active = 1u;
    exam_timer_start(EXAM_TIMER0);
  }
}

int answer_main(void)
{
  exam_init();
  exam_buttons_init();
  /* Package debounce recommendation; the paper does not prescribe 10/50 ms. */
  if (exam_debounce_config(10u, 50u) != EXAM_OK ||
      exam_rit_config_ms(10u) != EXAM_OK) {
    exam_led_write(0xFFu);
    for (;;) { __WFI(); }
  }
  exam_rit_start();
  exam_adc_init();
  exam_adc_start();

  return 0;
}

static void review_step(void){
    uint16_t sample;
    if (exam_adc_take(&sample)) {
      uint8_t value = (uint8_t)(sample >> 4);
      /* Playback owns the display. After it ends, hold its last value
         until a subsequent potentiometer high8 change restores preview. */
      if (!sequence_active && (!have_sample || value != latest_value))
        exam_led_write(value);
      latest_value = value;
      have_sample = 1u;
      exam_adc_start();
    }
    if ((exam_button_events_take() & EXAM_BUTTON_EVENT_KEY2) != 0u && have_sample)
      begin_sequence();
    if ((exam_events_take(EVENT_SEQUENCE_STEP) & EVENT_SEQUENCE_STEP) != 0u &&
        sequence_active) {
      exam_led_write((uint8_t)sequence[display_index++]);
      if (display_index >= sequence_length) {
        sequence_active = 0u;
        exam_timer_stop(EXAM_TIMER0);
        exam_timer_reset(EXAM_TIMER0);
      }
    }
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
mock_adc_value=0x40;mock_adc_fresh=1;review_step();mock_buttons=4;review_step();CHECK(mock_arg[0]==4&&mock_led==0&&display_index==1);
uint32_t expected[3]={1,3,6};for(int i=0;i<3;i++){TIMER0_IRQHandler();review_step();CHECK(mock_led==expected[i]);}CHECK(!mock_running[0]);
mock_adc_value=0;mock_adc_fresh=1;review_step();mock_buttons=4;review_step();CHECK(mock_led==0&&!sequence_active);
return 0;}
