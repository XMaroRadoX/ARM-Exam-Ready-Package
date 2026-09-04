#include "LPC17xx.h"
#include "exam_api.h"

int main (void)
{
  exam_init();

  while (1)
  {
    __WFI();
  }
}
