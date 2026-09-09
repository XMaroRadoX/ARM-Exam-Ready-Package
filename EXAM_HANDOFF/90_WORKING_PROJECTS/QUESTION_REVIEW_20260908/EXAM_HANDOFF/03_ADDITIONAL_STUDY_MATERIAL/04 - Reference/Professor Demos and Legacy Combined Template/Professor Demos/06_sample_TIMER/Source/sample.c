/*----------------------------------------------------------------------------
 * Name:    sample.c
 * Purpose: 
 *		to control led11 and led 10 through EINT buttons (similarly to project 03_)
 *		to control leds9 to led4 by the timer handler (1 second - circular cycling)
 * Note(s): this version supports the LANDTIGER Emulator
 * Author: 	Paolo BERNARDI - PoliTO - last modified 15/12/2020
 *----------------------------------------------------------------------------
 *
 * This software is supplied "AS IS" without warranties of any kind.
 *
 * Copyright (c) 2017 Politecnico di Torino. All rights reserved.
 *----------------------------------------------------------------------------*/

                  
#include <stdio.h>
#include "LPC17xx.h"                    /* LPC17xx definitions                */
#include "led.h"
#include "button.h"
#include "timer.h"
#include "systick.h"
#include "RIT.h"


#ifdef SIMULATOR
extern uint8_t ScaleFlag; // <- ScaleFlag needs to visible in order for the emulator to find the symbol (can be placed also inside system_LPC17xx.h but since it is RO, it needs more work)
#endif
/*----------------------------------------------------------------------------
  Main Program
 *----------------------------------------------------------------------------*/
int main (void) {
  	
	SystemInit();  												/* System Initialization (i.e., PLL)  */
  LED_init();                           /* LED Initialization                 */
  BUTTON_init();												/* BUTTON Initialization              */
	
	/* choose one of the following timers.
	They have the same behaviour: leds are turned off and on at regular intervals */
	
	/* 1) System Tick Timer */
	// systick_init(0xE4E1C0);							/* T = 0.15 sec. */
																					/* F = 100 MHz; K is expressed on 24 bits */
	
	/* 2) Standard Timers 	*/
	// init_timer(0,0x017D7840);					/* TIMER0 initialization, interrupts at 1 sec - 1 sec - 2 sec */
																				/* K = T * Fr = [s]*[Hz] = [s]*[1/s]	  */
																				/* T = K / Fr = 0x017D7840 / 25MHz = 25000000 / 25 * 10^6 Hz  = 1 sec	(one second) */
	/* Other notable values: */
	// init_timer(0,0xFFFFFFFF);					// 5 min 43sec
	// init_timer(0,0x00B41780);					// 1 min 0x2CB41780
	// init_timer(0,0x0EE6B280);					// 10 sec
	//enable_timer(0);
	
	/* 3) Repetitive Interrupt Timer (RIT) */
	init_RIT(0x05F5E100);									/* RIT initialization 1 sec */
	enable_RIT();
	
	LED_On(7);

	LPC_SC->PCON |= 0x1;		/* power-down mode */								
	LPC_SC->PCON &= 0xFFFFFFFFD; 
	SCB->SCR |= 0x2;				/* set SLEEPONEXIT */
	
	__ASM("wfi");
}
