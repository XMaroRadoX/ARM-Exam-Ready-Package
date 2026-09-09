/* Q3: complete game, using the Q1 assembly function.
 * Copy to Source/sample.c in a WORKING template.
 * Timer0 and RIT handlers are included here. Use both accompanying IRQ
 * replacement files so the linker sees exactly one owner per handler.
 */
#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t nextElementLCG(uint32_t previous, uint32_t a,
                               uint32_t c, uint32_t n, uint32_t m);

/* Persistent sequence state. n is the NEXT index, from 0 through 9. */
static uint32_t previous = 1u;
static uint32_t n = 0u;

/* 1 accepts one answer; 0 ignores answers until the next round. */
static volatile uint32_t waiting_for_move = 0u;
static volatile uint32_t expected_direction = 0u;
volatile uint32_t num_correct = 0u;
volatile uint32_t num_wrong = 0u;

/* Used to distinguish a new press from a direction being held. */
static uint32_t old_joystick = 0u;

/* remainder 0/1/2/3 -> LED 11/10/9/8 -> UP/LEFT/RIGHT/DOWN. */
static const uint32_t directions[4] = {
    EXAM_JOY_UP, EXAM_JOY_LEFT, EXAM_JOY_RIGHT, EXAM_JOY_DOWN
};

/* Called every three seconds by Timer0. */
void game_next_round(void)
{
    uint32_t value;
    uint32_t remainder;

    waiting_for_move = 0u;                /* Close the old response window. */
    exam_led_clear();                     /* Also clear an unanswered LED. */

    /* The tenth LED has already had its FULL three-second window.
     * This is timer interrupt 11, but it does NOT call the LCG.
     */
    if (n == 10u) {
        exam_timer_stop(EXAM_TIMER0);
        exam_rit_stop();
        if (num_correct > num_wrong) {
            exam_led_on(4u);              /* Victory. */
        } else {
            exam_led_on(5u);              /* Defeat, including a tie. */
        }
        return;
    }

    value = nextElementLCG(previous, 131u, 7u, n, 255u);
    previous = value;                     /* Input for the next generation. */
    remainder = value % 4u;
    expected_direction = directions[remainder];
    exam_led_on((uint8_t)(11u - remainder));
    waiting_for_move = 1u;                /* Allow precisely one response. */
    n++;
}

/* Called every 10 ms by RIT; this is input sampling, not a new round. */
void game_poll_joystick(void)
{
    uint32_t current;
    uint32_t pressed;

    /* Ignore centre/select; retain only the four directional inputs. */
    current = exam_joystick_read()
            & (EXAM_JOY_UP | EXAM_JOY_LEFT | EXAM_JOY_RIGHT | EXAM_JOY_DOWN);
    pressed = exam_joystick_pressed_edges(old_joystick, current);

    /* Update even when answers are disabled. A held direction must not
     * become a new answer just because the next round has started.
     */
    old_joystick = current;
    if (waiting_for_move == 0u || pressed == 0u) {
        return;
    }

    waiting_for_move = 0u;                /* First movement consumes answer. */
    if (pressed == expected_direction) {
        num_correct++;
    } else {
        num_wrong++;
    }
    exam_led_clear();                     /* Correct OR wrong: LED goes off. */
}

void TIMER0_IRQHandler(void)
{
    uint32_t pending = exam_timer_ack(EXAM_TIMER0);
    if ((pending & 1u) != 0u) {            /* MR0 is our 3-second interval. */
        game_next_round();
    }
}

void RIT_IRQHandler(void)
{
    exam_rit_ack();                       /* Acknowledge before sampling. */
    game_poll_joystick();
}

int main(void)
{
    exam_init();
    exam_led_clear();
    exam_joystick_init();
    old_joystick = exam_joystick_read()
                 & (EXAM_JOY_UP | EXAM_JOY_LEFT
                    | EXAM_JOY_RIGHT | EXAM_JOY_DOWN);

    if (exam_timer_config_ms(EXAM_TIMER0, 3000u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { }
    }
    if (exam_rit_config_ms(10u) != EXAM_OK) {
        while (1) { }
    }

    /* Equal priorities serialize the two handlers' shared-state updates.
     * volatile alone would NOT prevent one handler preempting the other.
     */
    NVIC_SetPriority(TIMER0_IRQn, 0u);
    NVIC_SetPriority(RIT_IRQn, 0u);
    exam_rit_start();
    exam_timer_start(EXAM_TIMER0);
    while (1) {
        __WFI();
    }
}
