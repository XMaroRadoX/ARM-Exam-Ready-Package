#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

extern int32_t SDIV64(int32_t upper, uint32_t lower, int32_t divisor);
extern int32_t SDIV64S(int32_t upper, uint32_t lower, int32_t divisor);

volatile int32_t division_result;
volatile int32_t flagged_division_result;

int main(void)
{
  exam_init();
  division_result = SDIV64(-3, 0xFFFFFFFAu, -5);
  flagged_division_result = SDIV64S(-3, 0xFFFFFFFAu, -5);

  for (;;) {
    __WFI();
  }
}
