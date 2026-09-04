#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t held, pressed, released;
static uint32_t previous;
void RIT_IRQHandler(void) {
  uint32_t current;
  exam_rit_ack();current=exam_joystick_read();
  pressed=exam_joystick_pressed_edges(previous,current);
  released=exam_joystick_released_edges(previous,current);
  held=current;previous=current;
  if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
  if (released & EXAM_JOY_SELECT) exam_led_clear();
}
int main(void) {
  exam_init();exam_joystick_init();previous=exam_joystick_read();
  require(exam_rit_config_ms(10u));exam_rit_start();
  for (;;) {}
}
