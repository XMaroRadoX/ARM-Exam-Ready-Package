#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

static void leds_fill(void)
{
  (void)exam_led_write(0xFFu);
}
#define ROWS 6u
#define COLS 5u
extern void depthFirstSearchRandom(uint8_t *maze,uint32_t rows,uint32_t columns,uint32_t start);
static uint8_t maze[ROWS][COLS];

static void initialize_maze(void)
{
  uint32_t r,c;
  for(r=0u;r<ROWS;++r)for(c=0u;c<COLS;++c)
    maze[r][c]=(r==0u||r==ROWS-1u||c==0u||c==COLS-1u)?0xFFu:0u;
}

int main(void)
{
  exam_init();
  initialize_maze();
  /* The Q2 Reset_Handler starts SysTick with TICKINT clear. */
  depthFirstSearchRandom(&maze[0][0],ROWS,COLS,7u);

  for (;;) {
    __WFI();
  }
}
