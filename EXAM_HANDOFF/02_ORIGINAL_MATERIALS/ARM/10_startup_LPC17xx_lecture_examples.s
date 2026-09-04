;/**************************************************************************//**
; * @file     startup_LPC17xx.s
; * @brief    CMSIS Cortex-M3 Core Device Startup File for
; *           NXP LPC17xx Device Series
; * @version  V1.10
; * @date     06. April 2011
; *
; * @note
; * Copyright (C) 2009-2011 ARM Limited. All rights reserved.
; *
; * @par
; * ARM Limited (ARM) is supplying this software for use with Cortex-M
; * processor based microcontrollers.  This file can be freely distributed
; * within development tools that are supporting such ARM based processors.
; *
; * @par
; * THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED
; * OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
; * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
; * ARM SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR
; * CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
; *
; ******************************************************************************/

; *------- <<< Use Configuration Wizard in Context Menu >>> ------------------

; <h> Stack Configuration
;   <o> Stack Size (in Bytes) <0x0-0xFFFFFFFF:8>
; </h>

Stack_Size      EQU     0x00000200

                AREA    STACK, DATA, NOINIT, READWRITE, ALIGN=3
Stack_Mem       SPACE   Stack_Size
__initial_sp

                AREA    processStack, DATA, NOINIT, READWRITE, ALIGN=3
				SPACE   Stack_Size
process_initial_sp

; <h> Heap Configuration
;   <o>  Heap Size (in Bytes) <0x0-0xFFFFFFFF:8>
; </h>

Heap_Size       EQU     0x00000000

                AREA    HEAP, NOINIT, READWRITE, ALIGN=3
__heap_base
Heap_Mem        SPACE   Heap_Size
__heap_limit


                PRESERVE8
                THUMB


; Vector Table Mapped to Address 0 at Reset

                AREA    RESET, DATA, READONLY
                EXPORT  __Vectors

__Vectors       DCD     __initial_sp              ; Top of Stack
                DCD     Reset_Handler             ; Reset Handler
                DCD     NMI_Handler               ; NMI Handler
                DCD     HardFault_Handler         ; Hard Fault Handler
                DCD     MemManage_Handler         ; MPU Fault Handler
                DCD     BusFault_Handler          ; Bus Fault Handler
                DCD     UsageFault_Handler        ; Usage Fault Handler
                DCD     0                         ; Reserved
                DCD     0                         ; Reserved
                DCD     0                         ; Reserved
                DCD     0                         ; Reserved
                DCD     SVC_Handler               ; SVCall Handler
                DCD     DebugMon_Handler          ; Debug Monitor Handler
                DCD     0                         ; Reserved
                DCD     PendSV_Handler            ; PendSV Handler
                DCD     SysTick_Handler           ; SysTick Handler

                ; External Interrupts
                DCD     WDT_IRQHandler            ; 16: Watchdog Timer
                DCD     TIMER0_IRQHandler         ; 17: Timer0
                DCD     TIMER1_IRQHandler         ; 18: Timer1
                DCD     TIMER2_IRQHandler         ; 19: Timer2
                DCD     TIMER3_IRQHandler         ; 20: Timer3
                DCD     UART0_IRQHandler          ; 21: UART0
                DCD     UART1_IRQHandler          ; 22: UART1
                DCD     UART2_IRQHandler          ; 23: UART2
                DCD     UART3_IRQHandler          ; 24: UART3
                DCD     PWM1_IRQHandler           ; 25: PWM1
                DCD     I2C0_IRQHandler           ; 26: I2C0
                DCD     I2C1_IRQHandler           ; 27: I2C1
                DCD     I2C2_IRQHandler           ; 28: I2C2
                DCD     SPI_IRQHandler            ; 29: SPI
                DCD     SSP0_IRQHandler           ; 30: SSP0
                DCD     SSP1_IRQHandler           ; 31: SSP1
                DCD     PLL0_IRQHandler           ; 32: PLL0 Lock (Main PLL)
                DCD     RTC_IRQHandler            ; 33: Real Time Clock
                DCD     EINT0_IRQHandler          ; 34: External Interrupt 0
                DCD     EINT1_IRQHandler          ; 35: External Interrupt 1
                DCD     EINT2_IRQHandler          ; 36: External Interrupt 2
                DCD     EINT3_IRQHandler          ; 37: External Interrupt 3
                DCD     ADC_IRQHandler            ; 38: A/D Converter
                DCD     BOD_IRQHandler            ; 39: Brown-Out Detect
                DCD     USB_IRQHandler            ; 40: USB
                DCD     CAN_IRQHandler            ; 41: CAN
                DCD     DMA_IRQHandler            ; 42: General Purpose DMA
                DCD     I2S_IRQHandler            ; 43: I2S
                DCD     ENET_IRQHandler           ; 44: Ethernet
                DCD     RIT_IRQHandler            ; 45: Repetitive Interrupt Timer
                DCD     MCPWM_IRQHandler          ; 46: Motor Control PWM
                DCD     QEI_IRQHandler            ; 47: Quadrature Encoder Interface
                DCD     PLL1_IRQHandler           ; 48: PLL1 Lock (USB PLL)
                DCD     USBActivity_IRQHandler    ; 49: USB Activity interrupt to wakeup
                DCD     CANActivity_IRQHandler    ; 50: CAN Activity interrupt to wakeup


                IF      :LNOT::DEF:NO_CRP
                AREA    |.ARM.__at_0x02FC|, CODE, READONLY
