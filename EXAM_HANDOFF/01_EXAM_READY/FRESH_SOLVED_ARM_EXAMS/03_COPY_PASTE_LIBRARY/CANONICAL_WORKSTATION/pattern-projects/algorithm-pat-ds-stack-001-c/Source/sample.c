#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Array-backed stack.
 * Recognition cue: bounded LIFO push pop.
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
int algorithm_algorithm_pat_ds_stack_001_c(int32_t *a, uint32_t cap, uint32_t *top, int push,
                     int32_t *value);



static int pattern_core_vector(void) {
  int32_t a[2], v = 7, o = 0;
  uint32_t top = 0;
  return algorithm_algorithm_pat_ds_stack_001_c(a, 2, &top, 1, &v) &&
         algorithm_algorithm_pat_ds_stack_001_c(a, 2, &top, 0, &o) && o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t guarded[1]={7},v_bad=9;uint32_t top_bad=2;if(algorithm_algorithm_pat_ds_stack_001_c(guarded,1,&top_bad,0,&v_bad)||v_bad!=9) return 0;
  int32_t a[1], v = 1, o = 0;
  uint32_t top = 0;
  return !algorithm_algorithm_pat_ds_stack_001_c(a, 1, &top, 0, &o) &&
         algorithm_algorithm_pat_ds_stack_001_c(a, 1, &top, 1, &v) &&
         !algorithm_algorithm_pat_ds_stack_001_c(a, 1, &top, 1, &v) &&
         algorithm_algorithm_pat_ds_stack_001_c(a, 1, &top, 0, &o) && o == 1;
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
