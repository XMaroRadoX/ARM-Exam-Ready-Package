#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"
enum {
  EXAM_EVENT_JOYSTICK = 1u << 1
};

extern int BullsAndCows(int guess[4], int secret[4],
                        int guessFrequency[4], int secretFrequency[4]);

typedef enum {
  WAIT_START = 0,
  EDIT_GUESS,
  SHOW_RESULT,
  FINISHED
} game_state_t;

static int guess[4];
static int secret[4];
static int guessFrequency[4];
static int secretFrequency[4];
static volatile uint32_t joystick_press_edges;
static uint32_t previous_joystick;
static uint32_t candidate_joystick;
static uint32_t stable_samples;
static game_state_t game_state;

static void clear_words(int values[4])
{
  uint32_t i;
  for (i = 0u; i < 4u; ++i) values[i] = 0;
}

static void display_guess(void)
{
  uint8_t packed = (uint8_t)(((uint32_t)guess[0] << 0) |
                             ((uint32_t)guess[1] << 2) |
                             ((uint32_t)guess[2] << 4) |
                             ((uint32_t)guess[3] << 6));
  (void)exam_led_write(packed);
}

static void capture_secret(void)
{
  uint32_t timer_value = exam_timer_read(EXAM_TIMER1);
  uint32_t i;
  for (i = 0u; i < 4u; ++i) {
    secret[i] = (int)((timer_value >> (i * 4u)) & 0x3u);
  }
}

static void begin_guess(void)
{
  clear_words(guess);
  exam_led_clear();
  display_guess();
  game_state = EDIT_GUESS;
}

static void increment_digit(uint32_t index)
{
  guess[index] = (guess[index] + 1) & 0x3;
  display_guess();
}

static void evaluate_guess(void)
{
  int result;
  clear_words(guessFrequency);
  clear_words(secretFrequency);
  result = BullsAndCows(guess, secret, guessFrequency, secretFrequency);
  (void)exam_led_write((uint8_t)result);
  game_state = ((((uint32_t)result >> 4) & 0xFu) == 0xFu) ? FINISHED : SHOW_RESULT;
}

void RIT_IRQHandler(void)
{
  uint32_t current;
  uint32_t pressed;
  exam_rit_ack();
  current=exam_joystick_read();
  if (current != candidate_joystick) {
    candidate_joystick = current; stable_samples = 1u; return;
  }
  if (stable_samples < 3u) ++stable_samples;
  if (stable_samples < 3u) return;
  pressed=exam_joystick_pressed_edges(previous_joystick,current);
  previous_joystick=current;
  if(pressed!=0u){joystick_press_edges|=pressed;exam_events_set(EXAM_EVENT_JOYSTICK);}
}

int main(void)
{
  exam_status_t timer_status;
  exam_status_t joystick_status;
  exam_init();

  clear_words(guess);
  clear_words(secret);
  clear_words(guessFrequency);
  clear_words(secretFrequency);
  joystick_press_edges = 0u;
  game_state = WAIT_START;
  exam_led_clear();

  timer_status=exam_timer_config_ticks(EXAM_TIMER1,UINT32_MAX,
                                       EXAM_TIMER_MODULO_NO_IRQ);
  if(timer_status==EXAM_OK)exam_timer_start(EXAM_TIMER1);
  exam_joystick_init();
  previous_joystick=exam_joystick_read();
  candidate_joystick=previous_joystick;
  stable_samples=3u;
  joystick_status=exam_rit_config_ms(10u);
  if(joystick_status==EXAM_OK)exam_rit_start();

  if (timer_status != EXAM_OK || joystick_status != EXAM_OK) {
    (void)exam_led_write(0xFFu);
    game_state = FINISHED;
  }

  for (;;) {
    uint32_t edges;
    uint32_t saved;

    if ((exam_events_take(EXAM_EVENT_JOYSTICK) & EXAM_EVENT_JOYSTICK) == 0u) {
      __WFI();
      continue;
    }

    saved = exam_critical_enter();
    edges = joystick_press_edges;
    joystick_press_edges = 0u;
    exam_critical_exit(saved);

    if ((edges & EXAM_JOY_SELECT) != 0u) {
      if (game_state == WAIT_START) {
        capture_secret();
        begin_guess();
      } else if (game_state == EDIT_GUESS) {
        evaluate_guess();
      } else if (game_state == SHOW_RESULT) {
        begin_guess();
      }
      __WFI();
      continue;
    }

    if (game_state != EDIT_GUESS) {
      __WFI();
      continue;
    }
    if ((edges & EXAM_JOY_DOWN) != 0u) increment_digit(0u);
    if ((edges & EXAM_JOY_LEFT) != 0u) increment_digit(1u);
    if ((edges & EXAM_JOY_RIGHT) != 0u) increment_digit(2u);
    if ((edges & EXAM_JOY_UP) != 0u) increment_digit(3u);
    __WFI();
  }
}
