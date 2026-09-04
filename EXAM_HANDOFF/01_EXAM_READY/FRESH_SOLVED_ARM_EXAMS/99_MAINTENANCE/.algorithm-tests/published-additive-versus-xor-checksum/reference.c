#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Checksums and CRC table structure.
 * Recognition cue: xor additive checksum table driven crc.
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

uint32_t algorithm_additive_versus_xor_checksum(const uint8_t *bytes, uint32_t count) {
  uint32_t xor_checksum = 0u;
  uint32_t additive_checksum = 0u;

  if ((bytes == NULL) && (count != 0u)) {
    return 0u;
  }
  while (count != 0u) {
    xor_checksum ^= *bytes;
    additive_checksum += *bytes;
    ++bytes;
    --count;
  }
  return (xor_checksum << 16u) | (additive_checksum & UINT32_C(0xFFFF));
}

uint32_t algorithm_additive_versus_xor_checksum_crc32_table(const uint8_t *bytes,
                                                            uint32_t count,
                                                            const uint32_t table[256]) {
  uint32_t crc = UINT32_MAX;

  if ((table == NULL) || ((bytes == NULL) && (count != 0u))) {
    return 0u;
  }
  while (count != 0u) {
    uint8_t index = (uint8_t)(crc ^ *bytes);
    crc = (crc >> 8u) ^ table[index];
    ++bytes;
    --count;
  }
  return crc ^ UINT32_MAX;
}