CRP_Key         DCD     0xFFFFFFFF
                ENDIF


				AREA example, DATA, READWRITE
var1			SPACE 4
var2			SPACE 1
var3			SPACE 8

				AREA example2, DATA, READONLY
myData			FILL 20, 1, 4

HardFaultStatusRegister	EQU 0xE000ED2C
SystemHandlerControlStateRegister EQU 0xE000ED24
UsageFaultStatusRegister EQU 0xE000ED2A
ConfigurationControlRegister EQU 0xE000ED14
BusFaultStatusRegister EQU 0xE000ED29
BusFaultAddressRegister EQU 0xE000ED38
	
SYScontrolAndStatusReg EQU 0xE000E010
SYSreloadValueReg EQU 0xE000E014
SYScurrentValueReg EQU 0xE000E018

	
                AREA    |.text|, CODE, READONLY


; Reset Handler
counter RN r6
myConstant EQU 3

Reset_Handler   PROC	
                EXPORT  Reset_Handler             [WEAK]				
				; enabling usage, memory management and bus faults
				;MOV r1, #2_1110000000000
				
				
				MOV r1, #0x70000
				LDR r2, =SystemHandlerControlStateRegister
				STR r1, [r2]
				MOV r3, #0xAAAAAAAA
				
				
				; example of systick timer
				LDR r0, =SYScontrolAndStatusReg
				MOV r1, #0
				STR r1, [r0]; step1; stop the timer
				LDR r0, =SYSreloadValueReg
				LDR r1, =1023; example
				STR r1, [r0] ; step2
				LDR r0, =SYScurrentValueReg
				STR r1, [r0] ; step3: timer counter is 0
				LDR r0, =SYScontrolAndStatusReg
				MOV r1, #7		; 2_111
				STR r1, [r0] ; step4: the timer starts
				
				MOV r4, #5
timerLoop		NOP			; do something
				CMP r4, #0
				BHI timerLoop	; when r4 = 0 the loop ends
				
				; stop the timer
				LDR r0, =SYScontrolAndStatusReg
				MOV r1, #0
				STR r1, [r0]; step1; stop the timer
				
				
				LDR r4, =process_initial_sp
				;LDR r4, =0
				MSR PSP, r4
				; thread mode, priviledged level
				; move to user level
				MRS r0, CONTROL
				ORR r0, r0, #1	; forces the least significant bit to 1
				ORR r0, r0, #2_10	; use the psp
				MSR CONTROL, r0
				
				; now we are at user level
				; we can not write the CONTROL register
				MRS r1, CONTROL
				;AND r1, r1, #FFFFFFFE	; forces the least significant bit to 0
				BIC r1, r1, #1
				MSR CONTROL, r1	
				
				SVC 67	; we move to privileged level

				; bus fault example: use of PSP without initialization
				PUSH {r3}
				
				
				; usage fault example: division by zero
				LDR r8, =ConfigurationControlRegister 
				MOV r7, #2_10000
				STR r7, [r8]
				
				MOV r5, #0xABCD
				MOV r6, #0
				UDIV r7, r5, r6

				; usage fault example: undefined instruction (only hardware debug)
				DCD 0xe7f0def0

				; usage fault example: coprocesssor instruction
				LDC p1, c0, [r1]

				; usage fault example: ARM state exceptions
				ADRL r0, stop
				BX r0
				
			
				
