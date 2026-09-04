#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Signed min max and sum reduction.
 * Recognition cue: reduce array to minimum maximum and sum.
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

typedef struct {
  int32_t minimum;
  int32_t maximum;
  int64_t sum;
} algorithm_algorithm_pat_alg_reduction_001_assembly_signed_result_t;

typedef struct {
  uint32_t minimum;
  uint32_t maximum;
  uint64_t sum;
} algorithm_algorithm_pat_alg_reduction_001_assembly_unsigned_result_t;

int algorithm_algorithm_pat_alg_reduction_001_assembly(const int32_t *values, uint32_t count,
                          algorithm_algorithm_pat_alg_reduction_001_assembly_signed_result_t *result);

int algorithm_algorithm_pat_alg_reduction_001_assembly_unsigned(
    const uint32_t *values, uint32_t count,
    algorithm_algorithm_pat_alg_reduction_001_assembly_unsigned_result_t *result);



static int pattern_core_vector(void) {
  int32_t a[] = {-2, 5, 1};
  algorithm_algorithm_pat_alg_reduction_001_assembly_signed_result_t r;
  return algorithm_algorithm_pat_alg_reduction_001_assembly(a, 3, &r) && r.minimum == -2 && r.maximum == 5 &&
         r.sum == 4;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {INT32_MIN, INT32_MAX};
  uint32_t u[] = {0, UINT32_MAX};
  algorithm_algorithm_pat_alg_reduction_001_assembly_signed_result_t s;
  algorithm_algorithm_pat_alg_reduction_001_assembly_unsigned_result_t r;
  return !algorithm_algorithm_pat_alg_reduction_001_assembly(NULL, 0, &s) &&
         algorithm_algorithm_pat_alg_reduction_001_assembly(a, 2, &s) && s.sum == -1 &&
         algorithm_algorithm_pat_alg_reduction_001_assembly_unsigned(u, 2, &r) && r.sum == UINT32_MAX;
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
