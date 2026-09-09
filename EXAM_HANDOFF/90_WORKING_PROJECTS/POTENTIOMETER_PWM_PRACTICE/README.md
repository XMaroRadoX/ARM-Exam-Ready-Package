# Potentiometer-controlled LED brightness

Open `sample.uvprojx` from this practice folder and rebuild before debugging.
This is a separate copy of the Official Combined Exam API template. Only
`Source/sample.c` is changed. The existing `Source/adc/IRQ_adc.c` owns
`ADC_IRQHandler` and already calls `exam_adc_irq_capture()`.

The potentiometer supplies ADC channel 5 on P1.31. LED11 is on P2.0,
which can output PWM1.1. The template has no PWM helper, so this exercise
uses the existing ADC API and direct PWM registers. No PWM interrupt is needed.

At the template's configured clock, the prescaler produces one count per
microsecond. MR0=1000 gives approximately 1 kHz PWM. MR1 controls the high
time: 0 is off, 500 is half duty, and 1000 is full duty. LER requests that
the new match value be applied at a cycle boundary. Clock division assumes
SystemFrequency is a multiple of 1 MHz, as in the supplied configuration.

The foreground loop takes each completed ADC reading, scales 0..4095 to
0..1000, updates MR1, and starts another conversion. It intentionally polls
without WFI. Hardware PWM continues independently while the CPU runs.
Do not use GPIO LED helpers on LED11 after assigning that pin to PWM.

## Try it

1. Watch `knob_value`, `pwm_on_ticks`, and PWM1 MR0/MR1 in the debugger.
2. Turn the physical knob: LED11 should change brightness.
3. At an ADC reading of 0 expect 0 ticks; 2048 gives 500; 4095 gives 1000.
4. Numeric duty is linear; perceived brightness need not look linear.
5. Simulator ADC input support and visible LED dimming are separate from
   compilation. A physical board is needed to confirm the visual result.

## Explain before looking at the solution

- Why does changing MR1 change brightness without changing MR0?
- Why multiply the ADC reading by 1000 before dividing by 4095?
- Which file handles ADC completion, and why is there only one handler?
- Predict the result for an ADC reading of 1024.

Hardware reference: NXP UM10360, chapters on pin selection and PWM1;
https://www.nxp.com/docs/en/user-guide/UM10360.pdf
