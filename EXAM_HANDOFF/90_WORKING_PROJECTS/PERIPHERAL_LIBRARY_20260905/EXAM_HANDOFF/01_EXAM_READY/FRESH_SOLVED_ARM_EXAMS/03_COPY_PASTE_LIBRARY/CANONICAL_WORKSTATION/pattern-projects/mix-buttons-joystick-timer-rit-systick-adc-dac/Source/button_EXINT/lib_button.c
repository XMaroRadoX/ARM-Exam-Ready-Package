
#include "button.h"
#include "LPC17xx.h"

/**
 * @brief  Function that initializes Buttons
 */
void BUTTON_init(void) {

  LPC_PINCON->PINSEL4    |= (1u << 20);		 /* External interrupt 0 pin selection */
  LPC_PINCON->PINSEL4    &= ~(1u << 21);

  LPC_PINCON->PINSEL4    |= (1u << 22);     /* External interrupt 1 pin selection */
  LPC_PINCON->PINSEL4    &= ~(1u << 23);
 
  LPC_PINCON->PINSEL4    |= (1u << 24);     /* External interrupt 2 pin selection */
  LPC_PINCON->PINSEL4    &= ~(1u << 25);

  /* FIOPIN reads are affected by FIOMASK; keep the three button bits visible. */
  LPC_GPIO2->FIOMASK &= ~((1u << 10) | (1u << 11) | (1u << 12));

  /* Configure only EINT0-EINT2. Preserve EINT3 if question code uses it. */
  LPC_SC->EXTMODE = (LPC_SC->EXTMODE & ~0x7u) | 0x7u; /* edge-sensitive */
  LPC_SC->EXTPOLAR &= ~0x7u;                          /* falling-edge */

  NVIC_EnableIRQ(EINT2_IRQn);              /* enable irq in nvic                 */
	NVIC_SetPriority(EINT2_IRQn, 1);				 /* priority, the lower the better     */
  NVIC_EnableIRQ(EINT1_IRQn);              /* enable irq in nvic                 */
	NVIC_SetPriority(EINT1_IRQn, 2);				 
  NVIC_EnableIRQ(EINT0_IRQn);              /* enable irq in nvic                 */
	NVIC_SetPriority(EINT0_IRQn, 3);				 /* decreasing priority	from EINT2->0	 */
}

