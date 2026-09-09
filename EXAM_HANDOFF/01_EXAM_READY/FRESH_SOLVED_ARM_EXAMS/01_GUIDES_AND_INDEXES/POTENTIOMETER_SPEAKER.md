# Potentiometer-controlled speaker

[Back to peripheral lessons](PERIPHERALS_CANONICAL.md#lesson-11-dac--speaker)

## What this example does

Turn the potentiometer to select a low, medium, or high square-wave tone.
This is a teaching example, not an answer to a specific exam paper.

A potentiometer is an adjustable resistor used on the board to supply an
adjustable voltage. Turning its knob changes the voltage presented to ADC
channel 5 on P1.31. The ADC converts that voltage into a number from 0 to 4095.
The program uses that number to choose the pitch; it does not send the ADC
reading directly to the speaker.

Timer0 alternates the DAC output on P0.26 between 400 and 624. These values
are within the DAC's 0..1023 range and make a moderate swing around midscale.
The connected speaker circuit turns the changing signal into sound. A constant
DAC value alone does not produce a sustained tone.

| ADC reading | Timer updates per second | Tone frequency |
|---|---:|---:|
| 0..1364 | 500 | 250 Hz |
| 1365..2729 | 1000 | 500 Hz |
| 2730..4095 | 2000 | 1000 Hz |

Each cycle needs two updates: low to high, then high to low. Therefore:

```text
Tone frequency = timer update frequency / 2
```

## Where to write the code

Copy [Official Combined Exam API](../../02_STARTING_TEMPLATES/Official%20Combined%20Exam%20API/)
into [90_WORKING_PROJECTS](../../../90_WORKING_PROJECTS/) and open the copy's
`sample.uvprojx` in Keil. Use a fresh copy for this example.

The three files below belong to that same copied project. Keep exactly one
definition of each interrupt handler. This example does not need RIT,
SysTick, button setup, or software events.

### 1. Source/sample.c

Replace its contents with:

```c
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
    uint16_t knob;
    uint32_t update_rate;
    uint32_t previous_rate = 0;

    exam_init();
    exam_adc_init();
    exam_dac_init();

    /* Initial DAC output level. */
    exam_dac_write(400);

    /* Request the first potentiometer measurement. */
    exam_adc_start();

    while (1)
    {
        if (exam_adc_take(&knob) != 0)
        {
            if (knob < 1365)
            {
                update_rate = 500;
            }
            else if (knob < 2730)
            {
                update_rate = 1000;
            }
            else
            {
                update_rate = 2000;
            }

            /* Change the timer only when the selected pitch changes. */
            if (update_rate != previous_rate)
            {
                if (exam_timer_config_hz(
                        EXAM_TIMER0,
                        update_rate,
                        EXAM_TIMER_PERIODIC) == EXAM_OK)
                {
                    exam_timer_start(EXAM_TIMER0);
                    previous_rate = update_rate;
                }
            }

            /* Start another measurement after collecting this one. */
            exam_adc_start();
        }
    }
}
```

### 2. Source/adc/IRQ_adc.c

The starting template already provides this handler. Keep it:

```c
#include "LPC17xx.h"
#include "adc.h"
#include "exam_api.h"

void ADC_IRQHandler(void)
{
    exam_adc_irq_capture();
}
```

### 3. Source/timer/IRQ_timer.c

Keep the existing includes and other timer handlers. Replace only the existing
`TIMER0_IRQHandler` with:

```c
void TIMER0_IRQHandler(void)
{
    static uint32_t high = 0;
    uint32_t pending;

    pending = exam_timer_ack(EXAM_TIMER0);

    if (exam_timer_match_happened(pending, 0))
    {
        if (high == 0)
        {
            exam_dac_write(624);
            high = 1;
        }
        else
        {
            exam_dac_write(400);
            high = 0;
        }
    }
}
```

## How the functions cooperate

| Function or variable | Purpose |
|---|---|
| `exam_adc_init()` | Prepare the potentiometer ADC input and its interrupt. |
| `exam_adc_start()` | Request one conversion; it does not wait for the result. |
| `exam_adc_irq_capture()` | Save the completed reading and mark it fresh. |
| `exam_adc_take(&knob)` | Copy a fresh reading into `knob`; return 1 when available, otherwise 0. |
| `&knob` | The address where the helper should put the measurement. |
| `exam_dac_init()` | Prepare DAC output P0.26 and initialize its output. |
| `exam_dac_write(...)` | Set the output level; retain it until the next write. |
| `exam_timer_config_hz(...)` | Configure the number of Timer0 interval interrupts per second. Stops/resets the timer during configuration. |
| `EXAM_OK` | Successful configuration; start the timer only after this result. |
| `previous_rate` | Avoid repeatedly resetting Timer0 while the knob stays in one pitch range. |
| `exam_timer_ack(...)` | Snapshot and clear pending Timer0 flags. |
| `exam_timer_match_happened(pending, 0)` | Test whether the saved flags contain the MR0 interval event. |
| `static uint32_t high` | Remember the selected output level between handler calls. |

```text
Knob movement -> ADC measurement -> main chooses update rate
                                      |
                                      v
Timer0 interrupts -> alternate DAC levels -> speaker circuit -> tone
```

Only one conversion is requested at a time: the next starts after the previous
result is collected. The ADC stores a latest result, not a queue. The fast main
loop does not determine the audio timing; Timer0 does.

## Check in Keil and on the board

1. Build the copied project and resolve any build errors before running.
2. Inspect `knob` and `update_rate` at a breakpoint after pitch selection.
3. Try readings around 0, 2048, and 4095. Expect update rates 500, 1000, and 2000.
4. Confirm the board's DAC-to-speaker connection and any required enable/jumper
   arrangement. Simulator variables alone do not prove physical sound output.
5. Run without repeatedly stopping the processor to assess tone timing.

Small ADC fluctuations near 1365 or 2730 can switch adjacent pitches. This
simple example has no boundary hysteresis; move the knob clearly into a range
while learning. A pitch change can also produce a transition click.

To stop the tone from foreground code:

```c
exam_timer_stop(EXAM_TIMER0);
exam_dac_write(512);
```

The code has been checked against the maintained API source. Native Keil
compilation and physical speaker operation have not been verified for this
example. Timer frequencies are nominal and depend on the configured clock.

## Related reference

- [ADC result collection](PORTAL/api/exam-adc-take.html)
- [Timer frequency configuration](PORTAL/api/exam-timer-config-hz.html)
- [DAC output](PORTAL/api/exam-dac-write.html)
- [Professor's speaker waveform handler](../../../03_ADDITIONAL_STUDY_MATERIAL/04%20-%20Reference/Professor%20Demos%20and%20Legacy%20Combined%20Template/Professor%20Demos/11_sample_LOUDSPEAKER/Source/timer/IRQ_timer.c)

The professor's demo writes a 45-sample sine table and uses the potentiometer
to select the timer interval. This example uses two square-wave levels so the
timing relationship is easier to follow.
