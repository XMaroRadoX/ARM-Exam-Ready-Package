#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
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

static uint32_t algorithm_algorithm_pat_alg_bitfield_001_assembly_mask(uint32_t width);

uint32_t algorithm_algorithm_pat_alg_bitfield_001_assembly(uint32_t word, uint32_t value, uint32_t shift,
                              uint32_t width);

uint32_t algorithm_algorithm_pat_alg_bitfield_001_assembly_extract(uint32_t word, uint32_t shift,
                                      uint32_t width);

uint32_t algorithm_algorithm_pat_alg_bitfield_001_assembly_pack_u16(uint16_t high, uint16_t low);



static int pattern_core_vector(void) {
  return algorithm_algorithm_pat_alg_bitfield_001_assembly(0, 3, 4, 2) == 0x30u;
}
static int pattern_edge_vectors(void) {
  return algorithm_algorithm_pat_alg_bitfield_001_assembly(UINT32_MAX, 0, 8, 8) == UINT32_C(0xffff00ff) &&
         algorithm_algorithm_pat_alg_bitfield_001_assembly_extract(UINT32_C(0x12345678), 8, 8) == 0x56 &&
         algorithm_algorithm_pat_alg_bitfield_001_assembly_pack_u16(0x1234, 0x5678) ==
             UINT32_C(0x12345678) &&
         algorithm_algorithm_pat_alg_bitfield_001_assembly(7, 0, 31, 2) == 7;
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
