
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
void bitMatrixMultiplication(const uint8_t*a,const uint8_t*b,uint8_t*c){mock_calls++;for(int i=0;i<8;i++)c[i]=(uint8_t)(i+1);}
/* Exam of 29 January 2025, ARM2, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern void bitMatrixMultiplication(const uint8_t *matrix_a,
                                    const uint8_t *matrix_b,
                                    uint8_t *matrix_c);

static uint8_t matrix_a[8];
static uint8_t matrix_b[8];
static uint8_t matrix_c[8];
static uint32_t input_rows;
static uint32_t output_row;

void EINT0_IRQHandler(void)
{
  uint32_t value;

  exam_button_ack(EXAM_BUTTON_INT0);
  if (input_rows >= 8u) {
    return;
  }

  value = exam_timer_read(EXAM_TIMER1) & 0xFFFFu;
  matrix_a[input_rows] = (uint8_t)(value >> 8);
  matrix_b[input_rows] = (uint8_t)value;
  input_rows++;
}

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);
  if (input_rows < 8u) {
    return;
  }

  bitMatrixMultiplication(matrix_a, matrix_b, matrix_c);

  output_row = 1u;
  (void)exam_led_write(matrix_c[0]);

  exam_timer_stop(EXAM_TIMER0);
  exam_timer_reset(EXAM_TIMER0);
  if (exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)==EXAM_OK)
    exam_timer_start(EXAM_TIMER0);
}

void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  if ((pending & 1u) == 0u) {
    return;
  }

  if (output_row < 8u) {
    (void)exam_led_write(matrix_c[output_row]);
    output_row++;
  } else {
    exam_led_clear();
    exam_timer_stop(EXAM_TIMER0);
    exam_timer_reset(EXAM_TIMER0);
  }
}

int answer_main(void)
{
  exam_init();
  exam_buttons_init();
  if (exam_timer_config_ticks(EXAM_TIMER1,0xFFFFu,
                              EXAM_TIMER_MODULO_NO_IRQ)==EXAM_OK)
    exam_timer_start(EXAM_TIMER1);

  return 0;
}

static void review_step(void){
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
EINT1_IRQHandler();CHECK(mock_calls==0);for(int i=0;i<8;i++){mock_counter[1]=0x4200+i;EINT0_IRQHandler();}EINT0_IRQHandler();CHECK(input_rows==8&&matrix_a[0]==0x42&&matrix_b[7]==7);
EINT1_IRQHandler();CHECK(mock_led==1&&mock_period[0]==500);for(int i=2;i<=8;i++){TIMER0_IRQHandler();CHECK(mock_led==(uint32_t)i);}TIMER0_IRQHandler();CHECK(mock_led==0&&!mock_running[0]);
return 0;}
