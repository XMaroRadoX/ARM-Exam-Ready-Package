
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
uint32_t LCGsequence(uint32_t p,uint32_t a,uint32_t c,uint32_t n,uint32_t m){mock_calls++;return ((p*a+c)^(p>>n))%m;}
/* Q2: one generated value and one LED every 2.5 seconds.
 * Copy this complete file to Source/sample.c in a WORKING template.
 * Use the supplied IRQ_timer.c replacement: Timer0 is owned here.
 */
#include "LPC17xx.h"
#include "exam_api.h"

/* Compiler passes the first four arguments in R0-R3 and m on the stack. */
extern uint32_t LCGsequence(uint32_t previous, uint32_t a,
                               uint32_t c, uint32_t n, uint32_t m);

void TIMER1_IRQHandler(void)
{
    /* Static locals retain their values between timer interrupts. */
    static uint32_t previous = 6u;
    static uint32_t n = 0u;
    uint32_t pending;
    uint32_t value;
    uint32_t remainder;
    uint8_t led;

    pending = exam_timer_ack(EXAM_TIMER1); /* Read AND clear event flags. */
    if ((pending & 1u) == 0u) {
        return;                           /* Not our MR0 interval event. */
    }
    if (n >= 10u) {
        return;                           /* Never call LCG an 11th time. */
    }

    value = LCGsequence(previous, 157u, 3u, 3u, 256u);
    remainder = value % 4u;
    led = (uint8_t)(4u + remainder);      /* 0->4, 1->5, 2->6, 3->7. */

    exam_led_clear();                     /* Old LED off before new LED on. */
    exam_led_on(led);                      /* Physical board label, not index. */
    previous = value;
    n++;

    if (n == 10u) {
        exam_timer_stop(EXAM_TIMER1);      /* Q2 leaves the last LED lit. */
    }
}

int answer_main(void)
{
    exam_init();
    exam_led_clear();
    if (exam_timer_config_ms(EXAM_TIMER1, 2500u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { }                     /* Configuration failed. */
    }
    exam_timer_start(EXAM_TIMER1);
    return 0;
}

static void review_step(void){
        __WFI();                          /* Hardware schedules the work. */
    }

/* Complete replacement for Source/timer/IRQ_timer.c.
 * TIMER1_IRQHandler is defined in the supplied sample.c answer.
 * Keep the unused timer handlers here; do not duplicate Timer0.
 */
#include "LPC17xx.h"
#include "exam_api.h"

void TIMER0_IRQHandler(void) { exam_timer_ack(EXAM_TIMER0); }
void TIMER2_IRQHandler(void) { exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { exam_timer_ack(EXAM_TIMER3); }

__declspec(dllexport) int test_main(void){answer_main();
int expected[10]={5,6,5,4,7,5,6,7,6,4};CHECK(mock_period[1]==2500);
for(int i=0;i<10;i++){TIMER1_IRQHandler();CHECK(mock_led==(1u<<(11-expected[i])));}CHECK(mock_calls==10&&!mock_running[1]);TIMER1_IRQHandler();CHECK(mock_calls==10);
return 0;}
