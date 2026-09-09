#define main answer_main
#define nextElementLCG counted_lcg
#include "C:/Personal/College/CA 2026/CA/ARM_Exam_Ready_Package/EXAM_HANDOFF/03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q3/main.c"
#undef main
#undef nextElementLCG

#include "exam_api.h"
static uint32_t joystick, led, clears, timer_stopped, rit_stopped, calls;
static uint32_t pending_flag=1u;
void exam_init(void) {}
void exam_joystick_init(void) {}
uint32_t exam_joystick_read(void) { return joystick; }
uint32_t exam_joystick_pressed_edges(uint32_t p,uint32_t c) {return c & ~p;}
void exam_led_clear(void) {led=0;clears++;}
exam_status_t exam_led_on(uint8_t label) {led=label;return EXAM_OK;}
uint32_t exam_timer_ack(exam_timer_t t) {(void)t;return pending_flag;}
void exam_rit_ack(void) {}
void exam_timer_stop(exam_timer_t t) {(void)t;timer_stopped++;}
void exam_rit_stop(void) {rit_stopped++;}
exam_status_t exam_timer_config_ms(exam_timer_t t,uint32_t ms,exam_timer_mode_t mode) {(void)t;(void)ms;(void)mode;return EXAM_OK;}
exam_status_t exam_rit_config_ms(uint32_t ms) {(void)ms;return EXAM_OK;}
void exam_timer_start(exam_timer_t t) {(void)t;}
void exam_rit_start(void) {}
void NVIC_SetPriority(int irq,uint32_t p) {(void)irq;(void)p;}
void __WFI(void) {}
extern uint32_t nextElementLCG(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);
uint32_t counted_lcg(uint32_t x,uint32_t a,uint32_t c,uint32_t n,uint32_t m) {
    calls++;return nextElementLCG(x,a,c,n,m);
}
#define CHECK(x) do {if (!(x)) return __LINE__;} while(0)

static void reset_game(void) {
    previous=1;n=0;waiting_for_move=0;expected_direction=0;
    num_correct=0;num_wrong=0;old_joystick=0;joystick=0;
    led=0;clears=0;timer_stopped=0;rit_stopped=0;calls=0;pending_flag=1;
}
static void input(uint32_t v) {joystick=v;RIT_IRQHandler();}
uint32_t test_main(void) {
    uint32_t i, saved;
    reset_game();
    input(EXAM_JOY_RIGHT);CHECK(num_correct==0 && num_wrong==0);
    TIMER0_IRQHandler();CHECK(led==9 && calls==1);
    input(EXAM_JOY_RIGHT);CHECK(waiting_for_move==1); /* held before round */
    input(0);input(EXAM_JOY_RIGHT);
    CHECK(num_correct==1 && waiting_for_move==0 && led==0);
    input(0);input(EXAM_JOY_LEFT);CHECK(num_wrong==0); /* second ignored */

    TIMER0_IRQHandler();CHECK(led==9);
    input(EXAM_JOY_LEFT);CHECK(waiting_for_move==1); /* still held */
    input(0);input(EXAM_JOY_UP);
    CHECK(num_wrong==1 && led==0);
    input(0);input(EXAM_JOY_RIGHT);CHECK(num_correct==1);

    TIMER0_IRQHandler();CHECK(led==8);
    input(0);input(EXAM_JOY_SELECT);CHECK(waiting_for_move==1);
    input(0);input(EXAM_JOY_DOWN|EXAM_JOY_RIGHT);
    CHECK(num_wrong==2 && waiting_for_move==0);

    /* No response: neither score changes when the next round starts. */
    TIMER0_IRQHandler();saved=num_correct+num_wrong;
    TIMER0_IRQHandler();CHECK(num_correct+num_wrong==saved);

    /* Reach tenth LED without ending its response window early. */
    while(n<10) TIMER0_IRQHandler();
    CHECK(calls==10 && waiting_for_move==1 && timer_stopped==0 && led==10);
    input(0);input(EXAM_JOY_LEFT);CHECK(num_correct==2);
    TIMER0_IRQHandler();
    CHECK(calls==10 && timer_stopped==1 && rit_stopped==1 && led==5);
    input(0);input(EXAM_JOY_LEFT);
    CHECK(led==5 && num_correct==2 && num_wrong==2); /* result stable */

    /* Ten correct answers => win, including a valid final-round answer. */
    reset_game();
    for(i=0;i<10;i++) {
        TIMER0_IRQHandler();input(0);input(expected_direction);
    }
    CHECK(calls==10 && num_correct==10 && timer_stopped==0);
    TIMER0_IRQHandler();CHECK(led==4 && rit_stopped==1);
    input(0);input(EXAM_JOY_UP);CHECK(led==4 && num_correct==10);

    /* Missing every response gives 0-0: a tie is defeat. */
    reset_game();
    for(i=0;i<11;i++) TIMER0_IRQHandler();
    CHECK(calls==10 && num_correct==0 && num_wrong==0 && led==5);
    return 0;
}
