/* Exam of 12 February 2025, ARM2, questions 1 and 2. */
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

extern int32_t Maclaurin_cos(int32_t y, uint32_t order);

int main(void)
{
  exam_init();
  exam_buttons_init();
  exam_dac_init();

  for (;;) {
    __WFI();
  }
}
