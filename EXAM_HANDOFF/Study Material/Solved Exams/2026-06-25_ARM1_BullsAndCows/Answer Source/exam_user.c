#include "exam_user.h"

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
  uint32_t timer_value = exam_timer_count(1u);
  uint32_t i;
  for (i = 0u; i < 4u; ++i) {
    secret[i] = (int)((timer_value >> (i * 4u)) & 0x3u);
  }
}

static void begin_guess(void)
{
  clear_words(guess);
  exam_leds_off();
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

void exam_user_init(void)
{
  exam_status_t timer_status;
  exam_status_t joystick_status;

  clear_words(guess);
  clear_words(secret);
  clear_words(guessFrequency);
  clear_words(secretFrequency);
  joystick_press_edges = 0u;
  game_state = WAIT_START;
  exam_leds_off();

  timer_status = exam_timer_prescaler(1u, 0u);
  if (timer_status == EXAM_OK) timer_status = exam_timer_reset(1u);
  if (timer_status == EXAM_OK) timer_status = exam_timer_start(1u);
  joystick_status = exam_joystick_start(exam_joystick_event);

  if (timer_status != EXAM_OK || joystick_status != EXAM_OK) {
    (void)exam_led_write(0xFFu);
    game_state = FINISHED;
  }
}

void exam_user_loop(void)
{
  uint32_t edges;
  uint32_t saved;

  if ((exam_events_take(EXAM_EVENT_JOYSTICK) & EXAM_EVENT_JOYSTICK) == 0u) return;

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
    return;
  }

  if (game_state != EDIT_GUESS) return;
  if ((edges & EXAM_JOY_DOWN) != 0u) increment_digit(0u);
  if ((edges & EXAM_JOY_LEFT) != 0u) increment_digit(1u);
  if ((edges & EXAM_JOY_RIGHT) != 0u) increment_digit(2u);
  if ((edges & EXAM_JOY_UP) != 0u) increment_digit(3u);
}

void exam_joystick_event(uint32_t current, uint32_t changed)
{
  joystick_press_edges |= current & changed;
  exam_events_set(EXAM_EVENT_JOYSTICK);
}

void exam_button_event(exam_button_t button, exam_button_event_t event)
{
  (void)button;
  (void)event;
}

void exam_timer_event(uint8_t timer, uint32_t flags)
{
  (void)timer;
  (void)flags;
}

void exam_user_10ms_hook(void)
{
}
