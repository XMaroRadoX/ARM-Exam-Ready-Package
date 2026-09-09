#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

static void leds_fill(void)
{
  (void)exam_led_write(0xFFu);
}
#define NUM_ROWS 10u
#define NUM_COLUMNS 8u
extern uint32_t mazeSolver(uint32_t rows, uint32_t columns, uint8_t *maze);
static uint8_t maze[NUM_ROWS][NUM_COLUMNS];
static volatile uint32_t longest_path;

static uint32_t lcg_next(uint32_t value) { return ((value % 101u) * 18u) % 101u; }

static void generate_maze(uint32_t seed)
{
  uint32_t r, c, value = seed;
  for (r=0u; r<NUM_ROWS; ++r) for (c=0u; c<NUM_COLUMNS; ++c) {
    if ((r==0u||r==NUM_ROWS-1u) && (c==0u||c==NUM_COLUMNS-1u)) maze[r][c]='*';
    else {
      value=lcg_next(value);
      if (r==0u) maze[r][c]=value<90u?'*':'n';
      else if (c==NUM_COLUMNS-1u) maze[r][c]=value<90u?'*':'e';
      else if (r==NUM_ROWS-1u) maze[r][c]=value<90u?'*':'s';
      else if (c==0u) maze[r][c]=value<90u?'*':'w';
      else maze[r][c]=value<60u?' ':'*';
    }
  }
}

void EINT2_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_KEY2);
  generate_maze(exam_timer_read(EXAM_TIMER0));
  longest_path=mazeSolver(NUM_ROWS,NUM_COLUMNS,&maze[0][0]);
}

int main(void)
{
  exam_init();
  exam_led_clear();
  exam_buttons_init();
  if (exam_timer_config_ticks(EXAM_TIMER0, UINT32_MAX,
                              EXAM_TIMER_MODULO_NO_IRQ) != EXAM_OK) {
    leds_fill();
  } else {
    exam_timer_start(EXAM_TIMER0);
  }

  for (;;) {
    __WFI();
  }
}
