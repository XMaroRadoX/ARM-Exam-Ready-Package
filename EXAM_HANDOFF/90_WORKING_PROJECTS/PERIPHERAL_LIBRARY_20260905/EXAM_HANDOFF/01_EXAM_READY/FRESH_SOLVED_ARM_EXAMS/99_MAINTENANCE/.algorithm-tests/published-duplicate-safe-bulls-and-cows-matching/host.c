#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Consume-once duplicate-safe matching.
 * Recognition cue: Bulls and Cows Mastermind duplicate-safe match.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
uint32_t algorithm_duplicate_safe_bulls_and_cows_matching(const uint8_t *secret,
                                                          const uint8_t *guess,
                                                          uint32_t n, uint32_t *cows) {
  uint8_t used_s[32] = {0}, used_g[32] = {0};
  uint32_t i, j, b = 0, c = 0;
  if (!secret || !guess || !cows || n > 32)
    return 0;
  for (i = 0; i < n; i++)
    if (secret[i] == guess[i]) {
      used_s[i] = used_g[i] = 1;
      b++;
    }
  for (i = 0; i < n; i++)
    if (!used_g[i])
      for (j = 0; j < n; j++)
        if (!used_s[j] && guess[i] == secret[j]) {
          used_g[i] = used_s[j] = 1;
          c++;
          break;
        }
  *cows = c;
  return b;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


/*
 * Exam-study reference: Consume-once duplicate-safe matching.
 * Recognition cue: Bulls and Cows Mastermind duplicate-safe match.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
uint32_t algorithm_duplicate_safe_bulls_and_cows_matching(const uint8_t *secret,
                                                          const uint8_t *guess,
                                                          uint32_t n, uint32_t *cows);

static int pattern_core_vector(void) {
  uint8_t s[] = {1, 1, 2, 3}, g[] = {1, 2, 1, 4};
  uint32_t c = 0;
  return algorithm_duplicate_safe_bulls_and_cows_matching(s, g, 4, &c) == 1 && c == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {1}, b[] = {2};
  uint32_t c = 9;
  return algorithm_duplicate_safe_bulls_and_cows_matching(a, b, 0, &c) == 0 && c == 0 &&
         algorithm_duplicate_safe_bulls_and_cows_matching(a, b, 1, &c) == 0 && c == 0 &&
         algorithm_duplicate_safe_bulls_and_cows_matching(a, b, 33, &c) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

int main(void){return test_main();}
