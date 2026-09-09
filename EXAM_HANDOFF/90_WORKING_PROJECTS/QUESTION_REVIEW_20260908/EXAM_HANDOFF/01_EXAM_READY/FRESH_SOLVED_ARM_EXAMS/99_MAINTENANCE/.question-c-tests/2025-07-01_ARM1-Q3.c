
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
uint32_t nextElementLCG(uint32_t p,uint32_t a,uint32_t c,uint32_t n,uint32_t m){mock_calls++;return ((p*a+c)^n)%m;}
/* Q3: complete game, using the Q1 assembly function.
 * Copy to Source/sample.c in a WORKING template.
 * Timer0 and RIT handlers are included here. Use both accompanying IRQ
 * replacement files so the linker sees exactly one owner per handler.
 */
#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t nextElementLCG(uint32_t previous, uint32_t a,
                               uint32_t c, uint32_t n, uint32_t m);

/* Persistent sequence state. n is the NEXT index, from 0 through 9. */
static uint32_t previous = 1u;
static uint32_t n = 0u;

/* 1 accepts one answer; 0 ignores answers until the next round. */
static volatile uint32_t waiting_for_move = 0u;
static volatile uint32_t expected_direction = 0u;
volatile uint32_t num_correct = 0u;
volatile uint32_t num_wrong = 0u;

/* Used to distinguish a new press from a direction being held. */
static uint32_t old_joystick = 0u;

/* remainder 0/1/2/3 -> LED 11/10/9/8 -> UP/LEFT/RIGHT/DOWN. */
static const uint32_t directions[4] = {
    EXAM_JOY_UP, EXAM_JOY_LEFT, EXAM_JOY_RIGHT, EXAM_JOY_DOWN
};

/* Called every three seconds by Timer0. */
void game_next_round(void)
{
    uint32_t value;
    uint32_t remainder;

    waiting_for_move = 0u;                /* Close the old response window. */
    exam_led_clear();                     /* Also clear an unanswered LED. */

    /* The tenth LED has already had its FULL three-second window.
     * This is timer interrupt 11, but it does NOT call the LCG.
     */
    if (n == 10u) {
        exam_timer_stop(EXAM_TIMER0);
        exam_rit_stop();
        if (num_correct > num_wrong) {
            exam_led_on(4u);              /* Victory. */
        } else {
            exam_led_on(5u);              /* Defeat, including a tie. */
        }
        return;
    }

    value = nextElementLCG(previous, 131u, 7u, n, 255u);
    previous = value;                     /* Input for the next generation. */
    remainder = value % 4u;
    expected_direction = directions[remainder];
    exam_led_on((uint8_t)(11u - remainder));
    waiting_for_move = 1u;                /* Allow precisely one response. */
    n++;
}

/* Called every 10 ms by RIT; this is input sampling, not a new round. */
void game_poll_joystick(void)
{
    uint32_t current;
    uint32_t pressed;

    /* Ignore centre/select; retain only the four directional inputs. */
    current = exam_joystick_read()
            & (EXAM_JOY_UP | EXAM_JOY_LEFT | EXAM_JOY_RIGHT | EXAM_JOY_DOWN);
    pressed = exam_joystick_pressed_edges(old_joystick, current);

    /* Update even when answers are disabled. A held direction must not
     * become a new answer just because the next round has started.
     */
    old_joystick = current;
    if (waiting_for_move == 0u || pressed == 0u) {
        return;
    }

    waiting_for_move = 0u;                /* First movement consumes answer. */
    if (pressed == expected_direction) {
        num_correct++;
    } else {
        num_wrong++;
    }
    exam_led_clear();                     /* Correct OR wrong: LED goes off. */
}

void TIMER0_IRQHandler(void)
{
    uint32_t pending = exam_timer_ack(EXAM_TIMER0);
    if ((pending & 1u) != 0u) {            /* MR0 is our 3-second interval. */
        game_next_round();
    }
}

void RIT_IRQHandler(void)
{
    exam_rit_ack();                       /* Acknowledge before sampling. */
    game_poll_joystick();
}

int answer_main(void)
{
    exam_init();
    exam_led_clear();
    exam_joystick_init();
    old_joystick = exam_joystick_read()
                 & (EXAM_JOY_UP | EXAM_JOY_LEFT
                    | EXAM_JOY_RIGHT | EXAM_JOY_DOWN);

    if (exam_timer_config_ms(EXAM_TIMER0, 3000u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { }
    }
    if (exam_rit_config_ms(10u) != EXAM_OK) {
        while (1) { }
    }

    /* Equal priorities serialize the two handlers' shared-state updates.
     * volatile alone would NOT prevent one handler preempting the other.
     */
    NVIC_SetPriority(TIMER0_IRQn, 0u);
    NVIC_SetPriority(RIT_IRQn, 0u);
    exam_rit_start();
    exam_timer_start(EXAM_TIMER0);
    return 0;
}

static void review_step(void){
        __WFI();
    }

/* Complete replacement for Source/RIT/IRQ_RIT.c.
 * RIT_IRQHandler is defined in the supplied sample.c answer.
 * This file deliberately defines no duplicate interrupt handler.
 */
#include "LPC17xx.h"
#include "exam_api.h"

/* Complete replacement for Source/timer/IRQ_timer.c.
 * TIMER0_IRQHandler is defined in the supplied sample.c answer.
 * Keep the unused timer handlers here; do not duplicate Timer0.
 */
#include "LPC17xx.h"
#include "exam_api.h"

void TIMER1_IRQHandler(void) { exam_timer_ack(EXAM_TIMER1); }
void TIMER2_IRQHandler(void) { exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { exam_timer_ack(EXAM_TIMER3); }

__declspec(dllexport) int test_main(void){answer_main();
TIMER0_IRQHandler();CHECK(waiting_for_move==1);mock_joy=expected_direction;RIT_IRQHandler();CHECK(num_correct==1&&waiting_for_move==0&&mock_led==0);
mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_UP|EXAM_JOY_DOWN;RIT_IRQHandler();CHECK(num_wrong==0);
for(int i=1;i<10;i++){TIMER0_IRQHandler();mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_UP|EXAM_JOY_DOWN;RIT_IRQHandler();}
CHECK(mock_calls==10&&num_wrong==9);TIMER0_IRQHandler();CHECK(mock_led==(1u<<(11-5))&&!mock_running[0]&&!mock_rit_running);
mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_LEFT;RIT_IRQHandler();CHECK(mock_led==(1u<<(11-5))&&mock_calls==10);
return 0;}
