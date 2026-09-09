
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

void copyData(const int8_t*a,int8_t*b,uint32_t n){while(n--)*b++=*a++;}
void insertionSort(int8_t*a,uint32_t n){mock_calls++;mock_arg[0]=n;for(uint32_t i=1;i<n;i++){int8_t x=a[i];uint32_t j=i;while(j&&a[j-1]>x){a[j]=a[j-1];j--;}a[j]=x;}}

/* Exam of 7 February 2023, questions 1 and 2. */
#include <stdint.h>
#include "LPC17xx.h"

/* Single-LED API arguments are physical board labels LD4 through LD11. */
#include "exam_api.h"

#define MAX_VALUES 20u

extern void copyData(const int8_t *source, int8_t *destination,
                     uint32_t length);
extern void insertionSort(int8_t *values, uint32_t length);

static int8_t values[MAX_VALUES];
static uint32_t value_count;
static uint32_t show_led6 = 1u;

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);

  if (value_count < MAX_VALUES) {
    values[value_count] = (int8_t)exam_timer_read(EXAM_TIMER1);
    value_count++;

    if (show_led6) {
      (void)exam_led_on(6u);  /* physical LED6 */
      (void)exam_led_off(7u); /* physical LED7 */
    } else {
      (void)exam_led_off(6u);
      (void)exam_led_on(7u);
    }
    show_led6 ^= 1u;
  }
}

void EINT1_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY1);
  (void)exam_led_off(6u);
  (void)exam_led_off(7u);
  insertionSort(values, value_count);
  (void)exam_led_on(11u); /* physical LED11 */
}

int answer_main(void)
{
  exam_init();
  exam_buttons_init();
  /* Timer1 resets at 0xFF, but its match does not generate an interrupt. */
  (void)exam_timer_config_ticks(EXAM_TIMER1, 0xFFu,
                                EXAM_TIMER_MODULO_NO_IRQ);
  exam_timer_start(EXAM_TIMER1);

  return 0;
}

static void review_step(void){
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
CHECK(mock_period[1]==255&&mock_mode[1]==EXAM_TIMER_MODULO_NO_IRQ);
mock_counter[1]=254;EINT0_IRQHandler();CHECK(values[0]==-2&&mock_led==(1u<<5));
mock_counter[1]=3;EINT0_IRQHandler();CHECK(values[1]==3&&mock_led==(1u<<4));
EINT1_IRQHandler();CHECK(mock_arg[0]==2&&mock_led==1);
for(int i=0;i<30;i++)EINT0_IRQHandler();CHECK(value_count==20);
return 0;}
