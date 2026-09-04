#include "LPC17xx.h"

int main (void)
{
  SystemInit();

  /* Initialize only the peripherals required by the exam question here. */

  while (1)
  {
    __WFI();
  }
}