stop 			B stop 				; stop 

				ENDP



; Dummy Exception Handlers (infinite loops which can be modified)

NMI_Handler     PROC
                EXPORT  NMI_Handler               [WEAK]
                B       .
                ENDP
HardFault_Handler\
                PROC
                EXPORT  HardFault_Handler         [WEAK]
				LDR r0, =HardFaultStatusRegister
				LDR r1, [r0]
				;TST r1, #2_0100 0000 0000 0000 0000 in binary
				TST r1, #0x40000000
				BNE usageFault
				; check other conditions
				B       .
				
				
usageFault		; do things
				B       .
					
                
                ENDP
MemManage_Handler\
                PROC
                EXPORT  MemManage_Handler         [WEAK]
                B       .
                ENDP
BusFault_Handler\
                PROC
                EXPORT  BusFault_Handler          [WEAK]
				LDR r0, =BusFaultStatusRegister
				LDRB r1, [r0]
				TST r1, #2_10
				BNE preciseBusFault
				; imprecise: do something else	
                B       .
				
preciseBusFault LDR r2, =BusFaultAddressRegister
				LDR r3, [r2]	
				
				B       .
                ENDP
UsageFault_Handler\
                PROC
                EXPORT  UsageFault_Handler        [WEAK]
				LDR r0, =UsageFaultStatusRegister
				LDRH r1, [r0]
				TST r1, #2_10	; if r1 = 2_10
									; AND r1, #2_0000000010 -> result is 000000010
									; -> zero flag is 0 because the result is not zero
									; we take the branch with BNE
				BNE ARMinstruction
				
				TST r1, #2_1000
				BNE coprocessorInstruction
				
				TST r1, #2_1
				BNE unsupportedInstruction
				
				; test something else
				B       .
