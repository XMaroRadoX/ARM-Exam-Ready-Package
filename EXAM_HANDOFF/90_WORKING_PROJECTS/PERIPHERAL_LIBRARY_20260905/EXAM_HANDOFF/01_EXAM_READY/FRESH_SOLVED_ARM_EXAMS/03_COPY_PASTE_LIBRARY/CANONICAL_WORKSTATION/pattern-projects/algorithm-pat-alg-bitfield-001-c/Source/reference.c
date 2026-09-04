#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bitfield extraction insertion and packing.
 * Recognition cue: mask shift pack unpack field.
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

static uint32_t algorithm_algorithm_pat_alg_bitfield_001_c_mask(uint32_t width) {
  if (width == 0u) {
    return 0u;
  }
  return (width >= 32u) ? UINT32_MAX : (UINT32_C(1) << width) - 1u;
}

uint32_t algorithm_algorithm_pat_alg_bitfield_001_c(uint32_t word, uint32_t value, uint32_t shift,
                              uint32_t width) {
  uint32_t field_mask;

  if ((width == 0u) || (shift >= 32u) || (width > 32u - shift)) {
    return word;
  }
  field_mask = algorithm_algorithm_pat_alg_bitfield_001_c_mask(width) << shift;
  return (word & ~field_mask) | ((value << shift) & field_mask);
}

uint32_t algorithm_algorithm_pat_alg_bitfield_001_c_extract(uint32_t word, uint32_t shift,
                                      uint32_t width) {
  if ((width == 0u) || (shift >= 32u) || (width > 32u - shift)) {
    return 0u;
  }
  return (word >> shift) & algorithm_algorithm_pat_alg_bitfield_001_c_mask(width);
}

uint32_t algorithm_algorithm_pat_alg_bitfield_001_c_pack_u16(uint16_t high, uint16_t low) {
  return ((uint32_t)high << 16u) | low;
}

