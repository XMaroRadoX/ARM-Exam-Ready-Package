# Five-minute exam checklist

## Before writing code

- Open `ARM_Exam_Template.uvprojx` and keep the single `ARM Exam` target.
- Rebuild the untouched template. Require zero errors and zero warnings.
- Underline every required C function, assembly function, peripheral, timer
  number, period, interrupt name, signed value and return value.
- Write down which work happens once, repeatedly, or inside an interrupt.
- Claim only the resources named by the question.

## While writing

- Edit `1_WRITE_C_HERE.c` and `2_WRITE_ASM_HERE.s` only.
- Put setup in `exam_user_init()` and repeated foreground work in
  `exam_user_loop()`.
- Keep interrupt work short. Clear the hardware flag and use `volatile` data
  or an event bit to notify the foreground loop.
- When the paper names an exact vector, enable only its `EXAM_OWN_*_HANDLER`
  switch. Do not enable ownership switches just because a peripheral is used.
- Preserve `R4-R11`, save `LR` before nested assembly calls, and keep SP
  eight-byte aligned at public call boundaries.
- Use static/global storage for large arrays. The project stack is 4 KB, but
  it is for calls, local working values and exception frames—not large tables.

## Before submitting

- Rebuild, not only Build. Require zero errors and zero warnings.
- Confirm every exact handler clears its W1C pending flag.
- Confirm every interrupt-shared variable is `volatile` or protected.
- Confirm timer PCLK, `PR+1`, MR value and reset/stop action match the paper.
- Confirm no long loop, wait or debounce delay is inside an interrupt.
- Fit JP12 for the potentiometer and JP2 for analog/speaker output.
- Test the real board when available; a successful compile does not verify
  jumpers, button wiring, timing or analog output.