ARMinstruction	; determine if the program was using the main stack or process stack
				TST LR, #2_100	; if MSP was used, bit 2 is zero
								; AND with 2_100  -> 000000 -> zero flag is 1
				ITE EQ
				MRSEQ r3, MSP
				MRSNE r3, PSP
				

				LDR r2, [r3, #28]
				ORR r2, r2, #0x1000000
				STR r2, [r3, #28]
				BX LR
				
coprocessorInstruction	
				; determine which stack was used -> save the stack pointer in register r3
				TST LR, #2_100	; if MSP was used, bit 2 is zero
				ITE EQ
				MRSEQ r3, MSP
				MRSNE r3, PSP
				LDR r2, [r3, #24]	; r2 now contains the PC
				LDR r1, [r2]

				B       .	; only because the code is incomplete

unsupportedInstruction
				; determine which stack was used -> save the stack pointer in register r3
				TST LR, #2_100	; if MSP was used, bit 2 is zero
				ITE EQ
				MRSEQ r3, MSP
				MRSNE r3, PSP
				LDR r2, [r3, #24]	; r2 now contains the PC
				LDR r1, [r2]

				B       .

				ENDP
SVC_Handler     PROC
                EXPORT  SVC_Handler               [WEAK]
				
				TST LR, #2_100	; if MSP was used, bit 2 is zero
								; AND with 2_100  -> 000000 -> zero flag is 1
				ITE EQ
				MRSEQ r3, MSP
				MRSNE r3, PSP
				

				LDR r2, [r3, #24]	; address stored in PC
				LDRB r4, [r2, #-2]	; r4 is the immediate value of SVC
				
				CMP r4, #67
				BEQ movePriviledge
				; test other immediate values
				; CMP r4, ....
				B .
				
movePriviledge	; only for SVC 67
				MRS r8, CONTROL
				BIC r8, r8, #1	;same as AND r8, r8, #0xfffffffe
				MSR CONTROL, r8			
					
                BX LR
                ENDP
DebugMon_Handler\
                PROC
                EXPORT  DebugMon_Handler          [WEAK]
                B       .
                ENDP
PendSV_Handler  PROC
                EXPORT  PendSV_Handler            [WEAK]
                B       .
                ENDP
SysTick_Handler PROC
                EXPORT  SysTick_Handler           [WEAK]
                
				SUB r4, r4, #1
				BX LR
                ENDP

Default_Handler PROC

                EXPORT  WDT_IRQHandler            [WEAK]
                EXPORT  TIMER0_IRQHandler         [WEAK]
                EXPORT  TIMER1_IRQHandler         [WEAK]
                EXPORT  TIMER2_IRQHandler         [WEAK]
                EXPORT  TIMER3_IRQHandler         [WEAK]
                EXPORT  UART0_IRQHandler          [WEAK]
                EXPORT  UART1_IRQHandler          [WEAK]
                EXPORT  UART2_IRQHandler          [WEAK]
                EXPORT  UART3_IRQHandler          [WEAK]
                EXPORT  PWM1_IRQHandler           [WEAK]
                EXPORT  I2C0_IRQHandler           [WEAK]
                EXPORT  I2C1_IRQHandler           [WEAK]
                EXPORT  I2C2_IRQHandler           [WEAK]
                EXPORT  SPI_IRQHandler            [WEAK]
                EXPORT  SSP0_IRQHandler           [WEAK]
                EXPORT  SSP1_IRQHandler           [WEAK]
                EXPORT  PLL0_IRQHandler           [WEAK]
                EXPORT  RTC_IRQHandler            [WEAK]
                EXPORT  EINT0_IRQHandler          [WEAK]
                EXPORT  EINT1_IRQHandler          [WEAK]
                EXPORT  EINT2_IRQHandler          [WEAK]
                EXPORT  EINT3_IRQHandler          [WEAK]
                EXPORT  ADC_IRQHandler            [WEAK]
                EXPORT  BOD_IRQHandler            [WEAK]
                EXPORT  USB_IRQHandler            [WEAK]
                EXPORT  CAN_IRQHandler            [WEAK]
                EXPORT  DMA_IRQHandler            [WEAK]
                EXPORT  I2S_IRQHandler            [WEAK]
                EXPORT  ENET_IRQHandler           [WEAK]
                EXPORT  RIT_IRQHandler            [WEAK]
                EXPORT  MCPWM_IRQHandler          [WEAK]
                EXPORT  QEI_IRQHandler            [WEAK]
                EXPORT  PLL1_IRQHandler           [WEAK]
                EXPORT  USBActivity_IRQHandler    [WEAK]
                EXPORT  CANActivity_IRQHandler    [WEAK]

WDT_IRQHandler
TIMER0_IRQHandler
TIMER1_IRQHandler
TIMER2_IRQHandler
TIMER3_IRQHandler
UART0_IRQHandler
UART1_IRQHandler
UART2_IRQHandler
UART3_IRQHandler
PWM1_IRQHandler
I2C0_IRQHandler
I2C1_IRQHandler
I2C2_IRQHandler
SPI_IRQHandler
SSP0_IRQHandler
SSP1_IRQHandler
PLL0_IRQHandler
RTC_IRQHandler
EINT0_IRQHandler
EINT1_IRQHandler
EINT2_IRQHandler
EINT3_IRQHandler
ADC_IRQHandler
BOD_IRQHandler
USB_IRQHandler
CAN_IRQHandler
DMA_IRQHandler
I2S_IRQHandler
ENET_IRQHandler
RIT_IRQHandler
MCPWM_IRQHandler
QEI_IRQHandler
PLL1_IRQHandler
USBActivity_IRQHandler
CANActivity_IRQHandler

                B       .

                ENDP


                ALIGN


; User Initial Stack & Heap

                IF      :DEF:__MICROLIB

                EXPORT  __initial_sp
                EXPORT  __heap_base
                EXPORT  __heap_limit

                ELSE

                IMPORT  __use_two_region_memory
                EXPORT  __user_initial_stackheap
__user_initial_stackheap

                LDR     R0, =  Heap_Mem
                LDR     R1, =(Stack_Mem + Stack_Size)
                LDR     R2, = (Heap_Mem +  Heap_Size)
                LDR     R3, = Stack_Mem
                BX      LR

                ALIGN

                ENDIF


                END
					; literal pool is saved here
