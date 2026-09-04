#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Indirect-index recurrence.
 * Recognition cue: Recaman or Hofstadter recurrence indexes earlier terms.
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

uint32_t algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly(uint32_t *output, uint32_t count);

uint32_t algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly_hofstadter_q(uint32_t *output,uint32_t count);



static int pattern_core_vector(void) {
  uint32_t a[4];
  return algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly(a, 4) == 4 && a[0] == 0 && a[1] == 1 &&
         a[2] == 3 && a[3] == 6;
}
static int pattern_edge_vectors(void) {
  uint32_t a[8], q[8];
  return algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly(NULL, 1) == 0 &&
         algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly(a, 1) == 1 && a[0] == 0 &&
         algorithm_algorithm_pat_alg_indirect_recurrence_001_assembly_hofstadter_q(q, 6) == 6 && q[5] == 4;
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
