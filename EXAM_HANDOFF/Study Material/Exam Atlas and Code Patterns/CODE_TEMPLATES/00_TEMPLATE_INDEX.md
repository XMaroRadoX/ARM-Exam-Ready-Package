# Canonical ARM exam template index

All assembly uses Keil/Arm syntax for ARMv7-M Thumb on Cortex-M3. The files are small patterns to copy into the normal answer files; they are not another linked library.

| I need to... | Recommended template | Main concepts | Verification |
|---|---|---|---|
| Write a simple function | `01_aapcs/leaf_function.s` | R0-R3, R0 result, BX LR | Assembled, 0 errors |
| Call another function | `01_aapcs/nonleaf_function.s` | R4/LR save, aligned PUSH/POP | Assembled, 0 errors |
| Read arguments 5-7 | `01_aapcs/five_to_seven_arguments.s` | Original SP, stacked arguments | Assembled, 0 errors |
| Call assembly from C | `01_aapcs/c_calls_assembly/` | Header, prototype, EXPORT | C compiled and ASM assembled separately |
| Scan a word array | `02_algorithms/array_scan_word.s` | Scaled LDR, unsigned comparison | Assembled, not executed |
| Use nested loops and break | `02_algorithms/nested_search_with_break.s` | Outer/inner state, controlled exit | Assembled, not executed |
| Address matrix[row][column] | `02_algorithms/matrix_row_major_byte.s` | row*columns+column, LDRB | Assembled, not executed |
| Read packed matrix bits | `02_algorithms/packed_bit_matrix.s` | MSB-first mask, TST | Assembled, not executed |
| Extract/rebuild decimal digits | `02_algorithms/digit_extract_and_rebuild.s` | UDIV, MLS, MUL | Assembled, not executed |
| Build a sequence in an array | `02_algorithms/recurrence_into_array.s` | Seeds, prior element, bounds | Assembled, not executed |
| Multiply Q15 values | `02_algorithms/fixed_point_recurrence.s` | SMULL, signed 64-bit shift | Assembled, not executed |
| Run a periodic timer | `03_board/periodic_timer.c` | Short callback, event, foreground | Compiled; hardware required |
| Use a free-running timer | `03_board/free_running_timer.c` | Match reset without IRQ | Compiled; hardware required |
| Coordinate three timers | `03_board/multi_timer_state.c` | Ownership, running bits, events | Compiled; hardware required |
| Confirm a button press | `03_board/button_debounce_event.c` | Debounce, press event | Compiled; hardware required |
| Build a joystick state machine | `03_board/joystick_state_machine.c` | Press edges, atomic handoff | Compiled; hardware required |
| Display ADC bits | `03_board/adc_to_leds.c` | 12-to-8-bit shift | Compiled; hardware required |
| Stream DAC samples | `03_board/dac_table_stream.c` | Timer callback, table index | Compiled; hardware required |
| Replace Reset_Handler | `04_rare_dangerous/reset_handler.s` | Strong handler, __main | Assembled; link only when required |
| Decode an SVC | `04_rare_dangerous/svc_handler.s` | MSP/PSP, stacked PC/R0 | Assembled; execution not verified |
| Configure raw SysTick | `04_rare_dangerous/systick_raw.s` | CSR/RVR/CVR, no interrupt | Assembled; hardware required |
| Produce APSR flags | `04_rare_dangerous/apsr_flags.s` | MRS/MSR, NZCV | Assembled; debugger check required |
| Add 64-bit register pairs | `04_rare_dangerous/two_word_arithmetic.s` | ADDS/ADC carry chain | Assembled, not executed |

## Adaptation checks

- Replace every symbol and prototype consistently.
- Recalculate stack-argument offsets after changing the prologue.
- Keep the stack eight-byte aligned before BL.
- Use LDRSB/LDRSH and signed branches for signed data.
- Keep interrupt callbacks bounded and move algorithm work to foreground code.
- Select a direct-register template only when the paper tests those registers.
