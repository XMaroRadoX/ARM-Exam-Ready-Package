#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Decimal digit algorithms.
 * Recognition cue: extract reconstruct sum palindrome Kaprekar digits.
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

uint32_t algorithm_kaprekar_digit_ordering_step(uint32_t value) {
  uint32_t digit_sum = 0u;
  uint32_t reversed = 0u;

  do {
    uint32_t digit = value % 10u;
    digit_sum += digit;
    reversed = reversed * 10u + digit;
    value /= 10u;
  } while (value != 0u);
  return (digit_sum << 16u) | (reversed & UINT32_C(0xFFFF));
}

uint32_t algorithm_kaprekar_digit_ordering_step_extract(uint32_t value, uint8_t *digits,
                                                        uint32_t capacity) {
  uint32_t count = 0u;

  if ((digits == NULL) || (capacity == 0u)) {
    return 0u;
  }
  do {
    if (count >= capacity) {
      return 0u;
    }
    digits[count++] = (uint8_t)(value % 10u);
    value /= 10u;
  } while (value != 0u);
  return count;
}

uint32_t algorithm_kaprekar_digit_ordering_step_reconstruct(const uint8_t *digits,
                                                            uint32_t count) {
  uint32_t value = 0u;

  while ((digits != NULL) && (count != 0u)) {
    --count;
    value = value * 10u + digits[count];
  }
  return value;
}

int algorithm_kaprekar_digit_ordering_step_is_palindrome(uint32_t value) {
  uint32_t original = value;
  uint64_t reversed = 0;
  do {
    reversed = reversed * 10u + value % 10u;
    value /= 10u;
  } while (value);
  return reversed == original;
}

uint32_t algorithm_kaprekar_digit_ordering_step_kaprekar_4(uint32_t value) {
  uint8_t digits[4];
  uint32_t ascending;
  uint32_t descending;
  uint32_t outer;
  uint32_t inner;

  for (outer = 0u; outer < 4u; ++outer) {
    digits[outer] = (uint8_t)(value % 10u);
    value /= 10u;
  }
  for (outer = 0u; outer < 4u; ++outer) {
    for (inner = outer + 1u; inner < 4u; ++inner) {
      if (digits[inner] < digits[outer]) {
        uint8_t temporary = digits[outer];
        digits[outer] = digits[inner];
        digits[inner] = temporary;
      }
    }
  }
  ascending = 0u;
  descending = 0u;
  for (outer = 0u; outer < 4u; ++outer) {
    ascending = ascending * 10u + digits[outer];
    descending = descending * 10u + digits[3u - outer];
  }
  return descending - ascending;
}
