#define main answer_main
#define nextElementLCG counted_lcg
#include "C:/Personal/College/CA 2026/CA/ARM_Exam_Ready_Package/EXAM_HANDOFF/03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q2/main.c"
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

uint32_t test_main(void) {
    const uint32_t expected[]={9,9,8,8,11,8,9,9,9,10};
    uint32_t i;
    pending_flag=0;TIMER0_IRQHandler();CHECK(calls==0);
    pending_flag=1;
    for(i=0;i<10;i++) {
        TIMER0_IRQHandler();CHECK(led==expected[i]);CHECK(calls==i+1);
        CHECK(clears==i+1);
    }
    CHECK(timer_stopped==1);
    TIMER0_IRQHandler();CHECK(calls==10 && led==10);
    return 0;
}
