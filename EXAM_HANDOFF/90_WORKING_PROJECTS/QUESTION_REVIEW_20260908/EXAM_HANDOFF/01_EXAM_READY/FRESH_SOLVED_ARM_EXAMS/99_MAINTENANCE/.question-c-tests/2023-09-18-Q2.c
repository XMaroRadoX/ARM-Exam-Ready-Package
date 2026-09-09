
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

uint32_t digitSum(uint32_t n){uint32_t s=0;do{s+=n%10;n/=10;}while(n);return s;}
uint32_t digitaddition(uint32_t*a,uint32_t n){mock_calls++;if(mock_return==1)return 0;uint32_t sum=digitSum(a[0]);for(uint32_t i=1;i<n;i++){a[i]=a[i-1]+digitSum(a[i-1]);sum+=digitSum(a[i]);}return sum;}

#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

/* Single-LED API arguments are physical board labels LD4 through LD11. */

extern uint32_t digitSum(uint32_t value);
extern uint32_t digitaddition(uint32_t *area, uint32_t count);

static uint32_t series[10];
static volatile uint32_t entered_value;

static void handle_button(exam_button_t button)
{
  uint32_t reported;
  uint32_t formula;
  if (button == EXAM_BUTTON_KEY1) {
    entered_value <<= 1;        /* append binary digit 0 */
  } else if (button == EXAM_BUTTON_KEY2) {
    entered_value = (entered_value << 1) | 1u;
  } else if (button == EXAM_BUTTON_INT0) {
    series[0] = entered_value;
    reported = digitaddition(series, 10u);
    /* Zero seed legitimately generates ten zeroes. Other zero returns mean
       overflow and leave the tail incomplete, so do not read that tail. */
    formula = (reported || series[0] == 0u)
      ? series[9] - series[0] + digitSum(series[9]) : UINT32_MAX;
    if (reported == formula) {
      (void)exam_led_on(4u);
      (void)exam_led_off(5u);
    } else {
      (void)exam_led_off(4u);
      (void)exam_led_on(5u);
    }
  }
}

void EINT0_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_INT0); handle_button(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY1); handle_button(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY2); handle_button(EXAM_BUTTON_KEY2); }

int answer_main(void)
{
  exam_init();
  entered_value = 0u;
  exam_led_clear();
  exam_buttons_init();

  return 0;
}

static void review_step(void){
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
EINT2_IRQHandler();EINT1_IRQHandler();EINT1_IRQHandler();EINT2_IRQHandler();EINT2_IRQHandler();EINT1_IRQHandler();CHECK(entered_value==38);
EINT0_IRQHandler();CHECK(mock_led==128);
mock_return=1;EINT0_IRQHandler();CHECK(mock_led==64);
entered_value=0;mock_return=0;EINT0_IRQHandler();CHECK(mock_led==128&&series[9]==0);
return 0;}
