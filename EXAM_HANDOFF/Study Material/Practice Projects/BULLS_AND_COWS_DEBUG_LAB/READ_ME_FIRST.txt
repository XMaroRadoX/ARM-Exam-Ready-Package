ULTIMATE CA EXAM TEMPLATE v2
============================

OPEN THIS PROJECT
  Ultimate_CA_Template_v2.uvprojx

USE ONE TARGET
  The project contains one target: CA Exam.

NORMAL WORKFLOW
  1. Edit Source\exam\exam_user.c for C.
  2. Edit Source\exam\exam_asm.s for ARM assembly.
  3. Build the same CA Exam target.
  4. Fix the first error before reading later errors.

YOU DO NOT CHOOSE BETWEEN DIFFERENT ANSWER TYPES
  Checked exam_* functions, familiar course function names, direct LPC1768
  registers, callbacks, exact interrupt handlers, SVC work, and self-tests
  are all available in the same project.

PERIPHERALS ARE OPT-IN
  Startup configures the clock, LEDs and fault support only. A button, RIT,
  joystick, timer, ADC or DAC is enabled only when your answer requests it.
  Foreground polling remains active; WFI sleep is off unless you explicitly
  set CA_IDLE_USE_WFI to 1.

WHERE STARTUP.S IS
  Source\startup_LPC17xx.s is included under 90 - INTERNAL - DO NOT EDIT.
  It contains the vector table, the default weak handlers and a 4 KB stack.
  Leave it unchanged in a normal answer. Large arrays should still be static
  or global instead of ordinary local variables.

WHEN THE PAPER NAMES RESET_HANDLER
  Define Reset_Handler in Source\exam\exam_asm.s. The supplied startup
  handler is weak, so your definition replaces it without editing startup.
  Finish the required initialization and then branch to __main. Do not use
  BX LR from Reset_Handler.

WHEN THE QUESTION REQUIRES AN EXACT HANDLER
  Open Source\platform\exam_config.h and set only the matching
  EXAM_OWN_*_HANDLER switch to 1. Then write that handler in exam_user.c.
  This prevents two files from defining the same vector.
  For an exact external button handler, call exam_button_irq_start() once in
  exam_user_init() to configure and enable only that EINT vector.
  A callback helper and an exact handler cannot own the same vector. In that
  conflict the helper returns EXAM_BUSY; other peripherals remain available.

IMPORTANT RAW-MODE RULES
  Confirmed buttons and joystick callbacks use the normal 10 ms RIT service.
  Do not use them while owning RIT_IRQHandler or using direct RIT mode.
  The cached exam_pot_* and exam_adc_read functions use the built-in ADC
  handler. If you own ADC_IRQHandler, read and decode LPC_ADC->ADGDR yourself.
  If you own TIMERn_IRQHandler, configure that timer and clear its IR flags in
  your handler; callback helpers for the other timers still work normally.

BOARD REMINDERS
  LEDs: printed numbers 4..11.
  External buttons: INT0, KEY1 and KEY2 are active-low.
  Potentiometer: fit JP12.
  Speaker/analog output: fit JP2.

READ NEXT
  Documentation\FIVE_MINUTE_CHECKLIST.md
  Documentation\PERIPHERAL_RECIPES.md
  Documentation\EXAM_WORKFLOW.md
  Documentation\TEMPLATE_GUIDE.md
  Documentation\API_REFERENCE.md
