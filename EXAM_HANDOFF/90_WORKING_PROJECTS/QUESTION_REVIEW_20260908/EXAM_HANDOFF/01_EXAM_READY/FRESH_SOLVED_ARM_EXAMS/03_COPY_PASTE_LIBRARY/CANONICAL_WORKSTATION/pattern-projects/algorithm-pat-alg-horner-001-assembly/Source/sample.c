#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Horner polynomial evaluation.
 * Recognition cue: evaluate polynomial with multiply accumulate.
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
int64_t algorithm_algorithm_pat_alg_horner_001_assembly(const int32_t *c, uint32_t n, int32_t x);

int algorithm_algorithm_pat_alg_horner_001_assembly_checked(const int32_t *c, uint32_t n, int32_t x, int64_t *out);



static int pattern_core_vector(void) {
  int32_t c[] = {1, 2};
  return algorithm_algorithm_pat_alg_horner_001_assembly(c, 2, 3) == 7;
}
static int pattern_edge_vectors(void) {
  int64_t checked=99;int32_t ok_poly[3]={1,2,3},overflow_poly[4]={0,0,0,INT32_MAX}; if(!algorithm_algorithm_pat_alg_horner_001_assembly_checked(ok_poly,3,2,&checked)||checked!=17)return 0;checked=99;if(algorithm_algorithm_pat_alg_horner_001_assembly_checked(overflow_poly,4,INT32_MAX,&checked)||checked!=99)return 0;
  if(algorithm_algorithm_pat_alg_horner_001_assembly(NULL,3,2)!=0)return 0;
  int32_t c[] = {5};
  return algorithm_algorithm_pat_alg_horner_001_assembly(c, 0, 7) == 0 && algorithm_algorithm_pat_alg_horner_001_assembly(c, 1, 7) == 5;
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
