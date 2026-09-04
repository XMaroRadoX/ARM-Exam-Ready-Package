#include "exam_api.h"
volatile uint32_t consumed;
void TIMER0_IRQHandler(void){uint32_t f=exam_timer_ack(EXAM_TIMER0);if(exam_timer_match_happened(f,0u))exam_events_set(1u);}
int main(void){exam_init();if(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)!=EXAM_OK)for(;;){}exam_timer_start(EXAM_TIMER0);for(;;){if(exam_events_take(1u)){++consumed;exam_led_write((uint8_t)consumed);}}}
