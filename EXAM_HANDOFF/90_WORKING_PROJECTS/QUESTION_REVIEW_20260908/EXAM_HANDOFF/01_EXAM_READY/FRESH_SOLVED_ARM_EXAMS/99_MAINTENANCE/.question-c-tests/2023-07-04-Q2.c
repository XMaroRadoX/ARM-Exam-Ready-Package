
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
uint32_t isSociable(uint32_t n){mock_arg[0]=n;mock_calls++;return mock_return;}
/* Exam of 4 July 2023, questions 1 and 2. */
#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t isSociable(uint32_t number);

static const uint32_t numbers[7] = {
  8128u, 5564u, 5400u, 14264u, 1305184u, 1598470u, 4938136u
};

static uint32_t current_number;

void TIMER1_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER1);
  uint32_t result;

  if ((pending & 1u) == 0u) {
    return;
  }

  result = isSociable(numbers[current_number]);
  current_number++;
  if (current_number == 7u) {
    current_number = 0u;
  }

  exam_led_clear();
  if ((result >= 1u) && (result <= 8u)) {
    /* result 1 -> physical LD4; result 8 -> LD11. */
    (void)exam_led_on((uint8_t)(result + 3u));
  }
}

int answer_main(void)
{
  exam_init();
  (void)exam_timer_config_ms(EXAM_TIMER1, 2000u, EXAM_TIMER_PERIODIC);
  exam_timer_start(EXAM_TIMER1);

  return 0;
}

static void review_step(void){
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
CHECK(mock_period[1]==2000);mock_return=1;TIMER1_IRQHandler();CHECK(mock_arg[0]==8128&&mock_led==128);
mock_return=0;TIMER1_IRQHandler();CHECK(mock_led==0);
for(int i=0;i<6;i++)TIMER1_IRQHandler();CHECK(mock_arg[0]==8128);
mock_pending[1]=0;TIMER1_IRQHandler();CHECK(mock_calls==8);
return 0;}
