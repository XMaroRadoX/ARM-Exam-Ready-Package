/* Exam of 24 February 2023. The complete answer is in assembly.s. */
#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
  exam_init();

  for (;;) {
    __WFI();
  }
}
