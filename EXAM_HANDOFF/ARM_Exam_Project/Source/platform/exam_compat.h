#ifndef EXAM_COMPAT_H
#define EXAM_COMPAT_H

#include "exam_board.h"

/* Familiar names from the course templates. */
extern unsigned char led_value;
extern unsigned short AD_current;
void LED_init(void);
void LED_deinit(void);
void LED_On(unsigned int bit_number);
void LED_Off(unsigned int bit_number);
void LED_Out(unsigned int value);
void BUTTON_init(void);
uint32_t init_timer(uint8_t timer_num, uint32_t interval);
void enable_timer(uint8_t timer_num);
void disable_timer(uint8_t timer_num);
void reset_timer(uint8_t timer_num);
uint32_t init_RIT(uint32_t interval);
void enable_RIT(void);
void disable_RIT(void);
void reset_RIT(void);
void ADC_init(void);
void ADC_start_conversion(void);

#endif
