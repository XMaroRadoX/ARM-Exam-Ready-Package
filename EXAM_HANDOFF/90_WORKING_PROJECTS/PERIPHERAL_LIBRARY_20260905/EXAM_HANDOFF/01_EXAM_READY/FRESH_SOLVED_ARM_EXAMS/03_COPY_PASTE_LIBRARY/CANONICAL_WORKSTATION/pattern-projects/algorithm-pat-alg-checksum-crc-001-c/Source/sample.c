#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
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

uint32_t algorithm_algorithm_pat_alg_checksum_crc_001_c(const uint8_t *bytes, uint32_t count);

uint32_t algorithm_algorithm_pat_alg_checksum_crc_001_c_crc32_table(const uint8_t *bytes,
                                              uint32_t count,
                                              const uint32_t table[256]);



static int pattern_core_vector(void) {
  uint8_t a[] = {1, 2};
  return algorithm_algorithm_pat_alg_checksum_crc_001_c(a, 2) == ((3u << 16) | 3u);
}
static int pattern_edge_vectors(void) {
  uint32_t table[256] = {0};
  uint8_t a[] = {1};
  return algorithm_algorithm_pat_alg_checksum_crc_001_c(NULL, 0) == 0 &&
         algorithm_algorithm_pat_alg_checksum_crc_001_c(a, 1) == ((1u << 16) | 1u) &&
         algorithm_algorithm_pat_alg_checksum_crc_001_c_crc32_table(a, 1, table) ==
             UINT32_C(0xff000000) &&
         algorithm_algorithm_pat_alg_checksum_crc_001_c_crc32_table(NULL, 1, table) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}
